# Weaviate

| Field | Details |
| --- | --- |
| Category | AI-native vector database |
| Project | Weaviate Database |
| License | BSD-3-Clause |
| Primary use cases | Semantic search, RAG, hybrid search, agents, multimodal retrieval |
| Core data model | Collections containing objects, properties, vectors, and metadata |
| Search modes | Vector search, BM25 keyword search, hybrid search, filters, reranking |
| Deployment | Embedded/local development, Docker, Kubernetes, Weaviate Cloud |
| Last reviewed | 2026-04-29 |

## English

### Overview

Weaviate is an open-source AI vector database for storing data objects and their vector embeddings. It supports semantic vector search, BM25 keyword search, hybrid search, filtering, reranking, multi-tenancy, and model integrations for vectorization and generative workflows.

Weaviate is often used as a retrieval backend for RAG and agent systems. Developers define collections, schemas, vectorizer settings, and indexes, then query through official clients, GraphQL, REST, or gRPC APIs.

### Why it matters

Search quality often requires both meaning and exact terms. Weaviate makes hybrid search a first-class feature by combining vector search with BM25 keyword scoring and configurable fusion. This helps when users ask natural-language questions but still expect exact names, codes, or domain terms to matter.

Weaviate also reduces integration work through modules and service integrations. Teams can bring their own vectors or let Weaviate call configured embedding providers, then use the same database for retrieval, metadata filtering, and generative RAG patterns.

### Architecture/Concepts

Key concepts:

- **Collection**: A typed grouping of objects, properties, vector settings, and indexes.
- **Object**: A stored item with properties, metadata, and one or more vectors.
- **Schema**: Defines property names, data types, vectorization behavior, and index settings.
- **Vector index**: Supports indexes such as HNSW, flat, and dynamic depending on workload needs.
- **Named vectors**: Multiple vectors on the same object for different fields, modalities, or embedding models.
- **BM25 index**: Keyword search over selected text properties.
- **Hybrid search**: Combines vector and BM25 results with configurable alpha and fusion strategy.
- **Filters**: Restrict results by property values, references, tenants, or other conditions.
- **Multi-tenancy**: Separates tenant data inside a collection while preserving operational efficiency.
- **Modules and integrations**: Connect embedding, reranking, and generative providers.

### Practical usage

Use Weaviate when:

- You want semantic and keyword search in one database.
- Hybrid retrieval and reranking are central to search quality.
- You need schema-driven objects with typed properties and filters.
- You want built-in vectorizer or generative model integrations.
- You need a path from local development to managed Weaviate Cloud.

Implementation tips:

- Choose whether vectors are generated outside Weaviate or by a configured vectorizer.
- Model collections around query patterns, not only source tables.
- Use named vectors when separate fields need separate semantic spaces.
- Tune hybrid search with `alpha` and evaluate against real queries.
- Use multi-tenancy for tenant isolation instead of mixing tenant IDs only as ordinary filters.
- Check client and server version compatibility before upgrades.

### Learning checklist

- [ ] Create a collection with typed properties.
- [ ] Insert objects with text properties and vectors.
- [ ] Run vector, BM25, and hybrid searches.
- [ ] Adjust the hybrid `alpha` value and compare rankings.
- [ ] Add filters over properties.
- [ ] Configure named vectors for multiple embedding spaces.
- [ ] Understand HNSW, flat, and dynamic vector indexes.
- [ ] Test backup, scaling, and multi-tenancy behavior before production.

## 繁體中文

### 概覽

Weaviate 是開源 AI 向量資料庫，用來儲存資料物件與其 vector embeddings。它支援語意向量搜尋、BM25 關鍵字搜尋、hybrid search、filtering、reranking、multi-tenancy，以及向量化與生成式流程的模型整合。

Weaviate 常被用作 RAG 與 Agent 系統的 retrieval backend。開發者定義 collections、schema、vectorizer 設定與索引，再透過官方 client、GraphQL、REST 或 gRPC API 查詢。

### 為什麼重要

好的搜尋品質通常同時需要語意與精確詞彙。Weaviate 將 hybrid search 作為一等功能，把 vector search 與 BM25 keyword scoring 結合，並提供可調整的 fusion。這讓自然語言查詢可以找到語意相近內容，也能保留名稱、代碼與領域術語的重要性。

Weaviate 也透過 modules 與服務整合降低開發成本。團隊可以自行產生 vectors，也可以讓 Weaviate 呼叫設定好的 embedding provider，並在同一套資料庫中完成 retrieval、metadata filtering 與生成式 RAG 流程。

### 架構/概念

核心概念：

- **Collection**：包含 objects、properties、vector settings 與 indexes 的型別化集合。
- **Object**：被儲存的項目，包含 properties、metadata 與一個或多個 vectors。
- **Schema**：定義 property 名稱、資料型別、向量化行為與索引設定。
- **Vector index**：依工作負載使用 HNSW、flat 或 dynamic 等索引。
- **Named vectors**：同一 object 上的多個 vectors，可對應不同欄位、模態或 embedding model。
- **BM25 index**：針對文字 property 的關鍵字搜尋。
- **Hybrid search**：以可調 alpha 與 fusion strategy 結合 vector 與 BM25 結果。
- **Filters**：依 property、reference、tenant 或其他條件限制結果。
- **Multi-tenancy**：在 collection 內分隔 tenant data。
- **Modules 與 integrations**：連接 embedding、reranking 與 generative providers。

### 實務使用

適合使用 Weaviate 的情境：

- 想在同一資料庫中使用語意與關鍵字搜尋。
- hybrid retrieval 與 reranking 是搜尋品質核心。
- 需要 schema-driven objects、typed properties 與 filters。
- 想使用內建 vectorizer 或 generative model integrations。
- 需要從本機開發銜接到 managed Weaviate Cloud。

實作建議：

- 先決定 vectors 要在外部產生，或由 Weaviate vectorizer 產生。
- 依查詢模式設計 collections，而不只是照來源資料表切分。
- 不同欄位需要不同語意空間時，使用 named vectors。
- 用真實查詢調整 hybrid search 的 `alpha` 並評估排名。
- 多租戶資料優先使用 multi-tenancy，而不只是一般 tenant ID filter。
- 升級前確認 client 與 server 版本相容性。

### 學習檢核表

- [ ] 建立含 typed properties 的 collection。
- [ ] 寫入含文字 properties 與 vectors 的 objects。
- [ ] 執行 vector、BM25 與 hybrid search。
- [ ] 調整 hybrid `alpha` 並比較排名。
- [ ] 對 properties 加入 filters。
- [ ] 設定 named vectors 以支援多個 embedding spaces。
- [ ] 理解 HNSW、flat 與 dynamic vector indexes。
- [ ] 生產前測試備份、擴展與 multi-tenancy 行為。

## References

- [Weaviate Database documentation](https://docs.weaviate.io/weaviate/)
- [Weaviate vector search concepts](https://docs.weaviate.io/weaviate/concepts/search/vector-search)
- [Weaviate hybrid search concepts](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search)
- [Weaviate hybrid search how-to](https://docs.weaviate.io/weaviate/search/hybrid)
- [Weaviate vector indexes](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index)
- [Weaviate deployment documentation](https://docs.weaviate.io/deploy)
