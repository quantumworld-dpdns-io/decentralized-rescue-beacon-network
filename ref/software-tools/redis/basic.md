# Redis Basics: Core Concepts, Data Structures, and Use Cases

| Field | Details |
|---|---|
| Topic | Redis fundamentals |
| Audience | Developers, backend engineers, data engineers, and cloud learners |
| Level | Beginner to intermediate |
| Prerequisites | Basic understanding of databases, APIs, and command-line tools |
| Learning goals | Understand Redis deployment models, core data structures, advanced capabilities, and common production use cases |

## English

### Overview

Redis is a high-performance, in-memory key-value data store. It stores data as **key-value pairs**, where the **key** is the identifier used to access data and the **value** is the stored content. Because Redis keeps active data in memory, it is commonly used when applications need very low latency and high throughput.

Redis is often described as a data structure server rather than only a cache. In addition to simple strings, it supports lists, sets, hashes, sorted sets, streams, geospatial indexes, probabilistic structures, JSON documents, search, and vector search. These capabilities make Redis useful for caching, session storage, queues, leaderboards, real-time analytics, event processing, and AI-powered retrieval systems.

Important Redis concepts include:

- **Keys**: Unique names used to store and retrieve values.
- **Values**: Data stored under keys, ranging from simple strings to complex structures.
- **TTL**: Time to live, used to automatically expire volatile keys.
- **Namespaces**: Naming conventions, often using colons such as `app:user:1001`.
- **Persistence**: Optional disk-backed durability through snapshots or append-only files.
- **Replication and high availability**: Copies data to replicas and supports failover in production deployments.

### Deployment options

Redis can be deployed in several ways depending on the environment, operational requirements, and desired level of management.

| Option | Description | Typical use |
|---|---|---|
| Redis Community Edition | Open-source Redis that can run locally, on virtual machines, or in containers such as Docker. | Local development, testing, learning, and self-managed workloads. |
| Redis Cloud | Fully managed database-as-a-service with plans such as Free, Essentials, and Pro. It can include managed failover, scaling, backups, and multi-region deployment depending on plan. | Production systems that need managed operations and cloud integration. |
| Redis Software | Enterprise self-managed Redis deployed on-premises, in private cloud, or in controlled infrastructure. | Organizations that need enterprise controls, private deployment, or strict operational ownership. |

For local learning, Docker is a common starting point:

```bash
docker run --name redis-basic -p 6379:6379 redis:latest
```

Redis Insight is a graphical tool for browsing keys, visualizing data structures, running commands, inspecting performance, and managing Redis databases.

### Core data structures

#### Strings

Strings are the simplest Redis value type. They are binary-safe byte sequences, so they can store text, numbers, serialized JSON, images, audio, or other binary content.

Common commands:

- `SET key value`: Store a value.
- `GET key`: Read a value.
- `INCR key`: Increment an integer value.
- `EXPIRE key seconds`: Set a TTL.

Typical uses include feature flags, counters, API response caching, tokens, and small serialized objects.

#### Lists

Lists are ordered collections of strings. They allow duplicate elements and support pushing or popping from either the head or tail.

Common commands:

- `LPUSH key value`: Push to the left.
- `RPUSH key value`: Push to the right.
- `LPOP key`: Pop from the left.
- `RPOP key`: Pop from the right.
- `LRANGE key start stop`: Read a range.

Typical uses include queues, stacks, recent activity feeds, job buffers, and simple task pipelines.

#### Sets

Sets are unordered collections of unique strings. Redis automatically removes duplicates and supports set operations.

Common commands:

- `SADD key member`: Add a member.
- `SISMEMBER key member`: Check membership.
- `SUNION key1 key2`: Union.
- `SINTER key1 key2`: Intersection.
- `SDIFF key1 key2`: Difference.

Typical uses include unique visitor tracking, tags, permissions, deduplication, and membership checks.

