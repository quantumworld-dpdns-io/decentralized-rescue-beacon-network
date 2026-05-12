# Apache Arrow

| Field | Details |
| --- | --- |
| Name | Apache Arrow |
| Category | In-memory columnar format, data interchange, analytics toolkit |
| License | Apache License 2.0 |
| Project | Apache Software Foundation |
| Primary use | Fast in-memory analytics and zero-copy data interchange across languages and systems |
| Typical users | Database developers, query engine developers, data frame library authors, ML/data platform engineers |
| Core components | Columnar format, IPC format, language libraries, C data interface, Flight RPC, Flight SQL, ADBC |
| Common integrations | DataFusion, DuckDB, Polars, Pandas/PyArrow, Spark integrations, database drivers, ML pipelines |
| Last verified | 2026-04-29 |

## English

### Overview

Apache Arrow is a standardized in-memory columnar format and a multi-language toolbox for high-performance analytics and data interchange. It gives databases, query engines, data frame libraries, and ML systems a common way to represent structured tabular data in memory.

Arrow is most useful as infrastructure. End users may see it through libraries such as PyArrow, Polars, DuckDB, DataFusion, or database connectors, while system builders use Arrow to reduce serialization overhead and improve vectorized processing.

### Why it matters

Without a shared memory format, every engine and language tends to define its own internal representation. Moving data between systems then requires conversion, copying, and serialization. That cost becomes large in analytics pipelines that pass data among Python, Rust, Java, C++, databases, and machine learning frameworks.

Arrow matters because it standardizes the in-memory representation. Systems can exchange batches of columnar data with little or no copying, reuse algorithms across languages, and feed vectorized execution engines efficiently. It is one of the key building blocks behind modern local analytics, query engines, and dataframe interoperability.

### Architecture/Concepts

- **Columnar format**: Values are stored by column rather than row, improving scan efficiency and vectorized processing.
- **Arrays**: A typed sequence of values, represented by metadata, buffers, length, null count, and optional child arrays.
- **RecordBatch**: A set of equal-length arrays that together represent a batch of rows with a schema.
- **Schema**: Field names, data types, nullability, and metadata describing tabular data.
- **Buffers and validity bitmaps**: Arrow uses contiguous buffers and null bitmaps to represent values and missingness efficiently.
- **Nested and complex types**: Structs, lists, maps, unions, dictionaries, timestamps, decimals, and extension types support analytical schemas.
- **IPC format**: A serialization format for moving Arrow data between processes or storing streams/files.
- **C data and stream interfaces**: Stable interfaces for exchanging Arrow data across language boundaries.
- **Flight and Flight SQL**: RPC protocols for high-throughput Arrow data transport and SQL-oriented access.
- **ADBC**: Arrow Database Connectivity, a database API focused on Arrow-native data exchange.

### Practical usage

Use Arrow when systems need fast, typed, columnar data exchange or an efficient in-memory representation.

Common workflows include:

1. Use PyArrow to read Parquet, IPC, or dataset files into Arrow tables.
2. Convert between Arrow, Pandas, Polars, DuckDB, or DataFusion while minimizing copies where possible.
3. Pass Arrow `RecordBatch` streams between services or query engine stages.
4. Use Flight for high-throughput network transport of Arrow data.
5. Use Arrow-native database connectivity where drivers support ADBC or Flight SQL.
6. Design extension types and schemas carefully so data remains portable across languages.

Example Python flow:

```python
import pyarrow.dataset as ds

dataset = ds.dataset("s3://example-bucket/events/", format="parquet")
table = dataset.to_table(columns=["account_id", "event_time", "event_type"])

print(table.schema)
```

### Learning checklist

- Understand why columnar memory layout improves analytical scans.
- Learn Arrow arrays, buffers, validity bitmaps, schemas, and record batches.
- Compare Arrow's in-memory format with Parquet's on-disk columnar format.
- Practice moving data among PyArrow, Pandas, Polars, DuckDB, and DataFusion.
- Learn IPC streams/files and when they are useful.
- Review the C data interface if integrating systems across languages.
- Explore Flight, Flight SQL, and ADBC for service and database connectivity.
- Validate zero-copy assumptions because some conversions still copy due to type, alignment, or ownership differences.

## 繁體中文

### 概觀

