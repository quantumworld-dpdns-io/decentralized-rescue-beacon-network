# DragonflyDB Dragonfly

| Field | Details |
| --- | --- |
| Project | Dragonfly |
| Vendor / steward | DragonflyDB |
| Category | In-memory data store, cache, Redis-compatible datastore |
| Naming note | This file is under `software-tools/Apache/`, but this entry refers to DragonflyDB Dragonfly, not an Apache Software Foundation project. |
| License | Business Source License 1.1, with an Apache License 2.0 change license on the configured change date |
| APIs | Redis-compatible API, Valkey-compatible API, Memcached-compatible API |
| Primary use cases | High-throughput caching, session storage, real-time application state, feature stores, job queues, and Redis/Memcached replacement evaluations |
| Implementation | C++ |
| Architecture emphasis | Multi-threaded, shared-nothing design with sharded keyspace ownership |
| Deployment options | Self-managed binary/container, Kubernetes operator, and Dragonfly Cloud |
| Official site | https://www.dragonflydb.io/ |
| Official docs | https://www.dragonflydb.io/docs |
| Source repository | https://github.com/dragonflydb/dragonfly |

## English

### Overview

Dragonfly is a modern in-memory data store from DragonflyDB. It is designed as a high-performance replacement or complement for Redis, Valkey, and Memcached-compatible workloads. The main adoption path is intentionally familiar: point existing Redis or Memcached clients at Dragonfly, validate command compatibility, and benchmark the workload under production-like conditions.

Dragonfly is not an Apache project. The "Apache" part of this file path should be treated as a repository categorization issue, not as a statement about the project's governance or license.

DragonflyDB describes Dragonfly as an in-memory datastore that is compatible with Redis and Memcached APIs and built around a multi-threaded, shared-nothing architecture. Its value proposition is higher throughput per instance, lower tail latency under heavy load, and simpler operations for workloads that would otherwise require Redis cluster sharding.

### Why it matters

Redis-compatible systems are common in application infrastructure, but large caches can become operationally expensive when a single-threaded or lightly threaded design requires many nodes, manual sharding, or cluster rebalancing. Dragonfly matters because it tries to preserve the client ecosystem while changing the execution architecture underneath.

For engineering teams, the practical benefits are:

- **Migration path**: Existing Redis clients, command patterns, and operational habits can often be reused.
- **Vertical scale**: A multi-core host can be used more fully before adding more nodes.
- **Operational simplicity**: Some workloads can run on fewer, larger instances instead of a larger Redis cluster.
- **Workload fit**: Caching, ephemeral state, leaderboards, queues, counters, feature stores, and real-time services can benefit from high in-memory throughput.
- **Cost evaluation**: Fewer nodes and better memory efficiency can reduce infrastructure cost, but this must be verified against the real dataset, command mix, persistence settings, and failure model.

The licensing model also matters. Dragonfly is source-available under BSL 1.1, not a conventional permissive open-source license for all uses. Production, hosted, or competitive service use should be reviewed against the official license before adoption.

### Architecture/Concepts

| Concept | Role in Dragonfly |
| --- | --- |
| Redis-compatible API | Lets many Redis clients and tools communicate with Dragonfly using familiar commands and RESP. |
| Valkey-compatible API | Supports migration paths from Valkey-compatible client ecosystems. |
| Memcached-compatible API | Allows selected Memcached workloads to be served by Dragonfly. |
| Multi-threaded engine | Uses multiple CPU cores for request processing instead of relying on a single main execution thread. |
| Shared-nothing architecture | Partitions keyspace ownership across shards so each thread manages its own slice of data. |
| Shards | Internal keyspace partitions assigned to worker threads. |
| Atomic operations | Dragonfly is designed to preserve atomicity guarantees while processing high-throughput workloads. |
| Dashtable | Dragonfly's memory-efficient hash table design, used to improve CPU and memory behavior. |
| Cache mode | Optional mode that turns Dragonfly into a cache with adaptive eviction near the memory limit. |
| Snapshotting | Persistence mechanism for saving the dataset without Redis-style fork overhead. |
| Replication / high availability | Operational features to evaluate carefully for the target deployment mode and version. |
| Metrics | Prometheus-compatible metrics are exposed for observability. |
| Kubernetes operator | DragonflyDB provides an operator for installing and managing Dragonfly instances in Kubernetes. |