#### Hashes

Hashes store field-value pairs under one Redis key. They are useful for representing objects or records without storing the whole object as one serialized string.

Common commands:

- `HSET key field value`: Set a field.
- `HGET key field`: Read a field.
- `HGETALL key`: Read all fields.
- `HINCRBY key field amount`: Increment a numeric field.

Typical uses include user profiles, product records, session data, configuration objects, and compact object storage.

#### Sorted sets

Sorted sets contain unique members, each associated with a numeric score. Redis keeps members ordered by score.

Common commands:

- `ZADD key score member`: Add or update a scored member.
- `ZRANGE key start stop`: Read members by rank.
- `ZREVRANGE key start stop`: Read members from highest score to lowest.
- `ZRANGEBYSCORE key min max`: Query by score range.

Typical uses include leaderboards, rankings, priority queues, recommendations, rate limiting windows, and time-ordered indexes.

#### JSON

Redis can store and update JSON documents when the JSON capability is available. JSON support allows nested documents to be queried and modified by path without manually deserializing and rewriting the whole object in application code.

Typical uses include document-style application data, product catalogs, user preferences, event payloads, and objects that need nested fields.

### Advanced capabilities

#### Key expiration and caching

Redis keys can be persistent or volatile:

- **Persistent keys** have no TTL and remain until deleted or overwritten.
- **Volatile keys** have a TTL and expire automatically.

TTL-based expiration is the foundation of Redis caching. A common pattern is to store frequently requested database or API results in Redis for a short period, reducing backend load and improving response time.

#### Streams

Redis Streams store append-only event records with unique IDs. They support consumer groups, making them useful for event processing and message-driven systems.

Typical uses include event buses, user activity streams, audit logs, IoT telemetry, and background processing pipelines.

#### Probabilistic data structures

Probabilistic structures trade exactness for very low memory usage and high throughput.

- **HyperLogLog** estimates cardinality, such as the number of unique visitors, with small memory usage and approximate results.
- **Bloom filters** test whether an item may exist in a set. A negative result means the item definitely does not exist; a positive result means it probably exists and may be a false positive.

Typical uses include unique count estimation, duplicate detection, cache penetration protection, and large-scale membership checks.

#### Geospatial indexing

Redis geospatial commands store longitude and latitude for named members and support distance calculations, radius queries, and nearby search.

Typical uses include store locators, delivery matching, proximity search, and location-aware services.

#### Search and query

Redis can support secondary indexes and search over hashes and JSON documents when search capabilities are available. This enables full-text search, numeric filtering, tag filtering, sorting, and aggregation.

Typical uses include product search, user directory search, log lookup, and real-time filtering over operational data.

#### Vector search

Redis can store vector embeddings and perform similarity search. Embeddings represent unstructured data such as text, images, PDFs, or audio in numeric vector form.

Typical uses include semantic search, retrieval-augmented generation, recommendation systems, chatbot memory, document search, and AI-powered personalization.

#### Persistence, replication, and reliability

Although Redis is memory-first, production deployments often use reliability features:

- **RDB snapshots** create point-in-time backups.
- **AOF** records write operations for stronger durability.
- **Replication** copies data to replica nodes.
- **Failover** promotes a replica when the primary node becomes unavailable.
- **Clustering** distributes data across multiple nodes for scale.

The right configuration depends on whether Redis is being used as a disposable cache, a durable operational store, or a mixed workload database.

### Use cases

- **Caching**: Store expensive database queries, API responses, rendered pages, and computed results for fast reuse.
- **Session management**: Keep user sessions, login state, shopping carts, and temporary profile data available across multiple application servers.
- **Queues and background jobs**: Use lists, streams, or sorted sets to coordinate work between producers and workers.
- **Leaderboards and rankings**: Use sorted sets to maintain real-time scores and rank users efficiently.
- **Rate limiting**: Track request counts or sliding windows to protect APIs and services from excessive traffic.
- **Real-time analytics**: Count events, estimate unique users, process streams, and maintain rolling metrics.
- **Search and filtering**: Query hashes or JSON records with secondary indexes when search capabilities are enabled.
- **Geospatial applications**: Find nearby drivers, stores, devices, or service locations.
- **AI and vector search**: Store embeddings for semantic retrieval, chatbot context, recommendation engines, and RAG workflows.

