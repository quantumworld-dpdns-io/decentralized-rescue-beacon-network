# Apache Gravitino

| Field | Details |
|---|---|
| Name | Apache Gravitino |
| Category | Metadata lake, lakehouse catalog, federated metadata governance |
| License | Apache License 2.0 |
| Project | Apache Software Foundation |
| Primary use | Unified metadata access and governance across lakehouse tables, relational systems, files, streams, and AI assets |
| Typical users | Data platform teams, data engineers, analytics engineers, ML platform teams, governance teams |
| Interfaces | REST API, Java client, Python client, query engine connectors |
| Common integrations | Apache Iceberg, Apache Hive, Apache Spark, Apache Flink, Trino, MySQL, PostgreSQL, Kafka, HDFS, S3-compatible storage |

## English

### Overview

Apache Gravitino is a federated metadata lake and technical data catalog for modern data and AI platforms. It gives teams a single control plane for metadata that may physically live in different systems, regions, clouds, and storage formats.

Gravitino should not be confused with Apache Gluten. Gluten accelerates Spark execution by offloading work to native engines; Gravitino manages metadata and governance. Its core purpose is to organize, expose, and govern metadata for tables, filesets, topics, models, and related assets through a consistent model and API.

### Why it matters

Large data platforms usually accumulate many catalogs: Hive Metastore, Iceberg REST catalogs, JDBC databases, object storage paths, streaming topics, and model registries. Without a unifying layer, users must learn different APIs, security patterns, naming rules, and operational workflows for each system.

Gravitino helps by providing:

- A single metadata access layer for heterogeneous data and AI assets.
- A common namespace model for catalogs, schemas, tables, filesets, models, and topics.
- Direct metadata management through connectors, so changes can be reflected in the underlying systems instead of only copied into a passive inventory.
- Centralized governance concepts such as access control, auditing, and discovery.
- Multi-engine access patterns, allowing engines such as Spark, Flink, and Trino to work with metadata managed through Gravitino.

### Architecture/Concepts

Gravitino is built around a layered architecture:

- **Functionality layer**: management and governance operations such as create, update, delete, discovery, and access control.
- **Interface layer**: a standard REST API, with client libraries and engine connectors layered on top.
- **Core object model**: a generic metadata model that represents different asset types in one structure.
- **Connection layer**: connectors that communicate with metadata systems such as Hive, Iceberg, MySQL, PostgreSQL, Kafka, and file/object stores.

The main metadata objects are:

- **Metalake**: the top-level metadata container or tenant. A metalake normally represents a group, platform domain, or organization boundary.
- **Catalog**: a collection of metadata from a specific source or provider. Examples include Hive, Iceberg, JDBC, fileset, or Kafka-related catalogs.
- **Schema**: the second-level namespace under a catalog. In relational systems it maps naturally to a database or schema; in fileset catalogs it is a logical grouping.
- **Table**: the table-level object for relational and lakehouse catalogs.
- **Fileset**: metadata for a group of files or directories in supported file systems or object stores.
- **Topic**: metadata for messaging or event-streaming systems such as Kafka.
- **Model**: metadata for AI or machine learning model assets.

In practice, the namespace is commonly expressed as:

```text
metalake.catalog.schema.asset
```

For table-oriented systems, the asset is usually a table. For file-oriented systems, it may be a fileset. For streaming systems, it may be a topic.

### Practical usage

Use Gravitino when a platform needs consistent metadata management across multiple storage systems and compute engines.

Common workflows include:

1. Create a **metalake** to define the governance and namespace boundary.
2. Create one or more **catalogs** for systems such as Hive, Iceberg, MySQL, PostgreSQL, Kafka, or filesets.
3. Create **schemas** under each catalog to organize assets.
4. Manage **tables**, **filesets**, **topics**, or **models** through REST APIs, Java/Python clients, or supported engine connectors.
5. Let compute engines such as Trino, Spark, or Flink discover and operate on metadata through Gravitino-aware connectors.

Example REST-style flow:

```bash
# Create a fileset catalog under an existing metalake.
curl -X POST \
  -H "Accept: application/vnd.gravitino.v1+json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "files",
    "type": "FILESET",
    "comment": "Shared file metadata",
    "properties": {
      "location": "s3://example-bucket/data"
    }
  }' \
  http://localhost:8090/api/metalakes/example/catalogs
```

Example Trino-oriented usage:

```sql
SHOW CATALOGS;

CREATE SCHEMA iceberg_catalog.analytics;

CREATE TABLE iceberg_catalog.analytics.events (
  event_id varchar,
  event_time timestamp,
  payload varchar
);
```

Operationally, Gravitino is most useful when the data platform team treats it as infrastructure: define naming conventions, catalog ownership, authentication, connector configuration, storage locations, and engine integration before broad adoption.

### Learning checklist

- Understand the difference between a passive data catalog and Gravitino's direct metadata management model.
- Learn the hierarchy: metalake, catalog, schema, table/fileset/topic/model.
- Identify which metadata systems your platform needs to federate.
- Review the REST API and client libraries for automation.
- Test one engine integration, such as Trino with Iceberg or Spark with Iceberg.
- Decide how catalog ownership, authentication, and access control should be managed.
- Validate storage behavior before using managed filesets or managed lakehouse tables in production.

## 繁體中文

### 概觀

Apache Gravitino 是一個聯邦式 metadata lake 與技術型資料目錄，適合用在現代資料平台與 AI 平台。它提供一個統一控制面，讓團隊可以管理分散在不同系統、區域、雲端與儲存格式中的中繼資料。

