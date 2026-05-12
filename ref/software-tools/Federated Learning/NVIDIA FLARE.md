# NVIDIA FLARE

| Field | Details |
| --- | --- |
| Category | Federated learning application runtime and SDK |
| Full name | NVIDIA Federated Learning Application Runtime Environment |
| Primary use | Build, simulate, deploy, and operate privacy-preserving multi-party ML, DL, XGBoost, and LLM fine-tuning workflows |
| Typical users | Data scientists, ML engineers, research consortia, healthcare AI teams, financial-services AI teams, platform/security teams |
| Frameworks | PyTorch, TensorFlow, XGBoost, scikit-learn, NVIDIA NeMo, Hugging Face workflows, Flower integration, and Python-based custom trainers |
| Key interfaces | Client API, Job Recipe API, FL Simulator, FLARE API, CLI tools, dashboard, admin client |
| Best fit | Cross-silo and regulated collaborations where data must stay with each institution but model updates can be coordinated securely |
| Current note | NVIDIA's current documentation highlights FLARE 2.7.x capabilities, while the cited 2024 technical blogs focus on FLARE 2.4 features such as the simplified Client API and large-object streaming. |
| Last reviewed | 2026-04-29 |

## English

### Overview

NVIDIA FLARE is an open-source, domain-agnostic Python SDK for federated learning. It lets multiple sites collaboratively train or evaluate models while keeping raw data local to each client. A server or workflow coordinator distributes work, clients train or evaluate on local data, and only model parameters, updates, metrics, or approved artifacts are returned for aggregation.

FLARE is aimed at practical federated AI rather than only research experiments. It supports local simulation, cross-silo production deployments, secure provisioning, site-level policies, privacy filters, auditability, and deployment patterns for Docker, Kubernetes, cloud, and edge environments. It also includes specific support for large models and LLM adaptation, including federated supervised fine-tuning, parameter-efficient fine-tuning, message quantization, memory-management guidance, tensor downloading, and file streaming.

### Why it matters

- Sensitive datasets are often locked inside hospitals, banks, governments, manufacturers, or regional business units.
- Centralizing that data can be blocked by privacy law, governance policy, data residency, commercial sensitivity, or sheer data size.
- Federated learning brings training to the data: sites keep local records, train locally, and share controlled updates instead of raw data.
- Combining updates from diverse sites can improve robustness and reduce site-specific bias compared with isolated local training.
- Production FL needs more than an algorithm: it needs identity, authorization, provisioning, monitoring, audit logs, privacy controls, deployment tooling, and repeatable job definitions.
- LLM fine-tuning makes transport and memory harder because full-model SFT may involve very large artifacts; PEFT methods such as LoRA reduce the amount of trainable data that must be exchanged.

### Architecture/Concepts

| Concept | Role |
| --- | --- |
| FL server | Coordinates jobs, rounds, aggregation, model distribution, and system control. |
| Client/site | Runs local training or evaluation against local data and returns approved updates or metrics. |
| Global model | The shared model state distributed to sites and updated through aggregation. |
| Local update | Parameters, gradients, weight differences, adapter weights, metrics, or metadata produced by a site. |
| Aggregator | Combines client updates using algorithms such as FedAvg or other configured strategies. |
| Controller/workflow | Defines job flow, task assignment, aggregation timing, validation, and lifecycle behavior. |
| Executor/trainer | Runs site-side application code, often wrapping existing ML training scripts. |
| Client API | Lightweight API for adapting existing Python training code with operations such as initialize, receive, train, package an `FLModel`, and send. |
| Job Recipe API | Higher-level recipe interface for common workflows such as FedAvg, FedOpt, SCAFFOLD, cyclic training, XGBoost, and framework-specific jobs. |
| FL Simulator | Runs federated jobs locally for development before deploying to real sites. |
| Provisioning | Generates deployment artifacts, identities, and certificates for secure multi-party operation. |
| Policies and filters | Enforce site-specific authorization, privacy, validation, and transformation rules on exchanged data. |
| Large-model support | File streaming, tensor download, message quantization, and memory practices for large model and LLM workflows. |
| Confidential AI | Uses trusted execution environments and confidential computing patterns where stronger protection of code, data, or model IP is required. |
| Hierarchical FL / Edge | Scales beyond simple server-client topologies through tiered architectures and edge/mobile support. |

