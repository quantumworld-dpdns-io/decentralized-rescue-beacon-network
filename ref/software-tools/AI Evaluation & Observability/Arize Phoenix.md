# Arize Phoenix

| Field | Details |
| --- | --- |
| Category | Open-source AI observability, LLM tracing, evaluation, prompt engineering |
| Maintainer / ecosystem | Arize AI and Phoenix open-source community |
| Primary use | Debug, evaluate, experiment with, and improve LLM applications and agents |
| Typical users | AI engineers, data scientists, ML platform teams, RAG and agent developers |
| Interfaces | Web UI, Python SDK, TypeScript SDK, OpenTelemetry Protocol, OpenInference instrumentation |
| Common integrations | OpenAI, Anthropic, Bedrock, Vertex AI, LangChain, LlamaIndex, DSPy, LiteLLM |
| Best fit | Teams wanting local or self-hosted LLM observability with open telemetry standards |
| Last reviewed | 2026-04-29 |

## English

### Overview

Arize Phoenix is an open-source AI observability and evaluation platform for LLM applications, RAG systems, and agents. It provides tracing, span analysis, prompt iteration, datasets, experiments, evaluations, annotations, and troubleshooting workflows.

Phoenix is closely associated with Arize AI's broader observability platform, but Phoenix itself is commonly used for local development, self-hosting, and open-source LLM debugging. A major 2026-facing theme is standards-based instrumentation: Phoenix accepts traces over OTLP and works with OpenInference and OpenTelemetry-style instrumentation.

### Why it matters

LLM failures are often hidden inside multi-step execution: the prompt may be weak, retrieval may return irrelevant context, an agent may choose the wrong tool, or an evaluator may be biased. Traditional logs usually do not show enough context to explain those failures.

Phoenix helps by providing:

- Trace visualization for model calls, retrievers, tools, chains, and agents.
- Span-level filtering and analysis for latency, token usage, errors, and metadata.
- Evaluation workflows for traces, datasets, and experiment outputs.
- Prompt playground and prompt management for systematic iteration.
- Dataset and experiment workflows for comparing model, prompt, and pipeline changes.
- OpenTelemetry and OpenInference alignment for lower vendor lock-in.

### Architecture/Concepts

Key concepts:

- **Project**: A workspace for related traces, datasets, experiments, and evaluations.
- **Trace**: One full execution path through an LLM application.
- **Span**: A timed operation within a trace, such as an LLM call, retriever call, tool call, or evaluator run.
- **OpenInference**: A set of semantic conventions and instrumentations for AI application telemetry, used heavily in the Phoenix ecosystem.
- **OTLP ingestion**: Phoenix can receive telemetry using the OpenTelemetry Protocol.
- **Dataset**: A collection of examples used for evaluation and regression testing.
- **Experiment**: A run of an application or prompt configuration against a dataset.
- **Evaluator**: A deterministic, heuristic, or LLM-as-judge scoring process.
- **Annotation**: Human feedback or labels attached to traces or examples.

Phoenix often fits a lifecycle model:

1. Develop locally with tracing enabled.
2. Inspect spans to understand failures.
3. Curate traces into datasets.
4. Run evaluations and experiments.
5. Promote lessons into prompts, retrieval logic, agent policies, or production monitoring.

### Practical usage

Use Phoenix when:

- You want open-source LLM tracing and evaluation.
- You prefer self-hosting or local observability during development.
- You need to debug RAG retrieval quality and generated answers together.
- You want OpenTelemetry-compatible trace collection.
- You need a prompt playground plus experiment tracking for model and prompt changes.

Typical workflow:

1. Start a Phoenix server locally or deploy it in a shared environment.
2. Instrument the app with an OpenInference integration or manual OpenTelemetry spans.
3. Capture LLM calls, retrieval calls, tools, prompts, outputs, token usage, latency, and errors.
4. Use span filters to isolate poor responses, slow steps, high-cost calls, or retrieval failures.
5. Convert important traces into datasets.
6. Run evaluations such as relevance, groundedness, hallucination checks, answer correctness, format checks, or custom business rules.
7. Compare prompt, model, chunking, embedding, reranking, and tool changes through experiments.

Operational tips:

- Treat Phoenix traces as sensitive because they may include prompts, user content, retrieved documents, and model outputs.
- Prefer structured span attributes for model, route, tenant, release, prompt version, and retriever version.
- Use deterministic evaluators where possible and LLM-as-judge where subjective quality matters.
- Keep evaluators observable too; Phoenix can trace evaluation runs so teams can inspect judge behavior.
- If production monitoring and alerting requirements exceed local Phoenix usage, evaluate how Phoenix and Arize production workflows should be connected.

### Learning checklist

- [ ] Start Phoenix locally and send a simple trace.
- [ ] Explain traces, spans, datasets, experiments, evaluators, and annotations.
- [ ] Instrument one LLM call and one retriever call.
- [ ] Inspect token usage, latency, prompt, retrieved context, and output in the trace UI.
- [ ] Create a dataset from traced examples.
- [ ] Run an evaluator against experiment results.
- [ ] Compare two prompt or retrieval configurations.
- [ ] Review OTLP/OpenInference instrumentation options for your framework.

## 繁體中文

### 概覽

