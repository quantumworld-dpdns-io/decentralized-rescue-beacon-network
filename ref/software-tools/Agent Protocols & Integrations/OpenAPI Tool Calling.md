# OpenAPI Tool Calling

| Field | Details |
| --- | --- |
| Category | API integration, agent tool calling |
| Primary use | Let AI agents select and call HTTP APIs from structured API descriptions |
| Common standards | OpenAPI 3.x, JSON Schema, REST, OAuth, API keys |
| OpenAI surface | GPT Actions for ChatGPT; function tools and custom tools in the OpenAI API |
| Core idea | Convert natural language intent into validated API parameters, execute the API call, and use the result in the response |
| Best fit | Existing REST APIs that need natural-language access with clear schemas and authentication |
| Last reviewed | 2026-04-29 |

## English

### Overview

OpenAPI tool calling uses an OpenAPI schema to describe HTTP endpoints that an agent can call. In ChatGPT, this pattern is exposed as GPT Actions: developers provide an OpenAPI schema, configure authentication, and the model decides when a listed API operation is relevant to the user's request.

OpenAPI tool calling is related to general function calling. Function calling gives the model JSON-schema-defined tools; OpenAPI tool calling derives those callable operations from an API description. The application or platform still executes the API request, handles authentication, and returns results for the model to summarize or continue reasoning over.

### Why it matters

- **Reuse existing APIs:** Teams can expose current REST services without building a full custom agent runtime.
- **Natural-language access:** Users ask for outcomes, while the model maps intent to endpoint, method, and parameters.
- **Structured execution:** OpenAPI schemas make inputs, required fields, descriptions, and response shapes explicit.
- **Authentication support:** Actions can use no auth, API keys, or OAuth depending on the platform and use case.
- **Governance hooks:** Consequential operations, rate limits, TLS, and endpoint descriptions help make API access safer.

### Architecture/Concepts

| Concept | Meaning |
| --- | --- |
| OpenAPI schema | Machine-readable API description with servers, paths, operations, parameters, request bodies, and responses. |
| Operation | A callable endpoint, usually identified by `operationId`, HTTP method, and path. |
| JSON Schema | Defines request parameters and payload shapes for model-generated arguments. |
| Tool selection | The model decides whether an operation is relevant to the user's request. |
| Tool execution | The platform or application calls the HTTP API with generated arguments. |
| Authentication | API key, OAuth, or no-auth setup used when executing the request. |
| Consequential action | A write or side-effecting operation that should require user confirmation. |

The typical flow:

1. The developer writes or imports an OpenAPI schema.
2. The platform turns operations into callable tools.
3. The user asks a natural-language question.
4. The model selects one or more operations and generates structured arguments.
5. The platform executes the API request.
6. The model receives the API result and produces the final response or calls another operation.

### Practical usage

Good OpenAPI tool definitions are written for both machines and models:

- Give every operation a stable, descriptive `operationId`.
- Keep endpoint summaries and descriptions short, factual, and action-specific.
- Use precise parameter descriptions and enums instead of broad free-text fields.
- Mark required fields accurately.
- Return raw structured data instead of prose whenever possible.
- Split read-only and write-capable operations.
- Use `x-openai-isConsequential: true` for operations that book, buy, send, delete, update, or otherwise create side effects.
- Keep request and response bodies small enough for the platform limits.
- Test endpoints in Postman, curl, or integration tests before debugging model behavior.

Use OpenAPI tool calling when:

| Scenario | Fit | Notes |
| --- | --- | --- |
| Query a business system | Strong | Search, lookup, reporting, and status APIs are good first targets. |
| Create tickets or records | Strong with confirmation | Require explicit user approval for writes. |
| Multi-step API workflows | Good | The model can call multiple operations, but schemas and responses must be clear. |
| Streaming or long-running jobs | Maybe | Prefer job-create plus job-status endpoints; avoid request timeouts. |
| Complex local system access | Weak | MCP or local tools may fit better than HTTP OpenAPI actions. |

Security and reliability checklist:

- Require HTTPS and valid certificates.
- Enforce authorization on the API server, not only in the schema.
- Rate limit exposed endpoints and handle 429/5xx responses cleanly.
- Validate all model-generated inputs server-side.
- Avoid exposing broad administrative operations.
- Log operation, user, request ID, and confirmation state.
- Redact secrets and sensitive response fields before returning data to the model.

### Learning checklist

- [ ] Explain how OpenAPI tool calling relates to function calling.
- [ ] Write a minimal OpenAPI schema with one GET operation.
- [ ] Add `operationId`, parameter descriptions, and response schema.
- [ ] Configure API key or OAuth authentication for a test action.
- [ ] Mark a write operation as consequential.
- [ ] Test a read-only query and inspect the generated API arguments.
- [ ] Test a multi-step workflow that calls two operations.
- [ ] Add server-side validation, rate limiting, and audit logging.
- [ ] Decide when MCP is a better fit than an OpenAPI action.

## 繁體中文

### 概覽

OpenAPI tool calling 使用 OpenAPI schema 描述 agent 可呼叫的 HTTP endpoints。在 ChatGPT 中，這個模式以 GPT Actions 呈現：開發者提供 OpenAPI schema、設定 authentication，模型再判斷哪個 API operation 與使用者需求相關。

