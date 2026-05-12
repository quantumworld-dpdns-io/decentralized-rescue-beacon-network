# Apache Polaris

| Field | Details |
| --- | --- |
| Project | Apache Polaris |
| Category | Lakehouse catalog / Apache Iceberg REST catalog |
| License | Apache License 2.0 |
| Governance | Apache Software Foundation Top-Level Project |
| Primary use case | Centralized catalog, metadata, and access control for Apache Iceberg tables across multiple engines |
| Common engines | Apache Spark, Apache Flink, Trino, Apache Doris, StarRocks, Dremio OSS, Snowflake integrations, and other Iceberg REST-compatible clients |
| Storage targets | Object storage such as Amazon S3, Azure Storage, and Google Cloud Storage |
| Official site | <https://polaris.apache.org/> |

## English

### Overview

Apache Polaris is an open source catalog for Apache Iceberg tables. It implements the Apache Iceberg REST catalog API so query engines can discover, create, read, and write Iceberg tables through a shared catalog interface instead of binding every engine to a proprietary metastore.

Polaris is designed for open lakehouse architectures: data and Iceberg metadata remain in object storage, while Polaris provides the catalog layer that tracks tables, namespaces, current metadata pointers, security policies, and service identities. Apache Polaris announced its graduation to an Apache Top-Level Project in February 2026, and the Apache Software Foundation later announced Apache Gluten and Apache Polaris together as Top-Level Projects in March 2026.

### Why it matters

Polaris matters because a table format alone is not enough to make a lakehouse interoperable. Apache Iceberg standardizes table metadata and file layout, but engines still need a consistent way to find tables, commit metadata changes atomically, and apply access controls. The Iceberg REST catalog protocol gives the ecosystem that shared control-plane API, and Polaris provides an open implementation of it.

For data platform teams, this reduces catalog lock-in. Spark, Flink, Trino, Snowflake-connected workflows, and other compatible engines can operate on the same Iceberg tables without copying data into separate silos. Polaris also centralizes policy management so access can be reasoned about at the catalog, namespace, and table levels.

### Architecture/Concepts

- **Catalog**: A top-level Polaris resource that organizes Iceberg tables. Internal catalogs are managed by Polaris and support read/write workflows. External catalogs are managed elsewhere and can be synced into Polaris for read-oriented access patterns.
- **Namespace**: A logical grouping inside a catalog. Namespaces can be nested and are used to organize Iceberg tables in a structure similar to databases and schemas.
- **Iceberg table**: The actual analytical table whose data files, metadata files, manifests, and snapshots live in object storage. Polaris tracks and governs the table through the catalog API.
- **Metadata pointer**: The catalog mapping from a table name to the current Iceberg metadata file. Updating this pointer atomically is central to Iceberg's commit model.
- **Storage configuration**: The cloud storage settings associated with a catalog, including locations and provider-specific identity details for S3, Azure, or GCS.
- **Service principal**: A machine identity used by engines and integrations to authenticate to Polaris.
- **RBAC model**: Polaris uses role-based access control with principal roles and catalog roles to grant privileges over catalogs, namespaces, and tables.
- **Credential vending**: Polaris can issue temporary storage credentials to query engines so engines can access table data without long-lived direct credentials to the storage layer.
- **APIs**: Polaris exposes management APIs for catalog administration and catalog APIs compatible with the Iceberg REST catalog specification.

### Practical usage

Use Polaris when you want a vendor-neutral catalog for Iceberg tables shared by multiple engines. A typical workflow is:

1. Deploy Polaris locally, in containers, on Kubernetes, or through a managed service built around Polaris.
2. Configure persistence and storage access for the target object store.
3. Create a catalog and one or more namespaces.
4. Create service principals for engines such as Spark, Flink, or Trino.
5. Grant catalog and namespace privileges through Polaris RBAC.
6. Configure each engine to use the Polaris Iceberg REST catalog endpoint.
7. Create or register Iceberg tables and let engines read and write through the shared catalog.

Polaris is especially useful when a platform needs Snowflake plus open-source engines, or several open engines, to work against one Iceberg lakehouse with consistent metadata and security controls.

### Learning checklist

- Understand the difference between an Iceberg table format and an Iceberg catalog.
- Read the Apache Iceberg REST catalog specification at a high level.
- Learn how Polaris models catalogs, namespaces, tables, service principals, principal roles, and catalog roles.
- Practice creating a catalog backed by S3, Azure Storage, GCS, or a local-compatible object store such as MinIO.
- Connect at least one engine, such as Apache Spark or Trino, through the REST catalog endpoint.
- Test table creation, reads, writes, and permission failures across two different identities.
- Review credential vending and storage IAM requirements before using Polaris in production.

## 繁體中文

### 概覽

Apache Polaris 是 Apache Iceberg 表格的開源 Catalog。它實作 Apache Iceberg REST catalog API，讓查詢引擎能透過共同的 Catalog 介面探索、建立、讀取與寫入 Iceberg 表格，而不是讓每個引擎綁定各自的專有 metastore。

