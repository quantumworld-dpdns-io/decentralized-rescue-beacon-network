# Redis Software Success Program

| Metadata | Details |
|:--|:--|
| Document purpose | Bilingual guide for understanding, planning, and operating a Redis Software Success Program. |
| Audience | Platform engineers, application developers, SREs, architects, technical account teams, and customer success teams. |
| Scope | Success roles, program components, production readiness, operational checks, and learning outcomes for Redis and Redis Enterprise environments. |
| Products referenced | Redis, Redis Enterprise Software, Redis Enterprise Cloud concepts where applicable. |
| Recommended use | Use as a workshop handout, onboarding checklist, and pre-production readiness review guide. |
| Last reviewed | 2026-04-29 |

## English

### Overview

The Redis Software Success Program is designed to help teams reach production success with Redis through three outcomes: speed, simplicity, and confidence. It combines customer success guidance, technical support, architecture review, production readiness practices, and hands-on learning so that teams can move from onboarding to stable operations with fewer surprises.

The program should not be treated as a one-time kickoff. It works best as a lifecycle model:

- **Onboard** the team, environment, access model, and initial workloads.
- **Validate** the architecture, security posture, performance baseline, and failure behavior before launch.
- **Operate** Redis with observability, backup validation, incident playbooks, and upgrade discipline.
- **Optimize** data models, client behavior, cost, memory usage, and scaling strategy as usage grows.

Successful Redis adoption depends on both software configuration and team behavior. A fast database can still fail in production if client retries are uncontrolled, backups are never restored, keys grow without bounds, or no one owns alerts. The success program turns those risks into explicit work items.

### Program Components

The program is usually delivered through a shared team model. Exact roles vary by contract and organization, but the responsibilities are consistent.

| Component | Primary responsibilities |
|:--|:--|
| Customer Success Engineer (CSE) | Leads onboarding, reviews configuration, helps troubleshoot technical issues, and shares Redis implementation practices. |
| 24/7 support | Handles urgent incidents, service-impacting issues, and break/fix escalation paths. |
| Technical Account Manager (TAM) | For larger accounts, provides proactive architecture review, performance tuning guidance, capacity planning, and upgrade coordination. |
| Customer Success Manager (CSM) | Aligns Redis adoption with business goals, success metrics, renewal health, and value realization. |
| Professional Services | Supports deeper engagements such as migrations, architecture assessments, performance optimization, automation, and custom training. |
| Customer delivery team | Owns application changes, infrastructure changes, release planning, testing evidence, and day-two operations. |

Core program activities include:

- **Discovery and workload mapping**: Identify applications, Redis databases, traffic patterns, latency targets, data structures, persistence needs, and availability requirements.
- **Architecture review**: Confirm cluster topology, shard count, replica placement, network paths, persistence, backup location, and disaster recovery assumptions.
- **Security review**: Validate authentication, authorization, TLS, network isolation, secrets handling, audit logging, and least-privilege access.
- **Performance readiness**: Establish baselines for throughput, latency, memory, key growth, eviction behavior, and client connection behavior.
- **Operational enablement**: Build dashboards, alerts, runbooks, incident contacts, maintenance windows, and upgrade procedures.
- **Knowledge transfer**: Train engineers on data modeling, anti-patterns, failure handling, and Redis Enterprise operational tools.

### Production Readiness

Production readiness means the Redis environment has been tested, observed, secured, and owned before real users depend on it. The following checklist can be used for a launch review.

| Category | Readiness standard |
|:--|:--|
| Security | Authentication is enabled; RBAC or ACLs are defined; TLS is configured where required; Redis is isolated from untrusted networks; firewall rules are explicit; secrets are not embedded in source code; audit logs are centralized. |
| Observability | Metrics, logs, and alerts are configured; dashboards exist for traffic, errors, latency, memory, persistence, replication, and cluster health; alert owners and response expectations are documented. |
| Architecture | Topology matches availability goals; replicas and shards are sized correctly; persistence is configured intentionally; capacity headroom is defined; deployment spans appropriate failure domains such as multiple availability zones where supported. |
| Performance | Load testing has been completed with realistic payloads and clients; p50, p95, and p99 latency targets are known; memory fragmentation, key size, command mix, and throughput limits have been reviewed. |
| High availability | Replication and failover behavior have been tested; quorum requirements are understood; backups are automated and restore-tested; maintenance and upgrade procedures avoid unnecessary downtime. |
| Client integration | Connection pools are bounded; timeouts are explicit; retry logic uses backoff and does not amplify incidents; error handling is tested; client-side caching is considered where appropriate. |
| Data modeling | Data structures match access patterns; large keys and hot keys are identified; TTL strategy is defined for cache workloads; key naming conventions are documented. |
| Operations | Runbooks exist for failover, restore, scaling, certificate rotation, upgrade, alert response, and support escalation. |