### Learning checklist

- Explain Redis as an in-memory key-value and data structure store.
- Distinguish Redis Community Edition, Redis Cloud, and Redis Software.
- Use `SET`, `GET`, `EXPIRE`, and `TTL` for basic key operations.
- Choose between strings, lists, sets, hashes, sorted sets, and JSON for common modeling tasks.
- Describe when to use streams, HyperLogLog, Bloom filters, geospatial indexes, search, and vector search.
- Design clear key names with namespaces such as `service:entity:id`.
- Explain the difference between persistent keys and volatile keys.
- Identify common Redis use cases including caching, sessions, queues, leaderboards, rate limiting, analytics, and AI retrieval.
- Understand the role of persistence, replication, failover, and clustering in production.
- Use Redis Insight or the Redis CLI to inspect data and run commands.

## 繁體中文

### 概觀

Redis 是高效能的記憶體內鍵值資料庫。它以**鍵值對（key-value pairs）**儲存資料，其中**鍵（key）**是存取資料的識別名稱，**值（value）**則是實際儲存的內容。由於 Redis 主要在記憶體中操作資料，因此常用於需要低延遲與高吞吐量的應用。

Redis 不只是快取系統，也常被稱為資料結構伺服器。除了簡單字串，Redis 也支援列表、集合、雜湊、有序集合、串流、地理空間索引、機率型資料結構、JSON 文件、搜尋與向量搜尋。這些能力讓 Redis 適用於快取、工作階段管理、佇列、排行榜、即時分析、事件處理與 AI 檢索系統。

重要概念包含：

- **鍵（Keys）**：用來儲存與讀取資料的唯一名稱。
- **值（Values）**：儲存在鍵底下的資料，可從簡單字串到複雜資料結構。
- **TTL（Time to live）**：鍵的存活時間，可讓資料自動過期。
- **命名空間（Namespaces）**：常用冒號建立層級式命名，例如 `app:user:1001`。
- **持久化（Persistence）**：可選擇透過快照或 append-only file 將資料寫入磁碟。
- **複寫與高可用（Replication and high availability）**：在生產環境中將資料複寫到副本並支援故障轉移。

### 部署選項

Redis 可依照環境、維運需求與管理程度採用不同部署方式。

| 選項 | 說明 | 常見用途 |
|---|---|---|
| Redis Community Edition | 開源 Redis，可安裝於本機、虛擬機，或使用 Docker 等容器執行。 | 本機開發、測試、學習與自管工作負載。 |
| Redis Cloud | 全託管資料庫服務，提供 Free、Essentials、Pro 等方案。依方案不同，可支援受管故障轉移、擴充、備份與多區域部署。 | 需要受管維運與雲端整合的生產系統。 |
| Redis Software | 企業級自管 Redis，可部署於地端、私有雲或受控基礎架構。 | 需要企業控管、私有部署或嚴格維運主控權的組織。 |

本機學習常用 Docker 啟動 Redis：

```bash
docker run --name redis-basic -p 6379:6379 redis:latest
```

Redis Insight 是圖形化管理工具，可瀏覽鍵、視覺化資料結構、執行指令、檢查效能並管理 Redis 資料庫。

### 核心資料結構

#### 字串（Strings）

字串是 Redis 最基本的值類型。它是二進位安全（binary-safe）的位元組序列，因此可儲存文字、數字、序列化 JSON、圖片、音訊或其他二進位內容。

常用指令：

