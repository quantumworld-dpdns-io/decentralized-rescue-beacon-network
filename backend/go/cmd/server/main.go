package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"

	"beacon-go/internal/api"
	"beacon-go/internal/clients"
	"beacon-go/internal/db"
)

func main() {
	ctx := context.Background()

	databaseURL := os.Getenv("DATABASE_URL")
	pythonURL := os.Getenv("PYTHON_SERVICE_URL")
	rustURL := os.Getenv("RUST_SERVICE_URL")
	port := os.Getenv("GO_SERVICE_PORT")
	if port == "" {
		port = "8080"
	}

	if databaseURL == "" || pythonURL == "" || rustURL == "" {
		slog.Error("DATABASE_URL, PYTHON_SERVICE_URL, and RUST_SERVICE_URL are required")
		os.Exit(1)
	}

	database, err := db.New(ctx, databaseURL)
	if err != nil {
		slog.Error("failed to connect to database", "error", err)
		os.Exit(1)
	}
	defer database.Close()

	python := clients.NewPythonClient(pythonURL)
	rust := clients.NewRustClient(rustURL)

	h := api.NewHandler(database, python, rust)

	mux := http.NewServeMux()

	mux.HandleFunc("GET /api/nodes", h.ListNodes)
	mux.HandleFunc("POST /api/nodes", h.CreateNode)
	mux.HandleFunc("POST /api/nodes/connect", h.ConnectNodes)
	mux.HandleFunc("GET /api/nodes/{id}/neighbors", h.GetNodeNeighbors)

	mux.HandleFunc("POST /api/packets", h.SubmitPacket)
	mux.HandleFunc("GET /api/packets/{id}", h.GetPacket)

	mux.HandleFunc("GET /api/metrics", h.GetMetrics)
	mux.HandleFunc("GET /api/audit-log", h.GetAuditLog)

	mux.HandleFunc("GET /health", h.Health)

	wrapped := api.CORSMiddleware(mux)

	slog.Info("Go API gateway listening", "port", port)
	if err := http.ListenAndServe(":"+port, wrapped); err != nil {
		slog.Error("server error", "error", err)
		os.Exit(1)
	}
}