Important implementation notes:

- Avoid `KEYS` in production because it can block Redis while scanning the keyspace. Use `SCAN` or application-maintained indexes instead.
- Treat large keys as production risks. Split very large strings, hashes, lists, sets, sorted sets, or JSON documents into smaller units aligned to access patterns.
- Treat hot keys as scaling risks. Use better sharding, request coalescing, client-side caching, or data model changes to reduce concentrated load.
- Configure TTLs for cache data so memory can be reclaimed predictably.
- Replication is not disaster recovery by itself. Accidental deletes, bad writes, and corruption can replicate quickly, so independent backups and restore tests are required.
- Hybrid persistence can combine RDB-style fast restart characteristics with AOF-style durability goals, but the final mode should match recovery point and recovery time requirements.

### Operations Checklist

Use this checklist before launch and repeat it during major releases, traffic changes, or Redis version upgrades.

| Area | Checklist |
|:--|:--|
| Installation | Confirm operating system prerequisites, kernel parameters, file descriptor limits, disk layout, DNS behavior, and required ports. On Ubuntu, check for conflicts with `systemd-resolved` when Redis Enterprise components require port 53. |
| Automation | Prefer repeatable installation and configuration through scripts or infrastructure as code. If using `install.sh`, document parameters such as `-y` and store evidence of the installed version. |
| Upgrade strategy | Plan rolling upgrades one node at a time, validating cluster and shard health before continuing. For Redis Enterprise, consider replace-node or extra-node approaches when resource constraints or risk profile require them. |
| Security operations | Review RBAC or ACL assignments; rotate credentials and certificates on a schedule; restrict access through private networking, firewall policy, VPC peering, or equivalent private connectivity. |
| Observability operations | Track RED-style signals: requests, errors, and duration. Include cache hit rate, failed commands, timeouts, evictions, memory pressure, replication lag, and p50/p95/p99 latency. |
| Backup and restore | Store backups away from the primary cluster, such as object storage. Test restores in non-production and record recovery time, recovery point, and any manual steps. |
| High availability | Use an odd number of nodes and failure domains where quorum-based decisions apply. Validate failover behavior and document expected client impact. |
| Support readiness | Know how to generate a support package from the UI or tools such as `log_collector`. Keep cluster identifiers, versions, recent changes, and incident timelines ready for escalation. |
| Administrative tools | Use Redis Enterprise tools such as `rladmin` for status checks and controlled administrative actions. Example checks include `rladmin status extra all`; failover commands such as `rladmin failover shard` should be restricted to trained operators. |
| Evidence | Store architecture diagrams, test results, dashboard screenshots, backup restore logs, upgrade plans, and launch approvals in a shared location. |

Readiness scoring can help teams make go/no-go decisions:

| Score | Meaning |
|:--|:--|
| A | Automated, tested, documented, and owned. |
| B | Implemented and documented, with limited manual steps or partial test evidence. |
| C | Partially implemented, not fully tested, or dependent on undocumented operator knowledge. |
| D | Missing, high risk, or unsuitable for production. |

Security and high availability gaps should normally be treated as launch blockers.

### Learning Checklist

By the end of the program, participants should be able to:

- Explain the business-critical workloads that depend on Redis and their latency, availability, and durability requirements.
- Choose Redis data structures based on access patterns, memory behavior, and update semantics.
- Use hashes for compact flat objects, sorted sets for ranking and score-based queries, HyperLogLog for approximate cardinality, and RedisJSON for nested documents requiring partial updates.
- Identify Redis anti-patterns such as `KEYS` in production, unbounded cache growth, large keys, hot keys, excessive connection counts, and uncontrolled retries.
- Interpret RED metrics: requests, errors, and duration.
- Read operational dashboards for memory, latency, evictions, replication, persistence, and cluster health.
- Describe the difference between replication, high availability, backup, and disaster recovery.
- Execute or rehearse incident runbooks for failover, restore, scaling, and support escalation.
- Participate in a production readiness review using evidence instead of assumptions.
- Own follow-up actions with a named owner, due date, implementation plan, and verification method.

## 繁體中文

### 概覽

Redis Software Success Program 的目標，是協助團隊以更快、更簡單且更有把握的方式，將 Redis 導入正式生產環境。此計畫結合客戶成功支援、技術支援、架構檢視、生產就緒檢核與實作型學習，讓團隊從上線準備到穩定營運都能有明確方法。

此計畫不應只被視為一次性的啟動會議，而應作為完整生命週期模型：