Federated learning patterns in FLARE include horizontal FL, where sites have different samples with similar features; vertical FL, where parties hold different features for overlapping records; swarm or decentralized styles; cross-silo collaboration among organizations; and edge/mobile deployments at much larger scale.

### Practical usage

Use NVIDIA FLARE when:

- Multiple organizations need to train or evaluate a model together without pooling raw data.
- The project needs production controls such as TLS/mTLS, certificates, authorization policy, audit logging, site policies, and deployment packages.
- You want to convert an existing PyTorch, TensorFlow, XGBoost, scikit-learn, NeMo, or Python training workflow into an FL job with limited code changes.
- You need to prototype locally, then move the same job concept toward a provisioned multi-site deployment.
- You are fine-tuning LLMs across private corpora using SFT, prompt tuning, or PEFT methods such as LoRA.
- You need governance-sensitive AI in healthcare, finance, government, drug discovery, autonomous systems, or other regulated domains.

Typical workflow:

1. Install FLARE and run a local quick-start or simulator example.
2. Identify the existing centralized training loop and the objects that must move between FL rounds.
3. Choose a Client API pattern or a Job Recipe API recipe.
4. Wrap local training so the client receives a global model, trains or evaluates locally, returns an `FLModel` with parameters, metrics, and metadata, then repeats until the job completes.
5. Test with the FL Simulator before involving real sites.
6. Add aggregation, validation, model selection, privacy filters, and metrics.
7. Provision a secure project for participating organizations.
8. Deploy server and clients with appropriate network, certificate, audit, and site-policy controls.
9. Monitor rounds, failures, runtime logs, and model-quality metrics.

Minimal Client API pattern:

```python
import nvflare.client as flare

flare.init()

while flare.is_running():
    input_model = flare.receive()
    model.load_state_dict(input_model.params)

    train_locally(model, local_data)
    accuracy = evaluate_locally(model, validation_data)

    output_model = flare.FLModel(
        params=model.cpu().state_dict(),
        metrics={"accuracy": accuracy},
        meta={"NUM_STEPS_CURRENT_ROUND": steps},
    )
    flare.send(output_model)
```

LLM-specific considerations:

- Prefer PEFT when full-model exchange is too expensive or unnecessary.
- For LoRA or prompt-tuning workflows, aggregate only the trainable adapter or prompt parameters when appropriate.
- For SFT, plan for full model transfer, memory pressure, network throughput, checkpoint size, and aggregation cost.
- Use FLARE large-object streaming or tensor-oriented transfer mechanisms for model artifacts that exceed normal message limits.
- Validate heterogeneous data partitions carefully; non-IID data can make local metrics misleading and aggregation unstable.
- Treat prompts, outputs, adapters, metrics, and checkpoints as sensitive artifacts, even when raw records never leave the site.

Production checks:

- Define the trust model among server operator, sites, auditors, and model owners.
- Decide what each site is allowed to receive, execute, return, and persist.
- Review privacy filters, differential privacy, secure aggregation or encryption requirements, and confidential-computing requirements.
- Test restart behavior, failed clients, slow clients, round timeouts, and partial participation.
- Keep job definitions, aggregation settings, model versions, dataset descriptions, and evaluation criteria reproducible.

### Learning checklist

- [ ] Explain the difference between centralized training and federated learning.
- [ ] Describe FLARE server, client, controller, executor, aggregator, and `FLModel` roles.
- [ ] Run a local FLARE simulator example.
- [ ] Convert a simple centralized training script with the Client API.
- [ ] Try a Job Recipe API example such as FedAvg.
- [ ] Add metrics and validation for server-side model selection.
- [ ] Explain how site policies and privacy filters protect exchanged artifacts.
- [ ] Compare SFT, prompt tuning, and LoRA in a federated LLM setting.
- [ ] Identify deployment requirements for certificates, authorization, audit logging, networking, and monitoring.

## 繁體中文

### 概覽

