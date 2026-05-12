CREATE TABLE IF NOT EXISTS nodes (
    node_id    TEXT PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS node_connections (
    left_node_id  TEXT NOT NULL REFERENCES nodes(node_id),
    right_node_id TEXT NOT NULL REFERENCES nodes(node_id),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (left_node_id, right_node_id)
);

CREATE TABLE IF NOT EXISTS beacon_packets (
    packet_id           TEXT PRIMARY KEY,
    origin_node_id      TEXT NOT NULL,
    distress_payload    JSONB NOT NULL,
    max_hops            INT NOT NULL DEFAULT 3,
    signature           TEXT,
    signature_algorithm TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS packet_deliveries (
    id         BIGSERIAL PRIMARY KEY,
    packet_id  TEXT NOT NULL REFERENCES beacon_packets(packet_id),
    node_id    TEXT NOT NULL,
    route      JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_events (
    id        BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    packet_id TEXT,
    action    TEXT NOT NULL,
    details   JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS metrics (
    id         BIGSERIAL PRIMARY KEY,
    metric     TEXT NOT NULL UNIQUE,
    value      BIGINT NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_node_connections_left  ON node_connections(left_node_id);
CREATE INDEX IF NOT EXISTS idx_node_connections_right ON node_connections(right_node_id);
CREATE INDEX IF NOT EXISTS idx_beacon_packets_origin  ON beacon_packets(origin_node_id);
CREATE INDEX IF NOT EXISTS idx_beacon_packets_created ON beacon_packets(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_events_timestamp ON audit_events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_events_packet_id ON audit_events(packet_id);
CREATE INDEX IF NOT EXISTS idx_packet_deliveries_packet_id ON packet_deliveries(packet_id);

INSERT INTO metrics (metric, value) VALUES
    ('submitted', 0),
    ('delivered', 0),
    ('dropped_duplicate', 0),
    ('dropped_invalid_signature', 0),
    ('dropped_invalid_packet', 0),
    ('dropped_unreachable', 0)
ON CONFLICT (metric) DO NOTHING;
