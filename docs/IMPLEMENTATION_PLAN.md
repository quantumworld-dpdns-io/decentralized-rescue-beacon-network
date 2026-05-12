# Decentralized Rescue Beacon Network: Expanded Implementation and Test Plan

## Objectives

- Build a resilient multi-hop distress relay baseline in `src/`.
- Add verifiable safety controls inspired by the reference folder.
- Provide executable tests and CI automation as the initial delivery gate.

## Reference-Driven Technical Direction

### MCP concepts (Model Context Protocol)
- Keep clear boundaries between read-only context and write-capable actions.
- Model future integrations as explicit tools with structured inputs and outputs.
- Keep auditable execution traces for sensitive actions.

### LangGraph/CrewAI concepts
- Separate workflow orchestration from worker logic.
- Keep state explicit and testable across each relay step.
- Design for parallel independent work units and deterministic merge behavior.

### Redis concepts
- Use key namespace conventions for de-duplication state.
- Support TTL expiration for volatile packet records.
- Keep path open for Redis-backed implementations without changing domain logic.

### PQC concepts
- Enforce signature validation before relaying distress packets.
- Keep algorithm labeling explicit to support crypto agility and migration.
- Avoid custom cryptographic protocols; keep a replaceable signer abstraction.

## Expanded Work Breakdown

1. **Domain model and boundary contracts**
   - Keep immutable packet and outcome structures.
   - Add explicit batch outcome and audit event models for deterministic orchestration and observability.
2. **Relay engine determinism and safety**
   - Keep bounded multi-hop delivery with deterministic route traversal order.
   - Enforce input validation boundaries before relay execution.
   - Preserve Redis-style namespace + TTL de-duplication behavior.
3. **Reference-driven workflow concepts**
   - Apply LangGraph/CrewAI orchestrator-worker concept with deterministic batch packet merge behavior.
   - Apply MCP-style auditable action traces through structured event records.
   - Keep signer abstraction and algorithm labeling for crypto agility.
4. **MCP-style tool boundary (`BeaconNetworkToolBoundary`)**
   - Expose read-only topology resources (`resource_registered_nodes`, `resource_node_neighbors`, `resource_reachable_nodes`) with no side effects on network state.
   - Expose write-capable packet submission tools (`tool_submit_packet`, `tool_submit_packets`) with observable side effects.
   - Maintain a separate, boundary-level audit log for every resource and tool call, independent of the network audit log.
5. **Quality and delivery gates**
   - Extend tests for validation boundaries, deterministic route selection, batch orchestration, and audit traces.
   - Add dedicated test file for tool boundary behavior: read/write separation, audit event correctness, no-side-effect guarantees for resource calls.
   - Maintain CI checks: unit tests + source compilation.
   - Keep user-facing docs in sync with implementation behavior.

## Test Plan

### Unit tests
- Verify multi-hop routing returns shortest discovered path and expected recipients.
- Verify deterministic path selection when multiple equal-hop routes exist.
- Verify target filtering relays only to requested reachable nodes.
- Verify duplicate packet submissions are rejected within TTL window.
- Verify invalid/tampered packet signatures are rejected.
- Verify invalid packet boundary checks reject malformed packets.
- Verify batch submissions produce deterministic packet ordering and merged summary counts.
- Verify audit log records accepted and dropped submission events with structured reasons.
- Verify TTL store expiration removes stale keys.
- Verify relay metrics reflect accepted and rejected packet attempts.
- **Tool boundary – read resources:** verify `resource_registered_nodes`, `resource_node_neighbors`, and `resource_reachable_nodes` return correct data without altering network state, dedupe slots, or metrics.
- **Tool boundary – write tools:** verify `tool_submit_packet` and `tool_submit_packets` deliver packets, update metrics, and emit boundary-level pre/post audit events.
- **Tool boundary – audit log:** verify boundary audit log is independent of the network audit log, supports limit slicing, and records timestamps.

### CI checks
- Run `python -m unittest discover -s tests -p 'test_*.py'`.
- Run `python -m compileall src` to catch syntax-level breakage.

## Delivery Scope Implemented in This Change

- Existing in-memory decentralized relay baseline with signer + TTL store abstractions.
- Expanded boundary model with `BatchRelayOutcome` and `AuditEvent`.
- Deterministic route traversal and deterministic batch merge ordering.
- Packet validation boundary checks before relay operations.
- Structured audit log for submission lifecycle observability.
- **`BeaconNetworkToolBoundary`** – explicit MCP-style read/write separation:
  - Read-only topology resources with no network side effects.
  - Write-capable packet submission tools with auditable pre/post events.
  - Separate boundary-level audit log independent of the network audit log.
- Expanded tests covering deterministic routing, validation boundaries, batch behavior, audit tracing, and full tool boundary behavior.
