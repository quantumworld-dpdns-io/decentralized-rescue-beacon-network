# Apache Iceberg

| Field | Details |
| --- | --- |
| Name | Apache Iceberg |
| Category | Open lakehouse table format |
| License | Apache License 2.0 |
| Project | Apache Software Foundation |
| Primary use | Reliable analytical tables on object storage and distributed file systems |
| Typical users | Data platform teams, data engineers, analytics engineers, query engine maintainers |
| Common engines | Apache Spark, Apache Flink, Trino, Presto, Apache Hive, Apache Impala, DuckDB integrations |
| Common catalogs | REST catalog, Hive Metastore, JDBC, Nessie, Apache Polaris, cloud catalog services |
| Last verified | 2026-04-29 |

## English

### Overview

Apache Iceberg is an open table format for large analytical datasets. It turns collections of data files, usually Parquet, Avro, or ORC, into tables that query engines can treat like SQL tables while preserving reliable metadata, snapshots, schema evolution, partition evolution, and time travel.

Iceberg is not a query engine or a storage system. It is the table layer between engines such as Spark, Flink, Trino, and DuckDB, and storage such as S3, Azure Storage, Google Cloud Storage, HDFS, or compatible object stores.

### Why it matters

Data lakes became hard to operate when tables were inferred from directory layouts and file naming conventions. That approach made schema changes, partition changes, concurrent writes, deletes, and rollbacks risky.

Iceberg matters because it gives lakehouse tables explicit metadata and atomic commits. Engines can read a consistent snapshot, writers can commit changes without rewriting the entire table, and users can evolve schemas and partitions without exposing partition layout details in every query. A shared Iceberg catalog also lets multiple engines work on the same table layer without copying data into separate warehouses.

### Architecture/Concepts

- **Table metadata**: JSON metadata files describe the table schema, partition specs, properties, sort order, snapshots, and current table state.
- **Snapshots**: Each commit creates a new snapshot that points to the set of data files that make up the table at that time.
- **Manifests and manifest lists**: Metadata files track data files, delete files, partition values, and file-level statistics so engines can plan scans efficiently.
- **Atomic commit**: The catalog updates the table's current metadata pointer atomically, enabling optimistic concurrency control.
- **Schema evolution**: Columns can be added, dropped, renamed, reordered, or widened with stable field IDs instead of relying only on column names.
- **Hidden partitioning**: Users query logical columns while Iceberg manages partition transforms such as day, bucket, truncate, or identity.
- **Partition evolution**: Tables can change partition layout over time without rewriting all historical data.
- **Deletes and updates**: Format v2 supports row-level operations through position deletes and equality deletes.
- **Time travel and rollback**: Queries can target earlier snapshots, and operators can roll back a table to a known good snapshot.
- **Catalogs**: Catalogs map table names to current metadata. The REST catalog protocol is increasingly important because it gives engines one common API for catalog operations.

### Practical usage

Use Iceberg when data is stored in a lake but needs warehouse-like reliability, multiple query engines, and long-lived table evolution.

Typical workflow:

1. Choose a catalog, such as REST, Hive Metastore, JDBC, Nessie, Apache Polaris, or a managed cloud catalog.
2. Configure engines to use the same catalog and warehouse/storage location.
3. Create Iceberg tables through Spark, Flink, Trino, or another compatible engine.
4. Write data with append, overwrite, merge, update, or delete operations supported by the chosen engine.
5. Compact small files, expire old snapshots, and remove orphan files as part of table maintenance.
6. Test cross-engine reads and writes before treating a table as a shared production asset.

Example Trino-style SQL:

```sql
CREATE SCHEMA lakehouse.analytics;

CREATE TABLE lakehouse.analytics.events (
  event_id varchar,
  event_time timestamp,
  account_id varchar
)
WITH (
  format = 'PARQUET',
  partitioning = ARRAY['day(event_time)']
);

SELECT count(*)
FROM lakehouse.analytics.events
WHERE event_time >= TIMESTAMP '2026-01-01 00:00:00';
```

### Learning checklist

- Understand the difference between file formats, table formats, catalogs, and query engines.
- Read the Iceberg table metadata, snapshot, manifest, and data file model.
- Learn schema evolution, hidden partitioning, partition evolution, and snapshot isolation.
- Compare catalog choices, especially REST catalog, Hive Metastore, JDBC, Nessie, and Polaris.
- Practice creating, appending, merging, deleting, and time-travel querying a table.
- Learn maintenance operations: compaction, snapshot expiration, metadata cleanup, and orphan file removal.
- Validate engine compatibility before relying on row-level deletes, branches, tags, or newer format features.

## 繁體中文

### 概觀