Gravitino 不應與 Apache Gluten 混淆。Gluten 的重點是透過 native engine 加速 Spark 執行；Gravitino 的重點則是中繼資料管理、湖倉目錄與治理。它用一致的模型與 API 管理 table、fileset、topic、model 等資料與 AI 資產的中繼資料。

### 為什麼重要

大型資料平台通常會累積多種目錄與中繼資料系統，例如 Hive Metastore、Iceberg REST catalog、JDBC 資料庫、物件儲存路徑、串流 topic、模型登錄系統等。若沒有統一層，使用者必須分別理解不同 API、安全模型、命名方式與維運流程。

Gravitino 的價值包括：

- 為異質資料與 AI 資產提供統一的中繼資料存取層。
- 使用共同命名空間管理 catalog、schema、table、fileset、model、topic。
- 透過 connector 直接管理底層系統的中繼資料，而不只是建立一份被動盤點。
- 集中處理存取控制、稽核、探索等治理需求。
- 支援多種運算引擎存取模式，讓 Spark、Flink、Trino 等引擎可以使用由 Gravitino 管理的中繼資料。

### 架構/概念

Gravitino 的架構可理解為幾個層次：

- **功能層**：提供建立、更新、刪除、探索、存取控制等管理與治理能力。
- **介面層**：以標準 REST API 為核心，並提供 client library 與運算引擎 connector。
- **核心物件模型**：用通用中繼資料模型描述不同類型的資產。
- **連接層**：透過 connector 連接 Hive、Iceberg、MySQL、PostgreSQL、Kafka、檔案系統與物件儲存等來源。

主要中繼資料物件如下：

- **Metalake**：最高層級的中繼資料容器或 tenant，通常代表一個群組、平台領域或組織邊界。
- **Catalog**：特定來源或 provider 的中繼資料集合，例如 Hive、Iceberg、JDBC、fileset、Kafka 相關 catalog。
- **Schema**：catalog 底下的第二層命名空間。在關聯式系統中通常對應 database 或 schema；在 fileset catalog 中則是邏輯分組。
- **Table**：關聯式與 lakehouse catalog 中的資料表物件。
- **Fileset**：一組檔案或目錄的中繼資料，可用於支援的檔案系統或物件儲存。
- **Topic**：訊息佇列或事件串流系統的 topic 中繼資料，例如 Kafka。
- **Model**：AI 或機器學習模型資產的中繼資料。

常見命名空間可表示為：

```text
metalake.catalog.schema.asset
```

對 table 型系統而言，asset 通常是 table；對檔案型系統而言可能是 fileset；對串流系統而言則可能是 topic。

### 實務用法

當資料平台需要跨多種儲存系統與運算引擎建立一致的中繼資料管理時，可以導入 Gravitino。

常見流程如下：

1. 建立 **metalake**，定義治理與命名空間邊界。
2. 為 Hive、Iceberg、MySQL、PostgreSQL、Kafka、fileset 等系統建立一個或多個 **catalog**。
3. 在每個 catalog 底下建立 **schema** 來組織資產。
4. 透過 REST API、Java/Python client 或支援的運算引擎 connector 管理 **table**、**fileset**、**topic** 或 **model**。
5. 讓 Trino、Spark、Flink 等運算引擎透過 Gravitino connector 探索並操作中繼資料。

REST 風格範例：

```bash
# 在既有 metalake 底下建立 fileset catalog。
curl -X POST \
  -H "Accept: application/vnd.gravitino.v1+json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "files",
    "type": "FILESET",
    "comment": "Shared file metadata",
    "properties": {
      "location": "s3://example-bucket/data"
    }
  }' \
  http://localhost:8090/api/metalakes/example/catalogs
```

Trino 使用情境範例：

```sql
SHOW CATALOGS;

CREATE SCHEMA iceberg_catalog.analytics;

CREATE TABLE iceberg_catalog.analytics.events (
  event_id varchar,
  event_time timestamp,
  payload varchar
);
```

在維運上，Gravitino 最適合作為資料平台基礎設施來管理。正式推廣前，應先定義命名規範、catalog 擁有者、驗證方式、connector 設定、儲存位置與運算引擎整合方式。

### 學習檢核表

- 理解被動式資料目錄與 Gravitino 直接中繼資料管理模式的差異。
- 熟悉階層關係：metalake、catalog、schema、table/fileset/topic/model。
- 盤點平台中需要聯邦整合的中繼資料系統。
- 閱讀 REST API 與 client library，規劃自動化方式。
- 先測試一種運算引擎整合，例如 Trino + Iceberg 或 Spark + Iceberg。
- 決定 catalog 擁有權、驗證方式與存取控制策略。
- 在生產環境使用 managed fileset 或 managed lakehouse table 前，先驗證儲存與刪除行為。

## References

- [Apache Gravitino official site](https://gravitino.apache.org/)
- [Apache Gravitino Overview](https://gravitino.apache.org/docs/1.1.0/overview)
- [Apache Gravitino REST API](https://gravitino.apache.org/docs/1.1.0/api/rest/gravitino-rest-api)
- [Manage fileset metadata using Gravitino](https://gravitino.apache.org/docs/1.1.0/manage-fileset-metadata-using-gravitino)
- [Apache Gravitino Iceberg catalog](https://gravitino.apache.org/docs/1.1.0/lakehouse-iceberg-catalog/)
- [Apache Gravitino Trino connector supported catalogs](https://gravitino.apache.org/docs/1.1.0/trino-connector/supported-catalog/)
- [Apache Gravitino Spark connector Iceberg catalog](https://gravitino.apache.org/docs/1.1.0/spark-connector/spark-catalog-iceberg)
- [Apache Gravitino Flink connector Iceberg catalog](https://gravitino.apache.org/docs/1.1.0/flink-connector/flink-catalog-iceberg/)