NVIDIA FLARE 是開源、domain-agnostic 的 Python federated learning SDK。它讓多個 site 可以共同訓練或評估模型，同時讓原始資料保留在各自 client 端。Server 或 workflow coordinator 負責分派工作，client 在本地資料上訓練或評估，再只回傳 model parameters、updates、metrics 或經核准的 artifacts 供聚合使用。

FLARE 的定位不只是研究原型，而是實務 federated AI。它支援本機模擬、cross-silo 生產部署、安全 provisioning、site-level policies、privacy filters、auditability，以及 Docker、Kubernetes、cloud、edge 等部署模式。它也針對 large models 與 LLM adaptation 提供能力，包括 federated supervised fine-tuning、parameter-efficient fine-tuning、message quantization、memory management 指引、tensor downloading 與 file streaming。

### 為什麼重要

- 敏感資料通常分散在醫院、銀行、政府、製造商或不同地區的 business units 之中。
- 集中資料可能受到隱私法規、治理政策、data residency、商業機密或資料量限制。
- Federated learning 將訓練帶到資料所在地：site 保留本地紀錄，只分享受控的 model updates，而不是 raw data。
- 來自多個 site 的 updates 可提升模型穩健性，並降低只用單一 site local training 造成的偏差。
- 生產級 FL 不只需要演算法，也需要 identity、authorization、provisioning、monitoring、audit logs、privacy controls、deployment tooling 與可重現的 job definitions。
- LLM fine-tuning 會放大傳輸與記憶體問題，因為 full-model SFT 可能涉及非常大的 artifacts；LoRA 等 PEFT 方法則可降低需要交換的可訓練資料量。

### 架構/概念

| 概念 | 角色 |
| --- | --- |
| FL server | 協調 jobs、rounds、aggregation、model distribution 與系統控制。 |
| Client/site | 在本地資料上執行 training 或 evaluation，並回傳核准的 updates 或 metrics。 |
| Global model | 分發給各 site，並透過 aggregation 更新的共享模型狀態。 |
| Local update | Site 產生的 parameters、gradients、weight differences、adapter weights、metrics 或 metadata。 |
| Aggregator | 使用 FedAvg 或其他設定策略合併 client updates。 |
| Controller/workflow | 定義 job flow、task assignment、aggregation timing、validation 與 lifecycle behavior。 |
| Executor/trainer | 執行 site-side application code，常用來包裝既有 ML training scripts。 |
| Client API | 輕量 API，可用 initialize、receive、train、封裝 `FLModel`、send 等動作改造既有 Python training code。 |
| Job Recipe API | 較高階的 recipe 介面，支援 FedAvg、FedOpt、SCAFFOLD、cyclic training、XGBoost 與框架特定 jobs。 |
| FL Simulator | 在部署到真實 sites 前，先於本機執行 federated jobs 進行開發測試。 |
| Provisioning | 產生 secure multi-party operation 所需的 deployment artifacts、identities 與 certificates。 |
| Policies and filters | 對交換資料執行 site-specific authorization、privacy、validation 與 transformation rules。 |
| Large-model support | 為 large model 與 LLM workflows 提供 file streaming、tensor download、message quantization 與 memory practices。 |
| Confidential AI | 在需要更強 code、data 或 model IP 保護時，使用 trusted execution environments 與 confidential computing patterns。 |
| Hierarchical FL / Edge | 透過 tiered architectures 與 edge/mobile support，擴展到比單純 server-client 更大的規模。 |

FLARE 支援的 federated learning pattern 包括 horizontal FL，也就是各 site 有不同樣本但 feature 類似；vertical FL，也就是各方對重疊紀錄持有不同 features；swarm 或 decentralized styles；組織間 cross-silo collaboration；以及更大規模的 edge/mobile deployments。

### 實務使用

適合使用 NVIDIA FLARE 的情境：

- 多個組織需要共同訓練或評估模型，但不能集中 raw data。
- 專案需要 TLS/mTLS、certificates、authorization policy、audit logging、site policies 與 deployment packages 等生產控制。
- 想以有限程式修改，將既有 PyTorch、TensorFlow、XGBoost、scikit-learn、NeMo 或 Python training workflow 轉成 FL job。
- 需要先在本機 prototype，再將相同 job concept 推進到 provisioned multi-site deployment。
- 要跨私有語料進行 LLM fine-tuning，例如 SFT、prompt tuning 或 LoRA 等 PEFT 方法。
- 需要用於 healthcare、finance、government、drug discovery、autonomous systems 或其他 regulated domains 的 governance-sensitive AI。

