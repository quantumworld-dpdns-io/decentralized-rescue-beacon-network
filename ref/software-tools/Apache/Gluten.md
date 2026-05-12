# Apache Gluten

| Field | Details |
| --- | --- |
| Project | Apache Gluten |
| Category | Apache Spark acceleration, native query execution |
| License | Apache License 2.0 |
| Primary use case | Offload Spark SQL / DataFrame execution from the JVM to native engines |
| Main backends | Velox and ClickHouse |
| Plan format | Substrait |
| Data format | Apache Arrow columnar batches |
| Current status | Apache Software Foundation top-level project |
| Latest official release noted | 1.6.0, released 2026-03-10 |

## English

### Overview

Apache Gluten is a middle layer for accelerating JVM-based SQL engines, especially Apache Spark SQL, by offloading compute-heavy query execution to native engines. Its name reflects its purpose: it "glues" Spark's distributed control flow to native execution libraries.

In Spark deployments, Gluten is typically used as a Spark plugin. Users keep their existing SQL or DataFrame logic while configuring Spark to load Gluten and a compatible backend. The goal is to preserve Spark's scheduling, fault tolerance, ecosystem integration, and APIs while moving expensive operators into faster native columnar execution.

### Why it matters

Spark is scalable and mature, but SQL execution inside the JVM can hit limits from object overhead, garbage collection, and CPU efficiency. Gluten addresses that by combining:

- Spark's distributed planning, scheduling, shuffle integration, and operational model.
- Native execution engines that use vectorized processing and columnar memory layouts.
- Apache Arrow-based columnar batches for data exchange between Spark and native code.
- Fallback behavior so unsupported operators can still run in vanilla Spark.

This makes Gluten relevant for teams that already operate Spark ETL, BI, or lakehouse workloads and want better CPU efficiency without rewriting jobs into a different SQL engine.

### Architecture/Concepts

| Concept | Role in Gluten |
| --- | --- |
| Spark plugin | Loads Gluten into Spark applications through Spark configuration. |
| Physical plan conversion | Converts Spark physical plans into Substrait plans for native execution. |
| Substrait | Provides a cross-language representation of relational operations. |
| JNI bridge | Passes execution plans and data between Spark's JVM runtime and native backends. |
| Native backend | Executes supported operators in engines such as Velox or ClickHouse. |
| Arrow columnar batch | Represents columnar data passed back to Spark through Spark's columnar APIs. |
| Columnar shuffle | Allows Gluten columnar data to participate in Spark shuffle workflows. |
| Unified memory management | Coordinates native memory allocation with Spark execution. |
| Fallback mechanism | Converts between row and columnar formats when an operator cannot be offloaded. |
| Metrics | Exposes native execution information through Spark UI for debugging and tuning. |

Typical execution flow:

1. Spark parses and optimizes SQL or DataFrame work as usual.
2. Gluten transforms supported physical plan sections into Substrait.
3. Executors pass the Substrait plan to the native backend through JNI.
4. The backend executes supported operators using native columnar processing.
5. Results return to Spark as Arrow-based columnar batches.
6. Unsupported sections fall back to Spark execution with row/columnar conversion as needed.

Backend notes:

- **Velox backend**: Uses Meta's Velox C++ execution engine for reusable, vectorized query execution components.
- **ClickHouse backend**: Uses a ClickHouse-derived native library so Spark can execute selected workloads with ClickHouse-style columnar processing.
- **Extensibility**: Gluten's design separates Spark integration from backend execution, so additional native backends can be added over time.

### Practical usage

Gluten is best approached as an infrastructure optimization project, not as a simple library import. A practical rollout usually includes:

1. **Choose the backend**
   - Use Velox for the common Spark SQL acceleration path.
   - Evaluate ClickHouse when its storage and execution model fits the workload.

2. **Match Spark and Gluten versions**
   - Download a release artifact built for the Spark version in use.
   - For production, consider building from source for the exact operating system, CPU, and dependency environment.

3. **Enable Gluten in Spark**
   - Add the Gluten JAR to driver and executor classpaths.
   - Configure Spark to load `org.apache.gluten.GlutenPlugin`.
   - Enable off-heap memory and size it explicitly.
   - Use the Gluten columnar shuffle manager when required by the selected backend and deployment mode.

4. **Validate query plans**
   - Run `EXPLAIN` on representative SQL.
   - Check for Gluten transformer nodes and fallback conversions.
   - Review executor logs for native validation or unsupported function messages.

