# Redis for JavaScript Developers

| Field | Details |
| --- | --- |
| Topic | Redis usage from Node.js and JavaScript applications |
| Audience | JavaScript developers building APIs, dashboards, background jobs, and real-time features |
| Runtime | Node.js with Express, Jest, and the official `redis` client |
| Redis concepts | Strings, Hashes, Sets, Sorted Sets, Streams, TTLs, transactions, and key design |
| Example domain | Redis Solar: a solar-site monitoring dashboard backed by Redis |
| Last reviewed | 2026-04-29 |

## English

### Overview

Redis is an in-memory data store commonly used by JavaScript applications for low-latency reads, caching, counters, queues, leaderboards, sessions, geospatial lookups, and real-time dashboards. It works especially well with Node.js because both systems are optimized for fast event-driven I/O.

This guide uses the Redis Solar training scenario as the running example:

- A utility company installs solar panels for homes and businesses.
- Each installation site has a smart meter that reports power consumption and generation every minute.
- The application must show all sites on a map, find nearby sites by latitude and longitude, and render trend charts for a single site.

Expected prerequisites:

- Modern JavaScript: Node.js, npm, ES modules or CommonJS, Promises, and `async`/`await`.
- Redis basics: Strings, Hashes, Sets, Sorted Sets, expiration, and command-line inspection with `redis-cli`.
- Web API basics: REST routes, HTTP methods, status codes, JSON payloads, and basic Express patterns.

The goal is not to treat Redis as a relational database replacement. The goal is to design small, explicit access patterns and choose Redis data structures that make those reads and writes simple, fast, and observable.

### Architecture

Redis Solar follows a conventional service architecture:

- Frontend: a Vue.js dashboard, provided as a prebuilt client so backend work can focus on data access and API behavior.
- Backend: an Express-based Node.js service that exposes REST endpoints and translates application operations into Redis commands.
- Data access layer: DAO classes or modules isolate Redis-specific commands from route handlers and business logic.
- Redis: stores site metadata, lookup indexes, geospatial coordinates, time-series-like readings, and cached aggregates.
- Tests and tooling: Jest validates DAO behavior and route responses; local development uses `config.json`, environment variables, or both to point at the target Redis instance.

The original course material uses a DAO pattern, which remains a good fit:

- Domain objects describe application concepts such as `Site`, `MeterReading`, and `EnergySummary`.
- DAO interfaces define operations such as `insert`, `findById`, `findAll`, `findNearby`, and `appendReading`.
- Redis DAO implementations contain command-level details such as `HSET`, `SADD`, `GEOADD`, `ZRANGE`, and key naming.

This separation keeps route handlers small and makes storage changes testable. If the application later moves a subset of data to PostgreSQL, OpenSearch, or a purpose-built time-series database, the higher-level API code does not need to know every storage detail.

Recommended runtime flow:

1. Load configuration from environment variables or a local config file.
2. Create one shared Redis client during application startup.
3. Connect before accepting HTTP traffic.
4. Pass the connected client into DAO modules.
5. Close the client during graceful shutdown.

Node.js and Redis are both highly efficient with a small number of connections. Most HTTP services should start with one shared client for normal commands, plus separate duplicated clients only when using blocking operations, Pub/Sub, or long-lived stream consumers.

### Node.js Client Usage

The official Node.js client is published as `redis` and is the default recommendation for new JavaScript applications. `ioredis` is also widely used, especially in projects with existing cluster, Sentinel, or BullMQ patterns. Choose deliberately, then standardize on one client across the service.

Install the official client:

```bash
npm install redis
```

Create and share a client:

```js
import { createClient } from 'redis';

export async function createRedisClient(url) {
  const client = createClient({ url });

  client.on('error', (err) => {
    console.error('Redis client error', err);
  });

  await client.connect();
  return client;
}
```

Use `async`/`await` consistently:

```js
export class SiteDao {
  constructor(redis, keygen) {
    this.redis = redis;
    this.keygen = keygen;
  }

  async insert(site) {
    const siteKey = this.keygen.site(site.id);

    await this.redis
      .multi()
      .hSet(siteKey, {
        id: site.id,
        address: site.address,
        capacityKwh: String(site.capacityKwh),
        latitude: String(site.latitude),
        longitude: String(site.longitude),
      })
      .sAdd(this.keygen.siteIds(), site.id)
      .geoAdd(this.keygen.siteGeo(), {
        longitude: site.longitude,
        latitude: site.latitude,
        member: site.id,
      })
      .exec();
  }

  async findById(id) {
    const raw = await this.redis.hGetAll(this.keygen.site(id));

    if (!raw.id) {
      return null;
    }

    return {
      id: raw.id,
      address: raw.address,
      capacityKwh: Number(raw.capacityKwh),
      latitude: Number(raw.latitude),
      longitude: Number(raw.longitude),
    };
  }
}
```

Important client practices:

- Prefer `async`/`await` over callbacks. Current Redis clients already expose Promise-based APIs.
- Register an `error` listener. Unhandled client errors can destabilize the process.
- Do not connect inside every request. Reuse a connected client.
- Use `multi()` when related writes must succeed together from the application perspective.
- Use `scanIterator()` or cursor-based `SCAN` for key discovery; avoid `KEYS` in production.
- Use command-specific options and structured return values rather than parsing raw protocol output.
- Duplicate the client for Pub/Sub or blocking reads because those modes reserve the connection for specialized command flows.

### Data Modeling

Redis modeling starts with access patterns. Before choosing keys, list the questions the application must answer:

- What site has ID `123`?
- Which sites should appear on the map?
- Which sites are within a radius of a coordinate?
- What are the latest readings for one site?
- What is the current aggregate production or consumption?
- Which cached values can expire safely?

Useful structures for the Redis Solar domain:

| Data need | Redis structure | Example key | Notes |
| --- | --- | --- | --- |
| Site metadata | Hash | `solar:site:{siteId}` | Store scalar fields; convert numbers on read. |
| All site IDs | Set | `solar:sites` | Supports membership and full-list traversal. |
| Site location lookup | Geospatial index | `solar:sites:geo` | Use `GEOADD` and radius or bounding queries. |
| Recent readings | Sorted Set | `solar:site:{siteId}:readings` | Score by timestamp; value can be compact JSON. |
| Latest reading | String or Hash | `solar:site:{siteId}:latest` | Optimized for dashboard refreshes. |
| Cached aggregate | String or Hash with TTL | `solar:summary:current` | Expire and recompute instead of serving stale values indefinitely. |
| Event pipeline | Stream | `solar:readings` | Good for ingestion workers and replayable processing. |

Key design rules:

- Use a clear namespace, such as `solar:` or `ru102js:`, to avoid collisions.
- Keep key generation centralized in a small helper module.
- Use stable identifiers in keys; avoid user-controlled free text unless sanitized.
- Choose one naming convention and apply it consistently.
- Store nested objects deliberately. Redis Hashes are flat, so either flatten fields or store a JSON document when partial field updates are not needed.
- Convert types explicitly. Redis stores strings at the protocol level, so numbers, booleans, timestamps, and JSON need clear encode/decode rules.
- Add TTLs only where expiration is part of the product behavior. Persistent domain records should not expire accidentally.

Example key generator:

```js
export function createKeyGenerator(prefix = 'solar') {
  return {
    site: (siteId) => `${prefix}:site:${siteId}`,
    siteIds: () => `${prefix}:sites`,
    siteGeo: () => `${prefix}:sites:geo`,
    siteReadings: (siteId) => `${prefix}:site:${siteId}:readings`,
    latestReading: (siteId) => `${prefix}:site:${siteId}:latest`,
    currentSummary: () => `${prefix}:summary:current`,
  };
}
```

Modeling tradeoffs:

- Hashes are efficient for field-level updates and reads, but they do not represent nested documents directly.
- Sorted Sets are useful for timestamp-ordered data, but very large histories need retention rules or archival storage.
- Streams are better than Lists when consumers need IDs, acknowledgements, consumer groups, and replay.
- JSON strings are simple, but they make partial updates and indexing harder unless RedisJSON is available and intentionally adopted.
- Duplicating data across keys is normal in Redis when it directly supports required reads. Keep write paths responsible for updating every derived index.

### Testing/Operations Checklist

