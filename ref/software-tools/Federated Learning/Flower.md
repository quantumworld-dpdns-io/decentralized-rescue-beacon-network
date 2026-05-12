# Flower (flwr)

| Field | Details |
| --- | --- |
| Category | Federated AI and federated learning framework |
| Project | Flower / `flwr` |
| License | Apache-2.0 |
| Primary use cases | Federated learning, federated analytics, cross-device training, cross-silo collaboration, edge AI experimentation |
| Core abstractions | `ServerApp`, `ClientApp`, Strategy, SuperLink, SuperNode, Messages, Records, Mods |
| ML framework support | PyTorch, TensorFlow, JAX, MLX, scikit-learn, XGBoost, fastai, PyTorch Lightning, Pandas, Transformers, and custom workloads |
| Deployment modes | Local simulation, managed local runs, multi-machine deployment runtime, Docker, Docker Compose, Helm, cloud and Kubernetes-style environments |
| Last reviewed | 2026-04-29 |

## English

### Overview

Flower is an open-source framework for building federated AI systems. It lets teams take an existing machine learning workload, split it into server-side orchestration and client-side local execution, and run collaborative training or evaluation without centralizing raw data.

The framework is intentionally ML-framework agnostic. A Flower app can use PyTorch, TensorFlow, JAX, MLX, scikit-learn, XGBoost, Transformers, Pandas, or custom code as long as the client can receive instructions, train or evaluate locally, and return model updates or metrics. This makes Flower useful for research prototypes, cross-silo pilots, mobile and edge experiments, and production-oriented federated learning deployments.

### Why it matters

Federated learning is valuable when useful data is distributed across devices, hospitals, banks, factories, regions, or business units and cannot be pooled easily because of privacy, governance, latency, cost, or ownership constraints. Flower provides a practical programming model for those cases: clients keep local data local, while the federation exchanges model parameters, metrics, or other controlled messages.

Flower also matters because federated systems need more than a training loop. Real deployments need client selection, fault tolerance, secure communication, privacy controls, aggregation strategies, simulation tooling, reproducible examples, and a path from local experiments to distributed deployments. Flower exposes these concerns as explicit concepts instead of hiding them inside a single monolithic trainer.

### Architecture/Concepts

| Concept | Role |
| --- | --- |
| Federation | The full system of one coordinating side and many participating client nodes. |
| `ServerApp` | Project-specific server-side code for selecting clients, configuring rounds, aggregating results, evaluating global state, and saving checkpoints. |
| `ClientApp` | Project-specific client-side code for local training, evaluation, preprocessing, post-processing, and returning results. |
| Strategy | The server-side algorithm for orchestration and aggregation, such as FedAvg, FedAdam, FedProx, FedMedian, Krum, Bulyan, or custom strategies. |
| SuperLink | Long-running server-side process that connects the federation, sends tasks to SuperNodes, and receives results. |
| SuperNode | Long-running client-side process that connects to the SuperLink, requests work, executes client tasks, and returns results. |
| SuperExec | Runtime process that launches and manages short-lived app processes such as `ServerApp` and `ClientApp`. |
| Messages and Records | The structured communication model used to send arrays, configs, metrics, and other data between server and clients. |
| Mods | Reusable client-side or message-processing extensions, including options for clipping, message-size checks, and local differential privacy. |
| Simulation Runtime | Runs many logical clients locally for experimentation, algorithm development, and reproducible research. |
| Deployment Runtime | Runs Flower across long-lived SuperLink and SuperNode processes for real federations and multi-run operation. |

Flower generally follows a hub-and-spoke pattern: the server coordinates work, clients perform local computation, and only task results are returned. In the current architecture, long-lived infrastructure processes handle networking and execution, while short-lived app processes contain the project logic. This separation allows multiple Flower app projects or runs to share the same federation infrastructure.

### Practical usage

Use Flower when:

- Data must remain on client devices, organizational sites, edge nodes, or regulated environments.
- You want to federate an existing ML project without rewriting the model stack.
- You need to compare FL strategies such as FedAvg, FedProx, FedAdam, robust aggregation, or custom algorithms.
- You want to simulate many clients locally before deploying across real machines.
- You need a path from notebook-scale experiments to Docker, Helm, cloud, or multi-machine deployments.

