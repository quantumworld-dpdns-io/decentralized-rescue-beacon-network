package models

type Node struct {
	NodeID    string `json:"node_id"`
	CreatedAt string `json:"created_at"`
}

type ConnectRequest struct {
	NodeA string `json:"node_a"`
	NodeB string `json:"node_b"`
}

type PacketSubmitRequest struct {
	OriginNodeID    string            `json:"origin_node_id"`
	DistressPayload map[string]string `json:"distress_payload"`
	MaxHops         int               `json:"max_hops"`
	TargetNodes     []string          `json:"target_nodes,omitempty"`
}

type Packet struct {
	PacketID           string            `json:"packet_id"`
	OriginNodeID       string            `json:"origin_node_id"`
	DistressPayload    map[string]string `json:"distress_payload"`
	MaxHops            int               `json:"max_hops"`
	Signature          string            `json:"signature,omitempty"`
	SignatureAlgorithm string            `json:"signature_algorithm,omitempty"`
	CreatedAt          string            `json:"created_at"`
}

type RelayOutcome struct {
	PacketID       string              `json:"packet_id"`
	DeliveredNodes []string            `json:"delivered_nodes"`
	Routes         map[string][]string `json:"routes"`
	DroppedReason  string              `json:"dropped_reason,omitempty"`
}

type PacketSubmitResponse struct {
	Packet      Packet       `json:"packet"`
	RelayOutcome RelayOutcome `json:"relay_outcome"`
}

type PacketDetail struct {
	Packet   Packet           `json:"packet"`
	Routes   map[string][]string `json:"routes"`
	Outcome  string           `json:"outcome"`
}

type MetricValue struct {
	Metric string `json:"metric"`
	Value  int64  `json:"value"`
}

type AuditEvent struct {
	Timestamp string `json:"timestamp"`
	PacketID  string `json:"packet_id"`
	Action    string `json:"action"`
	Details   map[string]string `json:"details"`
}