Development and testing:

- Use a dedicated Redis database, container, or key prefix for tests.
- Flush only the test namespace or test database; never run broad cleanup commands against shared environments.
- Cover DAO insert/read/update behavior with Jest integration tests.
- Test type conversion, missing records, duplicate inserts, TTL behavior, and transaction failure paths.
- Seed small deterministic fixtures for route tests.
- Run `npm test` before merging changes that touch Redis access code.

Operational readiness:

- Confirm Redis URL, username, password, TLS setting, and database number are supplied through environment-specific configuration.
- Add startup health checks that verify Redis connectivity before accepting traffic.
- Log command failures with enough context to identify the key family, but do not log secrets or full sensitive payloads.
- Set timeouts and reconnect behavior intentionally; do not allow requests to hang forever while Redis is unavailable.
- Track latency, error rate, memory use, evictions, connected clients, key count growth, and slow commands.
- Use `SCAN`, `MEMORY USAGE`, `INFO`, and slow log inspection during troubleshooting.
- Define retention for high-volume data such as meter readings.
- Prefer least-privilege Redis ACL users for application services.
- Back up persistent Redis data when Redis is used as a system of record.
- Document every key family, owner, TTL policy, and cleanup process.

Release checklist for a Redis-backed feature:

- Key names are centralized and reviewed.
- Data structures match the required read paths.
- All writes that maintain secondary indexes are tested.
- TTLs are explicit and covered by tests.
- Local and CI tests use isolated Redis data.
- Dashboards and alerts cover Redis availability and latency.
- A rollback plan exists for schema or key-format changes.

## 繁體中文

### 概覽

Redis 是常見的記憶體資料庫，JavaScript 應用程式常用它處理低延遲讀取、快取、計數器、佇列、排行榜、Session、地理位置查詢與即時儀表板。Redis 與 Node.js 都擅長事件驅動 I/O，因此在 API 服務與背景工作程式中很容易形成高效的組合。

本講義沿用 Redis Solar 實戰情境：

- 公用事業公司為家庭與企業安裝太陽能板。
- 每個安裝站點都有智慧電錶，每分鐘回傳用電量與發電量。
- 系統需要在地圖上顯示所有站點、依經緯度查詢附近站點，並呈現單一站點的趨勢圖表。

建議具備的前置能力：

- 現代 JavaScript：Node.js、npm、ES modules 或 CommonJS、Promises 與 `async`/`await`。
- Redis 基礎：Strings、Hashes、Sets、Sorted Sets、過期時間，以及使用 `redis-cli` 檢查資料。
- Web API 基礎：REST 路由、HTTP 方法、狀態碼、JSON payload 與基本 Express 寫法。

這份文件的重點不是把 Redis 當成關聯式資料庫替代品，而是先定義清楚存取模式，再選擇合適的 Redis 資料結構，讓讀寫路徑保持簡單、快速且可觀測。

### 架構

Redis Solar 採用典型服務架構：

- 前端：Vue.js 儀表板。課程提供預建版本，讓開發者專注於後端資料存取與 API 行為。
- 後端：Express Node.js 服務，提供 REST endpoint，並將應用操作轉換為 Redis 指令。
- 資料存取層：DAO 類別或模組隔離 Redis 指令細節，避免路由處理器直接散落資料庫邏輯。
- Redis：儲存站點 metadata、查詢索引、地理座標、類時間序列讀值與快取彙總。
- 測試與工具：Jest 驗證 DAO 與路由；本機開發可透過 `config.json`、環境變數或兩者指定 Redis instance。

原始課程採用 DAO 模式，這仍是合適的設計：

- 領域物件描述應用概念，例如 `Site`、`MeterReading`、`EnergySummary`。
- DAO 介面定義操作，例如 `insert`、`findById`、`findAll`、`findNearby`、`appendReading`。
- Redis DAO 實作封裝指令細節，例如 `HSET`、`SADD`、`GEOADD`、`ZRANGE` 與 key 命名。

這種分層能維持關注點分離。若未來部分資料移至 PostgreSQL、OpenSearch 或專用時間序列資料庫，上層 API 不需要理解每一個儲存細節。

建議的執行流程：

