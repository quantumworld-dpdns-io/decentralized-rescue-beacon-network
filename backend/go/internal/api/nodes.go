package api

import (
	"encoding/json"
	"net/http"

	"beacon-go/internal/models"
)

func (h *Handler) ListNodes(w http.ResponseWriter, r *http.Request) {
	nodes, err := h.db.ListNodes(r.Context())
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to list nodes")
		return
	}
	if nodes == nil {
		nodes = []models.Node{}
	}
	writeJSON(w, http.StatusOK, nodes)
}

func (h *Handler) CreateNode(w http.ResponseWriter, r *http.Request) {
	var req struct {
		NodeID string `json:"node_id"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "invalid request body")
		return
	}
	if req.NodeID == "" {
		writeError(w, http.StatusBadRequest, "node_id is required")
		return
	}

	if err := h.db.CreateNode(r.Context(), req.NodeID); err != nil {
		writeError(w, http.StatusInternalServerError, "failed to create node")
		return
	}

	writeJSON(w, http.StatusCreated, map[string]string{"node_id": req.NodeID})
}

func (h *Handler) ConnectNodes(w http.ResponseWriter, r *http.Request) {
	var req models.ConnectRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	if req.NodeA == "" || req.NodeB == "" {
		writeError(w, http.StatusBadRequest, "node_a and node_b are required")
		return
	}

	if err := h.db.CreateNode(r.Context(), req.NodeA); err != nil {
		writeError(w, http.StatusInternalServerError, "failed to create node_a")
		return
	}
	if err := h.db.CreateNode(r.Context(), req.NodeB); err != nil {
		writeError(w, http.StatusInternalServerError, "failed to create node_b")
		return
	}
	if err := h.db.ConnectNodes(r.Context(), req.NodeA, req.NodeB); err != nil {
		writeError(w, http.StatusInternalServerError, "failed to connect nodes")
		return
	}

	writeJSON(w, http.StatusOK, map[string]string{
		"left_node_id":  req.NodeA,
		"right_node_id": req.NodeB,
	})
}

func (h *Handler) GetNodeNeighbors(w http.ResponseWriter, r *http.Request) {
	nodeID := r.PathValue("id")
	if nodeID == "" {
		writeError(w, http.StatusBadRequest, "node id is required")
		return
	}

	exists, err := h.db.NodeExists(r.Context(), nodeID)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to check node")
		return
	}
	if !exists {
		writeError(w, http.StatusNotFound, "node not found")
		return
	}

	neighbors, err := h.db.GetNodeNeighbors(r.Context(), nodeID)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to get neighbors")
		return
	}
	if neighbors == nil {
		neighbors = []string{}
	}

	writeJSON(w, http.StatusOK, neighbors)
}
