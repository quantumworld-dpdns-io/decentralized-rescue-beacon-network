# LangSmith

| Field | Details |
| --- | --- |
| Category | AI agent observability, evaluation, prompt testing, deployment operations |
| Maintainer / ecosystem | LangChain |
| Primary use | Trace, debug, evaluate, monitor, and improve LLM applications and agents |
| Typical users | AI engineers, agent developers, ML platform teams, product engineering teams |
| Interfaces | Web UI, Python SDK, TypeScript SDK, API, framework integrations |
| Common integrations | LangChain, LangGraph, OpenAI, Anthropic, CrewAI, Vercel AI SDK, Pydantic AI |
| Deployment options | SaaS, hybrid, and self-hosted options |
| Last reviewed | 2026-04-29 |

## English

### Overview

LangSmith is LangChain's framework-agnostic platform for developing, debugging, evaluating, and operating LLM applications and AI agents. It is closely aligned with LangChain and LangGraph, but it can also trace applications built with other frameworks or custom code.

The core workflow is to capture detailed traces from an AI application, turn important examples into datasets, run offline or online evaluations, compare experiments, and monitor production behavior. For agent systems, LangSmith is especially useful because it exposes model calls, tool calls, routing decisions, retries, latency, token usage, and feedback in one place.

### Why it matters

LLM applications fail differently from traditional software. A deployment can pass unit tests while still producing hallucinated answers, weak tool choices, unsafe responses, or higher cost after a prompt or model change.

LangSmith helps teams manage that uncertainty by providing:

- End-to-end traces for prompts, model calls, tools, retrievers, chains, and agents.
- Offline evaluations on curated datasets before release.
- Online evaluations and monitoring on production traffic.
- Experiment comparison for prompt, model, retrieval, and workflow changes.
- Human feedback and annotation queues for improving datasets and evaluators.
- Prompt and agent debugging workflows that connect traces back to development.

### Architecture/Concepts

Key concepts:

- **Project**: A container for traces, logs, evaluations, and monitoring for one application or service.
- **Trace**: A full request or task execution, usually composed of multiple nested runs.
- **Run**: A single operation inside a trace, such as an LLM call, retriever call, tool call, chain step, or custom function.
- **Thread**: A grouping for multi-turn conversations so related traces can be analyzed together.
- **Dataset**: A collection of examples used for evaluations. Examples can be curated manually, imported, generated, or promoted from production traces.
- **Evaluator**: A scoring function. LangSmith supports human review, code rules, LLM-as-judge, pairwise comparison, and production online evaluators.
- **Experiment**: A run of an application against a dataset, producing outputs, scores, traces, and comparison data.
- **Feedback**: User, reviewer, or automated signals attached to runs and traces.

LangSmith's 2026-facing model is both development-time and production-time: teams use it to prototype locally, test changes against datasets, and then keep monitoring real traffic after deployment.

### Practical usage

Use LangSmith when:

- You are building LangChain or LangGraph applications and want native tracing.
- You need a shared evaluation workflow for prompts, RAG pipelines, and agents.
- You want to compare versions before shipping a model, prompt, or workflow change.
- You need production monitoring for quality, latency, token usage, cost, or safety.
- You want human annotation and feedback loops connected to datasets.

Typical workflow:

1. Instrument the application with the LangSmith SDK or framework integration.
2. Inspect traces to understand model prompts, tool calls, retrieval results, errors, latency, and cost.
3. Promote representative successes, failures, and edge cases into a dataset.
4. Define evaluators such as exact match, JSON validity, retrieval relevance, helpfulness, groundedness, or LLM-as-judge rubrics.
5. Run experiments for candidate prompts, model versions, retrievers, or agent graphs.
6. Configure online evaluators, sampling, alerts, and dashboards for production.
7. Feed failing production traces back into datasets and regression tests.

Operational tips:

- Keep dataset examples representative, not only hand-picked successes.
- Calibrate LLM-as-judge evaluators with human review before using them as release gates.
- Track cost and latency alongside quality scores.
- Redact or avoid logging sensitive prompt, user, and tool data unless governance allows it.
- Use tags and metadata consistently so traces can be filtered by customer, workflow, model, release, or risk level.

### Learning checklist

- [ ] Explain the difference between a trace, run, thread, dataset, evaluator, and experiment.
- [ ] Instrument a minimal LLM call and inspect the trace.
- [ ] Add custom run metadata such as model, release, tenant, or route.
- [ ] Create a dataset from curated cases and production traces.
- [ ] Run an offline evaluation with at least one deterministic scorer and one LLM-as-judge scorer.
- [ ] Compare two prompt or model versions in an experiment.
- [ ] Configure an online evaluator for production traffic.
- [ ] Review privacy, retention, and redaction settings before logging real user data.

## 繁體中文

### 概覽