OpenAPI tool calling 與一般 function calling 密切相關。Function calling 讓模型使用以 JSON Schema 定義的 tools；OpenAPI tool calling 則從 API 描述轉成可呼叫 operations。應用程式或平台仍負責執行 API request、處理 authentication，並把結果回傳給模型進行摘要或後續推理。

### 為什麼重要

- **重用既有 API：** 團隊可暴露現有 REST services，不必先建立完整自訂 agent runtime。
- **自然語言存取：** 使用者描述目標，模型負責映射到 endpoint、method 與 parameters。
- **結構化執行：** OpenAPI schema 讓 inputs、required fields、descriptions 與 response shapes 明確化。
- **支援 authentication：** Actions 可依平台與使用情境使用 no auth、API key 或 OAuth。
- **治理鉤子：** Consequential operations、rate limits、TLS 與 endpoint descriptions 有助於讓 API access 更安全。

### 架構/概念

| 概念 | 說明 |
| --- | --- |
| OpenAPI schema | 機器可讀 API 描述，包含 servers、paths、operations、parameters、request bodies 與 responses。 |
| Operation | 可呼叫 endpoint，通常由 `operationId`、HTTP method 與 path 識別。 |
| JSON Schema | 定義 request parameters 與 payload shapes，供模型產生 arguments。 |
| Tool selection | 模型判斷某個 operation 是否與使用者需求相關。 |
| Tool execution | 平台或應用程式用產生的 arguments 呼叫 HTTP API。 |
| Authentication | 執行 request 時使用 API key、OAuth 或 no-auth 設定。 |
| Consequential action | 會寫入或產生副作用的 operation，應要求使用者確認。 |

典型流程：

1. 開發者撰寫或匯入 OpenAPI schema。
2. 平台將 operations 轉成可呼叫 tools。
3. 使用者提出自然語言問題。
4. 模型選擇一個或多個 operations 並產生結構化 arguments。
5. 平台執行 API request。
6. 模型取得 API result，產生最終回覆或繼續呼叫下一個 operation。

### 實務使用

好的 OpenAPI tool definitions 同時服務機器與模型：

- 每個 operation 都應有穩定且具描述性的 `operationId`。
- Endpoint summary 與 description 應短、 factual、聚焦於該 action。
- 使用精準 parameter descriptions 與 enums，避免過度寬泛 free-text 欄位。
- 正確標記 required fields。
- 優先回傳 raw structured data，而不是自然語言 prose。
- 分開唯讀 operations 與可寫入 operations。
- 對會預訂、購買、寄送、刪除、更新或產生副作用的操作使用 `x-openai-isConsequential: true`。
- 讓 request 與 response bodies 維持在平台限制內。
- 先用 Postman、curl 或 integration tests 測通 endpoints，再除錯模型行為。

適合使用 OpenAPI tool calling 的情境：

| 場景 | 適合度 | 備註 |
| --- | --- | --- |
| 查詢商業系統 | 高 | Search、lookup、reporting、status APIs 都是好起點。 |
| 建立 tickets 或 records | 高但需確認 | 寫入操作需明確使用者批准。 |
| 多步驟 API workflow | 良好 | 模型可呼叫多個 operations，但 schema 與 responses 必須清楚。 |
| Streaming 或長時間 jobs | 視情況 | 優先設計 job-create 加 job-status endpoints，避免 request timeout。 |
| 複雜本機系統存取 | 較弱 | MCP 或本機 tools 可能比 HTTP OpenAPI actions 更適合。 |

安全與可靠性檢查：

- 要求 HTTPS 與有效憑證。
- 在 API server 強制 authorization，不只依賴 schema。
- 對暴露 endpoints 做 rate limiting，並清楚處理 429/5xx。
- 所有模型產生輸入都需 server-side validation。
- 避免暴露過度廣泛的 admin operations。
- 記錄 operation、user、request ID 與 confirmation state。
- 回傳資料給模型前，移除 secrets 與敏感 response fields。

### 學習檢核表

- [ ] 說明 OpenAPI tool calling 與 function calling 的關係。
- [ ] 撰寫包含一個 GET operation 的最小 OpenAPI schema。
- [ ] 加入 `operationId`、parameter descriptions 與 response schema。
- [ ] 為測試 action 設定 API key 或 OAuth authentication。
- [ ] 將寫入 operation 標記為 consequential。
- [ ] 測試唯讀查詢並檢查產生的 API arguments。
- [ ] 測試呼叫兩個 operations 的多步驟 workflow。
- [ ] 加入 server-side validation、rate limiting 與 audit logging。
- [ ] 判斷何時 MCP 比 OpenAPI action 更適合。

## References

- [OpenAI: GPT Actions introduction](https://platform.openai.com/docs/actions/introduction)
- [OpenAI: Getting started with GPT Actions](https://platform.openai.com/docs/actions/getting-started)
- [OpenAI: GPT Action authentication](https://platform.openai.com/docs/actions/authentication)
- [OpenAI: Production notes on GPT Actions](https://platform.openai.com/docs/actions/production)
- [OpenAI: Function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
