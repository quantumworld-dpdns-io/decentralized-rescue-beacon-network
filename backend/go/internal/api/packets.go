package api

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"beacon-go/internal/clients"
	"beacon-go/internal/models"
)

func generatePacketID() (string, error) {
	b := make([]byte, 16)
	if _, err := rand.Read(b); err != nil {
		return "", fmt.Errorf("generate id: %w", err)
	}
	return hex.EncodeToString(b), nil
}

func (h *Handler) SubmitPacket(w http.ResponseWriter, r *http.Request) {
	var req models.PacketSubmitRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "invalid request body")
		return
	}
	if req.OriginNodeID == "" {
		writeError(w, http.StatusBadRequest, "origin_node_id is required")
		return
	}
	if req.MaxHops <= 0 {
		req.MaxHops = 3
	}

	packetID, err := generatePacketID()
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to generate packet id")
		return
	}

	createdAt := time.Now().UTC().Format(time.RFC3339)

	canonical := map[string]any{
		"packet_id":        packetID,
		"origin_node_id":   req.OriginNodeID,
		"distress_payload": req.DistressPayload,
		"max_hops":         req.MaxHops,
		"created_at":       createdAt,
	}

	signature, algorithm, err := h.python.Sign(canonical)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to sign packet")
		return
	}

	exists, err := h.db.NodeExists(r.Context(), req.OriginNodeID)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to check node")
		return
	}
	if !exists {
		h.recordDrop(r.Context(), packetID, "origin_not_registered")
		writeJSON(w, http.StatusBadRequest, models.PacketSubmitResponse{
			Packet: models.Packet{
				PacketID:           packetID,
				OriginNodeID:       req.OriginNodeID,
				DistressPayload:    req.DistressPayload,
				MaxHops:            req.MaxHops,
				Signature:          signature,
				SignatureAlgorithm: algorithm,
				CreatedAt:          createdAt,
			},
			RelayOutcome: models.RelayOutcome{
				PacketID:      packetID,
				DeliveredNodes: []string{},
				Routes:         map[string][]string{},
				DroppedReason:  "origin_not_registered",
			},
		})
		return
	}

	topology, err := h.db.LoadTopology(r.Context())
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to load topology")
		return
	}
	if topology == nil {
		topology = make(map[string][]string)
	}

	routeResp, err := h.rust.ComputeRoute(&clients.RouteRequest{
		OriginNodeID: req.OriginNodeID,
		MaxHops:      req.MaxHops,
		Topology:     topology,
	})
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to compute routes")
		return
	}

	outcome := h.buildOutcome(packetID, routeResp, req.TargetNodes)

	if err := h.db.CreateAuditEvent(r.Context(), packetID, "submit_received", nil); err != nil {
		writeError(w, http.StatusInternalServerError, "failed to record audit")
		return
	}

	if outcome.DroppedReason != "" {
		h.db.IncrementMetric(r.Context(), "submitted")
		h.db.IncrementMetric(r.Context(), "dropped_unreachable")
		h.recordDrop(r.Context(), packetID, outcome.DroppedReason)
	} else {
		h.db.IncrementMetricBy(r.Context(), "delivered", int64(len(outcome.DeliveredNodes)))
	}

	h.db.IncrementMetric(r.Context(), "submitted")

	pkt := models.Packet{
		PacketID:           packetID,
		OriginNodeID:       req.OriginNodeID,
		DistressPayload:    req.DistressPayload,
		MaxHops:            req.MaxHops,
		Signature:          signature,
		SignatureAlgorithm: algorithm,
		CreatedAt:          createdAt,
	}

	if err := h.db.CreatePacket(r.Context(), pkt); err != nil {
		writeError(w, http.StatusInternalServerError, "failed to store packet")
		return
	}

	for nodeID, route := range outcome.Routes {
		h.db.CreateDelivery(r.Context(), packetID, nodeID, route)
	}

	if outcome.DroppedReason == "" {
		h.db.CreateAuditEvent(r.Context(), packetID, "submit_delivered",
			map[string]string{"delivered_nodes": joinStrings(outcome.DeliveredNodes)})
	}

	writeJSON(w, http.StatusCreated, models.PacketSubmitResponse{
		Packet:       pkt,
		RelayOutcome: outcome,
	})
}

func (h *Handler) buildOutcome(packetID string, resp *clients.RouteResponse, targetNodes []string) models.RelayOutcome {
	if len(resp.ReachableNodes) == 0 {
		return models.RelayOutcome{
			PacketID:       packetID,
			DeliveredNodes: []string{},
			Routes:         map[string][]string{},
			DroppedReason:  "no_reachable_targets",
		}
	}

	candidateSet := make(map[string]bool)
	for _, n := range resp.ReachableNodes {
		candidateSet[n] = true
	}
	if targetNodes != nil {
		filtered := make(map[string]bool)
		for _, t := range targetNodes {
			if candidateSet[t] {
				filtered[t] = true
			}
		}
		if len(filtered) == 0 {
			return models.RelayOutcome{
				PacketID:       packetID,
				DeliveredNodes: []string{},
				Routes:         map[string][]string{},
				DroppedReason:  "no_reachable_targets",
			}
		}
		candidateSet = filtered
	}

	delivered := sortedKeys(candidateSet)
	routes := make(map[string][]string)
	for _, n := range delivered {
		routes[n] = resp.Routes[n]
	}

	return models.RelayOutcome{
		PacketID:       packetID,
		DeliveredNodes: delivered,
		Routes:         routes,
	}
}

func (h *Handler) recordDrop(ctx context.Context, packetID, reason string) {
	h.db.CreateAuditEvent(ctx, packetID, "submit_dropped",
		map[string]string{"reason": reason})
}

func (h *Handler) GetPacket(w http.ResponseWriter, r *http.Request) {
	packetID := r.PathValue("id")
	if packetID == "" {
		writeError(w, http.StatusBadRequest, "packet id is required")
		return
	}

	pkt, err := h.db.GetPacket(r.Context(), packetID)
	if err != nil {
		writeError(w, http.StatusNotFound, "packet not found")
		return
	}

	routes, err := h.db.GetPacketDeliveries(r.Context(), packetID)
	if err != nil {
		routes = map[string][]string{}
	}

	outcome := "delivered"
	if len(routes) == 0 {
		outcome = "no_deliveries"
	}

	writeJSON(w, http.StatusOK, models.PacketDetail{
		Packet:  *pkt,
		Routes:  routes,
		Outcome: outcome,
	})
}