Typical request flow:

1. A client connects with a Redis, Valkey, or Memcached-compatible protocol.
2. Dragonfly maps the key or command to the relevant shard.
3. The owning thread processes the request against its shard-local data structures.
4. Multi-key or cross-shard operations use Dragonfly's transactional coordination model.
5. Results return through the same client protocol, so application code can often remain unchanged.

Architectural tradeoffs:

- Multi-threading can deliver much higher throughput on large machines, but it does not remove the need to benchmark command-specific behavior.
- Compatibility is broad, but not every Redis feature, module, command nuance, or operational assumption is automatically identical.
- Fewer nodes can simplify operations, but large single instances still need clear backup, failover, memory, and blast-radius planning.
- Source availability is useful for inspection and contribution, but BSL restrictions can affect commercial usage patterns.

### Practical usage

A pragmatic evaluation should start small, then move toward a representative production test.

1. **Run Dragonfly locally**

   ```bash
   docker run --network=host --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly
   ```

2. **Connect with a Redis client**

   ```bash
   redis-cli -p 6379
   SET hello world
   GET hello
   ```

3. **Test application compatibility**

   - Reuse the existing Redis client library.
   - Change only the endpoint, authentication, TLS, and connection settings required by the environment.
   - Run integration tests that cover key expiration, transactions, Lua scripts, pipelining, pub/sub, streams, and any commands the application depends on.

4. **Benchmark the real workload**

   - Measure read/write ratio, payload size, pipelining, connection count, TTL usage, hot-key behavior, and eviction pressure.
   - Compare p50, p95, p99, and p99.9 latency, not only peak QPS.
   - Include persistence, snapshots, replication, failover, and restart recovery in the test plan.
   - Compare against the current Redis, Valkey, or Memcached deployment using the same instance class and network conditions where possible.

5. **Prepare production operations**

   - Set `--requirepass` or equivalent authentication configuration.
   - Bind only to trusted interfaces and review HTTP/admin console exposure.
   - Configure `--maxmemory` and cache mode deliberately.
   - Export Prometheus metrics and define SLO alerts.
   - Validate backup, restore, upgrade, failover, and rollback procedures.
   - Review the BSL license terms for the intended use.

Example configuration shape:

```bash
dragonfly \
  --bind 127.0.0.1 \
  --port 6379 \
  --requirepass strong-password \
  --maxmemory 12gb \
  --cache_mode=true
```

Good initial fit:

- Large Redis caches constrained by CPU rather than memory alone.
- Redis clusters where sharding and rebalancing dominate operational work.
- Latency-sensitive read-heavy or mixed read/write workloads.
- Teams that want Redis ecosystem compatibility but are willing to validate behavior against a different engine.

Be cautious when:

- The application depends on obscure Redis command semantics, Redis modules, or version-specific behavior.
- Managed service licensing or competitive hosted-service usage is part of the business model.
- The workload requires mature multi-region disaster recovery patterns.
- A single large node would create an unacceptable failure domain.

### Learning checklist

- [ ] Confirm that this entry is DragonflyDB Dragonfly, not Apache Dragonfly or Dragonfly OSS P2P distribution.
- [ ] Read the official Dragonfly documentation overview.
- [ ] Review the BSL 1.1 license and the Apache 2.0 change-license date.
- [ ] Run Dragonfly locally with Docker.
- [ ] Connect using `redis-cli` and a production application client library.
- [ ] List every Redis, Valkey, or Memcached command used by the application.
- [ ] Check command compatibility against the official command reference.
- [ ] Benchmark realistic payload sizes, TTLs, connection counts, and pipeline depth.
- [ ] Compare p99 and p99.9 latency under sustained load.
- [ ] Test persistence, snapshotting, restart recovery, replication, and failover.
- [ ] Configure authentication, binding, metrics, and alerting before any production rollout.

## 繁體中文

### 概覽

Dragonfly 是 DragonflyDB 開發的現代化 in-memory data store。它的定位是 Redis、Valkey 與 Memcached 相容工作負載的高效能替代方案或補充方案。導入方式通常很接近既有 Redis/Memcached 運維流程：把 client endpoint 指向 Dragonfly，確認 command compatibility，然後用接近正式環境的流量與資料型態做 benchmark。

