# Claude Desktop

| Field | Details |
| --- | --- |
| Category | Desktop AI assistant with local tool and data integrations |
| Developer | Anthropic |
| Primary use | Use Claude from a native desktop app, connect local MCP servers, and install desktop extensions |
| Interfaces | macOS app, Windows app, Claude web, local MCP servers, Desktop Extensions |
| Platforms | macOS 11+ and Windows 10+ |
| Current status | Claude Desktop and MCP support are described by Anthropic as beta features |
| Best fit | Users who want Claude integrated with local files, desktop workflows, and MCP-based tools without building a custom app |
| Last reviewed | 2026-04-29 |

## English

### Overview

Claude Desktop is Anthropic's native desktop app for using Claude on macOS and Windows. It brings Claude closer to local workflows and is the main consumer surface where many users first encounter Model Context Protocol (MCP) integrations and Desktop Extensions.

The key distinction from the web app is local integration. Claude Desktop can connect to MCP servers and install Desktop Extensions, which package local tool integrations into installable `.dxt` bundles. This makes it practical to connect Claude to files, desktop apps, calendars, email, messaging, and other local or enterprise tools, subject to permissions and policies.

### Why it matters

LLM assistants become more useful when they can safely see and act on the context around a user. Claude Desktop is important because it gives non-developers and developers a more approachable way to attach local capabilities to Claude without manually wiring every integration into a custom application.

For teams, the security model matters as much as the assistant. Desktop Extensions and MCP servers can expose sensitive files, credentials, messages, and application actions. Good usage requires explicit permission boundaries, trusted extension sources, review of local server code, and enterprise policy controls where available.

### Architecture/Concepts

- **Native app:** Claude runs in a desktop application rather than only in the browser.
- **MCP client:** Claude Desktop can connect to local MCP servers that expose tools, resources, and prompts.
- **Desktop Extensions:** DXT packages make MCP-based local integrations easier to install and manage.
- **Extension directory:** Claude Desktop includes an Extensions area for browsing or managing available extensions.
- **Local permissions:** integrations may require access to files, apps, or credentials on the user's machine.
- **Secure packaging:** Anthropic describes Desktop Extensions as supporting features such as code signing, encrypted secret storage, and enterprise policy controls.
- **Beta status:** MCP and Desktop Extensions are powerful but should be treated as evolving platform features.

### Practical usage

Install Claude Desktop from Anthropic's downloads page, then sign in with a Claude account. For local integrations:

- Open Settings > Extensions.
- Install trusted Desktop Extensions from the directory or a verified `.dxt` package.
- Review requested permissions before enabling an extension.
- Use local MCP servers only from trusted maintainers or source code you can inspect.
- Keep API keys and app credentials in the extension's secure storage path where supported.
- Remove extensions that are no longer needed.

Good first integrations:

- Filesystem access limited to a specific project folder.
- Calendar or email summaries with read-only permissions.
- Local notes or knowledge base search.
- Developer tools that expose safe read-only project context.

Avoid broad filesystem, shell, browser, or credential access until you understand exactly what the extension or MCP server can do.

### Learning checklist

- [ ] Install Claude Desktop on macOS or Windows.
- [ ] Find Settings > Extensions.
- [ ] Explain what MCP does in Claude Desktop.
- [ ] Install one trusted Desktop Extension.
- [ ] Review extension permissions and remove unnecessary access.
- [ ] Connect a local MCP server in a test environment.
- [ ] Distinguish a tool, resource, and prompt exposed by MCP.
- [ ] Test a read-only local workflow before enabling write actions.
- [ ] Document approved extensions for a team or classroom.
- [ ] Track Anthropic updates because Desktop Extensions and MCP support are still evolving.

## 繁體中文

### 概覽

Claude Desktop 是 Anthropic 提供的 macOS 與 Windows 原生桌面 app，用來在桌面環境使用 Claude。它讓 Claude 更接近本機工作流，也是許多使用者接觸 Model Context Protocol（MCP）與 Desktop Extensions 的主要介面。

它和 web app 的關鍵差異在於本機整合。Claude Desktop 可連接 MCP servers，也能安裝 Desktop Extensions。Desktop Extensions 會把本機工具整合封裝成可安裝的 `.dxt` bundle，讓 Claude 在權限與政策允許下連接檔案、桌面 app、行事曆、email、訊息與企業工具。

### 為什麼重要

LLM assistant 如果能安全地理解並操作使用者周遭脈絡，實用性會大幅提高。Claude Desktop 的重要性在於，它讓開發者與非開發者都能用較容易的方式把本機能力接到 Claude，而不必為每個整合自行開發應用程式。

對團隊而言，安全模型和助理能力一樣重要。Desktop Extensions 與 MCP servers 可能暴露敏感檔案、憑證、訊息與應用程式動作。良好使用方式需要明確權限邊界、可信 extension 來源、審查本機 server 程式碼，以及在可用時套用企業政策控制。

### 架構/概念

- **Native app：** Claude 在桌面應用程式中執行，而不只是瀏覽器介面。
- **MCP client：** Claude Desktop 可連接本機 MCP servers，使用其 tools、resources 與 prompts。
- **Desktop Extensions：** DXT packages 讓基於 MCP 的本機整合更容易安裝與管理。
- **Extension directory：** Claude Desktop 提供 Extensions 區域，用於瀏覽或管理 extensions。
- **本機權限：** 整合可能需要存取使用者機器上的檔案、app 或 credentials。
- **安全封裝：** Anthropic 說明 Desktop Extensions 支援 code signing、加密 secret storage 與 enterprise policy controls 等能力。
- **Beta 狀態：** MCP 與 Desktop Extensions 很強大，但仍應視為持續演進的平台功能。

### 實務使用

從 Anthropic 下載頁安裝 Claude Desktop，並使用 Claude 帳號登入。使用本機整合時：

- 開啟 Settings > Extensions。
- 從 directory 或可信 `.dxt` package 安裝 Desktop Extensions。
- 啟用前審查要求的權限。
- 只使用可信維護者或可檢查原始碼的 local MCP servers。
- 在支援時，把 API keys 與 app credentials 放在 extension 的安全儲存方式中。
- 移除不再需要的 extensions。

適合的第一批整合：

- 限制在特定 project folder 的 filesystem access。
- 只讀權限的 calendar 或 email summaries。
- 本機 notes 或 knowledge base search。
- 只暴露安全 read-only project context 的開發工具。

在理解 extension 或 MCP server 能做什麼之前，不建議授予廣泛 filesystem、shell、browser 或 credential access。

### 學習檢核表

- [ ] 在 macOS 或 Windows 安裝 Claude Desktop。
- [ ] 找到 Settings > Extensions。
- [ ] 說明 MCP 在 Claude Desktop 中的作用。
- [ ] 安裝一個可信 Desktop Extension。
- [ ] 審查 extension 權限並移除不必要 access。
- [ ] 在測試環境連接 local MCP server。
- [ ] 區分 MCP 暴露的 tool、resource 與 prompt。
- [ ] 先測試 read-only 本機 workflow，再啟用 write actions。
- [ ] 為團隊或課堂記錄核准的 extensions。
- [ ] 持續追蹤 Anthropic 更新，因為 Desktop Extensions 與 MCP support 仍在演進。

## References

- [Installing Claude Desktop - Anthropic Help Center](https://support.anthropic.com/en/articles/10065433-installing-claude-desktop)
- [Getting started with Local MCP Servers on Claude Desktop - Anthropic Help Center](https://support.anthropic.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Code overview - Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/overview)