Apache Arrow 是標準化的 in-memory columnar format，也是一組多語言高效能分析與資料交換工具。它讓 database、query engine、dataframe library 與 ML 系統可以用共同方式在記憶體中表示結構化表格資料。

Arrow 最常作為基礎設施使用。一般使用者可能透過 PyArrow、Polars、DuckDB、DataFusion 或 database connector 接觸到它；系統開發者則用 Arrow 降低 serialization overhead 並提升 vectorized processing 效率。

### 為什麼重要

若沒有共享的記憶體格式，每個引擎與語言通常都會定義自己的內部表示。資料在系統間移動時就需要轉換、複製與序列化。當分析 pipeline 在 Python、Rust、Java、C++、database 與 machine learning framework 間傳遞資料時，這些成本會快速放大。

Arrow 的重要性在於它標準化了 in-memory representation。系統可以用很少甚至零複製的方式交換 columnar data batch，跨語言重用演算法，並有效餵給 vectorized execution engine。它是現代本機分析、查詢引擎與 dataframe interoperability 的關鍵基礎。

### 架構/概念

- **Columnar format**：資料依欄儲存，而不是依列儲存，可提升 scan 效率與 vectorized processing。
- **Arrays**：具型別的值序列，由 metadata、buffers、length、null count 與選用 child arrays 表示。
- **RecordBatch**：一組等長 arrays，搭配 schema 表示一批資料列。
- **Schema**：描述欄位名稱、資料型別、nullability 與 metadata。
- **Buffers 與 validity bitmaps**：Arrow 使用連續 buffers 與 null bitmaps 有效率地表示值與缺失值。
- **Nested 與 complex types**：struct、list、map、union、dictionary、timestamp、decimal、extension type 支援分析型 schema。
- **IPC format**：用於跨 process 傳輸 Arrow data 或儲存 stream/file 的序列化格式。
- **C data 與 stream interfaces**：跨語言交換 Arrow data 的穩定介面。
- **Flight 與 Flight SQL**：用於高吞吐 Arrow data transport 與 SQL-oriented access 的 RPC protocols。
- **ADBC**：Arrow Database Connectivity，是以 Arrow-native data exchange 為核心的 database API。

### 實務用法

當系統需要快速、具型別、columnar 的資料交換或高效 in-memory representation 時，可以使用 Arrow。

常見流程如下：

1. 使用 PyArrow 將 Parquet、IPC 或 dataset files 讀成 Arrow tables。
2. 在 Arrow、Pandas、Polars、DuckDB 或 DataFusion 間轉換，盡可能降低複製。
3. 在服務或 query engine stages 間傳遞 Arrow `RecordBatch` streams。
4. 使用 Flight 進行高吞吐網路傳輸。
5. 在 driver 支援時使用 ADBC 或 Flight SQL 做 Arrow-native database connectivity。
6. 謹慎設計 extension types 與 schemas，確保資料可跨語言攜帶。

Python 範例：

```python
import pyarrow.dataset as ds

dataset = ds.dataset("s3://example-bucket/events/", format="parquet")
table = dataset.to_table(columns=["account_id", "event_time", "event_type"])

print(table.schema)
```

### 學習檢核表

- 理解 columnar memory layout 為何能提升分析 scan 效率。
- 學習 Arrow arrays、buffers、validity bitmaps、schemas 與 record batches。
- 比較 Arrow 的 in-memory format 與 Parquet 的 on-disk columnar format。
- 練習在 PyArrow、Pandas、Polars、DuckDB、DataFusion 間移動資料。
- 學習 IPC streams/files 的使用時機。
- 若要跨語言整合系統，閱讀 C data interface。
- 探索 Flight、Flight SQL 與 ADBC 在服務與 database connectivity 中的用途。
- 驗證 zero-copy 假設，因為部分轉換仍可能因型別、alignment 或 ownership 差異而複製。

## References

- [Apache Arrow official site](https://arrow.apache.org/)
- [Apache Arrow documentation](https://arrow.apache.org/docs/)
- [Arrow columnar format](https://arrow.apache.org/docs/format/Columnar.html)
- [Arrow Flight RPC](https://arrow.apache.org/docs/format/Flight.html)
- [Arrow Flight SQL](https://arrow.apache.org/docs/format/FlightSql.html)
- [ADBC: Arrow Database Connectivity](https://arrow.apache.org/adbc/)
