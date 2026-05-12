# Model Context Protocol

| Field | Details |
| --- | --- |
| Category | Agent integration protocol, tool and data connectivity |
| Standard | Model Context Protocol (MCP) |
| Primary use | Connect AI applications to external tools, data sources, prompts, and workflows through a common protocol |
| Core participants | Host, client, server |
| Message format | JSON-RPC 2.0 |
| Current reference | MCP specification version 2025-06-18 |
| Best fit | Teams building reusable agent integrations across IDEs, chat apps, desktop clients, and enterprise systems |
| Last reviewed | 2026-04-29 |

## English

### Overview

Model Context Protocol (MCP) is an open protocol for connecting AI applications to external systems. Instead of building a separate connector for every model, app, and data source, MCP defines a shared way for an AI host to discover and use capabilities exposed by MCP servers.

In practice, MCP is the agent integration layer for tools, resources, prompts, and workflows. A coding assistant can use an MCP server for GitHub issues, a chat assistant can query a database, and a desktop agent can interact with local files or apps, all through a common client-server protocol.

### Why it matters

- **Reusable integrations:** One MCP server can serve multiple compatible clients instead of one-off plugins per app.
- **Cleaner agent architecture:** Tool and data access move behind explicit server boundaries.
- **Ecosystem portability:** MCP is supported by multiple AI clients, developer tools, and server implementations.
- **Better governance:** Hosts can inspect server capabilities, request user consent, and apply policy before sensitive actions.
- **Composable workflows:** Resources, prompts, and tools can be combined into richer agent behavior without hard-coding every path into the model prompt.

### Architecture/Concepts

| Concept | Meaning |
| --- | --- |
| Host | The AI application the user interacts with, such as an IDE, desktop assistant, or chat product. |
| Client | The connector inside the host that maintains an MCP connection to one server. |
| Server | A process or remote service that exposes capabilities to the host. |
| Resources | Data or context the model or user can read, such as files, records, documents, or database rows. |
| Prompts | Reusable templates or workflows a server can provide to users and hosts. |
| Tools | Callable functions that let the model request actions or computations. |
| Sampling | A client feature that lets a server request LLM completions through the host, subject to controls. |
| Roots | Filesystem or URI boundaries that help a server understand where it may operate. |
| Elicitation | A way for servers to ask the user for missing information through the client. |

The base protocol uses JSON-RPC 2.0 over stateful connections. MCP supports capability negotiation during startup so clients and servers can agree on which features are available. Common transports include local process connections for desktop tools and HTTP-based transports for remote servers.

MCP is powerful because servers can expose arbitrary data access and code execution paths. Hosts should treat tool descriptions, resource content, and server-provided text as untrusted unless the server is trusted. User consent, least privilege, audit logs, and clear approval UI are core design requirements, not optional polish.

### Practical usage

Use MCP when an integration should be reusable across agent clients:

| Scenario | MCP fit | Notes |
| --- | --- | --- |
| Internal knowledge base access | Strong | Expose search and document resources with access controls. |
| Developer tools | Strong | Source control, issue trackers, CI, code search, and design tools map well to tools and resources. |
| Local desktop automation | Strong but sensitive | Use strict permissions and clear user approval before file or app actions. |
| One private app endpoint | Maybe | A direct function call may be simpler if only one model app will ever use it. |
| High-risk write operations | Use with controls | Require confirmation, scoped credentials, and server-side authorization. |

Implementation tips:

- Design small, named tools with clear input schemas and deterministic outputs.
- Keep read-only resources separate from write-capable tools.
- Scope credentials per user and per server; do not share broad service tokens with every tool.
- Validate tool inputs server-side even if the model produced structured arguments.
- Return structured data where possible so the host or model can reason over results.
- Add logging for tool calls, user approvals, errors, and permission denials.
- Prefer official SDKs and follow the current specification version when building production servers.

### Learning checklist

- [ ] Explain host, client, and server roles.
- [ ] Distinguish resources, prompts, and tools.
- [ ] Understand MCP initialization and capability negotiation.
- [ ] Build or run a minimal local MCP server.
- [ ] Connect one MCP client to the server and inspect available tools.
- [ ] Add a read-only resource and a write-capable tool.
- [ ] Implement user approval before a sensitive action.
- [ ] Review transport, authentication, logging, and credential boundaries.
- [ ] Test prompt-injection and tool-confusion cases before production use.

## 繁體中文

### 概覽

Model Context Protocol（MCP）是一個開放協定，用來把 AI 應用程式連接到外部系統。與其為每個模型、應用與資料來源各自撰寫專用 connector，MCP 提供一套共通方式，讓 AI host 能發現並使用 MCP server 暴露的能力。

