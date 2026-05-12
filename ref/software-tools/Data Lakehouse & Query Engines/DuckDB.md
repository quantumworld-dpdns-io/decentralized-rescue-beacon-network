# DuckDB

| Field | Details |
| --- | --- |
| Name | DuckDB |
| Category | Embedded analytical database, local query engine |
| License | MIT License |
| Project stewardship | DuckDB Foundation |
| Primary use | In-process OLAP SQL over local files, data frames, and small-to-medium analytical datasets |
| Typical users | Data analysts, data scientists, analytics engineers, application developers, notebook users |
| Interfaces | CLI, C/C++, Python, R, Java/JDBC, Node.js, Go, Rust, ODBC, WebAssembly |
| Common integrations | CSV, Parquet, JSON, Apache Arrow, Pandas, Polars, S3/HTTP via extensions, Iceberg via extension |
| Last verified | 2026-04-29 |

## English

### Overview

DuckDB is an in-process analytical SQL database. It is often described as "SQLite for analytics": easy to embed, simple to install, and optimized for OLAP queries rather than high-concurrency transactional workloads.

DuckDB can run as a command-line tool, a library inside Python/R/Java/Node.js/Go/Rust applications, or in the browser through DuckDB-Wasm. It is especially useful for querying Parquet, CSV, JSON, Arrow, Pandas, and Polars data without standing up a database server.

### Why it matters

Many analytical tasks are too small or too local to justify a distributed warehouse, but too large or SQL-heavy for spreadsheets and ad hoc scripts. DuckDB fills that gap by bringing a fast columnar-vectorized engine directly into the process where the analyst or application already runs.

For lakehouse workflows, DuckDB is valuable as a local exploration and transformation tool. It can query Parquet files directly, interoperate with Arrow-based data frames, read from remote object storage through extensions, and increasingly participate in table-format workflows such as Iceberg.

### Architecture/Concepts

- **In-process execution**: DuckDB runs inside the host process instead of as a separate database server.
- **OLAP focus**: The engine is optimized for analytical scans, aggregations, joins, and transformations over large batches of rows.
- **Columnar-vectorized execution**: Queries process vectors of values at a time, reducing per-row overhead and improving CPU efficiency.
- **Single-file database option**: DuckDB can persist tables in a local database file, or operate directly over external files.
- **Replacement scans**: In clients such as Python, DuckDB can query data frames and files naturally through SQL.
- **File-native analytics**: CSV, Parquet, and JSON are common first-class inputs and outputs.
- **Extensions**: Features such as HTTP/S3 access, Arrow integration, spatial functions, and Iceberg support are delivered through built-in, core, or community extensions.
- **Client APIs**: DuckDB has idiomatic interfaces for common languages and tools, making it easy to embed in notebooks, apps, and pipelines.

### Practical usage

Use DuckDB when you need local analytical SQL without operating a database service.

Common workflows include:

1. Install DuckDB in the CLI or language runtime.
2. Query local Parquet, CSV, JSON, Arrow, Pandas, or Polars data directly.
3. Use SQL to join, aggregate, clean, and reshape data.
4. Write results back to Parquet, CSV, JSON, or a DuckDB database file.
5. Load extensions when network storage, Arrow, Iceberg, or domain-specific features are needed.
6. Move heavy shared workloads to Trino, Spark, or a warehouse when concurrency, governance, or scale exceeds local execution.

Example:

```sql
INSTALL httpfs;
LOAD httpfs;

SELECT
  account_id,
  count(*) AS events,
  max(event_time) AS last_event
FROM read_parquet('s3://example-bucket/events/*.parquet')
WHERE event_time >= TIMESTAMP '2026-01-01 00:00:00'
GROUP BY account_id
ORDER BY events DESC
LIMIT 20;
```

### Learning checklist

- Understand where DuckDB fits relative to SQLite, PostgreSQL, Trino, Spark, and cloud warehouses.
- Install the CLI and one client API, usually Python or R.
- Practice querying CSV, Parquet, JSON, and data frames directly.
- Learn the SQL dialect, including aggregates, windows, `COPY`, and file functions.
- Learn when to use a persistent DuckDB file versus external files.
- Explore extensions such as `httpfs`, `parquet`, `json`, `arrow`, and `iceberg`.
- Review security guidance before executing untrusted SQL or allowing extension/network access in applications.

