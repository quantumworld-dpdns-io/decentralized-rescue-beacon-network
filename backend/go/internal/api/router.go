package api

import (
	"beacon-go/internal/clients"
	"beacon-go/internal/db"
)

type Handler struct {
	db     *db.DB
	python *clients.PythonClient
	rust   *clients.RustClient
}

func NewHandler(database *db.DB, python *clients.PythonClient, rust *clients.RustClient) *Handler {
	return &Handler{
		db:     database,
		python: python,
		rust:   rust,
	}
}
