package api

import (
	"net/http"

	"beacon-go/internal/models"
)

func (h *Handler) GetMetrics(w http.ResponseWriter, r *http.Request) {
	metrics, err := h.db.GetMetrics(r.Context())
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to get metrics")
		return
	}
	if metrics == nil {
		metrics = []models.MetricValue{}
	}

	result := make(map[string]int64)
	for _, m := range metrics {
		result[m.Metric] = m.Value
	}

	writeJSON(w, http.StatusOK, result)
}