LangSmith 是 LangChain 提供的 AI Agent 與 LLM 應用開發、除錯、評估與維運平台。它與 LangChain、LangGraph 整合很深，但本身是 framework-agnostic，也可以用於其他框架或自寫程式。

核心流程是：擷取 AI 應用的詳細 traces，將重要案例整理成 datasets，執行 offline 或 online evaluations，比較 experiments，並持續監控 production 行為。對 Agent 系統而言，LangSmith 特別有價值，因為它能在同一處呈現模型呼叫、工具呼叫、路由決策、重試、延遲、token 使用量與回饋。

### 為什麼重要

LLM 應用的失敗模式不同於傳統軟體。一次部署可能通過單元測試，卻因 prompt 或 model 變更而產生幻覺、錯誤工具選擇、不安全回覆或成本上升。

LangSmith 的價值包括：

- 針對 prompts、model calls、tools、retrievers、chains 與 agents 建立端到端 traces。
- 在發布前用 curated datasets 執行 offline evaluations。
- 對 production traffic 執行 online evaluations 與 monitoring。
- 比較 prompt、model、retrieval 與 workflow 變更造成的差異。
- 透過 human feedback 與 annotation queues 改善 datasets 與 evaluators。
- 將 trace 除錯流程接回 prompt 與 agent 開發。

### 架構/概念

核心概念：

- **Project**：單一應用或服務的 traces、logs、evaluations 與 monitoring 容器。
- **Trace**：一次完整 request 或任務執行，通常由多個巢狀 runs 組成。
- **Run**：trace 中的一個操作，例如 LLM call、retriever call、tool call、chain step 或自訂函式。
- **Thread**：多輪對話的關聯群組，方便分析同一段 conversation 的 traces。
- **Dataset**：用於 evaluations 的案例集合，可手動整理、匯入、產生，或從 production traces 轉入。
- **Evaluator**：評分函式。LangSmith 支援人工審核、程式規則、LLM-as-judge、pairwise comparison 與 production online evaluators。
- **Experiment**：讓應用在 dataset 上執行，產生 outputs、scores、traces 與比較資料。
- **Feedback**：使用者、審核者或自動化流程加到 runs 與 traces 上的訊號。

以 2026 年的使用方式來看，LangSmith 同時涵蓋開發期與 production：團隊可在本機原型開發、用 datasets 測試變更，並在部署後持續監控真實流量。

### 實務使用

適合使用 LangSmith 的情境：

- 正在建立 LangChain 或 LangGraph 應用，並需要原生 tracing。
- 需要針對 prompts、RAG pipelines 與 agents 建立共用評估流程。
- 想在發布 model、prompt 或 workflow 變更前比較版本。
- 需要監控 production 的品質、延遲、token 使用量、成本或安全性。
- 想把人工標註與回饋流程連到 datasets。

常見流程：

1. 用 LangSmith SDK 或 framework integration instrument 應用。
2. 檢查 traces，理解 prompts、tool calls、retrieval results、errors、latency 與 cost。
3. 將具代表性的成功、失敗與邊界案例轉入 dataset。
4. 定義 evaluators，例如 exact match、JSON validity、retrieval relevance、helpfulness、groundedness 或 LLM-as-judge rubrics。
5. 對候選 prompts、model versions、retrievers 或 agent graphs 執行 experiments。
6. 為 production 設定 online evaluators、sampling、alerts 與 dashboards。
7. 將 production 中失敗的 traces 回饋到 datasets 與 regression tests。

維運建議：

- Dataset 要具代表性，不要只收成功案例。
- LLM-as-judge 作為 release gate 前，應先用人工審核校準。
- 品質分數應與成本、延遲一起追蹤。
- 除非治理允許，否則應遮罩或避免記錄敏感 prompt、user 與 tool data。
- 一致使用 tags 與 metadata，方便依 customer、workflow、model、release 或 risk level 篩選 traces。

### 學習檢核表

- [ ] 說明 trace、run、thread、dataset、evaluator 與 experiment 的差異。
- [ ] Instrument 一個最小 LLM call 並檢查 trace。
- [ ] 加入 model、release、tenant 或 route 等自訂 run metadata。
- [ ] 從 curated cases 與 production traces 建立 dataset。
- [ ] 使用至少一個 deterministic scorer 與一個 LLM-as-judge scorer 執行 offline evaluation。
- [ ] 在 experiment 中比較兩個 prompt 或 model 版本。
- [ ] 為 production traffic 設定 online evaluator。
- [ ] 記錄真實使用者資料前，檢查 privacy、retention 與 redaction 設定。

## References

- [LangSmith documentation](https://docs.langchain.com/langsmith)
- [LangSmith observability](https://docs.langchain.com/langsmith/observability)
- [LangSmith observability concepts](https://docs.langchain.com/langsmith/observability-concepts)
- [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation)
- [LangSmith reference overview](https://docs.langchain.com/langsmith/reference-overview)
