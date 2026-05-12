# Apache DataFusion

| Field | Details |
| --- | --- |
| Name | Apache DataFusion |
| Category | Extensible query engine, Rust analytics engine |
| License | Apache License 2.0 |
| Project | Apache Software Foundation |
| Primary use | Building databases, dataframes, query services, and analytical systems on Apache Arrow |
| Typical users | Database developers, Rust developers, query engine teams, data platform engineers |
| Interfaces | Rust APIs, SQL API, DataFrame API, CLI, Python bindings |
| Common integrations | Apache Arrow, Parquet, CSV, JSON, Avro, object stores, Ballista, Comet, custom table providers |
| Last verified | 2026-04-29 |

## English

### Overview

Apache DataFusion is an extensible query engine written in Rust that uses Apache Arrow as its in-memory format. It provides SQL and DataFrame APIs, a query optimizer, a vectorized execution engine, and extension points for building custom analytical systems.

DataFusion is usually a library or engine component rather than a standalone warehouse. Teams use it to build databases, embedded analytics, dataframe libraries, stream processors, query services, and domain-specific data platforms.

### Why it matters

Building a query engine from scratch is expensive. A production-quality system needs SQL parsing, logical and physical planning, optimization, expression evaluation, file readers, execution scheduling, metrics, and extension hooks.

DataFusion matters because it provides these pieces as composable Rust libraries. It lets system builders focus on their storage layer, catalog, domain functions, security model, or product experience while reusing an Arrow-native execution engine. It is also important in the broader Arrow ecosystem because it demonstrates how Arrow batches can flow through a modern vectorized query engine.

### Architecture/Concepts

- **SessionContext**: The high-level entry point for registering data sources and running SQL or DataFrame queries.
- **DataFrame API**: A lazy API for projection, filtering, aggregation, joins, and other transformations.
- **SQL API**: Executes SQL strings and returns DataFrames or record batch streams.
- **Logical plan**: Represents what a query should do independently from physical execution details.
- **Optimizer**: Applies rewrites and planning rules such as projection pushdown, filter pushdown, constant folding, and join optimization.
- **Physical plan**: Represents executable operators that process Arrow `RecordBatch` streams.
- **Execution engine**: Columnar, streaming, multi-threaded, vectorized execution built around Arrow.
- **Table providers**: Extension points for custom data sources, catalogs, schemas, and tables.
- **Functions and expressions**: Scalar, aggregate, window, and table functions can be added or customized.
- **Subprojects**: DataFusion Python provides Python bindings, Ballista extends DataFusion for distributed execution, and Comet accelerates Spark workloads using DataFusion.

### Practical usage

Use DataFusion when building a Rust-based analytical system or when Python bindings are sufficient for local SQL/DataFrame workflows.

Common workflows include:

1. Create a `SessionContext`.
2. Register CSV, Parquet, JSON, Avro, in-memory batches, object store paths, or custom table providers.
3. Run SQL or build a lazy DataFrame.
4. Collect results as Arrow `RecordBatch` values, stream them, or write them to files.
5. Add custom functions, table providers, optimizers, or physical operators when building a product.
6. Use Ballista or another distributed layer if a workload needs multi-node execution.

Example Python usage:

```python
from datafusion import SessionContext

ctx = SessionContext()
df = ctx.read_parquet("events.parquet")
df = df.select("account_id", "event_time").filter("event_time >= '2026-01-01'")
df.show()
```

### Learning checklist

- Understand DataFusion's role as an embeddable query engine, not a complete database by itself.
- Learn Apache Arrow arrays and record batches first.
- Run SQL and DataFrame examples with CSV and Parquet.
- Read logical plans, physical plans, and `EXPLAIN` output.
- Learn `SessionContext`, table registration, and catalog/schema/table concepts.
- Implement one scalar UDF and one custom table provider.
- Study optimizer rules, execution plans, metrics, and memory behavior before embedding in production.
- Evaluate whether single-process DataFusion, Ballista, Comet, or another engine is the right fit for scale requirements.

## 繁體中文

### 概觀

