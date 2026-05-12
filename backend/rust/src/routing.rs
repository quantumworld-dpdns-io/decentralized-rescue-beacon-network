use std::collections::{HashMap, VecDeque};

pub fn find_routes(
    origin: &str,
    max_hops: usize,
    topology: &HashMap<String, Vec<String>>,
) -> HashMap<String, Vec<String>> {
    let mut routes: HashMap<String, Vec<String>> = HashMap::new();
    routes.insert(origin.to_string(), vec![origin.to_string()]);

    let mut queue: VecDeque<(String, usize)> = VecDeque::new();
    queue.push_back((origin.to_string(), 0));

    while let Some((node, hops)) = queue.pop_front() {
        if hops >= max_hops {
            continue;
        }
        if let Some(neighbors) = topology.get(&node) {
            let mut sorted = neighbors.clone();
            sorted.sort();
            for neighbor in sorted {
                if routes.contains_key(&neighbor) {
                    continue;
                }
                let path = routes[&node].clone();
                let mut new_path = path;
                new_path.push(neighbor.clone());
                routes.insert(neighbor.clone(), new_path);
                queue.push_back((neighbor.clone(), hops + 1));
            }
        }
    }

    routes
}