- **上線導入**：建立團隊分工、環境、存取權限與初始工作負載。
- **上線前驗證**：確認架構、安全、效能基準與故障行為。
- **日常營運**：建立可觀測性、備份驗證、事件處理手冊與升級紀律。
- **持續最佳化**：隨著使用量成長，調整資料模型、客戶端行為、成本、記憶體使用與擴展策略。

Redis 的成功導入不只取決於軟體設定，也取決於團隊的操作方式。即使資料庫本身速度很快，若客戶端重試失控、備份從未驗證還原、鍵值無限制成長，或告警沒有人負責，仍可能在生產環境中失敗。Success Program 的價值，就是把這些風險轉化為可追蹤、可執行、可驗證的工作項目。

### 計畫組成

此計畫通常由多個角色共同交付。實際角色名稱會依合約與組織而不同，但責任範圍大致如下。

| 組成項目 | 主要責任 |
|:--|:--|
| 客戶成功工程師（CSE） | 主導上線導入、檢視設定、協助疑難排解，並分享 Redis 實作最佳實務。 |
| 24/7 支援服務 | 處理緊急事件、服務影響問題與 break/fix 升級支援。 |
| 技術客戶經理（TAM） | 針對大型帳戶提供主動式架構檢視、效能調校、容量規劃與升級協調。 |
| 客戶成功經理（CSM） | 將 Redis 採用情況與業務目標、成功指標、續約健康度與投資價值對齊。 |
| 專業服務（Professional Services） | 支援遷移、架構評估、效能最佳化、自動化與客製化培訓等深度專案。 |
| 客戶交付團隊 | 負責應用程式變更、基礎設施變更、發布計畫、測試證據與第二天營運。 |

核心活動包括：

- **需求探索與工作負載盤點**：辨識應用程式、Redis 資料庫、流量模式、延遲目標、資料結構、持久化需求與可用性要求。
- **架構檢視**：確認叢集拓撲、分片數量、副本配置、網路路徑、持久化、備份位置與災難恢復假設。
- **安全檢視**：驗證身分驗證、授權、TLS、網路隔離、密鑰管理、稽核日誌與最小權限原則。
- **效能就緒**：建立吞吐量、延遲、記憶體、鍵值成長、逐出行為與客戶端連線行為的基準。
- **營運賦能**：建立儀表板、告警、操作手冊、事件聯絡窗口、維護時段與升級流程。
- **知識移轉**：訓練工程團隊理解資料建模、反模式、故障處理與 Redis Enterprise 營運工具。

### 生產就緒

生產就緒代表 Redis 環境在正式承載使用者前，已完成測試、監控、安全防護與責任歸屬。下表可作為上線審查檢查清單。

| 類別 | 就緒標準 |
|:--|:--|
| 安全性 | 已啟用身分驗證；已定義 RBAC 或 ACL；必要時已設定 TLS；Redis 與不受信任網路隔離；防火牆規則明確；密鑰未寫入原始碼；稽核日誌已集中管理。 |
| 可觀測性 | 已設定指標、日誌與告警；具備流量、錯誤、延遲、記憶體、持久化、複製與叢集健康狀態儀表板；告警負責人與回應期待已文件化。 |
| 架構 | 拓撲符合可用性目標；副本與分片容量合適；持久化設定有明確理由；已定義容量餘裕；在支援情境下跨多個可用區等故障域部署。 |
| 效能 | 已使用接近真實的 payload 與客戶端進行負載測試；已掌握 p50、p95、p99 延遲目標；已檢視記憶體碎片、鍵值大小、命令組合與吞吐限制。 |
| 高可用性 | 已測試複製與容錯移轉行為；理解 quorum 要求；備份已自動化且完成還原測試；維護與升級流程避免不必要停機。 |
| 客戶端整合 | 連線池有上限；逾時設定明確；重試邏輯具備退避機制且不會放大事故；錯誤處理已測試；已評估是否適合使用客戶端快取。 |
| 資料建模 | 資料結構符合存取模式；已辨識大鍵與熱鍵；快取工作負載已定義 TTL 策略；鍵命名慣例已文件化。 |
| 營運 | 已建立容錯移轉、還原、擴展、憑證輪替、升級、告警處理與支援升級的操作手冊。 |

重要實作提醒：

