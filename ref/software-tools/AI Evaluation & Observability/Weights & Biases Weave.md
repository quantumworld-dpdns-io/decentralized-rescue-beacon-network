# Weights & Biases Weave

| Field | Details |
| --- | --- |
| Category | LLM observability, evaluation, experiment tracking, prompt and model iteration |
| Maintainer / ecosystem | Weights & Biases |
| Primary use | Trace, evaluate, compare, and improve LLM applications using the W&B platform |
| Typical users | AI engineers, ML engineers, data scientists, product engineering teams |
| Interfaces | Web UI, Python SDK, TypeScript SDK, W&B platform integrations |
| Common integrations | OpenAI, Anthropic, Cohere, Mistral, LangChain-style apps, custom Python and TypeScript functions |
| Best fit | Teams already using W&B or wanting LLM evaluation tied to experiment tracking and model development workflows |
| Last reviewed | 2026-04-29 |

## English

### Overview

Weights & Biases Weave is W&B's observability and evaluation platform for LLM applications. It helps teams trace model calls and application functions, evaluate outputs with custom scorers or LLM judges, compare prompts and models, collect feedback, version objects, and monitor production behavior.

Weave is strongest when a team already uses W&B for machine learning experiments, model development, or shared reporting. It brings LLM app traces and evaluations into the same organizational workflow as experiments, artifacts, dashboards, and collaboration.

### Why it matters

LLM development requires more than logging prompts and outputs. Teams need to understand which function produced an answer, which model and parameters were used, how much it cost, which examples regressed, and whether a prompt change improved quality across a dataset.

Weave helps by providing:

- Automatic and manual tracing for LLM calls and application functions.
- Trace trees made of calls with inputs, outputs, metadata, exceptions, usage, and timing.
- Evaluations with datasets, scorers, LLM judges, and custom metrics.
- Prompt and model comparison workflows.
- Versioning for functions, prompts, datasets, and other objects.
- Feedback collection and production monitoring.
- Integration with broader W&B experiment tracking and collaboration workflows.

### Architecture/Concepts

Key concepts:

- **Project**: A W&B workspace where Weave traces, evaluations, objects, and reports are organized.
- **Call**: The fundamental Weave execution record. A call captures a function or model invocation, including inputs, output, metadata, duration, exceptions, and LLM usage.
- **Trace**: A tree of related calls from one application execution.
- **Op**: A tracked function or operation. In Python, functions can be decorated so their executions become calls.
- **Object versioning**: Weave can version prompts, datasets, functions, and other tracked objects so experiments can be reproduced.
- **Dataset**: A set of examples used for evaluation.
- **Scorer**: A function or judge that measures output quality.
- **Evaluation**: A repeatable test of an application, model, prompt, or function against a dataset and scorer set.

Weave calls are conceptually similar to spans in a trace, but the W&B workflow emphasizes linking those calls to experiments, evaluations, datasets, and versioned objects.

### Practical usage

Use Weave when:

- Your team already uses W&B and wants LLM observability in the same platform.
- You need Python or TypeScript tracing for LLM calls and custom functions.
- You want to compare prompts, models, parameters, or pipeline versions.
- You need evaluation workflows with custom scorers and LLM judges.
- You want production feedback and monitoring connected to development experiments.

Typical workflow:

1. Install the Weave library and authenticate with W&B.
2. Initialize a Weave project in the application.
3. Use automatic LLM library tracking or decorate/wrap important application functions.
4. Inspect traces to understand inputs, outputs, exceptions, latency, token usage, and nested calls.
5. Create datasets from curated examples or logged production calls.
6. Define scorers for correctness, relevance, safety, formatting, retrieval quality, or domain rules.
7. Run evaluations and compare prompts, models, and code changes.
8. Monitor production behavior and route user feedback into future evaluation data.

Operational tips:

- Add structured metadata for model, prompt version, release, customer segment, environment, and route.
- Keep sensitive prompt and output data governed by W&B access controls and retention policy.
- Use custom scorers for hard product requirements; use LLM judges for subjective quality only after calibration.
- Version prompts and functions so evaluation results can be reproduced.
- Track latency, token usage, and cost-like metrics next to quality scores.

### Learning checklist

- [ ] Initialize Weave in a Python or TypeScript project.
- [ ] Trace a simple model call and inspect the call record.
- [ ] Decorate or wrap an application function as a tracked operation.
- [ ] Explain calls, traces, ops, datasets, scorers, and evaluations.
- [ ] Create a dataset and run an evaluation.
- [ ] Compare two prompt or model variants.
- [ ] Add metadata for release, model, prompt version, and environment.
- [ ] Review privacy controls before logging real user prompts or outputs.

## 繁體中文

### 概覽