常見流程：

1. 安裝 FLARE，執行本機 quick-start 或 simulator example。
2. 找出既有 centralized training loop，以及 FL rounds 之間必須交換的 objects。
3. 選擇 Client API pattern 或 Job Recipe API recipe。
4. 包裝 local training，讓 client 接收 global model、本地訓練或評估、回傳帶有 parameters、metrics 與 metadata 的 `FLModel`，並重複直到 job 結束。
5. 在納入真實 sites 前，先用 FL Simulator 測試。
6. 加入 aggregation、validation、model selection、privacy filters 與 metrics。
7. 為參與組織 provision secure project。
8. 依照 network、certificate、audit 與 site-policy 控制部署 server 與 clients。
9. 監控 rounds、failures、runtime logs 與 model-quality metrics。

最小 Client API pattern：

```python
import nvflare.client as flare

flare.init()

while flare.is_running():
    input_model = flare.receive()
    model.load_state_dict(input_model.params)

    train_locally(model, local_data)
    accuracy = evaluate_locally(model, validation_data)

    output_model = flare.FLModel(
        params=model.cpu().state_dict(),
        metrics={"accuracy": accuracy},
        meta={"NUM_STEPS_CURRENT_ROUND": steps},
    )
    flare.send(output_model)
```

LLM 相關注意事項：

- 當 full-model exchange 成本過高或不必要時，優先考慮 PEFT。
- LoRA 或 prompt-tuning workflows 可在適合時只聚合 trainable adapter 或 prompt parameters。
- SFT 需要規劃 full model transfer、memory pressure、network throughput、checkpoint size 與 aggregation cost。
- 對超過一般 message limits 的 model artifacts，使用 FLARE large-object streaming 或 tensor-oriented transfer mechanisms。
- 仔細驗證 heterogeneous data partitions；non-IID data 可能讓 local metrics 失真並造成 aggregation 不穩定。
- 即使 raw records 不離開 site，prompts、outputs、adapters、metrics 與 checkpoints 仍應視為敏感 artifacts。

生產檢查：

- 定義 server operator、sites、auditors 與 model owners 之間的 trust model。
- 決定每個 site 可以接收、執行、回傳與保存哪些內容。
- 檢查 privacy filters、differential privacy、secure aggregation 或 encryption requirements，以及 confidential-computing requirements。
- 測試 restart behavior、failed clients、slow clients、round timeouts 與 partial participation。
- 讓 job definitions、aggregation settings、model versions、dataset descriptions 與 evaluation criteria 可重現。

### 學習檢核表

- [ ] 說明 centralized training 與 federated learning 的差異。
- [ ] 描述 FLARE server、client、controller、executor、aggregator 與 `FLModel` 的角色。
- [ ] 執行一個本機 FLARE simulator example。
- [ ] 用 Client API 改造一個簡單 centralized training script。
- [ ] 嘗試 FedAvg 等 Job Recipe API example。
- [ ] 加入 metrics 與 validation 以支援 server-side model selection。
- [ ] 說明 site policies 與 privacy filters 如何保護交換 artifacts。
- [ ] 比較 federated LLM 情境中的 SFT、prompt tuning 與 LoRA。
- [ ] 辨識 certificates、authorization、audit logging、networking 與 monitoring 等部署需求。

## References

- [NVIDIA FLARE documentation](https://nvflare.readthedocs.io/en/main/)
- [Welcome to NVIDIA FLARE](https://nvflare.readthedocs.io/en/main/welcome.html)
- [Scalable Federated Learning with NVIDIA FLARE for Enhanced LLM Performance](https://developer.nvidia.com/blog/scalable-federated-learning-with-nvidia-flare-for-enhanced-llm-performance/)
- [Turning Machine Learning to Federated Learning in Minutes with NVIDIA FLARE 2.4](https://developer.nvidia.com/blog/turning-machine-learning-to-federated-learning-in-minutes-with-nvidia-flare-2-4/)
