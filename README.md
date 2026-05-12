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

signer = HMACPacketSigner(secret="rescue-secret")
network = DecentralizedRescueBeaconNetwork(signer=signer)
network.connect_nodes("A", "B")
network.connect_nodes("B", "C")

packet = signer.sign(BeaconPacket(origin_node_id="A", distress_payload={"type": "medical"}, max_hops=2))
outcome = network.submit_distress_packet(packet)
print(outcome.delivered_nodes)  # ['B', 'C']

batch = network.submit_distress_packets([packet])
print(batch.ordered_packet_ids)  # deterministic packet id order
print(network.audit_log(limit=2))  # latest structured relay events
```

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) before opening a pull request.

## License

[MIT](LICENSE)
