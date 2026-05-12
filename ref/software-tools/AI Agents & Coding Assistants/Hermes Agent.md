# Hermes Agent

| Field | Details |
| --- | --- |
| Category | Open-source autonomous AI agent and personal automation runtime |
| Developer | Nous Research |
| Primary use | Run a persistent agent from CLI or messaging apps, with tools, memory, skills, subagents, and scheduled automations |
| Interfaces | Terminal UI, messaging gateway, local dashboard, MCP, editor integrations through Agent Communication Protocol |
| Deployment | Linux, macOS, WSL2, Android via Termux; local machine, VPS, Docker, SSH, Daytona, Singularity, Modal |
| Licensing | MIT |
| Best fit | Users who want a self-hosted, model-agnostic agent that can live on their own infrastructure instead of only inside an IDE |
| Last reviewed | 2026-04-29 |

## English

### Overview

Hermes Agent is an open-source AI agent from Nous Research. It is designed to run as a persistent assistant on a laptop, server, VPS, or cloud backend while users interact with it from a terminal or messaging channels such as Telegram, Discord, Slack, WhatsApp, Signal, email, or CLI.

Its 2026-facing positioning is broader than a coding autocomplete tool. Hermes combines a terminal agent, messaging gateway, tool system, persistent memory, skills, scheduled jobs, model routing, and isolated subagents. The project emphasizes self-hosting, model choice, and a learning loop where the agent can preserve useful knowledge and improve reusable skills over time.

### Why it matters

Most coding assistants are tied to one surface: an IDE, a web app, or a vendor-hosted cloud workspace. Hermes is useful when the agent should keep working somewhere durable and reachable from multiple channels. A developer can run it on a low-cost server, connect tools and providers, schedule reports or audits, and continue conversations from a phone while the agent executes in its configured environment.

Hermes also matters for agent research and advanced automation. It supports tool-calling workflows, MCP connections, terminal backends, subagent parallelism, skills, trajectory generation, and long-lived memory. The tradeoff is operational responsibility: because Hermes is self-hosted and tool-capable, users must manage secrets, command approvals, isolation, updates, and provider costs carefully.

### Architecture/Concepts

- **CLI/TUI:** the `hermes` command starts an interactive terminal interface with conversation history, slash commands, streaming tool output, and model/tool configuration.
- **Messaging gateway:** one gateway process can connect Hermes to chat platforms, so users can delegate work from messaging apps while execution happens on the configured host.
- **Model routing:** Hermes is model-agnostic and can use providers such as Nous Portal, OpenRouter, OpenAI, Anthropic, Kimi/Moonshot, MiniMax, z.ai/GLM, Hugging Face, and compatible custom endpoints.
- **Tools and toolsets:** tools cover terminal, filesystem, browser/search, media, MCP, and other agent capabilities. Toolsets help control what is enabled for a context.
- **Persistent memory and skills:** Hermes can store durable memory, search previous sessions, and use skills as reusable procedural knowledge.
- **Subagents:** large tasks can be split into isolated child agents with their own workspace and tool context.
- **Cron scheduling:** natural-language recurring jobs can run unattended and report back through configured channels.
- **Execution backends:** terminal sessions can run locally or through Docker, SSH, Daytona, Singularity, Modal, and related environments.

### Practical usage