Apache Iceberg 是用於大型分析資料集的開放式 table format。它把通常存放為 Parquet、Avro 或 ORC 的資料檔案組織成查詢引擎可視為 SQL table 的資料表，同時提供可靠的 metadata、snapshot、schema evolution、partition evolution 與 time travel。

Iceberg 不是查詢引擎，也不是儲存系統。它位於 Spark、Flink、Trino、DuckDB 等運算引擎與 S3、Azure Storage、Google Cloud Storage、HDFS 或相容物件儲存之間，負責 lakehouse 的資料表層。

### 為什麼重要

傳統 data lake 常用目錄結構與檔名慣例推論資料表狀態。這種方式在 schema 變更、partition 變更、並行寫入、刪除與 rollback 時容易出錯。

Iceberg 的重要性在於它為 lakehouse table 提供明確 metadata 與原子提交。查詢引擎可以讀取一致的 snapshot，寫入端可以提交變更而不必重寫整張表，使用者也能演進 schema 與 partition，而不需要在每個查詢中理解底層 partition 配置。透過共享 Iceberg catalog，多個引擎也能操作同一份 table layer，而不必複製資料到不同倉儲。

### 架構/概念

- **Table metadata**：JSON metadata 檔描述 schema、partition spec、properties、sort order、snapshots 與目前表格狀態。
- **Snapshots**：每次 commit 都會建立新的 snapshot，指向該時間點構成表格的一組資料檔。
- **Manifests 與 manifest lists**：追蹤資料檔、delete files、partition values 與檔案層級統計，讓引擎有效規劃 scan。
- **Atomic commit**：catalog 以原子方式更新目前 metadata pointer，支援 optimistic concurrency control。
- **Schema evolution**：透過穩定 field ID 支援新增、刪除、重新命名、重新排序與擴大欄位型別。
- **Hidden partitioning**：使用者查詢邏輯欄位，Iceberg 管理 day、bucket、truncate、identity 等 partition transform。
- **Partition evolution**：表格可隨時間變更 partition layout，而不需重寫所有歷史資料。
- **Deletes 與 updates**：format v2 透過 position delete 與 equality delete 支援 row-level 操作。
- **Time travel 與 rollback**：查詢可指定舊 snapshot，維運人員也可將表格 rollback 到已知正常狀態。
- **Catalogs**：catalog 將表格名稱對應到目前 metadata。REST catalog protocol 越來越重要，因為它提供跨引擎的共同 catalog API。

### 實務用法

當資料存放在 data lake，但需要接近 data warehouse 的可靠性、多引擎互通與長期表格演進時，可以使用 Iceberg。

典型流程如下：

1. 選擇 catalog，例如 REST、Hive Metastore、JDBC、Nessie、Apache Polaris 或雲端託管 catalog。
2. 將各個引擎設定為使用同一個 catalog 與 warehouse/storage location。
3. 透過 Spark、Flink、Trino 或其他相容引擎建立 Iceberg table。
4. 使用引擎支援的 append、overwrite、merge、update 或 delete 寫入資料。
5. 將 small file compaction、snapshot expiration、orphan file cleanup 納入表格維護流程。
6. 在把表格視為共享 production asset 前，先測試跨引擎讀寫行為。

Trino 風格 SQL 範例：

```sql
CREATE SCHEMA lakehouse.analytics;

CREATE TABLE lakehouse.analytics.events (
  event_id varchar,
  event_time timestamp,
  account_id varchar
)
WITH (
  format = 'PARQUET',
  partitioning = ARRAY['day(event_time)']
);

SELECT count(*)
FROM lakehouse.analytics.events
WHERE event_time >= TIMESTAMP '2026-01-01 00:00:00';
```

### 學習檢核表

- 理解 file format、table format、catalog 與 query engine 的差異。
- 讀懂 Iceberg 的 table metadata、snapshot、manifest 與 data file 模型。
- 學習 schema evolution、hidden partitioning、partition evolution 與 snapshot isolation。
- 比較 REST catalog、Hive Metastore、JDBC、Nessie、Polaris 等 catalog 選項。
- 練習建立、append、merge、delete 與 time-travel 查詢。
- 學習 compaction、snapshot expiration、metadata cleanup、orphan file removal 等維護操作。
- 在依賴 row-level delete、branch、tag 或新版 format 功能前，先驗證引擎相容性。

## References

- [Apache Iceberg documentation](https://iceberg.apache.org/)
- [Apache Iceberg table specification](https://iceberg.apache.org/spec/)
- [Apache Iceberg REST catalog specification](https://iceberg.apache.org/rest-catalog-spec/)
- [Apache Iceberg configuration and catalog properties](https://iceberg.apache.org/docs/latest/docs/configuration/)