5. **Benchmark carefully**
   - Compare against the same Spark version, cluster shape, data layout, and query set.
   - Measure end-to-end job time, CPU utilization, memory pressure, spill behavior, and failure rates.
   - Treat published speedups as workload-specific, not guaranteed.

Example configuration shape:

```bash
spark-shell \
  --conf spark.plugins=org.apache.gluten.GlutenPlugin \
  --conf spark.memory.offHeap.enabled=true \
  --conf spark.memory.offHeap.size=20g \
  --conf spark.shuffle.manager=org.apache.spark.shuffle.sort.ColumnarShuffleManager \
  --jars /path/to/gluten-velox-bundle.jar
```

Operational cautions:

- Native execution increases the importance of OS, CPU, compiler, and native dependency compatibility.
- Unsupported Spark expressions or data sources may fall back to Spark and reduce the expected gain.
- Off-heap memory must be monitored separately from JVM heap sizing.
- Release binaries are useful for evaluation, but source builds may be more reliable for production compatibility and performance.

### Learning checklist

- [ ] Understand the Spark SQL physical plan and where whole-stage execution appears.
- [ ] Learn the difference between row-based and columnar execution in Spark.
- [ ] Read the Gluten architecture overview and identify the Spark-to-Substrait-to-native path.
- [ ] Compare Velox and ClickHouse backend assumptions.
- [ ] Run a small Spark SQL query with Gluten enabled.
- [ ] Use `EXPLAIN` to confirm which operators are offloaded.
- [ ] Identify fallback nodes and their causes.
- [ ] Tune off-heap memory and watch spill behavior.
- [ ] Benchmark a representative workload before and after enabling Gluten.
- [ ] Verify release artifacts with SHA-512 hashes and signatures before production use.

## 繁體中文

### 概覽

Apache Gluten 是用來加速 JVM 型 SQL 引擎的中介層，主要應用在 Apache Spark SQL。它會把計算量大的查詢執行下推到 native engine，讓 Spark 保留既有的分散式控制流程，同時使用更有效率的原生欄式執行能力。

在 Spark 環境中，Gluten 通常以 Spark plugin 的方式啟用。使用者可以保留原本的 SQL 或 DataFrame 程式碼，只需要在 Spark 設定中載入 Gluten 與相容的 backend。這讓既有 ETL、BI、資料湖或 lakehouse 工作負載可以在較少改寫的前提下評估效能提升。

### 為什麼重要

Spark 具備成熟的分散式處理能力，但 JVM 內的 SQL 執行可能受到物件開銷、GC 壓力與 CPU 效率限制。Gluten 的價值在於結合：

- Spark 的分散式規劃、排程、shuffle 整合與操作模型。
- native engine 的向量化處理與欄式記憶體布局。
- 以 Apache Arrow 為基礎的 columnar batch，降低 JVM 與 native 之間的資料交換成本。
- fallback 機制，讓不支援下推的 operator 仍可回到原生 Spark 執行。

因此，Gluten 適合已經大量使用 Spark，但希望降低 CPU 成本、GC 壓力或提升查詢吞吐量的團隊。

### 架構/概念

| 概念 | 在 Gluten 中的角色 |
| --- | --- |
| Spark plugin | 透過 Spark 設定把 Gluten 載入 Spark application。 |
| Physical plan conversion | 將 Spark physical plan 轉成 Substrait plan，交給 native backend。 |
| Substrait | 跨語言的關聯式運算表示格式。 |
| JNI bridge | 在 Spark JVM runtime 與 native backend 之間傳遞 plan 與資料。 |
| Native backend | 使用 Velox 或 ClickHouse 等 engine 執行支援的 operator。 |
| Arrow columnar batch | 以欄式格式把結果回傳給 Spark columnar API。 |
| Columnar shuffle | 讓 Gluten 的欄式資料可以參與 Spark shuffle 流程。 |
| Unified memory management | 協調 native memory allocation 與 Spark 執行。 |
| Fallback mechanism | 當 operator 無法下推時，在 row 與 columnar 格式之間轉換並回到 Spark。 |
| Metrics | 將 native execution 指標顯示在 Spark UI，方便除錯與調校。 |

典型執行流程：

