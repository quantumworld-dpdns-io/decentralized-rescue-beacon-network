# Trino

| Field | Details |
| --- | --- |
| Name | Trino |
| Category | Distributed SQL query engine, query federation |
| License | Apache License 2.0 |
| Project stewardship | Trino Software Foundation |
| Primary use | Interactive and batch SQL across data lakes, lakehouses, databases, and object storage |
| Typical users | Data platform teams, analytics engineers, BI users, data engineers |
| Interfaces | ANSI SQL, CLI, JDBC, ODBC, REST API, BI tools |
| Common integrations | Apache Iceberg, Hive, Delta Lake, Hudi, PostgreSQL, MySQL, Kafka, Cassandra, Elasticsearch, object storage |
| Last verified | 2026-04-29 |

## English

### Overview

Trino is a distributed SQL query engine for large datasets spread across one or more heterogeneous data sources. It separates compute from storage and lets users run SQL over data lakes, lakehouse tables, relational databases, streaming systems, and specialized stores through connectors.

Trino is not a storage engine. It does not own data files by default. Instead, it plans and executes queries across worker nodes and delegates data access to connectors such as Iceberg, Hive, PostgreSQL, Kafka, or many others.

### Why it matters

Modern data platforms rarely keep all data in one database. Analytical data may live in object storage, operational data in PostgreSQL or MySQL, events in Kafka, and curated lakehouse tables in Iceberg. Copying everything into one warehouse can be expensive, slow, and operationally fragile.

Trino matters because it provides a fast SQL layer over many systems. It is widely used for interactive analytics, BI dashboards, data exploration, and federated joins. In lakehouse architectures, Trino is commonly the serving/query layer over Iceberg, Hive, Delta Lake, or Hudi tables stored in object storage.

### Architecture/Concepts

- **Coordinator**: Accepts client connections, parses SQL, analyzes queries, creates distributed plans, and schedules work.
- **Workers**: Execute query fragments, read data through connectors, process pages, exchange intermediate data, and return results.
- **Catalog**: A named connector configuration. Users refer to tables as `catalog.schema.table`.
- **Connector**: The plugin that gives Trino access to a data source and exposes metadata, splits, reads, writes, pushdown, and type mapping.
- **Schema and table**: Logical namespaces and relations exposed by each catalog.
- **Splits**: Units of parallel work produced by connectors and scheduled across workers.
- **Cost-based optimizer**: Uses statistics and rules to choose join order, pushdown, partition pruning, and distributed execution strategies.
- **Query federation**: A single SQL query can join data from different catalogs when connectors support the required operations.
- **Security model**: Trino can integrate with authentication systems, access control plugins, TLS, impersonation, and connector-specific authorization.

### Practical usage

Use Trino when many users or applications need SQL access to large datasets across data lakes and other systems.

Typical workflow:

1. Deploy a Trino coordinator and one or more workers.
2. Configure catalogs for systems such as Iceberg, Hive, PostgreSQL, Kafka, or object storage backed tables.
3. Connect with the CLI, JDBC, ODBC, or BI tools.
4. Query tables using fully qualified names such as `iceberg.analytics.events`.
5. Tune worker sizing, memory limits, exchange settings, statistics, and connector-specific pushdown behavior.
6. Add authentication, authorization, resource groups, and auditing before broad production use.

Example:

```sql
SELECT
  e.account_id,
  c.segment,
  count(*) AS events
FROM iceberg.analytics.events e
JOIN postgres.crm.customers c
  ON e.account_id = c.account_id
WHERE e.event_date >= DATE '2026-01-01'
GROUP BY e.account_id, c.segment
ORDER BY events DESC
LIMIT 50;
```

### Learning checklist

- Understand Trino's role as a query engine rather than a database or storage layer.
- Learn the coordinator, worker, catalog, connector, schema, table, and split model.
- Configure one lakehouse catalog, usually Iceberg or Hive, and one relational catalog.
- Practice query federation and understand when cross-source joins are expensive.
- Learn connector-specific capabilities such as predicate pushdown, projection pushdown, writes, and table maintenance.
- Review memory management, resource groups, spill, dynamic filtering, and statistics.
- Plan authentication, authorization, TLS, secrets management, and auditing before production rollout.

## 繁體中文