1. 從環境變數或本機設定檔載入設定。
2. 應用程式啟動時建立一個共用 Redis client。
3. 在開始接受 HTTP request 前完成連線。
4. 將已連線的 client 傳入 DAO 模組。
5. 在 graceful shutdown 時關閉 client。

Node.js 與 Redis 都能以少量連線處理大量 I/O。多數 HTTP 服務應先使用一個共用 client；只有在 blocking operation、Pub/Sub 或長時間執行的 Stream consumer 情境下，才建立 duplicated client。

### Node.js 用戶端使用方式

官方 Node.js client 套件名稱為 `redis`，新專案通常可優先採用它。`ioredis` 也很常見，尤其是既有專案已使用 Redis Cluster、Sentinel 或 BullMQ 的情境。請有意識地選擇其中一個，並在同一個服務內保持一致。

安裝官方 client：

```bash
npm install redis
```

建立並共用 client：

```js
import { createClient } from 'redis';

export async function createRedisClient(url) {
  const client = createClient({ url });

  client.on('error', (err) => {
    console.error('Redis client error', err);
  });

  await client.connect();
  return client;
}
```

一致使用 `async`/`await`：

```js
export class SiteDao {
  constructor(redis, keygen) {
    this.redis = redis;
    this.keygen = keygen;
  }

  async insert(site) {
    const siteKey = this.keygen.site(site.id);

    await this.redis
      .multi()
      .hSet(siteKey, {
        id: site.id,
        address: site.address,
        capacityKwh: String(site.capacityKwh),
        latitude: String(site.latitude),
        longitude: String(site.longitude),
      })
      .sAdd(this.keygen.siteIds(), site.id)
      .geoAdd(this.keygen.siteGeo(), {
        longitude: site.longitude,
        latitude: site.latitude,
        member: site.id,
      })
      .exec();
  }

  async findById(id) {
    const raw = await this.redis.hGetAll(this.keygen.site(id));

    if (!raw.id) {
      return null;
    }

    return {
      id: raw.id,
      address: raw.address,
      capacityKwh: Number(raw.capacityKwh),
      latitude: Number(raw.latitude),
      longitude: Number(raw.longitude),
    };
  }
}
```

重要實務：

- 優先使用 `async`/`await`，現代 Redis client 已提供 Promise API，不需要再以 callback 為主。
- 註冊 `error` listener，避免未處理的 client error 影響 process 穩定性。
- 不要在每個 request 裡重新連線；應重用已連線 client。
- 相關寫入需要一起成功時，使用 `multi()`。
- 生產環境不要使用 `KEYS` 掃描 key；請使用 `scanIterator()` 或 cursor-based `SCAN`。
- 優先使用 client 提供的命令選項與結構化回傳值，不要自行解析底層 protocol。
- Pub/Sub 或 blocking read 會佔用特定連線，應使用 duplicated client。

### 資料建模

Redis 建模應從存取模式開始。設計 key 前，先列出應用程式需要回答的問題：

- ID 為 `123` 的站點資料是什麼？
- 地圖上應顯示哪些站點？
- 哪些站點位於某個經緯度半徑內？
- 某站點最近的讀值是什麼？
- 目前總發電量或總用電量是多少？
- 哪些快取值可以安全過期？

Redis Solar 可使用的資料結構：

| 資料需求 | Redis 結構 | 範例 key | 說明 |
| --- | --- | --- | --- |
| 站點 metadata | Hash | `solar:site:{siteId}` | 儲存純量欄位；讀出時轉回數字。 |
| 所有站點 ID | Set | `solar:sites` | 支援 membership 與全站點遍歷。 |
| 站點地理查詢 | Geospatial index | `solar:sites:geo` | 使用 `GEOADD` 與半徑或範圍查詢。 |
| 近期讀值 | Sorted Set | `solar:site:{siteId}:readings` | score 使用 timestamp；value 可放精簡 JSON。 |
| 最新讀值 | String 或 Hash | `solar:site:{siteId}:latest` | 針對儀表板刷新最佳化。 |
| 快取彙總 | 帶 TTL 的 String 或 Hash | `solar:summary:current` | 過期後重算，避免永久提供過期資料。 |
| 事件管線 | Stream | `solar:readings` | 適合 ingestion worker 與可 replay 的處理流程。 |