- 生產環境應避免使用 `KEYS`，因為它可能在掃描 keyspace 時阻塞 Redis。請改用 `SCAN` 或由應用程式維護索引。
- 大鍵應視為生產風險。過大的 string、hash、list、set、sorted set 或 JSON 文件應依存取模式拆分為較小單位。
- 熱鍵是擴展風險。可透過更合適的分片、請求合併、客戶端快取或資料模型調整降低集中負載。
- 快取資料應設定 TTL，讓記憶體能以可預期方式回收。
- 複製本身不等於災難恢復。誤刪、錯誤寫入與資料毀損可能快速同步到副本，因此仍需要獨立備份與還原測試。
- Hybrid 持久化可結合 RDB 類型的快速啟動特性與 AOF 類型的資料耐久性目標，但最終模式應依 RPO 與 RTO 要求決定。

### 營運檢查清單

此清單適用於上線前，也應在重大發布、流量變化或 Redis 版本升級時重新檢視。

| 領域 | 檢查項目 |
|:--|:--|
| 安裝 | 確認作業系統前置需求、核心參數、檔案描述子限制、磁碟配置、DNS 行為與必要連接埠。在 Ubuntu 上，若 Redis Enterprise 元件需要使用 53 號連接埠，需檢查是否與 `systemd-resolved` 衝突。 |
| 自動化 | 優先使用腳本或基礎設施即程式碼完成可重複的安裝與設定。若使用 `install.sh`，需記錄 `-y` 等參數並保存安裝版本證據。 |
| 升級策略 | 規劃一次升級一個節點的滾動升級，並在繼續下一節點前驗證叢集與分片健康狀態。使用 Redis Enterprise 時，可依資源限制與風險選擇 replace-node 或 extra-node 方法。 |
| 安全營運 | 定期檢視 RBAC 或 ACL；排程輪替憑證與密碼；透過私有網路、防火牆政策、VPC peering 或等效私密連線限制存取。 |
| 可觀測性營運 | 追蹤 RED 類型訊號：requests、errors、duration。應包含快取命中率、失敗命令、逾時、逐出、記憶體壓力、複製延遲與 p50/p95/p99 延遲。 |
| 備份與還原 | 將備份存放於主要叢集之外，例如物件儲存。定期在非生產環境測試還原，並記錄 RTO、RPO 與人工步驟。 |
| 高可用性 | 在需要 quorum 決策的情境中，使用奇數節點與奇數故障域。驗證容錯移轉行為並記錄預期客戶端影響。 |
| 支援就緒 | 知道如何透過 UI 或 `log_collector` 等工具產生支援包。升級支援時需準備叢集識別資訊、版本、近期變更與事件時間線。 |
| 管理工具 | 使用 Redis Enterprise 工具如 `rladmin` 進行狀態檢查與受控管理操作。常見檢查包含 `rladmin status extra all`；如 `rladmin failover shard` 等容錯移轉命令應僅由受訓操作人員執行。 |
| 證據 | 將架構圖、測試結果、儀表板截圖、備份還原紀錄、升級計畫與上線核准存放於共享位置。 |

可使用下列評分協助 go/no-go 決策：

| 分數 | 意義 |
|:--|:--|
| A | 已自動化、已測試、已文件化，且有明確負責人。 |
| B | 已實作並文件化，但仍有少量人工步驟或測試證據不完整。 |
| C | 部分實作、尚未完整測試，或仰賴未文件化的操作人員知識。 |
| D | 缺失、高風險，或不適合進入生產環境。 |

安全性與高可用性缺口通常應視為上線阻礙。

### 學習檢核表

完成此計畫後，參與者應能夠：

- 說明依賴 Redis 的關鍵業務工作負載，以及其延遲、可用性與耐久性需求。
- 根據存取模式、記憶體行為與更新語意選擇 Redis 資料結構。
- 使用 hash 儲存精簡的扁平物件，使用 sorted set 支援排行榜與分數範圍查詢，使用 HyperLogLog 進行近似基數估計，並在需要巢狀文件與局部更新時使用 RedisJSON。
- 辨識 Redis 反模式，例如在生產環境使用 `KEYS`、快取無限制成長、大鍵、熱鍵、連線數過多與失控重試。
- 解讀 RED 指標：requests、errors、duration。
- 閱讀記憶體、延遲、逐出、複製、持久化與叢集健康狀態儀表板。
- 說明複製、高可用性、備份與災難恢復之間的差異。
- 執行或演練容錯移轉、還原、擴展與支援升級的事件處理手冊。
- 使用證據而非假設參與生產就緒審查。
- 以負責人、截止日期、實作計畫與驗證方式追蹤後續工作。

## References

- Redis Documentation: https://redis.io/docs/latest/
- Redis Enterprise Software documentation: https://redis.io/docs/latest/operate/rs/
- Redis command reference: https://redis.io/docs/latest/commands/
- Redis observability guidance: https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/monitoring/
- Redis persistence documentation: https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
- Redis anti-patterns: https://redis.io/learn/howtos/antipatterns