Polaris 的定位是開放式 lakehouse 架構中的 Catalog 層：資料檔案與 Iceberg metadata 保留在物件儲存中，Polaris 則負責表格、namespace、目前 metadata pointer、安全政策與服務身分的管理。Apache Polaris 於 2026 年 2 月宣布畢業成為 Apache Top-Level Project；Apache Software Foundation 隨後於 2026 年 3 月將 Apache Gluten 與 Apache Polaris 一併公告為 Top-Level Projects。

### 為什麼重要

Polaris 的重要性在於，只有表格格式並不足以完成 lakehouse 的互通性。Apache Iceberg 標準化了表格 metadata 與檔案配置，但各個引擎仍然需要一致的方法來找到表格、原子性提交 metadata 變更，並套用存取控制。Iceberg REST catalog protocol 提供共同的控制平面 API，而 Polaris 則是這個 API 的開源實作。

對資料平台團隊來說，Polaris 可以降低 Catalog 鎖定風險。Spark、Flink、Trino、與 Snowflake 整合的流程，以及其他相容 Iceberg REST 的客戶端，都可以操作同一份 Iceberg 表格，不需要把資料複製到不同平台。Polaris 也能集中管理權限，讓 catalog、namespace 與 table 層級的存取控制更容易審計與維運。

### 架構/概念

- **Catalog**：Polaris 中組織 Iceberg 表格的最上層資源。Internal catalog 由 Polaris 管理並支援讀寫；external catalog 則由其他 Iceberg catalog provider 管理，可同步到 Polaris 供特定讀取情境使用。
- **Namespace**：Catalog 內的邏輯分組，可巢狀化，用來組織 Iceberg 表格，概念上接近 database 或 schema。
- **Iceberg table**：實際的分析表格；資料檔、metadata 檔、manifest 與 snapshot 存放在物件儲存中，Polaris 透過 Catalog API 追蹤與治理這些表格。
- **Metadata pointer**：Catalog 將表格名稱對應到目前 Iceberg metadata file 的指標。原子性更新此指標是 Iceberg commit model 的核心。
- **Storage configuration**：Catalog 對應的雲端儲存設定，包含 S3、Azure 或 GCS 的位置與身分設定。
- **Service principal**：引擎或整合服務連線到 Polaris 時使用的機器身分。
- **RBAC model**：Polaris 使用 role-based access control，透過 principal role 與 catalog role 管理 catalog、namespace 與 table 權限。
- **Credential vending**：Polaris 可發放暫時性的儲存存取憑證給查詢引擎，避免引擎長期持有底層儲存憑證。
- **APIs**：Polaris 提供管理 Catalog 的 management APIs，以及相容 Iceberg REST catalog specification 的 catalog APIs。

### 實務使用

當你需要為多個引擎共享的 Iceberg 表格建立中立、開放的 Catalog 時，可以使用 Polaris。典型流程如下：

1. 在本機、container、Kubernetes，或以 Polaris 為基礎的託管服務中部署 Polaris。
2. 設定 persistence 與目標物件儲存的存取方式。
3. 建立 catalog 與一個或多個 namespace。
4. 為 Spark、Flink、Trino 等引擎建立 service principal。
5. 透過 Polaris RBAC 授予 catalog 與 namespace 權限。
6. 將各引擎設定為使用 Polaris 的 Iceberg REST catalog endpoint。
7. 建立或註冊 Iceberg 表格，讓不同引擎透過共享 Catalog 進行讀寫。

Polaris 特別適合需要 Snowflake 與開源引擎共用 Iceberg lakehouse，或需要多個開源引擎在一致 metadata 與安全控制下操作同一份資料的平台。

### 學習檢核表

- 理解 Iceberg table format 與 Iceberg catalog 的差異。
- 先高層次讀懂 Apache Iceberg REST catalog specification。
- 熟悉 Polaris 如何建模 catalog、namespace、table、service principal、principal role 與 catalog role。
- 練習建立以 S3、Azure Storage、GCS，或 MinIO 這類本機相容物件儲存為後端的 catalog。
- 至少連接一個引擎，例如 Apache Spark 或 Trino，並透過 REST catalog endpoint 操作表格。
- 使用兩個不同身分測試建表、讀取、寫入與權限失敗情境。
- 在正式環境使用前，檢查 credential vending 與儲存 IAM 設定。

## References

- [Apache Polaris official documentation](https://polaris.apache.org/docs/)
- [Apache Polaris GitHub repository](https://github.com/apache/polaris)
- [Apache Polaris 1.4.0 documentation overview](https://polaris.apache.org/releases/1.4.0/)
- [Apache Software Foundation: Apache Gluten and Apache Polaris Become Top-Level Projects](https://news.apache.org/foundation/entry/the-apache-software-foundation-graduates-two-open-source-projects-from-incubator)
- [Snowflake: Polaris Catalog Is Now Open Source](https://www.snowflake.com/en/blog/polaris-catalog-open-source/)
- [Snowflake: Introducing Polaris Catalog](https://www.snowflake.com/en/blog/introducing-polaris-catalog/)
- [Apache Iceberg REST catalog specification](https://iceberg.apache.org/rest-catalog-spec/)