Key 設計規則：

- 使用清楚 namespace，例如 `solar:` 或 `ru102js:`，避免 key 衝突。
- 將 key 產生集中在小型 helper module。
- key 中使用穩定 ID；避免直接放入未清理的使用者輸入文字。
- 選定一種命名慣例後保持一致。
- 明確處理巢狀物件。Redis Hash 是扁平欄位，若不需要部分更新，可改用 JSON document。
- 明確處理型別轉換。Redis protocol 層多以字串表示資料，因此數字、布林、timestamp 與 JSON 都需要清楚的 encode/decode 規則。
- 只有當過期是產品行為的一部分時才設定 TTL。持久領域資料不應意外過期。

Key generator 範例：

```js
export function createKeyGenerator(prefix = 'solar') {
  return {
    site: (siteId) => `${prefix}:site:${siteId}`,
    siteIds: () => `${prefix}:sites`,
    siteGeo: () => `${prefix}:sites:geo`,
    siteReadings: (siteId) => `${prefix}:site:${siteId}:readings`,
    latestReading: (siteId) => `${prefix}:site:${siteId}:latest`,
    currentSummary: () => `${prefix}:summary:current`,
  };
}
```

建模取捨：

- Hash 適合欄位級更新與讀取，但不能直接表示深層巢狀文件。
- Sorted Set 適合依 timestamp 排序的資料，但大量歷史資料需要 retention 規則或歸檔儲存。
- 當 consumer 需要 ID、acknowledgement、consumer group 與 replay 時，Stream 通常比 List 更合適。
- JSON 字串簡單直接，但除非明確採用 RedisJSON，否則部分更新與索引會較困難。
- 為了支援必要讀取而在多個 key 複製資料是 Redis 常見做法；寫入路徑必須負責同步更新所有衍生索引。

### 測試與營運檢查清單

開發與測試：

- 測試使用專用 Redis database、container 或 key prefix。
- 只清除測試 namespace 或測試 database；不要在共享環境執行廣泛清除指令。
- 使用 Jest integration tests 覆蓋 DAO 的新增、讀取與更新行為。
- 測試型別轉換、找不到資料、重複新增、TTL 行為與 transaction 失敗路徑。
- 路由測試使用小型且可重現的 fixture。
- 修改 Redis access code 後，merge 前執行 `npm test`。

營運準備：

- 確認 Redis URL、username、password、TLS 設定與 database number 都由環境設定提供。
- 加入啟動健康檢查，確認 Redis 連線正常後才接受流量。
- 記錄 command failure 時提供足夠 key family context，但不要記錄 secrets 或完整敏感 payload。
- 明確設定 timeout 與 reconnect 行為，避免 Redis 不可用時 request 無限等待。
- 追蹤 latency、error rate、memory use、evictions、connected clients、key count growth 與 slow commands。
- 疑難排解時使用 `SCAN`、`MEMORY USAGE`、`INFO` 與 slow log。
- 對 meter readings 這類高量資料定義 retention。
- 應用服務使用 least-privilege Redis ACL user。
- 若 Redis 被當作 system of record，必須備份持久資料。
- 文件化每個 key family 的用途、owner、TTL policy 與清理流程。

Redis-backed feature 發布檢查：

- Key 名稱已集中管理並經過 review。
- 資料結構符合必要讀取路徑。
- 維護 secondary index 的寫入路徑都有測試。
- TTL 明確且有測試覆蓋。
- 本機與 CI 測試使用隔離 Redis 資料。
- Dashboard 與 alert 覆蓋 Redis availability 與 latency。
- schema 或 key format 變更具備 rollback plan。

## References

- [Redis documentation](https://redis.io/docs/latest/)
- [Redis commands](https://redis.io/docs/latest/commands/)
- [Node Redis client guide](https://redis.io/docs/latest/develop/clients/nodejs/)
- [node-redis GitHub repository](https://github.com/redis/node-redis)
- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis geospatial indexes](https://redis.io/docs/latest/develop/data-types/geospatial/)
- [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/)
- [Jest documentation](https://jestjs.io/docs/getting-started)