- `SET key value`：寫入值。
- `GET key`：讀取值。
- `INCR key`：遞增整數值。
- `EXPIRE key seconds`：設定 TTL。

常見用途包含功能開關、計數器、API 回應快取、權杖與小型序列化物件。

#### 列表（Lists）

列表是有序字串集合，允許重複元素，並支援從頭端或尾端加入與移除資料。

常用指令：

- `LPUSH key value`：從左側加入。
- `RPUSH key value`：從右側加入。
- `LPOP key`：從左側取出。
- `RPOP key`：從右側取出。
- `LRANGE key start stop`：讀取範圍。

常見用途包含佇列、堆疊、近期活動、工作緩衝區與簡易任務流程。

#### 集合（Sets）

集合是無序且不重複的字串集合。Redis 會自動去除重複成員，並支援集合運算。

常用指令：

- `SADD key member`：新增成員。
- `SISMEMBER key member`：檢查成員是否存在。
- `SUNION key1 key2`：聯集。
- `SINTER key1 key2`：交集。
- `SDIFF key1 key2`：差集。

常見用途包含不重複訪客追蹤、標籤、權限、資料去重與成員檢查。

#### 雜湊（Hashes）

雜湊在單一 Redis 鍵底下儲存欄位與值的對應關係。它適合表示物件或紀錄，不必把整個物件都序列化成單一字串。

常用指令：

- `HSET key field value`：設定欄位。
- `HGET key field`：讀取欄位。
- `HGETALL key`：讀取所有欄位。
- `HINCRBY key field amount`：遞增數值欄位。

常見用途包含使用者資料、產品紀錄、工作階段資料、設定物件與精簡物件儲存。

#### 有序集合（Sorted Sets）

有序集合包含不重複成員，每個成員都關聯一個數值分數。Redis 會依分數維持排序。

常用指令：

- `ZADD key score member`：新增或更新具分數的成員。
- `ZRANGE key start stop`：依排名讀取成員。
- `ZREVRANGE key start stop`：從高分到低分讀取成員。
- `ZRANGEBYSCORE key min max`：依分數範圍查詢。

常見用途包含排行榜、排名、優先佇列、推薦、速率限制視窗與時間排序索引。

#### JSON

當 Redis 啟用 JSON 能力時，可儲存與更新 JSON 文件。JSON 支援透過路徑查詢或修改巢狀欄位，應用程式不必手動反序列化並重寫整份物件。

常見用途包含文件型應用資料、產品目錄、使用者偏好、事件 payload 與需要巢狀欄位的物件。

### 進階能力

#### 鍵過期與快取

Redis 鍵可分為持久鍵與揮發鍵：

- **持久鍵（Persistent keys）**沒有 TTL，會保留到被刪除或覆寫為止。
- **揮發鍵（Volatile keys）**設定 TTL，到期後會自動刪除。

TTL 過期機制是 Redis 快取的基礎。常見模式是將頻繁請求的資料庫查詢結果或 API 回應短暫存入 Redis，以降低後端負載並提升回應速度。

#### 串流（Streams）

Redis Streams 儲存 append-only 的事件紀錄，每筆紀錄都有唯一 ID。Streams 支援 consumer groups，適合事件處理與訊息驅動系統。

常見用途包含事件匯流排、使用者行為串流、稽核紀錄、IoT 遙測與背景處理管線。

#### 機率型資料結構

機率型資料結構以適度犧牲精確度換取極低記憶體使用量與高吞吐。

- **HyperLogLog** 用於估計基數，例如不重複訪客數，能以少量記憶體取得近似結果。
- **Bloom filter（布隆過濾器）** 用於測試項目是否可能存在於集合中。若回傳否，代表一定不存在；若回傳是，代表可能存在且可能有誤報。

常見用途包含不重複數量估算、重複資料偵測、快取穿透保護與大規模成員檢查。

#### 地理空間索引（Geospatial indexing）

