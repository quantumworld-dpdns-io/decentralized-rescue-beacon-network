"use client";

import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

interface AuditEvent {
  timestamp: string;
  packet_id: string;
  action: string;
  details: Record<string, string>;
}

export default function AuditPage() {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/audit-log?limit=100`)
      .then((r) => r.json())
      .then(setEvents)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <>
      <h1>Audit Log</h1>

      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Packet ID</th>
              <th>Action</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {events.length === 0 && (
              <tr>
                <td colSpan={4}>No audit events recorded.</td>
              </tr>
            )}
            {events.map((e, i) => (
              <tr key={i}>
                <td>{new Date(e.timestamp).toLocaleString()}</td>
                <td style={{ fontFamily: "monospace", fontSize: "0.8rem" }}>
                  {e.packet_id.substring(0, 12)}...
                </td>
                <td>
                  <span
                    className={`badge ${
                      e.action.includes("delivered")
                        ? "success"
                        : e.action.includes("dropped")
                        ? "error"
                        : "warning"
                    }`}
                  >
                    {e.action}
                  </span>
                </td>
                <td style={{ fontFamily: "monospace", fontSize: "0.75rem" }}>
                  {JSON.stringify(e.details)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
