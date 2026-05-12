# Milvus

| Field | Details |
| --- | --- |
| Category | Cloud-native vector database |
| Project | Milvus |
| License | Apache-2.0 |
| Primary use cases | Large-scale similarity search, RAG, AI agents, recommendations, multimodal retrieval |
| Core data model | Collections, partitions, schemas, vector fields, scalar fields, indexes |
| Search modes | Vector search, scalar query, hybrid search, full-text search, multi-vector search |
| Deployment | Standalone, distributed cluster on Kubernetes, Zilliz Cloud |
| Last reviewed | 2026-04-29 |

## English

### Overview

Milvus is an open-source, cloud-native vector database designed for high-performance similarity search over large vector datasets. It supports dense vectors, sparse vectors, scalar fields, filtering, hybrid search, full-text search features, and multiple index types through libraries such as Faiss, HNSW, DiskANN, and SCANN.

Milvus can run as a simple standalone service for smaller workloads or as a distributed cluster for large datasets and high-throughput production traffic. Zilliz Cloud provides a managed service built around Milvus.

### Why it matters

Vector search moves from prototype to infrastructure once data volume, write rate, availability, and operational controls matter. Milvus is built for that scale: it separates access, coordination, worker execution, and storage so each layer can scale independently.

This makes Milvus a strong fit for teams building retrieval systems over millions to billions of vectors, especially when they need Kubernetes deployment, independent scaling, background compaction and indexing, and a path to managed cloud operations.

### Architecture/Concepts

Key concepts:

- **Collection**: A logical dataset with schema, vector fields, scalar fields, and index definitions.
- **Partition**: A subdivision of a collection, often used for time, category, or tenant-based organization.
- **Schema**: Defines primary keys, vector dimensions, scalar fields, dynamic fields, and data types.
- **Index**: Accelerates vector search using index families such as HNSW, IVF, DiskANN, SCANN, or sparse indexes.
- **Proxy**: Stateless access layer that validates requests and aggregates results.
- **Coordinator**: Control-plane service that manages metadata, scheduling, topology, timestamps, and consistency.
- **Streaming Node**: Handles real-time write processing, growing data search, and WAL-backed recovery.
- **Query Node**: Loads sealed historical segments and serves search/query requests.
- **Data Node**: Runs offline work such as compaction and index building.
- **Storage layer**: Uses metadata storage, object storage, and WAL storage for persistence.

### Practical usage

Use Milvus when:

- You expect large vector collections and heavy search traffic.
- You need a distributed, Kubernetes-friendly vector database.
- You need multiple index choices for different latency, recall, memory, and cost targets.
- You want vector search with scalar filtering and hybrid retrieval.
- You need a managed option through Zilliz Cloud but want open-source portability.

Implementation tips:

- Start standalone for learning, but design production around the cluster architecture if scale is expected.
- Choose index types based on vector count, update pattern, recall target, and hardware.
- Use scalar fields and partitions to reduce the search space where natural boundaries exist.
- Track segment growth, compaction, index build time, and object storage behavior.
- Test consistency expectations for recent writes before relying on read-after-write behavior.
- Plan backup, restore, monitoring, and upgrade procedures as part of the first production design.

### Learning checklist

- [ ] Create a collection with vector and scalar fields.
- [ ] Insert, upsert, delete, and query records.
- [ ] Build and compare at least two vector index types.
- [ ] Run vector search with scalar filters.
- [ ] Try hybrid retrieval with dense and sparse signals.
- [ ] Explain Proxy, Coordinator, Streaming Node, Query Node, and Data Node roles.
- [ ] Deploy standalone Milvus locally.
- [ ] Review the cluster dependencies for metadata, object storage, and WAL storage.

## 繁體中文

### 概覽

Milvus 是開源、cloud-native 的向量資料庫，設計目標是在大型向量資料集上進行高效能相似度搜尋。它支援 dense vectors、sparse vectors、scalar fields、filtering、hybrid search、full-text search 功能，以及 Faiss、HNSW、DiskANN、SCANN 等多種索引。

Milvus 可以用 standalone 模式支援較小工作負載，也可以用分散式 cluster 支援大型資料集與高流量生產環境。Zilliz Cloud 則提供以 Milvus 為核心的 managed service。

### 為什麼重要

當資料量、寫入率、可用性與維運控制變重要時，向量搜尋就不再只是 prototype，而是基礎架構。Milvus 透過 access、coordination、worker execution 與 storage 分層，讓不同層能獨立擴展。

因此 Milvus 適合在數百萬到數十億 vectors 上建立檢索系統，尤其是需要 Kubernetes 部署、獨立擴展、背景 compaction/indexing，以及 managed cloud 選項的團隊。

### 架構/概念

核心概念：

- **Collection**：包含 schema、vector fields、scalar fields 與 index definitions 的邏輯資料集。
- **Partition**：collection 的子分區，常用於時間、分類或租戶切分。
- **Schema**：定義 primary key、vector dimensions、scalar fields、dynamic fields 與資料型別。
- **Index**：用 HNSW、IVF、DiskANN、SCANN 或 sparse index 等方式加速搜尋。
- **Proxy**：stateless access layer，負責驗證請求與彙總結果。
- **Coordinator**：控制平面服務，管理 metadata、排程、拓撲、timestamp 與一致性。
- **Streaming Node**：處理即時寫入、growing data search 與 WAL-backed recovery。
- **Query Node**：載入 sealed historical segments 並服務 search/query requests。
- **Data Node**：執行 compaction、index building 等離線工作。
- **Storage layer**：使用 metadata storage、object storage 與 WAL storage 進行持久化。

### 實務使用

適合使用 Milvus 的情境：

- 預期有大型 vector collections 與高搜尋流量。
- 需要分散式、適合 Kubernetes 的向量資料庫。
- 需要多種索引以平衡 latency、recall、memory 與成本。
- 需要 vector search 搭配 scalar filtering 與 hybrid retrieval。
- 想使用 Zilliz Cloud managed option，同時保留開源可攜性。

實作建議：

- 學習可從 standalone 開始；若預期擴展，生產設計應以 cluster 架構為準。
- 依 vector 數量、更新模式、recall 目標與硬體選擇 index type。
- 有自然邊界時，用 scalar fields 與 partitions 縮小搜尋範圍。
- 監控 segment growth、compaction、index build time 與 object storage 行為。
- 在依賴 read-after-write 前，先測試近期寫入的一致性行為。
- 將備份、還原、監控與升級流程納入第一版生產設計。

### 學習檢核表

- [ ] 建立含 vector 與 scalar fields 的 collection。
- [ ] 執行 insert、upsert、delete 與 query。
- [ ] 建立並比較至少兩種 vector index。
- [ ] 執行帶 scalar filters 的 vector search。
- [ ] 試用 dense 與 sparse 訊號的 hybrid retrieval。
- [ ] 說明 Proxy、Coordinator、Streaming Node、Query Node 與 Data Node 的角色。
- [ ] 在本機部署 standalone Milvus。
- [ ] 檢查 cluster 對 metadata、object storage 與 WAL storage 的依賴。

## References

- [Milvus documentation](https://milvus.io/docs)
- [Milvus architecture overview](https://milvus.io/docs/architecture_overview.md)
- [Milvus main components](https://milvus.io/docs/main_components.md)
- [Milvus install documentation](https://milvus.io/docs/install-overview.md)
- [Milvus manage collections](https://milvus.io/docs/manage-collections.md)
- [Milvus hybrid search](https://milvus.io/docs/multi-vector-search.md)
