package clients

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type RustClient struct {
	baseURL string
	hc      *http.Client
}

func NewRustClient(baseURL string) *RustClient {
	return &RustClient{
		baseURL: baseURL,
		hc:      &http.Client{Timeout: 10 * time.Second},
	}
}

type RouteRequest struct {
	OriginNodeID string              `json:"origin_node_id"`
	MaxHops      int                 `json:"max_hops"`
	Topology     map[string][]string `json:"topology"`
}

type RouteResponse struct {
	Routes         map[string][]string `json:"routes"`
	ReachableNodes []string            `json:"reachable_nodes"`
}

func (c *RustClient) ComputeRoute(req *RouteRequest) (*RouteResponse, error) {
	body, _ := json.Marshal(req)
	resp, err := c.hc.Post(c.baseURL+"/route", "application/json", bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("rust route: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("rust route: status %d", resp.StatusCode)
	}

	var result RouteResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("rust route decode: %w", err)
	}
	return &result, nil
}
