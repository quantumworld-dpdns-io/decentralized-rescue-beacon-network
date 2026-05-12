# LanceDB

| Field | Details |
| --- | --- |
| Category | Multimodal lakehouse and vector database |
| Project | LanceDB |
| License | Apache-2.0 for core open-source components |
| Primary use cases | RAG, multimodal retrieval, dataset curation, model training data, semantic search |
| Core data model | Lance tables with vectors, metadata, and multimodal columns |
| Search modes | Vector search, full-text search, SQL-style filtering, hybrid search |
| Deployment | Embedded OSS library, server/cloud and enterprise deployments |
| Last reviewed | 2026-04-29 |

## English

### Overview

LanceDB is an AI-native data and retrieval system built on the Lance columnar format. It is often described as a multimodal lakehouse for AI: vectors, metadata, text, images, video references, and other features can live together in versioned tables.

Unlike databases that only store vectors plus small metadata fields, LanceDB is designed for both retrieval applications and AI data management. It can support RAG and semantic search, but it is also useful for dataset curation, embedding pipelines, feature engineering, and model training data workflows.

### Why it matters

AI teams often split data across object storage, feature stores, vector databases, search indexes, and training pipelines. That makes retrieval and model development harder to reproduce. LanceDB matters because it keeps embeddings and the underlying multimodal records close together in a columnar table format with versioning and schema evolution.

This is useful when the same data must power online retrieval, offline evaluation, dataset sampling, labeling, and training. Teams can search by vector, filter by metadata, run full-text or hybrid search, and still treat the table as part of a broader lakehouse-style data workflow.

### Architecture/Concepts

Key concepts:

- **Lance format**: Columnar storage format designed for AI data, fast random access, versioning, and multimodal columns.
- **Table**: Main storage unit containing vectors, scalar metadata, text, and other columns.
- **Vector column**: Stores embeddings for similarity search.
- **Scalar and metadata columns**: Used for filtering, grouping, evaluation, and application constraints.
- **Full-text index**: Supports keyword search over text columns.
- **Hybrid search**: Combines vector and text search signals.
- **Versioning**: Tables can evolve over time while preserving reproducibility.
- **Schema evolution**: New columns can be added as features or metadata change.
- **Embedded usage**: OSS LanceDB can run inside Python, Node.js, or Rust applications without a separate server.
- **Managed/distributed options**: Cloud and enterprise offerings target larger-scale and operational workloads.

### Practical usage

Use LanceDB when:

- Your retrieval data is multimodal or larger than simple text chunks.
- You want vectors and source records in the same table.
- Dataset curation and model training data workflows matter alongside search.
- You need local embedded development with a path to managed or distributed deployment.
- You want table versioning and schema evolution for AI data.

Implementation tips:

- Store original content pointers, metadata, and embeddings together so retrieval results are auditable.
- Use separate vector columns when comparing embedding models.
- Add scalar filters for tenant, source, split, label status, language, and time.
- Keep evaluation datasets and production retrieval tables versioned.
- Benchmark both retrieval latency and data-management workloads such as sampling, filtering, and scans.

### Learning checklist

- [ ] Create a LanceDB table with vector and metadata columns.
- [ ] Insert text records and embeddings.
- [ ] Run vector search with scalar filters.
- [ ] Add full-text search and compare keyword, vector, and hybrid results.
- [ ] Add a new metadata or feature column through schema evolution.
- [ ] Use table versions to reproduce an earlier retrieval experiment.
- [ ] Compare embedded usage with server or managed deployment needs.
- [ ] Design a table that supports both RAG and offline evaluation.

## 繁體中文

### 概覽

LanceDB 是建立在 Lance 欄式格式上的 AI-native data 與 retrieval 系統。它常被描述為 AI 的 multimodal lakehouse：vectors、metadata、文字、圖片、影片參照與其他 features 可以一起存在具版本管理的 tables 中。

不同於只儲存 vectors 加少量 metadata 的資料庫，LanceDB 同時面向 retrieval application 與 AI data management。它可用於 RAG 與語意搜尋，也適合 dataset curation、embedding pipelines、feature engineering 與模型訓練資料流程。

### 為什麼重要

AI 團隊常把資料分散在 object storage、feature store、vector database、search index 與 training pipeline 中，導致 retrieval 與模型開發難以重現。LanceDB 的價值在於把 embeddings 與底層多模態資料放在同一個具版本與 schema evolution 的欄式 table format 中。

當同一批資料要支援線上 retrieval、離線評估、dataset sampling、標註與訓練時，這種設計很有用。團隊可以進行 vector search、metadata filtering、full-text 或 hybrid search，同時仍把 table 當作 lakehouse-style data workflow 的一部分。

### 架構/概念

核心概念：

- **Lance format**：為 AI data 設計的欄式儲存格式，支援快速 random access、versioning 與多模態欄位。
- **Table**：主要儲存單位，包含 vectors、scalar metadata、text 與其他欄位。
- **Vector column**：儲存 embeddings 以進行相似度搜尋。
- **Scalar 與 metadata columns**：用於 filtering、grouping、evaluation 與應用限制。
- **Full-text index**：支援文字欄位的 keyword search。
- **Hybrid search**：結合 vector 與 text search 訊號。
- **Versioning**：table 可隨時間演進並保留可重現性。
- **Schema evolution**：features 或 metadata 變化時可新增欄位。
- **Embedded usage**：OSS LanceDB 可在 Python、Node.js 或 Rust 應用內執行，不一定需要獨立 server。
- **Managed/distributed options**：cloud 與 enterprise 版本支援更大規模與維運需求。

### 實務使用

適合使用 LanceDB 的情境：

- retrieval data 是多模態，或比單純文字 chunk 更複雜。
- 想把 vectors 與 source records 放在同一張 table。
- 除搜尋外，也重視 dataset curation 與模型訓練資料流程。
- 需要本機 embedded 開發，並保留 managed 或 distributed deployment 路徑。
- 想替 AI data 使用 table versioning 與 schema evolution。

實作建議：

- 將原始內容指標、metadata 與 embeddings 一起儲存，讓 retrieval result 可稽核。
- 比較 embedding models 時，使用不同 vector columns。
- 為 tenant、source、split、label status、language 與 time 加入 scalar filters。
- 讓 evaluation datasets 與 production retrieval tables 都具備版本管理。
- 同時 benchmark retrieval latency 與 sampling、filtering、scan 等資料管理工作。

### 學習檢核表

- [ ] 建立含 vector 與 metadata columns 的 LanceDB table。
- [ ] 寫入文字 records 與 embeddings。
- [ ] 執行帶 scalar filters 的 vector search。
- [ ] 加入 full-text search，並比較 keyword、vector 與 hybrid results。
- [ ] 透過 schema evolution 新增 metadata 或 feature column。
- [ ] 使用 table versions 重現早期 retrieval experiment。
- [ ] 比較 embedded usage 與 server 或 managed deployment 需求。
- [ ] 設計同時支援 RAG 與離線評估的 table。

## References

- [LanceDB documentation](https://docs.lancedb.com/)
- [LanceDB official site](https://www.lancedb.com/)
- [LanceDB quickstart](https://docs.lancedb.com/core/)
- [LanceDB search documentation](https://docs.lancedb.com/core/search/)
- [LanceDB tables documentation](https://docs.lancedb.com/core/table/)
- [Lance format documentation](https://lancedb.github.io/lance/)