Apache DataFusion 是以 Rust 撰寫、使用 Apache Arrow 作為 in-memory format 的可擴充 query engine。它提供 SQL 與 DataFrame API、query optimizer、vectorized execution engine，以及用於建立客製分析系統的 extension points。

DataFusion 通常是 library 或 engine component，而不是完整 standalone warehouse。團隊會用它建立 database、embedded analytics、dataframe library、stream processor、query service 與 domain-specific data platform。

### 為什麼重要

從零建立 query engine 成本很高。production-quality 系統需要 SQL parsing、logical/physical planning、optimization、expression evaluation、file readers、execution scheduling、metrics 與 extension hooks。

DataFusion 的重要性在於它以可組合的 Rust libraries 提供這些元件。系統開發者可以專注在 storage layer、catalog、domain functions、security model 或產品體驗，同時重用 Arrow-native execution engine。它在 Arrow 生態中也很重要，因為它展示 Arrow batches 如何流經現代 vectorized query engine。

### 架構/概念

- **SessionContext**：註冊資料來源並執行 SQL 或 DataFrame query 的高階入口。
- **DataFrame API**：用於 projection、filtering、aggregation、join 等 transformation 的 lazy API。
- **SQL API**：執行 SQL 字串並回傳 DataFrame 或 record batch stream。
- **Logical plan**：描述查詢要做什麼，不綁定實際執行細節。
- **Optimizer**：套用 projection pushdown、filter pushdown、constant folding、join optimization 等 rewrite 與 planning rules。
- **Physical plan**：描述可執行 operators，處理 Arrow `RecordBatch` streams。
- **Execution engine**：以 Arrow 為核心的 columnar、streaming、multi-threaded、vectorized execution。
- **Table providers**：用於 custom data source、catalog、schema、table 的 extension points。
- **Functions 與 expressions**：可新增或客製 scalar、aggregate、window 與 table functions。
- **Subprojects**：DataFusion Python 提供 Python bindings，Ballista 將 DataFusion 擴展到分散式執行，Comet 使用 DataFusion 加速 Spark workloads。

### 實務用法

當你要建立 Rust-based analytical system，或 Python bindings 已足夠支援本機 SQL/DataFrame 工作流程時，可以使用 DataFusion。

常見流程如下：

1. 建立 `SessionContext`。
2. 註冊 CSV、Parquet、JSON、Avro、in-memory batches、object store paths 或 custom table providers。
3. 執行 SQL 或建立 lazy DataFrame。
4. 將結果 collect 為 Arrow `RecordBatch`、以 stream 輸出，或寫入檔案。
5. 建立產品時加入 custom functions、table providers、optimizers 或 physical operators。
6. 若 workload 需要多節點執行，可評估 Ballista 或其他 distributed layer。

Python 使用範例：

```python
from datafusion import SessionContext

ctx = SessionContext()
df = ctx.read_parquet("events.parquet")
df = df.select("account_id", "event_time").filter("event_time >= '2026-01-01'")
df.show()
```

### 學習檢核表

- 理解 DataFusion 是 embeddable query engine，本身不是完整 database。
- 先學 Apache Arrow arrays 與 record batches。
- 用 CSV 與 Parquet 執行 SQL 與 DataFrame 範例。
- 閱讀 logical plan、physical plan 與 `EXPLAIN` output。
- 學習 `SessionContext`、table registration、catalog/schema/table concepts。
- 實作一個 scalar UDF 與一個 custom table provider。
- 在嵌入 production 前研究 optimizer rules、execution plans、metrics 與 memory behavior。
- 依 scale 需求評估 single-process DataFusion、Ballista、Comet 或其他引擎是否合適。

## References

- [Apache DataFusion official documentation](https://datafusion.apache.org/)
- [Apache DataFusion introduction](https://datafusion.apache.org/user-guide/introduction.html)
- [DataFusion SQL API](https://datafusion.apache.org/library-user-guide/using-the-sql-api.html)
- [DataFusion DataFrame API](https://datafusion.apache.org/user-guide/dataframe.html)
- [DataFusion Python documentation](https://datafusion.apache.org/python/)
- [Gentle Arrow introduction for DataFusion](https://datafusion.apache.org/user-guide/arrow-introduction.html)