Install from the official repository instructions:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.zshrc
hermes
```

Common commands:

- `hermes` starts an interactive session.
- `hermes setup` runs guided configuration.
- `hermes model` selects provider and model.
- `hermes tools` configures enabled tools.
- `hermes gateway` manages messaging integrations.
- `hermes update` updates the installation.
- `hermes doctor` checks common setup problems.

Good first workflows:

- Run Hermes locally with filesystem and shell permissions constrained to a test project.
- Configure one model provider and verify cost controls before enabling more tools.
- Add a messaging gateway only after the CLI workflow is stable.
- Use cron for low-risk recurring reports before scheduling write-capable jobs.
- Use Docker, SSH, or another isolated backend for tasks that run untrusted commands.

### Learning checklist

- [ ] Install Hermes and run `hermes doctor`.
- [ ] Configure one model provider and switch models with `hermes model`.
- [ ] Start a CLI session and learn `/new`, `/model`, `/skills`, `/usage`, and `/compress`.
- [ ] Enable only the tools needed for one small project.
- [ ] Configure the messaging gateway for one private channel.
- [ ] Create or use one skill for a repeatable workflow.
- [ ] Schedule a simple report with the cron system.
- [ ] Run a task in an isolated backend such as Docker or SSH.
- [ ] Review security settings, command approvals, and secret handling.
- [ ] Track release notes before upgrading because the project is changing quickly.

## 繁體中文

### 概覽

Hermes Agent 是 Nous Research 推出的開源 AI Agent。它可以長時間運行在筆電、伺服器、VPS 或雲端後端，使用者則能透過終端機或 Telegram、Discord、Slack、WhatsApp、Signal、email、CLI 等通道與它互動。

它在 2026 年的定位不只是程式補全工具，而是結合終端機 Agent、訊息 Gateway、工具系統、持久記憶、Skills、排程、自動化、模型路由與隔離 Subagents 的自架式 Agent Runtime。Hermes 強調自架、模型選擇，以及能把經驗保存成記憶與可重用技能的 learning loop。

### 為什麼重要

許多 coding assistant 綁定在單一介面，例如 IDE、Web app 或供應商雲端工作區。Hermes 適合需要 Agent 長時間待在可控環境中工作的情境。開發者可以把它部署在低成本伺服器上，接上工具與模型供應商，安排報告或稽核任務，並從手機訊息通道持續追蹤工作。

Hermes 也適合 Agent 研究與進階自動化。它支援 tool calling、MCP、terminal backends、subagent parallelism、skills、trajectory generation 與長期記憶。代價是使用者必須自己負責營運安全：包含 secrets、command approval、隔離、更新與模型成本。

### 架構/概念

- **CLI/TUI：** `hermes` 命令啟動互動式終端介面，支援對話歷史、slash commands、串流工具輸出與模型/工具設定。
- **Messaging Gateway：** 單一 gateway process 可連接多個聊天平台，讓使用者從訊息 App 指派工作，而實際執行發生在設定好的主機上。
- **模型路由：** Hermes 不綁定單一模型，可使用 Nous Portal、OpenRouter、OpenAI、Anthropic、Kimi/Moonshot、MiniMax、z.ai/GLM、Hugging Face 與相容 endpoint。
- **Tools 與 Toolsets：** 工具涵蓋 terminal、filesystem、browser/search、media、MCP 等能力；toolsets 用來控制不同情境可用工具。
- **持久記憶與 Skills：** Hermes 可保存長期記憶、搜尋過去 sessions，並用 skills 保存可重複使用的程序知識。
- **Subagents：** 大型任務可拆給彼此隔離的 child agents，各自有自己的工作區與工具脈絡。
- **Cron 排程：** 可用自然語言設定定期工作，並把結果送回指定通道。
- **執行後端：** 終端環境可在 local、Docker、SSH、Daytona、Singularity、Modal 等後端執行。

### 實務使用

依官方 repository 安裝：

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.zshrc
hermes
```

常用命令：

- `hermes` 啟動互動 session。
- `hermes setup` 執行設定精靈。
- `hermes model` 選擇 provider 與模型。
- `hermes tools` 設定可用工具。
- `hermes gateway` 管理訊息平台整合。
- `hermes update` 更新安裝。
- `hermes doctor` 檢查常見設定問題。

建議入門流程：

- 先在本機以受限 filesystem 與 shell 權限測試一個專案。
- 只設定一個模型供應商，確認成本與限制後再擴充。
- CLI 穩定後再加入 messaging gateway。
- 先用 cron 做低風險定期報告，再安排可寫入或可改動系統的工作。
- 對會執行不可信命令的任務使用 Docker、SSH 或其他隔離後端。

### 學習檢核表

- [ ] 安裝 Hermes 並執行 `hermes doctor`。
- [ ] 設定一個模型供應商，並用 `hermes model` 切換模型。
- [ ] 啟動 CLI session，熟悉 `/new`、`/model`、`/skills`、`/usage`、`/compress`。
- [ ] 只為一個小專案啟用必要工具。
- [ ] 為一個私人通道設定 messaging gateway。
- [ ] 建立或使用一個可重複 workflow 的 skill。
- [ ] 用 cron 排程一個簡單報告。
- [ ] 在 Docker 或 SSH 等隔離後端執行任務。
- [ ] 檢查安全設定、command approvals 與 secrets 管理。
- [ ] 升級前追蹤 release notes，因為專案仍快速變動。

## References

- [Hermes Agent GitHub repository - NousResearch](https://github.com/NousResearch/hermes-agent)
- [Hermes Agent releases - GitHub](https://github.com/NousResearch/hermes-agent/releases)
- [Hermes Agent overview](https://hermesagent.fyi/en/overview)
- [Nous Research GitHub organization](https://github.com/nousresearch)