Weights & Biases Weave 是 W&B 的 LLM application observability 與 evaluation 平台。它協助團隊 trace model calls 與 application functions，用 custom scorers 或 LLM judges 評估 outputs，比較 prompts 與 models，收集 feedback，版本化 objects，並監控 production 行為。

當團隊已使用 W&B 管理 machine learning experiments、model development 或共享報告時，Weave 特別有價值。它將 LLM app traces 與 evaluations 放進與 experiments、artifacts、dashboards、collaboration 相同的組織流程。

### 為什麼重要

LLM 開發不只是記錄 prompts 與 outputs。團隊需要知道哪個 function 產生答案、使用哪個 model 與參數、成本如何、哪些 examples regression，以及 prompt 變更是否在 dataset 上改善品質。

Weave 的價值包括：

- 自動與手動 tracing LLM calls 與 application functions。
- 以 calls 組成 trace trees，記錄 inputs、outputs、metadata、exceptions、usage 與 timing。
- 使用 datasets、scorers、LLM judges 與 custom metrics 執行 evaluations。
- 比較 prompts 與 models。
- 版本化 functions、prompts、datasets 與其他 objects。
- 收集 feedback 並進行 production monitoring。
- 整合 W&B 更廣泛的 experiment tracking 與 collaboration workflows。

### 架構/概念

核心概念：

- **Project**：W&B workspace，用來組織 Weave traces、evaluations、objects 與 reports。
- **Call**：Weave 的基本執行紀錄。Call 會擷取 function 或 model invocation 的 inputs、output、metadata、duration、exceptions 與 LLM usage。
- **Trace**：由同一次 application execution 中相關 calls 組成的樹。
- **Op**：被追蹤的 function 或 operation。在 Python 中，可透過 decorator 讓 function executions 變成 calls。
- **Object versioning**：Weave 可版本化 prompts、datasets、functions 與其他 tracked objects，讓 experiments 可重現。
- **Dataset**：用於 evaluation 的案例集合。
- **Scorer**：衡量 output quality 的 function 或 judge。
- **Evaluation**：讓 application、model、prompt 或 function 在 dataset 與 scorers 上執行的可重複測試。

Weave calls 在概念上類似 trace 裡的 spans，但 W&B workflow 更強調將 calls 連到 experiments、evaluations、datasets 與 versioned objects。

### 實務使用

適合使用 Weave 的情境：

- 團隊已使用 W&B，並希望在同一平台加入 LLM observability。
- 需要 Python 或 TypeScript tracing LLM calls 與 custom functions。
- 想比較 prompts、models、parameters 或 pipeline versions。
- 需要 custom scorers 與 LLM judges 的 evaluation workflows。
- 想把 production feedback 與 monitoring 接回 development experiments。

常見流程：

1. 安裝 Weave library 並登入 W&B。
2. 在應用中初始化 Weave project。
3. 使用 automatic LLM library tracking，或 decorate/wrap 重要 application functions。
4. 檢查 traces，理解 inputs、outputs、exceptions、latency、token usage 與 nested calls。
5. 從 curated examples 或 logged production calls 建立 datasets。
6. 為 correctness、relevance、safety、formatting、retrieval quality 或 domain rules 定義 scorers。
7. 執行 evaluations 並比較 prompts、models 與 code changes。
8. 監控 production behavior，並將 user feedback 導回未來 evaluation data。

維運建議：

- 加入 model、prompt version、release、customer segment、environment 與 route 等 structured metadata。
- 透過 W&B access controls 與 retention policy 管理敏感 prompts 與 outputs。
- 對硬性產品需求使用 custom scorers；主觀品質使用 LLM judges 前應先校準。
- 版本化 prompts 與 functions，讓 evaluation results 可重現。
- 將 latency、token usage 與成本類 metrics 與 quality scores 一起追蹤。

### 學習檢核表

- [ ] 在 Python 或 TypeScript project 中初始化 Weave。
- [ ] Trace 一個簡單 model call 並檢查 call record。
- [ ] 將 application function decorate 或 wrap 成 tracked operation。
- [ ] 說明 calls、traces、ops、datasets、scorers 與 evaluations。
- [ ] 建立 dataset 並執行 evaluation。
- [ ] 比較兩個 prompt 或 model variants。
- [ ] 加入 release、model、prompt version 與 environment metadata。
- [ ] 記錄真實使用者 prompts 或 outputs 前，檢查 privacy controls。

## References

- [W&B Weave documentation](https://docs.wandb.ai/weave/)
- [What is Weave?](https://docs.wandb.ai/weave/guides/tracking)
- [Weave tracing basics](https://docs.wandb.ai/weave/guides/tracking/tracing/)
- [Learn Weave with W&B Inference](https://docs.wandb.ai/weave/quickstart-inference)
