# Qdrant

| Field | Details |
| --- | --- |
| Category | Vector database and retrieval engine |
| Project | Qdrant |
| License | Apache-2.0 |
| Primary use cases | Semantic search, RAG, AI agent memory, recommendations, anomaly search |
| Core data model | Collections of points with vectors, IDs, and JSON payload metadata |
| Search modes | Dense vector, sparse vector, hybrid retrieval, filtered search, multivector search |
| Deployment | Local Docker, self-hosted server, Kubernetes, Qdrant Cloud |
| Last reviewed | 2026-04-29 |

## English

### Overview

Qdrant is an open-source vector database written in Rust. It stores embeddings and payload metadata, then retrieves similar items with low-latency vector search and filtering. It is commonly used as the retrieval layer for RAG systems, semantic search, recommendations, AI agents, and multimodal search.

Qdrant is especially strong when retrieval needs metadata-aware filtering. A point can hold one or more named dense vectors, sparse vectors, and JSON payload fields. Queries can combine vector similarity with filters over tags, numbers, geo fields, nested objects, text fields, and vector presence.

### Why it matters

Modern AI systems rarely need pure nearest-neighbor search only. They need semantic matching plus business constraints such as tenant, language, time range, access rights, source type, and product availability. Qdrant matters because it treats filtering as part of retrieval, not only as a post-processing step.

It also supports hybrid dense-sparse retrieval, so teams can combine semantic similarity with lexical relevance from sparse vectors such as BM25-style or SPLADE-style representations. That is useful when exact terms, IDs, product names, code symbols, or legal phrases must rank well alongside paraphrases.

### Architecture/Concepts

Key concepts:

- **Collection**: A named group of points with vector configuration, distance metrics, shard settings, and payload indexes.
- **Point**: The stored record. It has an integer or UUID ID, vectors, and optional JSON payload.
- **Named vectors**: Multiple vectors per point, useful for text, image, title, body, or model-version-specific embeddings.
- **Sparse vectors**: High-dimensional sparse representations for lexical or hybrid search.
- **Payload indexes**: Indexes over metadata fields so filters can run efficiently during search.
- **HNSW index**: Approximate nearest-neighbor graph used for fast dense-vector search.
- **Segments**: Internal storage units that Qdrant optimizes in the background.
- **Shards and replicas**: Distribution units for scaling collections and improving availability.
- **Quantization**: Compression options that trade some precision for lower memory and faster search.
- **Universal Query API**: Query interface for composing dense, sparse, hybrid, prefetch, reranking, and fusion workflows.

### Practical usage

Use Qdrant when:

- You need production-grade vector retrieval with strong metadata filtering.
- RAG results must respect permissions, tenants, recency, product state, or document type.
- Hybrid dense-sparse retrieval is important for relevance.
- You want a self-hosted engine with a managed cloud option.
- You need multiple vectors per object for multimodal or multi-field retrieval.

Implementation tips:

- Create payload indexes for fields used in filters before scaling traffic.
- Use named vectors instead of separate collections when one object needs multiple embedding views.
- Evaluate dense-only, sparse-only, and hybrid retrieval against the same relevance set.
- Tune HNSW, quantization, and replication based on recall, latency, and memory goals.
- Store authorization metadata with each point and filter on it at query time.

### Learning checklist

- [ ] Create a collection with a dense vector configuration.
- [ ] Insert points with vectors and JSON payload metadata.
- [ ] Run a nearest-neighbor search with a metadata filter.
- [ ] Add a payload index for a frequently filtered field.
- [ ] Add named vectors for separate title and body embeddings.
- [ ] Compare dense, sparse, and hybrid retrieval quality.
- [ ] Understand when HNSW parameters affect recall and latency.
- [ ] Test backup, restore, sharding, and replication before production.

## 繁體中文

### 概覽

