# Chroma

| Field | Details |
| --- | --- |
| Category | Open-source AI search and vector database |
| Project | Chroma |
| License | Apache-2.0 |
| Primary use cases | RAG prototypes, AI applications, agent memory, semantic search, local retrieval |
| Core data model | Collections of records with IDs, embeddings, documents, and metadata |
| Search modes | Dense vector search, sparse and hybrid search, metadata filters, full-text and regex search |
| Deployment | Local embedded use, self-hosted server, Chroma Cloud |
| Last reviewed | 2026-04-29 |

## English

### Overview

Chroma is an open-source data infrastructure and search engine for AI applications. It stores documents, embeddings, IDs, and metadata in collections, then supports retrieval through vector search, metadata filtering, document search, full-text search, regex search, and hybrid retrieval.

Chroma is popular for fast RAG development because it is simple to start locally, has first-party Python, TypeScript, and Rust clients, and can run embedded, self-hosted, or through Chroma Cloud.

### Why it matters

Many teams need a retrieval layer before they need a large distributed vector database. Chroma matters because it makes the core RAG loop direct: create a collection, add documents or precomputed embeddings, attach metadata, and query with filters.

As applications mature, Chroma also supports more advanced retrieval patterns, including dense and sparse search, hybrid search, metadata array filters, document substring filters, and multimodal retrieval. This lets teams prototype locally while keeping a path to hosted or cloud deployment.

### Architecture/Concepts

Key concepts:

- **Client**: Connects to local, self-hosted, or cloud Chroma.
- **Collection**: Fundamental unit for storing and querying records.
- **Record**: Identified by a string ID and may contain a document, embedding, metadata, or a combination.
- **Embedding function**: Optional function used by a collection to generate embeddings when documents are added.
- **Metadata**: Key-value fields used for filtering and application context.
- **Metadata filters**: Query-time filters with comparison, inclusion, logical, and array operators.
- **Document filters**: Search document text using conditions such as substring matching.
- **Dense and sparse embeddings**: Support semantic and lexical retrieval signals.
- **Hybrid retrieval**: Combines multiple retrieval strategies to improve relevance.
- **Cloud and Sync APIs**: Managed Chroma features for hosted databases and syncing sources into collections.

### Practical usage

Use Chroma when:

- You want the fastest path to a working RAG or agent memory prototype.
- Local development and simple client APIs matter.
- Your app stores documents, embeddings, IDs, and metadata together.
- You need metadata filters without operating a complex cluster.
- You want to move from local or self-hosted use to Chroma Cloud later.

Implementation tips:

- Use stable, meaningful IDs so records can be updated and traced back to source data.
- Store source, tenant, timestamp, chunk index, and access-control metadata with each record.
- Decide whether Chroma or your application owns embedding generation.
- Use filters aggressively to keep retrieval scoped before generation.
- Evaluate retrieval with representative questions before adding reranking or complex agents.
- Plan migration carefully if the prototype grows into a high-scale production service.

### Learning checklist

- [ ] Create a Chroma collection.
- [ ] Add records with IDs, documents, metadata, and embeddings.
- [ ] Query by text using an embedding function.
- [ ] Query with precomputed embeddings.
- [ ] Use `where` metadata filters.
- [ ] Use document filters for text constraints.
- [ ] Compare dense, sparse, and hybrid retrieval.
- [ ] Run Chroma locally and connect from Python or TypeScript.

## 繁體中文

### 概覽

Chroma 是開源的 AI data infrastructure 與 search engine。它以 collections 儲存 documents、embeddings、IDs 與 metadata，並支援 vector search、metadata filtering、document search、full-text search、regex search 與 hybrid retrieval。

Chroma 因為容易在本機啟動、具備第一方 Python、TypeScript 與 Rust clients，且可 embedded、自架或使用 Chroma Cloud，因此常被用於快速開發 RAG。

### 為什麼重要

許多團隊在需要大型分散式向量資料庫之前，先需要一個好用的 retrieval layer。Chroma 的價值在於讓 RAG 核心流程很直接：建立 collection、加入 documents 或預先計算的 embeddings、附上 metadata，然後用 filters 查詢。

隨著應用成熟，Chroma 也支援更進階的 retrieval patterns，例如 dense 與 sparse search、hybrid search、metadata array filters、document substring filters 與 multimodal retrieval。這讓團隊能先在本機 prototype，再保留 hosted 或 cloud deployment 的路徑。

### 架構/概念

核心概念：

- **Client**：連接 local、self-hosted 或 cloud Chroma。
- **Collection**：儲存與查詢 records 的基本單位。
- **Record**：以 string ID 識別，可包含 document、embedding、metadata 或其組合。
- **Embedding function**：collection 可選的函式，在加入 documents 時產生 embeddings。
- **Metadata**：用於 filtering 與應用脈絡的 key-value 欄位。
- **Metadata filters**：query time filter，支援比較、包含、邏輯與 array operators。
- **Document filters**：使用 substring 等條件搜尋 document text。
- **Dense 與 sparse embeddings**：支援語意與詞彙 retrieval 訊號。
- **Hybrid retrieval**：結合多種 retrieval 策略以提升相關性。
- **Cloud 與 Sync APIs**：Chroma managed features，可用於 hosted databases 與同步來源資料。

### 實務使用

適合使用 Chroma 的情境：

- 想快速建立可運作的 RAG 或 Agent memory prototype。
- 重視本機開發與簡單 client APIs。
- 應用需要一起儲存 documents、embeddings、IDs 與 metadata。
- 需要 metadata filters，但不想維運複雜 cluster。
- 想未來從 local 或 self-hosted 遷移到 Chroma Cloud。

實作建議：

- 使用穩定且有意義的 IDs，方便更新與追溯來源資料。
- 在每筆 record 存入 source、tenant、timestamp、chunk index 與 access-control metadata。
- 先決定 embedding generation 由 Chroma 或應用程式負責。
- 在生成回答前，用 filters 將 retrieval 範圍縮小。
- 加入 reranking 或複雜 agents 前，先用代表性問題評估 retrieval。
- 若 prototype 成長為高流量生產服務，需謹慎規劃遷移。

### 學習檢核表

- [ ] 建立 Chroma collection。
- [ ] 加入含 IDs、documents、metadata 與 embeddings 的 records。
- [ ] 使用 embedding function 以文字查詢。
- [ ] 使用預先計算的 embeddings 查詢。
- [ ] 使用 `where` metadata filters。
- [ ] 使用 document filters 加入文字條件。
- [ ] 比較 dense、sparse 與 hybrid retrieval。
- [ ] 在本機執行 Chroma，並從 Python 或 TypeScript 連線。

## References

- [Chroma documentation](https://docs.trychroma.com/)
- [Chroma collections documentation](https://docs.trychroma.com/docs/collections/manage-collections)
- [Chroma add data documentation](https://docs.trychroma.com/docs/collections/add-data)
- [Chroma metadata filtering](https://docs.trychroma.com/docs/querying-collections/metadata-filtering)
- [Chroma API and SDK reference](https://docs.trychroma.com/reference/chroma-reference)
- [Chroma GitHub repository](https://github.com/chroma-core/chroma)