實務上，MCP 是 agent 的整合層，涵蓋 tools、resources、prompts 與 workflows。程式助理可以透過 MCP server 存取 GitHub issues，聊天助理可以查詢資料庫，桌面 agent 可以操作本機檔案或應用程式，且都使用共同的 client-server 協定。

### 為什麼重要

- **可重用整合：** 同一個 MCP server 可服務多個相容 client，不必為每個 app 做一次 plugin。
- **更清楚的 agent 架構：** 工具與資料存取被放在明確的 server 邊界後方。
- **生態可攜性：** 多個 AI client、開發工具與 server 實作已支援 MCP。
- **治理能力更好：** Host 可以檢查 server 能力，要求使用者同意，並在敏感操作前套用政策。
- **可組合工作流：** Resources、prompts 與 tools 可組合出更豐富的 agent 行為，而不必把所有流程硬寫進 prompt。

### 架構/概念

| 概念 | 說明 |
| --- | --- |
| Host | 使用者互動的 AI 應用，例如 IDE、桌面助理或聊天產品。 |
| Client | Host 內部的連接器，通常維持一條到一個 server 的 MCP 連線。 |
| Server | 暴露能力給 host 的本機程序或遠端服務。 |
| Resources | 模型或使用者可讀取的資料與上下文，例如檔案、紀錄、文件或資料庫列。 |
| Prompts | Server 提供給使用者與 host 的可重用範本或工作流。 |
| Tools | 讓模型要求執行動作或計算的可呼叫函式。 |
| Sampling | Client 功能，讓 server 在受控情況下透過 host 要求 LLM completion。 |
| Roots | 檔案系統或 URI 邊界，協助 server 理解可操作範圍。 |
| Elicitation | Server 透過 client 向使用者要求缺少資訊的機制。 |

基礎協定使用 JSON-RPC 2.0 與具狀態連線。MCP 在啟動時支援 capability negotiation，讓 client 與 server 協調可用功能。常見 transport 包含桌面工具的本機程序連線，以及遠端 server 使用的 HTTP 類型傳輸。

MCP 很強大，因為 server 可能暴露任意資料存取與程式執行路徑。Host 應將 tool description、resource content 與 server 提供文字視為不可信，除非 server 本身可信。使用者同意、最小權限、稽核記錄與清楚批准 UI 都是核心設計需求。

### 實務使用

當整合需要跨多個 agent client 重用時，適合使用 MCP：

| 場景 | MCP 適合度 | 備註 |
| --- | --- | --- |
| 內部知識庫存取 | 高 | 暴露搜尋與文件 resources，並加上存取控制。 |
| 開發工具 | 高 | Source control、issue tracker、CI、code search、設計工具都適合映射成 tools 與 resources。 |
| 本機桌面自動化 | 高但敏感 | 檔案或 app 操作前需嚴格權限與明確批准。 |
| 單一私有 app endpoint | 視情況 | 若只會被一個模型 app 使用，直接 function call 可能更簡單。 |
| 高風險寫入操作 | 可用但需控制 | 必須加入確認、憑證範圍限制與 server-side authorization。 |

實作建議：

- 設計小型、命名清楚、input schema 明確且輸出穩定的 tools。
- 將唯讀 resources 與可寫入 tools 分開。
- 依使用者與 server 限縮憑證，不要讓所有工具共用廣泛 service token。
- 即使模型產生結構化參數，也必須在 server-side 驗證輸入。
- 優先回傳結構化資料，方便 host 或模型推理。
- 記錄 tool calls、使用者批准、錯誤與權限拒絕。
- 生產 server 優先使用官方 SDK，並依目前規格版本實作。

### 學習檢核表

- [ ] 說明 host、client、server 的角色。
- [ ] 區分 resources、prompts、tools。
- [ ] 理解 MCP 初始化與 capability negotiation。
- [ ] 建立或執行最小本機 MCP server。
- [ ] 連接一個 MCP client 並檢查可用 tools。
- [ ] 加入唯讀 resource 與可寫入 tool。
- [ ] 在敏感操作前加入使用者批准。
- [ ] 檢查 transport、authentication、logging 與 credential 邊界。
- [ ] 上線前測試 prompt injection 與 tool confusion 風險。

## References

- [Model Context Protocol: What is MCP?](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Model Context Protocol Specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)
- [MCP Architecture](https://modelcontextprotocol.io/docs/getting-started/architecture)
- [MCP Server Features: Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [MCP GitHub organization](https://github.com/modelcontextprotocol)