Dragonfly 不是 Apache Software Foundation 專案。本檔案位於 `software-tools/Apache/` 目錄下，應視為此 repository 的分類問題，不代表 Dragonfly 的治理模式或授權屬於 Apache。

DragonflyDB 官方將 Dragonfly 描述為相容 Redis 與 Memcached API 的 in-memory datastore，核心設計採用 multi-threaded、shared-nothing 架構。它主打在單一 instance 上提供更高吞吐量、在高負載下維持較低 tail latency，並降低原本需要 Redis cluster sharding 的操作複雜度。

### 為什麼重要

Redis-compatible 系統在應用基礎設施中很常見，但大型 cache 若受到單執行緒或有限多執行緒設計限制，可能需要更多節點、手動 sharding 或 cluster rebalancing，進而提高成本與操作複雜度。Dragonfly 的重要性在於保留既有 client 生態，同時替換底層執行架構。

對工程團隊而言，實務價值包括：

- **遷移路徑**：許多 Redis client、command pattern 與操作習慣可以沿用。
- **垂直擴展**：在增加節點前，更充分利用單台多核心主機。
- **降低操作複雜度**：部分工作負載可用較少、較大的 instance 取代較大的 Redis cluster。
- **工作負載適配**：cache、ephemeral state、leaderboard、queue、counter、feature store 與 real-time service 都可能受益於高 in-memory throughput。
- **成本評估**：較少節點與較佳記憶體效率可能降低成本，但必須用實際資料集、command mix、persistence 設定與故障模型驗證。

授權模式也很重要。Dragonfly 是以 BSL 1.1 提供 source-available 授權，不是所有用途都無限制的傳統 permissive open-source license。若要用於正式環境、hosted service 或可能與 DragonflyDB 競爭的服務，導入前應檢查官方授權條款。

### 架構/概念

| 概念 | 在 Dragonfly 中的角色 |
| --- | --- |
| Redis-compatible API | 讓許多 Redis client 與工具透過熟悉的 command 與 RESP 協定連到 Dragonfly。 |
| Valkey-compatible API | 支援從 Valkey-compatible client 生態遷移。 |
| Memcached-compatible API | 讓特定 Memcached 工作負載可由 Dragonfly 提供服務。 |
| Multi-threaded engine | 使用多個 CPU core 處理 request，而不是依賴單一主要執行緒。 |
| Shared-nothing architecture | 將 keyspace ownership 分散到 shard，讓每個 thread 管理自己的資料切片。 |
| Shards | 由 worker thread 負責的內部 keyspace partition。 |
| Atomic operations | Dragonfly 設計目標是在高吞吐量下保留 operation atomicity guarantee。 |
| Dashtable | Dragonfly 的記憶體效率 hash table 設計，用來改善 CPU 與 memory behavior。 |
| Cache mode | 可選模式，讓 Dragonfly 在接近 memory limit 時以 adaptive eviction 作為 cache 使用。 |
| Snapshotting | 用於保存資料集的 persistence 機制，避免 Redis fork-style snapshot 的部分額外負擔。 |
| Replication / high availability | 需要依部署模式與版本仔細評估的營運能力。 |
| Metrics | 提供 Prometheus-compatible metrics，方便觀測與告警。 |
| Kubernetes operator | DragonflyDB 提供 operator，用於在 Kubernetes 中安裝與管理 Dragonfly instance。 |

典型 request flow：

1. Client 使用 Redis、Valkey 或 Memcached-compatible protocol 連線。
2. Dragonfly 依 key 或 command 對應到相關 shard。
3. 擁有該 shard 的 thread 對 shard-local data structure 執行 request。
4. Multi-key 或 cross-shard operation 透過 Dragonfly 的 transactional coordination model 處理。
5. 結果透過相同 client protocol 回傳，因此 application code 通常可少量或不需修改。

架構取捨：

