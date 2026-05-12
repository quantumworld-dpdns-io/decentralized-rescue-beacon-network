package db

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"beacon-go/internal/models"
)

func (d *DB) CreateNode(ctx context.Context, nodeID string) error {
	_, err := d.Pool.Exec(ctx,
		`INSERT INTO nodes (node_id) VALUES ($1) ON CONFLICT DO NOTHING`, nodeID)
	return err
}

func (d *DB) ConnectNodes(ctx context.Context, leftID, rightID string) error {
	_, err := d.Pool.Exec(ctx,
		`INSERT INTO node_connections (left_node_id, right_node_id) VALUES ($1, $2)
		 ON CONFLICT DO NOTHING`, leftID, rightID)
	if err != nil {
		return err
	}
	_, err = d.Pool.Exec(ctx,
		`INSERT INTO node_connections (left_node_id, right_node_id) VALUES ($1, $2)
		 ON CONFLICT DO NOTHING`, rightID, leftID)
	return err
}

func (d *DB) ListNodes(ctx context.Context) ([]models.Node, error) {
	rows, err := d.Pool.Query(ctx,
		`SELECT node_id, created_at FROM nodes ORDER BY node_id`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var nodes []models.Node
	for rows.Next() {
		var n models.Node
		var t time.Time
		if err := rows.Scan(&n.NodeID, &t); err != nil {
			return nil, err
		}
		n.CreatedAt = t.Format(time.RFC3339)
		nodes = append(nodes, n)
	}
	return nodes, rows.Err()
}

func (d *DB) GetNodeNeighbors(ctx context.Context, nodeID string) ([]string, error) {
	rows, err := d.Pool.Query(ctx,
		`SELECT right_node_id FROM node_connections WHERE left_node_id = $1 ORDER BY right_node_id`, nodeID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var neighbors []string
	for rows.Next() {
		var n string
		if err := rows.Scan(&n); err != nil {
			return nil, err
		}
		neighbors = append(neighbors, n)
	}
	return neighbors, rows.Err()
}

func (d *DB) NodeExists(ctx context.Context, nodeID string) (bool, error) {
	var exists bool
	err := d.Pool.QueryRow(ctx,
		`SELECT EXISTS(SELECT 1 FROM nodes WHERE node_id = $1)`, nodeID).Scan(&exists)
	return exists, err
}

func (d *DB) LoadTopology(ctx context.Context) (map[string][]string, error) {
	rows, err := d.Pool.Query(ctx,
		`SELECT left_node_id, right_node_id FROM node_connections ORDER BY left_node_id, right_node_id`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	topology := make(map[string][]string)
	for rows.Next() {
		var left, right string
		if err := rows.Scan(&left, &right); err != nil {
			return nil, err
		}
		topology[left] = append(topology[left], right)
	}
	return topology, rows.Err()
}

func (d *DB) CreatePacket(ctx context.Context, pkt models.Packet) error {
	payloadJSON, _ := json.Marshal(pkt.DistressPayload)
	_, err := d.Pool.Exec(ctx,
		`INSERT INTO beacon_packets (packet_id, origin_node_id, distress_payload, max_hops, signature, signature_algorithm)
		 VALUES ($1, $2, $3, $4, $5, $6)`,
		pkt.PacketID, pkt.OriginNodeID, payloadJSON, pkt.MaxHops, pkt.Signature, pkt.SignatureAlgorithm)
	return err
}

func (d *DB) CreateDelivery(ctx context.Context, packetID, nodeID string, route []string) error {
	routeJSON, _ := json.Marshal(route)
	_, err := d.Pool.Exec(ctx,
		`INSERT INTO packet_deliveries (packet_id, node_id, route) VALUES ($1, $2, $3)`,
		packetID, nodeID, routeJSON)
	return err
}

func (d *DB) GetPacket(ctx context.Context, packetID string) (*models.Packet, error) {
	var pkt models.Packet
	var payloadJSON []byte
	var t time.Time
	var sig, sigAlg *string

	err := d.Pool.QueryRow(ctx,
		`SELECT packet_id, origin_node_id, distress_payload, max_hops, signature, signature_algorithm, created_at
		 FROM beacon_packets WHERE packet_id = $1`, packetID).
		Scan(&pkt.PacketID, &pkt.OriginNodeID, &payloadJSON, &pkt.MaxHops, &sig, &sigAlg, &t)
	if err != nil {
		return nil, fmt.Errorf("get packet: %w", err)
	}

	json.Unmarshal(payloadJSON, &pkt.DistressPayload)
	pkt.CreatedAt = t.Format(time.RFC3339)
	if sig != nil {
		pkt.Signature = *sig
	}
	if sigAlg != nil {
		pkt.SignatureAlgorithm = *sigAlg
	}
	return &pkt, nil
}

func (d *DB) GetPacketDeliveries(ctx context.Context, packetID string) (map[string][]string, error) {
	rows, err := d.Pool.Query(ctx,
		`SELECT node_id, route FROM packet_deliveries WHERE packet_id = $1 ORDER BY node_id`, packetID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	routes := make(map[string][]string)
	for rows.Next() {
		var nodeID string
		var routeJSON []byte
		if err := rows.Scan(&nodeID, &routeJSON); err != nil {
			return nil, err
		}
		var route []string
		json.Unmarshal(routeJSON, &route)
		routes[nodeID] = route
	}
	return routes, rows.Err()
}

func (d *DB) IncrementMetric(ctx context.Context, metric string) error {
	_, err := d.Pool.Exec(ctx,
		`INSERT INTO metrics (metric, value) VALUES ($1, 1)
		 ON CONFLICT (metric) DO UPDATE SET value = metrics.value + 1, updated_at = NOW()`, metric)
	return err
}

func (d *DB) IncrementMetricBy(ctx context.Context, metric string, delta int64) error {
	_, err := d.Pool.Exec(ctx,
		`INSERT INTO metrics (metric, value) VALUES ($1, $2)
		 ON CONFLICT (metric) DO UPDATE SET value = metrics.value + $2, updated_at = NOW()`, metric, delta)
	return err
}

func (d *DB) GetMetrics(ctx context.Context) ([]models.MetricValue, error) {
	rows, err := d.Pool.Query(ctx,
		`SELECT metric, value FROM metrics ORDER BY metric`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var metrics []models.MetricValue
	for rows.Next() {
		var m models.MetricValue
		if err := rows.Scan(&m.Metric, &m.Value); err != nil {
			return nil, err
		}
		metrics = append(metrics, m)
	}
	return metrics, rows.Err()
}

func (d *DB) CreateAuditEvent(ctx context.Context, packetID, action string, details map[string]string) error {
	detailsJSON, _ := json.Marshal(details)
	_, err := d.Pool.Exec(ctx,
		`INSERT INTO audit_events (packet_id, action, details) VALUES ($1, $2, $3)`,
		packetID, action, detailsJSON)
	return err
}

func (d *DB) ListAuditEvents(ctx context.Context, limit int) ([]models.AuditEvent, error) {
	if limit <= 0 {
		limit = 100
	}
	rows, err := d.Pool.Query(ctx,
		`SELECT timestamp, packet_id, action, details
		 FROM audit_events ORDER BY timestamp DESC LIMIT $1`, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var events []models.AuditEvent
	for rows.Next() {
		var e models.AuditEvent
		var t time.Time
		var detailsJSON []byte
		if err := rows.Scan(&t, &e.PacketID, &e.Action, &detailsJSON); err != nil {
			return nil, err
		}
		e.Timestamp = t.Format(time.RFC3339)
		json.Unmarshal(detailsJSON, &e.Details)
		events = append(events, e)
	}
	return events, rows.Err()
}
