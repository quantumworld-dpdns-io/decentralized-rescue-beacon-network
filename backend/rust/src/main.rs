mod api;
mod models;
mod routing;

use std::sync::Arc;

use axum::{
    routing::{get, post},
    Router,
};
use tower_http::cors::CorsLayer;
use tracing_subscriber::EnvFilter;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("info")),
        )
        .init();

    let state = Arc::new(api::AppState);

    let app = Router::new()
        .route("/health", get(api::health))
        .route("/route", post(api::compute_route))
        .layer(CorsLayer::permissive())
        .with_state(state);

    let port = std::env::var("RUST_SERVICE_PORT")
        .unwrap_or_else(|_| "9090".to_string());

    let addr = format!("0.0.0.0:{}", port);
    tracing::info!("Rust engine listening on {}", addr);

    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