Typical workflow:

1. Install Flower in a fresh Python environment, commonly with `pip install -U "flwr[simulation]"` for local simulation work.
2. Create or adapt a Flower project with a `ClientApp`, a `ServerApp`, and shared model or task code.
3. Implement local client behavior: load local data, receive model parameters or configs, train or evaluate, and return arrays and metrics.
4. Choose or implement a server strategy for client sampling, configuration, aggregation, and evaluation.
5. Run local simulations to test correctness, convergence, client heterogeneity, failures, and metrics.
6. Move to deployment runtime when real SuperNodes need to connect to a SuperLink over the network.

Production checks:

- Treat federated learning as privacy-improving, not automatically privacy-preserving; add differential privacy, secure aggregation, TLS, authentication, and audit logging when required.
- Validate non-IID data behavior, client availability, partial participation, dropped clients, and skewed metrics.
- Pin Flower versions and confirm runtime compatibility before upgrading, especially around Message API and deployment runtime changes.
- Track model checkpoints, strategy configuration, client sampling policy, and evaluation metrics for every run.
- Keep client code minimal, observable, and safe to run in constrained edge or partner environments.

### Learning checklist

- [ ] Explain the difference between centralized learning, federated learning, and federated evaluation.
- [ ] Build a minimal Flower app with one `ServerApp` and one `ClientApp`.
- [ ] Run a local simulation with multiple logical clients.
- [ ] Use a built-in strategy such as FedAvg, then change strategy parameters.
- [ ] Add custom metrics aggregation and checkpoint saving.
- [ ] Test a non-IID data partition with Flower Datasets or a custom partitioner.
- [ ] Add a client-side Mod such as clipping or local differential privacy where appropriate.
- [ ] Understand when to use simulation runtime versus deployment runtime.
- [ ] Run a small multi-machine deployment with SuperLink and SuperNodes.
- [ ] Review secure aggregation, TLS, authentication, and audit logging options before real data use.

## 繁體中文

### 概覽

Flower 是用來建立 federated AI system 的開源框架。它讓團隊可以把既有機器學習工作負載拆成 server-side orchestration 與 client-side local execution，在不集中原始資料的情況下進行協同訓練或評估。

Flower 的設計重點是 ML framework agnostic。Flower app 可以使用 PyTorch、TensorFlow、JAX、MLX、scikit-learn、XGBoost、Transformers、Pandas 或自訂程式，只要 client 能接收指令、在本地訓練或評估，並回傳模型更新或 metrics。這讓 Flower 適合研究原型、跨組織 pilot、行動與邊緣裝置實驗，以及更接近生產環境的 federated learning 部署。

### 為什麼重要

當有價值的資料分散在裝置、醫院、銀行、工廠、地區或不同業務單位，而且因為隱私、治理、延遲、成本或資料所有權而難以集中時，federated learning 就有實務價值。Flower 提供一個可操作的 programming model：client 保留本地資料，federation 只交換模型參數、metrics 或其他受控訊息。

Flower 的重要性也在於 federated system 不只是 training loop。真實部署需要 client selection、fault tolerance、安全通訊、隱私控制、aggregation strategy、simulation tooling、可重現範例，以及從本地實驗走向分散式部署的路徑。Flower 把這些需求變成明確概念，而不是藏在單一 trainer 裡。

### 架構/概念

| 概念 | 角色 |
| --- | --- |
| Federation | 由協調端與多個 client node 組成的完整系統。 |
| `ServerApp` | 專案特定的 server-side 程式，用於選擇 client、設定 rounds、聚合結果、評估全域狀態與儲存 checkpoints。 |
| `ClientApp` | 專案特定的 client-side 程式，用於本地訓練、評估、前處理、後處理與回傳結果。 |
| Strategy | Server-side 的 orchestration 與 aggregation 演算法，例如 FedAvg、FedAdam、FedProx、FedMedian、Krum、Bulyan 或自訂策略。 |
| SuperLink | 長時間執行的 server-side process，負責連接 federation、向 SuperNode 發送任務並接收結果。 |
| SuperNode | 長時間執行的 client-side process，負責連到 SuperLink、取得工作、執行 client task 並回傳結果。 |
| SuperExec | Runtime process，用來啟動與管理 `ServerApp`、`ClientApp` 等短生命週期 app process。 |
| Messages and Records | Server 與 client 之間傳遞 arrays、configs、metrics 與其他資料的結構化通訊模型。 |
| Mods | 可重用的 client-side 或 message-processing extension，包含 clipping、message-size checks 與 local differential privacy 等選項。 |
| Simulation Runtime | 在本機執行多個邏輯 client，用於實驗、演算法開發與可重現研究。 |
| Deployment Runtime | 透過長時間執行的 SuperLink 與 SuperNode，在真實 federation 與 multi-run 情境中運作。 |

