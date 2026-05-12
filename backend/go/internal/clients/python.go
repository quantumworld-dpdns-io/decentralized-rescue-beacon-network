package clients

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type PythonClient struct {
	baseURL string
	hc      *http.Client
}

func NewPythonClient(baseURL string) *PythonClient {
	return &PythonClient{
		baseURL: baseURL,
		hc:      &http.Client{Timeout: 10 * time.Second},
	}
}

type signRequest struct {
	Payload map[string]any `json:"payload"`
}

type signResponse struct {
	Signature string `json:"signature"`
	Algorithm string `json:"algorithm"`
}

type verifyRequest struct {
	Payload   map[string]any `json:"payload"`
	Signature string         `json:"signature"`
}

type verifyResponse struct {
	Valid bool `json:"valid"`
}

func (c *PythonClient) Sign(payload map[string]any) (signature, algorithm string, err error) {
	body, _ := json.Marshal(signRequest{Payload: payload})
	resp, err := c.hc.Post(c.baseURL+"/sign", "application/json", bytes.NewReader(body))
	if err != nil {
		return "", "", fmt.Errorf("python sign: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", "", fmt.Errorf("python sign: status %d", resp.StatusCode)
	}

	var result signResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", "", fmt.Errorf("python sign decode: %w", err)
	}
	return result.Signature, result.Algorithm, nil
}

func (c *PythonClient) Verify(payload map[string]any, signature string) (bool, error) {
	body, _ := json.Marshal(verifyRequest{Payload: payload, Signature: signature})
	resp, err := c.hc.Post(c.baseURL+"/verify", "application/json", bytes.NewReader(body))
	if err != nil {
		return false, fmt.Errorf("python verify: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return false, fmt.Errorf("python verify: status %d", resp.StatusCode)
	}

	var result verifyResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return false, fmt.Errorf("python verify decode: %w", err)
	}
	return result.Valid, nil
}