Redis 地理空間指令可儲存成員的經度與緯度，並支援距離計算、半徑查詢與附近搜尋。

常見用途包含門市查找、配送媒合、鄰近搜尋與位置感知服務。

#### 搜尋與查詢

當 Redis 啟用搜尋能力時，可對 hashes 與 JSON 文件建立次級索引並執行查詢。這讓 Redis 可支援全文搜尋、數值過濾、標籤過濾、排序與聚合。

常見用途包含商品搜尋、使用者目錄搜尋、日誌查詢與即時營運資料過濾。

#### 向量搜尋

Redis 可儲存向量嵌入（embeddings）並執行相似度搜尋。Embeddings 可將文字、圖片、PDF 或音訊等非結構化資料表示為數值向量。

常見用途包含語意搜尋、檢索增強生成（RAG）、推薦系統、聊天機器人記憶、文件搜尋與 AI 個人化。

#### 持久化、複寫與可靠性

雖然 Redis 以記憶體優先，但生產環境通常會搭配可靠性功能：

- **RDB snapshots** 建立時間點快照。
- **AOF** 記錄寫入操作以提升耐久性。
- **Replication** 將資料複寫到副本節點。
- **Failover** 在主要節點不可用時提升副本。
- **Clustering** 將資料分散到多個節點以支援擴充。

正確設定取決於 Redis 是作為可拋棄式快取、具耐久性的營運資料庫，還是混合型工作負載資料庫。

### 使用場景

- **快取（Caching）**：儲存昂貴的資料庫查詢、API 回應、已渲染頁面與計算結果，以便快速重用。
- **工作階段管理（Session management）**：讓使用者 session、登入狀態、購物車與暫存個人資料可在多台應用伺服器間共享。
- **佇列與背景工作（Queues and background jobs）**：使用 lists、streams 或 sorted sets 協調生產者與工作者。
- **排行榜與排名（Leaderboards and rankings）**：使用 sorted sets 即時維護分數與排名。
- **速率限制（Rate limiting）**：追蹤請求次數或滑動視窗，保護 API 與服務避免過量流量。
- **即時分析（Real-time analytics）**：計算事件、估算不重複使用者、處理串流並維護滾動指標。
- **搜尋與過濾（Search and filtering）**：啟用搜尋能力後，可對 hash 或 JSON 紀錄進行索引查詢。
- **地理空間應用（Geospatial applications）**：尋找附近司機、門市、裝置或服務位置。
- **AI 與向量搜尋（AI and vector search）**：儲存 embeddings 以支援語意檢索、聊天機器人上下文、推薦引擎與 RAG 流程。

### 學習檢核表

- 說明 Redis 作為記憶體內鍵值與資料結構資料庫的定位。
- 區分 Redis Community Edition、Redis Cloud 與 Redis Software。
- 使用 `SET`、`GET`、`EXPIRE`、`TTL` 執行基本鍵操作。
- 針對常見建模需求選擇 strings、lists、sets、hashes、sorted sets 與 JSON。
- 說明何時使用 streams、HyperLogLog、Bloom filters、地理空間索引、搜尋與向量搜尋。
- 設計清楚的鍵命名空間，例如 `service:entity:id`。
- 說明持久鍵與揮發鍵的差異。
- 辨識 Redis 常見使用場景，包含快取、session、佇列、排行榜、速率限制、分析與 AI 檢索。
- 理解持久化、複寫、故障轉移與叢集在生產環境中的角色。
- 使用 Redis Insight 或 Redis CLI 檢查資料並執行指令。

## References

- Redis Documentation: <https://redis.io/docs/latest/>
- Redis Data Types: <https://redis.io/docs/latest/develop/data-types/>
- Redis Commands: <https://redis.io/docs/latest/commands/>
- Redis Insight: <https://redis.io/insight/>
- Redis Cloud: <https://redis.io/cloud/>