Flower 通常採用 hub-and-spoke 模式：server 協調工作，client 執行本地計算，最後只回傳任務結果。在目前架構中，長生命週期的 infrastructure process 處理網路與執行，短生命週期的 app process 承載專案邏輯。這種分離讓多個 Flower app project 或 run 可以共享同一組 federation infrastructure。

### 實務使用

適合使用 Flower 的情境：

- 資料必須留在 client device、組織據點、edge node 或受監管環境。
- 想 federate 既有 ML 專案，而不重寫整個模型技術棧。
- 需要比較 FedAvg、FedProx、FedAdam、robust aggregation 或自訂 FL strategy。
- 想先在本機模擬大量 clients，再部署到真實機器。
- 需要從 notebook 等級實驗走到 Docker、Helm、cloud 或 multi-machine deployment。

典型流程：

1. 在新的 Python environment 安裝 Flower；本地 simulation 常用 `pip install -U "flwr[simulation]"`。
2. 建立或調整 Flower project，包含 `ClientApp`、`ServerApp` 與共用 model/task code。
3. 實作 client 本地行為：載入本地資料、接收 model parameters 或 configs、訓練或評估，並回傳 arrays 與 metrics。
4. 選擇或實作 server strategy，處理 client sampling、configuration、aggregation 與 evaluation。
5. 執行 local simulation，測試正確性、收斂、client heterogeneity、失敗情境與 metrics。
6. 當真實 SuperNode 需要透過網路連接 SuperLink 時，再移到 deployment runtime。

生產檢查：

- 將 federated learning 視為改善隱私風險的架構，而不是自動保證隱私；必要時加入 differential privacy、secure aggregation、TLS、authentication 與 audit logging。
- 驗證 non-IID data、client availability、partial participation、dropped clients 與偏斜 metrics 的行為。
- 固定 Flower 版本並在升級前確認 runtime 相容性，特別是 Message API 與 deployment runtime 的變更。
- 為每次 run 追蹤 model checkpoint、strategy configuration、client sampling policy 與 evaluation metrics。
- 讓 client code 維持精簡、可觀測，並適合在受限 edge 或合作夥伴環境中執行。

### 學習檢核表

- [ ] 說明 centralized learning、federated learning 與 federated evaluation 的差異。
- [ ] 建立一個最小 Flower app，包含一個 `ServerApp` 與一個 `ClientApp`。
- [ ] 用多個 logical clients 執行 local simulation。
- [ ] 使用 FedAvg 等內建 strategy，並調整 strategy 參數。
- [ ] 加入自訂 metrics aggregation 與 checkpoint saving。
- [ ] 使用 Flower Datasets 或自訂 partitioner 測試 non-IID data partition。
- [ ] 在適合情境加入 clipping 或 local differential privacy 等 client-side Mod。
- [ ] 理解何時使用 simulation runtime，何時使用 deployment runtime。
- [ ] 以 SuperLink 與 SuperNodes 執行小型 multi-machine deployment。
- [ ] 在使用真實資料前檢查 secure aggregation、TLS、authentication 與 audit logging 選項。

## References

- [Flower documentation overview](https://flower.ai/docs/)
- [Flower Framework documentation](https://flower.ai/docs/framework/)
- [Flower Architecture](https://flower.ai/docs/framework/explanation-flower-architecture.html)
- [Get started with Flower](https://flower.ai/docs/framework/tutorial-series-get-started-with-flower-pytorch.html)
- [Install Flower](https://flower.ai/docs/framework/how-to-install-flower.html)
- [Secure Aggregation Protocols](https://flower.ai/docs/framework/explanation-ref-secure-aggregation-protocols.html)
- [Flower GitHub repository](https://github.com/adap/flower)
