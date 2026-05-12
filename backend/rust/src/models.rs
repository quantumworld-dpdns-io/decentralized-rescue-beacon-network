use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Deserialize)]
pub struct RouteRequest {
    pub origin_node_id: String,
    pub max_hops: usize,
    pub topology: HashMap<String, Vec<String>>,
}

#[derive(Debug, Serialize)]
pub struct RouteResponse {
    pub routes: HashMap<String, Vec<String>>,
    pub reachable_nodes: Vec<String>,
}
