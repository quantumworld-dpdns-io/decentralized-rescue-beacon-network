# OpenTelemetry for LLM Apps

| Field | Details |
| --- | --- |
| Category | Observability standard, distributed tracing, metrics, logs, GenAI telemetry |
| Project | OpenTelemetry, Cloud Native Computing Foundation ecosystem |
| License | Apache License 2.0 |
| Primary use | Collect standardized traces, metrics, logs, and GenAI semantic telemetry from LLM applications |
| Typical users | Platform engineers, SRE teams, AI infrastructure teams, agent developers |
| Interfaces | SDKs, automatic instrumentation, OpenTelemetry Protocol, Collector, exporters |
| Common backends | Prometheus, Grafana, Jaeger, Tempo, Honeycomb, Datadog, New Relic, Phoenix, vendor observability platforms |
| Current note | OpenTelemetry GenAI semantic conventions are still marked Development; verify stability and SDK support before enforcing them as a hard contract. |
| Last reviewed | 2026-04-29 |

## English

### Overview

OpenTelemetry is the open standard toolkit for collecting traces, metrics, and logs from applications. For LLM apps, it provides a vendor-neutral way to observe model calls, prompts, embeddings, retrieval, tool execution, agent steps, latency, errors, token usage, and evaluation results.

The important 2026-facing detail is that OpenTelemetry's GenAI semantic conventions exist, but many parts are still marked Development. That means teams can use them now, especially through mature instrumentations and backends, but should expect naming, attributes, and SDK support to keep evolving.

### Why it matters

AI observability tools are useful, but every AI platform also needs an interoperability layer. Without a common telemetry model, each framework, model provider, and evaluation platform invents a separate trace schema.

OpenTelemetry helps by providing:

- A standard way to emit and transport traces, metrics, logs, and events.
- OTLP, a widely supported protocol for sending telemetry to collectors and backends.
- A Collector that can receive, filter, redact, batch, route, and export telemetry.
- Semantic conventions for GenAI model calls, embeddings, retrieval, tools, agents, events, and metrics.
- A path to connect AI traces with normal service telemetry such as HTTP, database, queue, and infrastructure spans.
- Reduced vendor lock-in because telemetry can be routed to multiple backends.

### Architecture/Concepts

Key concepts:

- **Trace**: The full execution of a request or task.
- **Span**: A timed operation inside a trace, such as an HTTP request, LLM call, vector search, tool execution, or evaluator run.
- **Metric**: Numeric measurements such as request count, latency, token usage, error rate, queue length, or cost estimate.
- **Log/Event**: Time-stamped records. GenAI events can represent detailed inference data or evaluation results, depending on instrumentation support.
- **Semantic conventions**: Standard attribute names and span/event names so telemetry has consistent meaning.
- **Instrumentation**: Code or libraries that create telemetry. This may be automatic, framework-provided, provider-specific, or manual.
- **OTLP**: The OpenTelemetry Protocol used to send telemetry.
- **Collector**: A deployable pipeline for receiving, processing, redacting, sampling, and exporting telemetry.
- **Exporter**: A component that sends telemetry to a backend.

Important GenAI concepts in the OpenTelemetry specification include:

- Inference spans for operations such as chat, text completion, content generation, and embeddings.
- Retrieval spans for RAG data access.
- Tool execution spans for agent tool calls.
- Agent spans for creating and invoking agents.
- Attributes such as provider name, request model, response model, operation name, output type, token usage, conversation id, and error type.
- Optional events for detailed request/response content and evaluation results.

### Practical usage

Use OpenTelemetry for LLM apps when:

- You want AI traces connected to the rest of your production observability.
- You need one instrumentation path that can feed multiple vendors or internal systems.
- Your platform already uses OpenTelemetry for services and infrastructure.
- You want to adopt AI observability tools without hard-coding one backend.
- You need a Collector layer for redaction, routing, sampling, and governance.

Typical workflow:

1. Add OpenTelemetry SDK and framework/provider instrumentation to the application.
2. Capture normal service spans such as HTTP, database, queue, cache, and background jobs.
3. Add GenAI spans for model calls, embeddings, retrieval, tools, and agent steps.
4. Attach consistent metadata such as application, environment, release, tenant, route, prompt version, model, and evaluator version.
5. Send telemetry to an OpenTelemetry Collector over OTLP.
6. Use Collector processors for batching, redaction, sampling, and routing.
7. Export to one or more backends, such as a general observability platform and an AI-specific trace viewer.

Operational tips:

- Treat prompt and completion content as sensitive. Do not record full content by default unless privacy and retention controls are clear.
- Keep high-cardinality data out of metric labels; use traces or logs for request-specific details.
- Add manual spans around retrieval, ranking, tool calls, guardrails, and business decisions that automatic instrumentation cannot see.
- Version prompt templates, evaluators, retrieval settings, and agent policies in attributes.
- Check the GenAI semantic convention version emitted by each instrumentation. Some SDKs may keep older conventions by default unless configured.
- Use the Collector as the policy enforcement point for redaction and routing.

### Learning checklist

- [ ] Explain traces, spans, metrics, logs, semantic conventions, OTLP, Collector, and exporters.
- [ ] Instrument a simple LLM call with OpenTelemetry.
- [ ] Add manual spans around retrieval and tool execution.
- [ ] Send telemetry to a local Collector.
- [ ] Export traces to at least one backend.
- [ ] Add attributes for model, prompt version, release, route, and environment.
- [ ] Decide what prompt and output content may be recorded.
- [ ] Review current OpenTelemetry GenAI semantic convention stability before production rollout.

## 繁體中文

### 概覽