- Multi-threading 可以在大型機器上提供更高 throughput，但仍需針對特定 command behavior 做 benchmark。
- Compatibility 很廣，但並不代表每個 Redis feature、module、command 細節或操作假設都完全相同。
- 較少節點可降低操作複雜度，但大型單一 instance 仍需清楚規劃 backup、failover、memory 與 blast radius。
- Source availability 有助於檢視與貢獻，但 BSL 限制可能影響商業使用情境。

### 實務使用

實際評估建議從小規模開始，再逐步推進到接近正式環境的代表性測試。

1. **本機執行 Dragonfly**

   ```bash
   docker run --network=host --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly
   ```

2. **使用 Redis client 連線**

   ```bash
   redis-cli -p 6379
   SET hello world
   GET hello
   ```

3. **測試 application compatibility**

   - 沿用既有 Redis client library。
   - 只調整環境必要的 endpoint、authentication、TLS 與 connection 設定。
   - 執行 integration tests，覆蓋 key expiration、transaction、Lua script、pipelining、pub/sub、streams 與 application 依賴的所有 command。

4. **用真實工作負載 benchmark**

   - 測量 read/write ratio、payload size、pipelining、connection count、TTL usage、hot-key behavior 與 eviction pressure。
   - 比較 p50、p95、p99 與 p99.9 latency，不只看 peak QPS。
   - 將 persistence、snapshot、replication、failover 與 restart recovery 納入測試計畫。
   - 盡可能在相同 instance class 與 network condition 下，與目前 Redis、Valkey 或 Memcached 部署比較。

5. **準備正式環境操作**

   - 設定 `--requirepass` 或等效 authentication configuration。
   - 只 bind 到可信任 interface，並檢查 HTTP/admin console 是否暴露。
   - 明確設定 `--maxmemory` 與 cache mode。
   - 匯出 Prometheus metrics 並建立 SLO alert。
   - 驗證 backup、restore、upgrade、failover 與 rollback procedure。
   - 依預期用途檢查 BSL 授權條款。

設定範例：

```bash
dragonfly \
  --bind 127.0.0.1 \
  --port 6379 \
  --requirepass strong-password \
  --maxmemory 12gb \
  --cache_mode=true
```

適合優先評估的情境：

- 大型 Redis cache 主要受 CPU 限制，而不只是受 memory 限制。
- Redis cluster 的 sharding 與 rebalancing 已成為主要操作負擔。
- 對 latency 敏感的 read-heavy 或 mixed read/write workload。
- 團隊希望保留 Redis 生態相容性，但願意針對不同 engine 驗證行為。

需要謹慎的情境：

- Application 依賴較冷門的 Redis command semantics、Redis modules 或特定版本行為。
- 商業模式包含 managed service、hosted service 或可能與 DragonflyDB 競爭的服務。
- 工作負載需要成熟的 multi-region disaster recovery pattern。
- 單一大型節點會造成無法接受的 failure domain。

### 學習檢核表

- [ ] 確認本條目是 DragonflyDB Dragonfly，不是 Apache Dragonfly 或 Dragonfly OSS P2P distribution。
- [ ] 閱讀 Dragonfly 官方文件 overview。
- [ ] 檢查 BSL 1.1 授權與 Apache 2.0 change-license date。
- [ ] 使用 Docker 在本機執行 Dragonfly。
- [ ] 使用 `redis-cli` 與正式 application client library 連線。
- [ ] 列出 application 使用的所有 Redis、Valkey 或 Memcached command。
- [ ] 依官方 command reference 檢查 compatibility。
- [ ] 用實際 payload size、TTL、connection count 與 pipeline depth 做 benchmark。
- [ ] 在 sustained load 下比較 p99 與 p99.9 latency。
- [ ] 測試 persistence、snapshotting、restart recovery、replication 與 failover。
- [ ] 在正式導入前設定 authentication、binding、metrics 與 alerting。

## References

- [Dragonfly official website](https://www.dragonflydb.io/)
- [Dragonfly documentation](https://www.dragonflydb.io/docs)
- [Dragonfly installation guide](https://www.dragonflydb.io/install)
- [Dragonfly GitHub repository](https://github.com/dragonflydb/dragonfly)
- [Dragonfly license](https://github.com/dragonflydb/dragonfly/blob/main/LICENSE.md)
- [Dragonfly Kubernetes operator](https://github.com/dragonflydb/dragonfly-operator)
