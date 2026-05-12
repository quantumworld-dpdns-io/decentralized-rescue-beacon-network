package api

import (
	"net/http"
	"strconv"

	"beacon-go/internal/models"
)

func (h *Handler) GetAuditLog(w http.ResponseWriter, r *http.Request) {
	limitStr := r.URL.Query().Get("limit")
	limit := 100
	if limitStr != "" {
		if parsed, err := strconv.Atoi(limitStr); err == nil && parsed > 0 {
			limit = parsed
		}
	}

	events, err := h.db.ListAuditEvents(r.Context(), limit)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "failed to list audit events")
		return
	}
	if events == nil {
		events = []models.AuditEvent{}
	}

	writeJSON(w, http.StatusOK, events)
}