Arize Phoenix 是一個開源 AI observability 與 evaluation 平台，適合 LLM applications、RAG systems 與 agents。它提供 tracing、span analysis、prompt iteration、datasets、experiments、evaluations、annotations 與除錯流程。

Phoenix 與 Arize AI 的商業 observability 平台密切相關，但 Phoenix 本身常用於本機開發、自行部署與開源 LLM 除錯。以 2026 年的方向來看，Phoenix 的重點之一是標準化 instrumentation：它可透過 OTLP 接收 traces，並與 OpenInference、OpenTelemetry 風格的 instrumentation 搭配。

### 為什麼重要

LLM 失敗常藏在多步驟執行之中：prompt 可能不夠清楚、retrieval 可能取回不相關內容、agent 可能選錯工具，或 evaluator 本身有偏差。傳統 logs 通常不足以解釋這些問題。

Phoenix 的價值包括：

- 視覺化 model calls、retrievers、tools、chains 與 agents 的 traces。
- 以 span 層級分析 latency、token usage、errors 與 metadata。
- 針對 traces、datasets 與 experiment outputs 執行 evaluations。
- 提供 prompt playground 與 prompt management 來系統化迭代。
- 透過 datasets 與 experiments 比較 model、prompt 與 pipeline 變更。
- 對齊 OpenTelemetry 與 OpenInference，降低 vendor lock-in。

### 架構/概念

核心概念：

- **Project**：相關 traces、datasets、experiments 與 evaluations 的工作區。
- **Trace**：LLM 應用的一次完整執行路徑。
- **Span**：trace 中的一個計時操作，例如 LLM call、retriever call、tool call 或 evaluator run。
- **OpenInference**：AI 應用 telemetry 的 semantic conventions 與 instrumentations，在 Phoenix 生態中很常見。
- **OTLP ingestion**：Phoenix 可使用 OpenTelemetry Protocol 接收 telemetry。
- **Dataset**：用於 evaluation 與 regression testing 的案例集合。
- **Experiment**：讓應用或 prompt configuration 在 dataset 上執行的結果。
- **Evaluator**：deterministic、heuristic 或 LLM-as-judge 的評分流程。
- **Annotation**：附加在 traces 或 examples 上的人工回饋或標籤。

Phoenix 常見生命週期如下：

1. 開發時啟用 tracing。
2. 檢查 spans 來理解失敗原因。
3. 將 traces 整理成 datasets。
4. 執行 evaluations 與 experiments。
5. 將結果回饋到 prompts、retrieval logic、agent policies 或 production monitoring。

### 實務使用

適合使用 Phoenix 的情境：

- 想使用開源 LLM tracing 與 evaluation。
- 偏好在開發階段本機或自行部署 observability。
- 需要同時除錯 RAG retrieval quality 與 generated answers。
- 想使用 OpenTelemetry-compatible trace collection。
- 需要 prompt playground 與 experiment tracking 來比較 model 與 prompt 變更。

常見流程：

1. 在本機啟動 Phoenix server，或部署到共享環境。
2. 用 OpenInference integration 或 manual OpenTelemetry spans instrument 應用。
3. 擷取 LLM calls、retrieval calls、tools、prompts、outputs、token usage、latency 與 errors。
4. 使用 span filters 找出差回覆、慢步驟、高成本呼叫或 retrieval failures。
5. 將重要 traces 轉成 datasets。
6. 執行 relevance、groundedness、hallucination checks、answer correctness、format checks 或 custom business rules 等 evaluations。
7. 透過 experiments 比較 prompt、model、chunking、embedding、reranking 與 tool 變更。

維運建議：

- Phoenix traces 可能包含 prompts、使用者內容、retrieved documents 與 model outputs，應視為敏感資料。
- 為 model、route、tenant、release、prompt version 與 retriever version 使用結構化 span attributes。
- 可用 deterministic evaluators 時優先使用；主觀品質再使用 LLM-as-judge。
- Evaluators 本身也應可觀測；Phoenix 可追蹤 evaluation runs，協助檢查 judge 行為。
- 若 production monitoring 與 alerting 需求超過本機 Phoenix 使用，應評估 Phoenix 與 Arize production workflow 的銜接方式。

### 學習檢核表

- [ ] 在本機啟動 Phoenix 並送出一筆簡單 trace。
- [ ] 說明 traces、spans、datasets、experiments、evaluators 與 annotations。
- [ ] Instrument 一個 LLM call 與一個 retriever call。
- [ ] 在 trace UI 中檢查 token usage、latency、prompt、retrieved context 與 output。
- [ ] 從 traced examples 建立 dataset。
- [ ] 對 experiment results 執行 evaluator。
- [ ] 比較兩種 prompt 或 retrieval configuration。
- [ ] 檢查目前框架可用的 OTLP/OpenInference instrumentation。

## References

- [Arize Phoenix documentation](https://arize.com/docs/phoenix/)
- [Phoenix LLM observability guide](https://arize.com/docs/phoenix/llm-observability)
- [Phoenix evaluation documentation](https://arize.com/docs/phoenix/evaluation/llm-evals/evaluator-traces)
- [Phoenix open-source site](https://phoenix.arize.com/)
- [Arize Phoenix GitHub repository](https://github.com/Arize-ai/phoenix)