1. Spark 照常解析與最佳化 SQL 或 DataFrame 工作。
2. Gluten 將可支援的 physical plan 區段轉換成 Substrait。
3. Executor 透過 JNI 把 Substrait plan 交給 native backend。
4. Backend 使用 native columnar processing 執行支援的 operator。
5. 結果以 Arrow-based columnar batch 回到 Spark。
6. 不支援的區段透過 row/columnar 轉換 fallback 到 Spark 執行。

Backend 重點：

- **Velox backend**：使用 Meta 的 Velox C++ execution engine，提供可重用、向量化的查詢執行元件。
- **ClickHouse backend**：使用源自 ClickHouse 的 native library，讓 Spark 在特定工作負載中利用 ClickHouse 風格的欄式執行。
- **可擴充性**：Gluten 將 Spark 整合層與 backend 執行層拆開，未來可接入更多 native backend。

### 實務使用

Gluten 應被視為基礎架構層的效能最佳化，而不是單純加入一個 library。實務導入通常包含：

1. **選擇 backend**
   - 一般 Spark SQL 加速可優先評估 Velox。
   - 若工作負載與 ClickHouse 的儲存或執行模型吻合，可評估 ClickHouse backend。

2. **對齊 Spark 與 Gluten 版本**
   - 下載符合目前 Spark 版本的 release artifact。
   - 生產環境建議評估自行從 source build，以符合實際 OS、CPU 與相依套件環境。

3. **在 Spark 啟用 Gluten**
   - 將 Gluten JAR 加到 driver 與 executor classpath。
   - 設定 Spark 載入 `org.apache.gluten.GlutenPlugin`。
   - 啟用 off-heap memory 並明確設定大小。
   - 依 backend 與部署模式需求啟用 Gluten columnar shuffle manager。

4. **驗證 query plan**
   - 對代表性 SQL 執行 `EXPLAIN`。
   - 檢查 Gluten transformer node 與 fallback conversion。
   - 從 executor log 觀察 native validation 或 unsupported function 訊息。

5. **謹慎 benchmark**
   - 使用相同 Spark 版本、cluster 規格、資料布局與查詢集合比較。
   - 觀察 end-to-end job time、CPU utilization、memory pressure、spill behavior 與失敗率。
   - 將官方或公開效能數字視為特定工作負載結果，而非保證值。

設定範例：

```bash
spark-shell \
  --conf spark.plugins=org.apache.gluten.GlutenPlugin \
  --conf spark.memory.offHeap.enabled=true \
  --conf spark.memory.offHeap.size=20g \
  --conf spark.shuffle.manager=org.apache.spark.shuffle.sort.ColumnarShuffleManager \
  --jars /path/to/gluten-velox-bundle.jar
```

營運注意事項：

- native execution 對 OS、CPU、compiler 與 native dependency 相容性更敏感。
- 不支援的 Spark expression 或 data source 可能 fallback，降低預期效益。
- off-heap memory 需要和 JVM heap 分開監控。
- release binary 適合初步評估；生產環境可能需要 source build 來取得較好的相容性與效能。

### 學習檢核表

- [ ] 理解 Spark SQL physical plan，以及 whole-stage execution 出現的位置。
- [ ] 分辨 Spark row-based execution 與 columnar execution 的差異。
- [ ] 閱讀 Gluten architecture overview，掌握 Spark 到 Substrait 再到 native 的路徑。
- [ ] 比較 Velox 與 ClickHouse backend 的假設與適用情境。
- [ ] 啟用 Gluten 執行一個小型 Spark SQL query。
- [ ] 使用 `EXPLAIN` 確認哪些 operator 被 offload。
- [ ] 找出 fallback node 與 fallback 原因。
- [ ] 調整 off-heap memory 並觀察 spill behavior。
- [ ] 針對代表性 workload 比較啟用前後效能。
- [ ] 在生產使用前驗證 release artifact 的 SHA-512 hash 與 signature。

## References

- [Apache Gluten official site](https://gluten.apache.org/)
- [Apache Gluten downloads](https://gluten.apache.org/downloads/)
- [Apache Gluten GitHub repository](https://github.com/apache/gluten)
- [Apache Gluten documentation](https://gluten.apache.org/docs/latest.html)
- [Apache Gluten configuration](https://github.com/apache/gluten/blob/main/docs/Configuration.md)
- [Substrait project](https://substrait.io/)
- [Velox project](https://velox-lib.io/)
- [Apache Arrow](https://arrow.apache.org/)
- [Apache Spark plugin documentation](https://spark.apache.org/docs/latest/api/java/org/apache/spark/api/plugin/SparkPlugin.html)
