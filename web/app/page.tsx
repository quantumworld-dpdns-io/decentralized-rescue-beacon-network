"use client";

import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

interface Metrics {
  submitted: number;
  delivered: number;
  dropped_duplicate: number;
  dropped_invalid_signature: number;
  dropped_invalid_packet: number;
  dropped_unreachable: number;
}

interface Node {
  node_id: string;
  created_at: string;
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [nodes, setNodes] = useState<Node[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/metrics`).then((r) => r.json()),
      fetch(`${API}/api/nodes`).then((r) => r.json()),
    ])
      .then(([m, n]) => {
        setMetrics(m);
        setNodes(n);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <>
      <h1>Dashboard</h1>
      <div className="grid">
        <div className="stat">
          <div className="value">{nodes.length}</div>
          <div className="label">Registered Nodes</div>
        </div>
        <div className="stat">
          <div className="value">{metrics?.submitted ?? 0}</div>
          <div className="label">Packets Submitted</div>
        </div>
        <div className="stat">
          <div className="value">{metrics?.delivered ?? 0}</div>
          <div className="label">Packets Delivered</div>
        </div>
        <div className="stat">
          <div className="value">{metrics?.dropped_unreachable ?? 0}</div>
          <div className="label">Dropped (Unreachable)</div>
        </div>
      </div>

      <div className="card">
        <h2>Recent Nodes</h2>
        <table>
          <thead>
            <tr>
              <th>Node ID</th>
              <th>Registered</th>
            </tr>
          </thead>
          <tbody>
            {nodes.length === 0 && (
              <tr>
                <td colSpan={2}>No nodes registered yet.</td>
              </tr>
            )}
            {nodes.map((n) => (
              <tr key={n.node_id}>
                <td>{n.node_id}</td>
                <td>{new Date(n.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