Qdrant 是以 Rust 撰寫的開源向量資料庫。它會儲存 embedding 與 payload metadata，並以低延遲的向量搜尋與過濾功能找出相似資料。常見用途包含 RAG、語意搜尋、推薦系統、AI Agent 記憶與多模態搜尋。

Qdrant 的特色是 metadata-aware retrieval。一筆 point 可以包含一個或多個具名 dense vector、sparse vector，以及 JSON payload。查詢時可以把向量相似度與標籤、數值、地理位置、巢狀物件、文字欄位或向量存在性等條件一起使用。

### 為什麼重要

現代 AI 系統很少只需要單純最近鄰搜尋。實務上還需要租戶、語言、時間範圍、存取權限、來源類型與商品狀態等限制。Qdrant 的價值在於把 filter 視為 retrieval 的一部分，而不是搜尋後才補做的處理。

它也支援 dense-sparse hybrid retrieval，可把語意相似度與 BM25 或 SPLADE 類型 sparse vector 的詞彙訊號結合。當查詢包含精確術語、ID、商品名稱、程式符號或法律片語時，這點特別有用。

### 架構/概念

核心概念：

- **Collection**：point 的集合，包含 vector 設定、距離度量、shard 與 payload index。
- **Point**：被儲存的資料紀錄，包含整數或 UUID ID、vectors 與可選 JSON payload。
- **Named vectors**：同一筆資料可有多個向量，例如文字、圖片、標題、內文或不同模型版本。
- **Sparse vectors**：用於詞彙或 hybrid search 的高維稀疏表示。
- **Payload indexes**：針對 metadata 欄位建立索引，讓 filter 搜尋更有效率。
- **HNSW index**：用於快速 dense-vector search 的近似最近鄰圖索引。
- **Segments**：Qdrant 內部儲存單位，會在背景自動最佳化。
- **Shards 與 replicas**：用於擴展 collection 與提升可用性的分散單位。
- **Quantization**：壓縮選項，可在精度、記憶體與速度之間取捨。
- **Universal Query API**：用來組合 dense、sparse、hybrid、prefetch、reranking 與 fusion 查詢。

### 實務使用

適合使用 Qdrant 的情境：

- 需要具備強 metadata filtering 的生產級向量檢索。
- RAG 結果必須遵守權限、租戶、時間、商品狀態或文件類型。
- 需要 hybrid dense-sparse retrieval 來提升相關性。
- 想要可自架，也有 managed cloud 的向量引擎。
- 單一物件需要多個向量來支援多模態或多欄位檢索。

實作建議：

- 對常用 filter 欄位先建立 payload index。
- 同一物件有多種 embedding view 時，優先使用 named vectors。
- 用相同 relevance set 比較 dense-only、sparse-only 與 hybrid retrieval。
- 依 recall、latency 與 memory 目標調整 HNSW、quantization 與 replication。
- 將授權 metadata 存在 point 上，並在 query time filter。

### 學習檢核表

- [ ] 建立一個含 dense vector 設定的 collection。
- [ ] 寫入含 vectors 與 JSON payload metadata 的 points。
- [ ] 執行帶 metadata filter 的 nearest-neighbor search。
- [ ] 為常用 filter 欄位建立 payload index。
- [ ] 使用 named vectors 分別存標題與內文 embedding。
- [ ] 比較 dense、sparse 與 hybrid retrieval 品質。
- [ ] 理解 HNSW 參數如何影響 recall 與 latency。
- [ ] 在生產前測試備份、還原、sharding 與 replication。

## References

- [Qdrant official site](https://qdrant.tech/)
- [Qdrant documentation overview](https://qdrant.tech/documentation/overview/)
- [Qdrant filtering documentation](https://qdrant.tech/documentation/concepts/filtering/)
- [Qdrant hybrid queries](https://qdrant.tech/documentation/concepts/hybrid-queries/)
- [Qdrant vector configuration](https://qdrant.tech/documentation/concepts/vectors/)
- [Qdrant deployment documentation](https://qdrant.tech/documentation/guides/installation/)
