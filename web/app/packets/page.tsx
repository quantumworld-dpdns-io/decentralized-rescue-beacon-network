"use client";

import { useState, FormEvent } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

interface PacketResponse {
  packet: {
    packet_id: string;
    origin_node_id: string;
    distress_payload: Record<string, string>;
    max_hops: number;
    signature: string;
    signature_algorithm: string;
    created_at: string;
  };
  relay_outcome: {
    packet_id: string;
    delivered_nodes: string[];
    routes: Record<string, string[]>;
    dropped_reason?: string;
  };
}

export default function PacketsPage() {
  const [originNodeId, setOriginNodeId] = useState("");
  const [message, setMessage] = useState("");
  const [maxHops, setMaxHops] = useState(3);
  const [targetNodes, setTargetNodes] = useState("");
  const [result, setResult] = useState<PacketResponse | null>(null);
  const [error, setError] = useState("");
  const [packetId, setPacketId] = useState("");
  const [lookupResult, setLookupResult] = useState<any>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setResult(null);

    const targets = targetNodes
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    const body: any = {
      origin_node_id: originNodeId,
      distress_payload: { message },
      max_hops: maxHops,
    };
    if (targets.length > 0) body.target_nodes = targets;

    const res = await fetch(`${API}/api/packets`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await res.json();
    if (res.ok) {
      setResult(data);
    } else {
      setError(data.error || "Submission failed");
    }
  }

  async function handleLookup() {
    if (!packetId.trim()) return;
    const res = await fetch(`${API}/api/packets/${packetId}`);
    if (res.ok) {
      setLookupResult(await res.json());
    } else {
      setLookupResult({ error: "Packet not found" });
    }
  }

  return (
    <>
      <h1>Packets</h1>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem" }}>
        <div className="card">
          <h2>Submit Distress Packet</h2>
          <form onSubmit={handleSubmit}>
            <label>Origin Node ID</label>
            <input
              value={originNodeId}
              onChange={(e) => setOriginNodeId(e.target.value)}
              placeholder="node-1"
              required
            />

            <label>Distress Message</label>
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="SOS! Need assistance..."
              required
            />

            <label>Max Hops</label>
            <input
              type="number"
              min={1}
              value={maxHops}
              onChange={(e) => setMaxHops(Number(e.target.value))}
            />

            <label>Target Nodes (comma-separated, optional)</label>
            <input
              value={targetNodes}
              onChange={(e) => setTargetNodes(e.target.value)}
              placeholder="node-4, node-5"
            />

            <button type="submit">Submit Packet</button>
          </form>

          {error && <p style={{ color: "#fca5a5", marginTop: "1rem" }}>{error}</p>}

          {result && (
            <div className="mt-4">
              <h2>Result</h2>
              <p>
                <strong>Packet ID:</strong> {result.packet.packet_id}
              </p>
              <p>
                <strong>Status:</strong>{" "}
                {result.relay_outcome.dropped_reason ? (
                  <span className="badge error">{result.relay_outcome.dropped_reason}</span>
                ) : (
                  <span className="badge success">
                    Delivered to {result.relay_outcome.delivered_nodes.length} nodes
                  </span>
                )}
              </p>
              {result.relay_outcome.delivered_nodes.length > 0 && (
                <>
                  <p>
                    <strong>Delivered Nodes:</strong>{" "}
                    {result.relay_outcome.delivered_nodes.join(", ")}
                  </p>
                  <pre>{JSON.stringify(result.relay_outcome.routes, null, 2)}</pre>
                </>
              )}
            </div>
          )}
        </div>

        <div className="card">
          <h2>Lookup Packet</h2>
          <div className="flex">
            <input
              value={packetId}
              onChange={(e) => setPacketId(e.target.value)}
              placeholder="Enter packet ID"
            />
            <button onClick={handleLookup}>Lookup</button>
          </div>

          {lookupResult && (
            <div className="mt-4">
              {lookupResult.error ? (
                <p style={{ color: "#fca5a5" }}>{lookupResult.error}</p>
              ) : (
                <>
                  <p>
                    <strong>Origin:</strong> {lookupResult.packet.origin_node_id}
                  </p>
                  <p>
                    <strong>Outcome:</strong> {lookupResult.outcome}
                  </p>
                  <p>
                    <strong>Routes:</strong>
                  </p>
                  <pre>{JSON.stringify(lookupResult.routes, null, 2)}</pre>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