### 概觀

Trino 是用於大型資料集的分散式 SQL query engine，可查詢分散在一個或多個異質資料來源中的資料。它將 compute 與 storage 分離，並透過 connectors 讓使用者以 SQL 查詢 data lake、lakehouse table、關聯式資料庫、串流系統與特殊儲存系統。

Trino 不是 storage engine，預設不擁有資料檔案。它負責在 worker nodes 上規劃與執行查詢，並把資料存取交給 Iceberg、Hive、PostgreSQL、Kafka 等 connector。

### 為什麼重要

現代資料平台很少把所有資料放在單一資料庫。分析資料可能在物件儲存，營運資料在 PostgreSQL 或 MySQL，事件在 Kafka，整理後的 lakehouse table 則在 Iceberg。把所有資料複製進單一 warehouse 可能昂貴、緩慢且維運複雜。

Trino 的重要性在於它提供跨系統的快速 SQL 層。它常用於互動式分析、BI dashboard、資料探索與 federated join。在 lakehouse 架構中，Trino 常作為 Iceberg、Hive、Delta Lake 或 Hudi 表格的查詢服務層。

### 架構/概念

- **Coordinator**：接受 client 連線、解析 SQL、分析查詢、建立分散式 plan 並排程工作。
- **Workers**：執行 query fragments，透過 connector 讀取資料，處理 pages，交換中間結果並回傳結果。
- **Catalog**：具名 connector configuration。使用者以 `catalog.schema.table` 參照表格。
- **Connector**：讓 Trino 存取資料來源的 plugin，負責 metadata、splits、讀取、寫入、pushdown 與 type mapping。
- **Schema 與 table**：每個 catalog 暴露出的邏輯 namespace 與 relations。
- **Splits**：connector 產生並分派到 workers 的平行工作單位。
- **Cost-based optimizer**：使用 statistics 與 rules 選擇 join order、pushdown、partition pruning 與分散式執行策略。
- **Query federation**：當 connector 支援必要操作時，單一 SQL 可 join 不同 catalog 的資料。
- **Security model**：Trino 可整合 authentication、access control plugins、TLS、impersonation 與 connector-specific authorization。

### 實務用法

當多位使用者或應用程式需要跨 data lake 與其他系統查詢大型資料集時，可以使用 Trino。

典型流程如下：

1. 部署 Trino coordinator 與一個或多個 workers。
2. 為 Iceberg、Hive、PostgreSQL、Kafka 或物件儲存表格設定 catalogs。
3. 透過 CLI、JDBC、ODBC 或 BI tools 連線。
4. 使用完整名稱查詢資料表，例如 `iceberg.analytics.events`。
5. 調整 worker sizing、memory limits、exchange settings、statistics 與 connector-specific pushdown 行為。
6. 在廣泛上線前加入 authentication、authorization、resource groups 與 auditing。

範例：

```sql
SELECT
  e.account_id,
  c.segment,
  count(*) AS events
FROM iceberg.analytics.events e
JOIN postgres.crm.customers c
  ON e.account_id = c.account_id
WHERE e.event_date >= DATE '2026-01-01'
GROUP BY e.account_id, c.segment
ORDER BY events DESC
LIMIT 50;
```

### 學習檢核表

- 理解 Trino 是 query engine，而不是 database 或 storage layer。
- 熟悉 coordinator、worker、catalog、connector、schema、table、split 模型。
- 設定一個 lakehouse catalog，通常是 Iceberg 或 Hive，再設定一個 relational catalog。
- 練習 query federation，並理解跨來源 join 何時昂貴。
- 學習 connector-specific 能力，例如 predicate pushdown、projection pushdown、寫入與 table maintenance。
- 了解 memory management、resource groups、spill、dynamic filtering 與 statistics。
- 在 production rollout 前規劃 authentication、authorization、TLS、secrets management 與 auditing。

## References

- [Trino official site](https://trino.io/)
- [Trino documentation overview](https://trino.io/docs/current/overview.html)
- [Trino concepts](https://trino.io/docs/current/overview/concepts.html)
- [Trino connectors](https://trino.io/docs/current/connector.html)
- [Developing Trino connectors](https://trino.io/docs/current/develop/connectors.html)
- [Trino security](https://trino.io/docs/current/security.html)
