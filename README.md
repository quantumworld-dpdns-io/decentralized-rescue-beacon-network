# decentralized-rescue-beacon-network

> Decentralized rescue beacon network – secure distress-signal system utilizing multi-hop emergency packets across any reachable node.

## Overview

This repository is part of the [quantumworld-dpdns-io](https://github.com/quantumworld-dpdns-io) Wild SaaS & Tech Development initiative.

This baseline implementation now includes:

- In-memory multi-hop distress packet relay engine.
- Packet signing and verification boundary for crypto-agile security migration.
- Redis-style TTL de-duplication primitives.
- Deterministic route traversal and deterministic batch packet orchestration.
- Structured relay audit events for operational observability.
- **MCP-style tool boundary** – explicit read-only topology resources and write-capable packet submission tools with separate audit trails.
- Unit tests and CI execution commands.

## Project Structure

```
.
├── src/rescue_beacon_network/   # Core relay package
├── tests/                       # Unit tests
├── docs/                        # Contributing and implementation plans
├── ref/                         # Reference technology notes
└── .github/workflows/           # CI pipelines
```

## Getting Started

```bash
git clone https://github.com/quantumworld-dpdns-io/decentralized-rescue-beacon-network.git
cd decentralized-rescue-beacon-network
python -m unittest discover -s tests -p 'test_*.py'
```

## Example (Python)

```python
from src.rescue_beacon_network import BeaconPacket, DecentralizedRescueBeaconNetwork, HMACPacketSigner
from src.rescue_beacon_network import BeaconNetworkToolBoundary

signer = HMACPacketSigner(secret="rescue-secret")
network = DecentralizedRescueBeaconNetwork(signer=signer)
network.connect_nodes("A", "B")
network.connect_nodes("B", "C")

# Direct network usage
packet = signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "medical"}, max_hops=2))
outcome = network.submit_distress_packet(packet)
print(outcome.delivered_nodes)  # ['B', 'C']

batch = network.submit_distress_packets([packet])
print(batch.ordered_packet_ids)  # deterministic packet id order
print(network.audit_log(limit=2))  # latest structured relay events

# MCP-style tool boundary
boundary = BeaconNetworkToolBoundary(network)

# Read-only topology resources (no side effects)
print(boundary.resource_registered_nodes())          # ['A', 'B', 'C']
print(boundary.resource_node_neighbors("B"))         # ['A', 'C']
print(boundary.resource_reachable_nodes("A", max_hops=2))  # ['B', 'C']

# Write-capable packet submission tools
packet2 = signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "fire"}, max_hops=1))
outcome2 = boundary.tool_submit_packet(packet2)
print(outcome2.delivered_nodes)  # ['B']
print(boundary.audit_log(limit=2))  # boundary-level audit events
```

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) before opening a pull request.

## License

[MIT](LICENSE)
