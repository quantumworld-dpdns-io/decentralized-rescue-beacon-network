"use client";

import { useEffect, useState, FormEvent } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

interface Node {
  node_id: string;
  created_at: string;
}

export default function NodesPage() {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [neighbors, setNeighbors] = useState<Record<string, string[]>>({});
  const [nodeId, setNodeId] = useState("");
  const [connA, setConnA] = useState("");
  const [connB, setConnB] = useState("");

  function loadNodes() {
    fetch(`${API}/api/nodes`)
      .then((r) => r.json())
      .then(setNodes)
      .catch(console.error);
  }

  useEffect(() => {
    loadNodes();
  }, []);

  async function handleRegister(e: FormEvent) {
    e.preventDefault();
    if (!nodeId.trim()) return;
    await fetch(`${API}/api/nodes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ node_id: nodeId }),
    });
    setNodeId("");
    loadNodes();
  }

  async function handleConnect(e: FormEvent) {
    e.preventDefault();
    if (!connA.trim() || !connB.trim()) return;
    await fetch(`${API}/api/nodes/connect`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ node_a: connA, node_b: connB }),
    });
    setConnA("");
    setConnB("");
    loadNodes();
  }

  async function loadNeighbors(id: string) {
    const res = await fetch(`${API}/api/nodes/${id}/neighbors`);
    if (res.ok) {
      const data = await res.json();
      setNeighbors((prev) => ({ ...prev, [id]: data }));
    }
  }

  return (
    <>
      <h1>Nodes</h1>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem" }}>
        <div className="card">
          <h2>Register Node</h2>
          <form onSubmit={handleRegister}>
            <label>Node ID</label>
            <input
              value={nodeId}
              onChange={(e) => setNodeId(e.target.value)}
              placeholder="e.g. node-1"
            />
            <button type="submit">Register</button>
          </form>
        </div>

        <div className="card">
          <h2>Connect Nodes</h2>
          <form onSubmit={handleConnect}>
            <label>Node A</label>
            <input value={connA} onChange={(e) => setConnA(e.target.value)} placeholder="node-1" />
            <label>Node B</label>
            <input value={connB} onChange={(e) => setConnB(e.target.value)} placeholder="node-2" />
            <button type="submit">Connect</button>
          </form>
        </div>
      </div>

      <div className="card">
        <h2>Registered Nodes ({nodes.length})</h2>
        <table>
          <thead>
            <tr>
              <th>Node ID</th>
              <th>Neighbors</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {nodes.length === 0 && (
              <tr>
                <td colSpan={3}>No nodes registered.</td>
              </tr>
            )}
            {nodes.map((n) => (
              <tr key={n.node_id}>
                <td>{n.node_id}</td>
                <td>
                  {neighbors[n.node_id]
                    ? neighbors[n.node_id].join(", ")
                    : "—"}
                </td>
                <td>
                  <button className="secondary" onClick={() => loadNeighbors(n.node_id)}>
                    Load Neighbors
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