## 繁體中文

### 概觀

DuckDB 是 in-process analytical SQL database，常被形容為「分析場景的 SQLite」：容易嵌入、安裝簡單，並針對 OLAP 查詢最佳化，而不是針對高併發交易 workload。

DuckDB 可以作為 command-line tool，也可以嵌入 Python、R、Java、Node.js、Go、Rust 應用程式，或透過 DuckDB-Wasm 在瀏覽器中執行。它特別適合在不架設資料庫伺服器的情況下查詢 Parquet、CSV、JSON、Arrow、Pandas 與 Polars 資料。

### 為什麼重要

許多分析任務小到不需要分散式 warehouse，但又大到不適合 spreadsheet 或臨時腳本。DuckDB 補上這個空缺，將快速的 columnar-vectorized engine 帶進分析師或應用程式原本執行的 process。

對 lakehouse 工作流程而言，DuckDB 是很實用的本機探索與轉換工具。它可以直接查詢 Parquet，與 Arrow-based dataframe 互通，透過 extension 讀取遠端物件儲存，並逐步支援 Iceberg 等 table format 工作流程。

### 架構/概念

- **In-process execution**：DuckDB 在 host process 內執行，不需要獨立 database server。
- **OLAP focus**：引擎針對大量資料的 scan、aggregation、join 與 transformation 最佳化。
- **Columnar-vectorized execution**：查詢一次處理一批 value vector，降低逐列處理成本並提升 CPU 效率。
- **Single-file database option**：DuckDB 可把 table 持久化到單一 database file，也可直接操作外部檔案。
- **Replacement scans**：在 Python 等 client 中，可自然地以 SQL 查詢 dataframe 與檔案。
- **File-native analytics**：CSV、Parquet、JSON 是常見的一等輸入與輸出格式。
- **Extensions**：HTTP/S3 存取、Arrow 整合、spatial functions、Iceberg 支援等功能可透過 built-in、core 或 community extension 提供。
- **Client APIs**：DuckDB 提供多種常用語言介面，方便嵌入 notebook、應用程式與 pipeline。

### 實務用法

當你需要本機 analytical SQL，但不想維運資料庫服務時，可以使用 DuckDB。

常見流程如下：

1. 在 CLI 或語言 runtime 中安裝 DuckDB。
2. 直接查詢本機 Parquet、CSV、JSON、Arrow、Pandas 或 Polars 資料。
3. 用 SQL 進行 join、aggregate、清理與 reshaping。
4. 將結果寫回 Parquet、CSV、JSON 或 DuckDB database file。
5. 需要 network storage、Arrow、Iceberg 或領域功能時載入 extension。
6. 當 concurrency、governance 或 scale 超過本機執行範圍時，將共享重型 workload 移到 Trino、Spark 或 warehouse。

範例：

```sql
INSTALL httpfs;
LOAD httpfs;

SELECT
  account_id,
  count(*) AS events,
  max(event_time) AS last_event
FROM read_parquet('s3://example-bucket/events/*.parquet')
WHERE event_time >= TIMESTAMP '2026-01-01 00:00:00'
GROUP BY account_id
ORDER BY events DESC
LIMIT 20;
```

### 學習檢核表

- 理解 DuckDB 相對於 SQLite、PostgreSQL、Trino、Spark 與 cloud warehouse 的定位。
- 安裝 CLI 與一種 client API，通常是 Python 或 R。
- 練習直接查詢 CSV、Parquet、JSON 與 dataframe。
- 學習 SQL dialect，包括 aggregates、windows、`COPY` 與 file functions。
- 理解何時使用持久化 DuckDB file，何時直接使用外部檔案。
- 探索 `httpfs`、`parquet`、`json`、`arrow`、`iceberg` 等 extensions。
- 在應用程式中執行不可信 SQL 或允許 extension/network access 前，先閱讀安全設定。

## References

- [DuckDB official site](https://duckdb.org/)
- [Why DuckDB](https://duckdb.org/why_duckdb.html)
- [DuckDB stable documentation](https://duckdb.org/docs/stable/)
- [DuckDB client overview](https://duckdb.org/docs/stable/clients/overview)
- [DuckDB extensions overview](https://duckdb.org/docs/stable/extensions/overview)
- [Securing DuckDB](https://duckdb.org/docs/stable/operations_manual/securing_duckdb/overview.html)
