use axum::{extract::State, http::StatusCode, Json};
use std::sync::Arc;

use crate::models::{RouteRequest, RouteResponse};
use crate::routing::find_routes;

pub async fn health() -> Json<serde_json::Value> {
    Json(serde_json::json!({"status": "ok"}))
}

pub async fn compute_route(
    State(_state): State<Arc<AppState>>,
    Json(req): Json<RouteRequest>,
) -> Result<Json<RouteResponse>, StatusCode> {
    if req.origin_node_id.is_empty() || req.topology.is_empty() {
        return Err(StatusCode::BAD_REQUEST);
    }
    if req.max_hops == 0 {
        return Err(StatusCode::BAD_REQUEST);
    }

    let all_routes = find_routes(&req.origin_node_id, req.max_hops, &req.topology);

    let reachable: Vec<String> = all_routes
        .keys()
        .filter(|k| *k != &req.origin_node_id)
        .cloned()
        .collect::<Vec<_>>();

    let response = RouteResponse {
        routes: all_routes,
        reachable_nodes: reachable,
    };

    Ok(Json(response))
}

pub struct AppState;
