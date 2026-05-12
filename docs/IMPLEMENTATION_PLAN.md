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

## Planned Work Breakdown

1. **Domain model foundation**
   - Define packet and relay outcome structures.
   - Define deterministic packet identity and metadata fields.
2. **Core network relay engine**
   - Build in-memory node graph registration and bidirectional links.
   - Implement bounded multi-hop route discovery.
   - Add target-specific delivery filtering.
3. **Safety controls**
   - Add packet de-duplication with TTL semantics.
   - Add signer abstraction and packet signature verification.
   - Add basic relay metrics for operational observability.
4. **Quality and developer workflow**
   - Add unit tests for routing, edge cases, de-duplication, and signature validation.
   - Add CI workflow commands to run the test suite and source compilation checks.
   - Update README with architecture and local usage instructions.

## Test Plan

### Unit tests
- Verify multi-hop routing returns shortest discovered path and expected recipients.
- Verify target filtering relays only to requested reachable nodes.
- Verify duplicate packet submissions are rejected within TTL window.
- Verify invalid/tampered packet signatures are rejected.
- Verify TTL store expiration removes stale keys.
- Verify relay metrics reflect accepted and rejected packet attempts.

### CI checks
- Run `python -m unittest discover -s tests -p 'test_*.py'`.
- Run `python -m compileall src` to catch syntax-level breakage.

## Delivery Scope Implemented in This Change

- A working in-memory decentralized relay baseline.
- A replaceable signer and TTL cache abstraction.
- Test coverage for routing and safety controls.
- CI and README updates to support ongoing iteration.