OpenTelemetry 是用於收集 traces、metrics 與 logs 的開放標準工具組。對 LLM apps 而言，它提供 vendor-neutral 的方式來觀察 model calls、prompts、embeddings、retrieval、tool execution、agent steps、latency、errors、token usage 與 evaluation results。

以 2026 年的狀態來看，重要細節是 OpenTelemetry 已有 GenAI semantic conventions，但許多部分仍標示為 Development。團隊可以開始使用，特別是透過成熟的 instrumentations 與 backends，但應預期命名、attributes 與 SDK 支援仍會演進。

### 為什麼重要

AI observability tools 很有用，但每個 AI 平台也需要 interoperability layer。若沒有共同 telemetry model，各框架、model provider 與 evaluation platform 都會發明自己的 trace schema。

OpenTelemetry 的價值包括：

- 以標準方式產生與傳輸 traces、metrics、logs 與 events。
- 提供廣泛支援的 OTLP，將 telemetry 送到 collectors 與 backends。
- 透過 Collector 接收、過濾、遮罩、批次、路由與匯出 telemetry。
- 為 GenAI model calls、embeddings、retrieval、tools、agents、events 與 metrics 提供 semantic conventions。
- 將 AI traces 與 HTTP、database、queue、infrastructure spans 等一般 service telemetry 連在一起。
- 因 telemetry 可送往多個 backends，降低 vendor lock-in。

### 架構/概念

核心概念：

- **Trace**：一次 request 或 task 的完整執行。
- **Span**：trace 中的一個計時操作，例如 HTTP request、LLM call、vector search、tool execution 或 evaluator run。
- **Metric**：數值量測，例如 request count、latency、token usage、error rate、queue length 或 cost estimate。
- **Log/Event**：具時間戳的紀錄。依 instrumentation 支援程度，GenAI events 可表示詳細 inference data 或 evaluation results。
- **Semantic conventions**：標準化 attribute names 與 span/event names，讓 telemetry 有一致語意。
- **Instrumentation**：建立 telemetry 的程式或函式庫，可為 automatic、framework-provided、provider-specific 或 manual。
- **OTLP**：OpenTelemetry Protocol，用於送出 telemetry。
- **Collector**：可部署的 pipeline，用於接收、處理、遮罩、sampling 與匯出 telemetry。
- **Exporter**：將 telemetry 送到 backend 的元件。

OpenTelemetry specification 中重要的 GenAI 概念包括：

- 針對 chat、text completion、content generation 與 embeddings 等操作的 inference spans。
- RAG data access 的 retrieval spans。
- Agent tool calls 的 tool execution spans。
- 建立與呼叫 agents 的 agent spans。
- provider name、request model、response model、operation name、output type、token usage、conversation id 與 error type 等 attributes。
- 用於詳細 request/response content 與 evaluation results 的 optional events。

### 實務使用

適合在 LLM apps 使用 OpenTelemetry 的情境：

- 想把 AI traces 連到既有 production observability。
- 需要一條 instrumentation path 同時供應多個 vendors 或 internal systems。
- 平台已使用 OpenTelemetry 觀察 services 與 infrastructure。
- 想採用 AI observability tools，但不想 hard-code 單一 backend。
- 需要 Collector layer 處理 redaction、routing、sampling 與 governance。

常見流程：

1. 在應用中加入 OpenTelemetry SDK 與 framework/provider instrumentation。
2. 擷取 HTTP、database、queue、cache 與 background jobs 等一般 service spans。
3. 為 model calls、embeddings、retrieval、tools 與 agent steps 加上 GenAI spans。
4. 加入 application、environment、release、tenant、route、prompt version、model 與 evaluator version 等一致 metadata。
5. 透過 OTLP 將 telemetry 送到 OpenTelemetry Collector。
6. 用 Collector processors 進行 batching、redaction、sampling 與 routing。
7. 匯出到一個或多個 backends，例如一般 observability platform 與 AI-specific trace viewer。

維運建議：

- Prompt 與 completion content 應視為敏感資料。除非 privacy 與 retention controls 清楚，否則不要預設記錄完整內容。
- 避免把高基數資料放進 metric labels；請用 traces 或 logs 記錄 request-specific details。
- 對 automatic instrumentation 看不到的 retrieval、ranking、tool calls、guardrails 與 business decisions 加上 manual spans。
- 在 attributes 中記錄 prompt templates、evaluators、retrieval settings 與 agent policies 的版本。
- 檢查每個 instrumentation 送出的 GenAI semantic convention 版本。有些 SDK 預設會維持舊 conventions，除非另外設定。
- 將 Collector 作為 redaction 與 routing 的 policy enforcement point。

### 學習檢核表

- [ ] 說明 traces、spans、metrics、logs、semantic conventions、OTLP、Collector 與 exporters。
- [ ] 用 OpenTelemetry instrument 一個簡單 LLM call。
- [ ] 在 retrieval 與 tool execution 周圍加入 manual spans。
- [ ] 將 telemetry 送到本機 Collector。
- [ ] 將 traces 匯出到至少一個 backend。
- [ ] 加入 model、prompt version、release、route 與 environment 等 attributes。
- [ ] 決定哪些 prompt 與 output content 可以被記錄。
- [ ] Production rollout 前檢查目前 OpenTelemetry GenAI semantic convention 的穩定性。

## References

- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [OpenTelemetry semantic conventions for generative AI systems](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [OpenTelemetry generative AI spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/)
- [OpenTelemetry GenAI agent and framework spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)
- [OpenTelemetry Generative AI events](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/)
- [OpenTelemetry Generative AI metrics](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics/)
