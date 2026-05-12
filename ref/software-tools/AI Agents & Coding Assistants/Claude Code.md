# Claude Code

| Field | Details |
| --- | --- |
| Category | Agentic coding assistant |
| Developer | Anthropic |
| Primary use | Read codebases, edit files, run commands, automate development tasks, and integrate with developer tools |
| Interfaces | Terminal CLI, IDE integrations, desktop app, browser, SDK, GitHub/CI workflows |
| Requirements | Node.js 18+ for standard CLI installation; supported OS depends on interface |
| Account model | Claude.ai subscription or Anthropic Console account; provider options vary by surface |
| Best fit | Developers who want an agent that can work inside existing terminal and repository workflows |
| Last reviewed | 2026-04-29 |

## English

### Overview

Claude Code is Anthropic's agentic coding tool. It can understand a repository, answer questions about code, edit files, run commands, debug failures, write tests, automate repetitive tasks, and integrate with tools through MCP and related developer workflows.

The original center of gravity is the terminal: install the CLI, move into a project, run `claude`, and collaborate with the agent in the same environment where builds, tests, linters, and Git commands already run. By 2026, Anthropic also describes Claude Code as available across terminal, IDE, desktop app, and browser surfaces.

### Why it matters

Claude Code is important because it treats coding assistance as an execution loop, not just code suggestion. The agent can inspect the repository, form a plan, modify multiple files, run commands, observe errors, and iterate. This fits real engineering tasks such as small feature work, bug fixes, test creation, CI repair, release notes, migration steps, and codebase Q&A.

The risk profile is also higher than autocomplete. A tool that can edit files and run commands needs repository hygiene, version control discipline, secrets protection, command permission controls, and human review before deployment.

### Architecture/Concepts

- **CLI agent:** the `claude` command opens an interactive coding session in the current project.
- **Repository context:** Claude Code can inspect project structure and files to answer questions or make changes.
- **Tool execution:** it can edit files, run shell commands, and use configured tools subject to permissions.
- **MCP integrations:** MCP lets Claude Code connect to external data sources and development tools.
- **Settings hierarchy:** configuration can live in user settings, project settings, local project settings, and enterprise policy settings.
- **Subagents:** specialized assistants can be configured as Markdown files with YAML frontmatter at user or project level.
- **Automation:** non-interactive prompt mode and CI usage allow Claude Code to perform scripted or background tasks.
- **Enterprise deployment:** Anthropic documents options for Anthropic API, Amazon Bedrock, and Google Vertex AI.

### Practical usage

Install the CLI:

```bash
npm install -g @anthropic-ai/claude-code
cd your-project
claude
```

Common workflows:

- Ask for a codebase tour before requesting edits.
- Have Claude write or update tests around the change.
- Let Claude run the test command, then inspect the failure and patch.
- Ask for a concise summary of changed files before review.
- Use project settings to document build, test, lint, and permission expectations.
- Use MCP only for sources and tools that are needed for the task.

Good first tasks:

- Explain a module or unfamiliar code path.
- Add one focused unit test.
- Fix a lint error.
- Update documentation for an existing API.
- Reproduce and patch a small bug with a known failing case.

### Learning checklist

- [ ] Install Claude Code and run `claude` in a test repository.
- [ ] Ask Claude to summarize repository structure before editing.
- [ ] Configure project-level settings in `.claude/settings.json`.
- [ ] Learn the difference between user, project, local, and enterprise settings.
- [ ] Run a small edit and inspect the Git diff manually.
- [ ] Ask Claude to run tests and explain failures.
- [ ] Configure one MCP integration.
- [ ] Create one project subagent for a specialized review or test-writing role.
- [ ] Practice non-interactive prompt mode for a low-risk scripted task.
- [ ] Keep human review and CI checks as required gates before merge or deploy.

## 繁體中文

### 概覽

Claude Code 是 Anthropic 的 agentic coding tool。它能理解 repository、回答程式碼問題、編輯檔案、執行命令、除錯失敗、撰寫測試、自動化重複任務，並透過 MCP 與其他開發工具整合。

它最早的核心介面是終端機：安裝 CLI、進入專案、執行 `claude`，就能在原本執行 build、test、lint、Git 命令的環境中與 Agent 協作。到 2026 年，Anthropic 也描述 Claude Code 可用於 terminal、IDE、desktop app 與 browser 等介面。

### 為什麼重要

Claude Code 的重要性在於，它把 coding assistance 當成可執行的迭代迴圈，而不只是程式碼建議。Agent 可以檢查 repository、形成計畫、修改多個檔案、執行命令、觀察錯誤並繼續修正。這很適合小功能、bug fix、測試建立、CI 修復、release notes、migration steps 與 codebase Q&A。

風險也比 autocomplete 高。能編輯檔案與執行命令的工具，需要良好的 repository hygiene、版本控制習慣、secrets 保護、command permission controls，以及部署前的人類 review。

### 架構/概念

- **CLI agent：** `claude` 命令會在目前專案中開啟互動式 coding session。
- **Repository context：** Claude Code 可檢查專案結構與檔案，用於回答問題或進行修改。
- **Tool execution：** 在權限允許下，它可編輯檔案、執行 shell commands 並使用設定好的工具。
- **MCP integrations：** MCP 讓 Claude Code 可連接外部資料來源與開發工具。
- **Settings hierarchy：** 設定可位於 user settings、project settings、local project settings 與 enterprise policy settings。
- **Subagents：** 可用帶 YAML frontmatter 的 Markdown 檔，在 user 或 project 層級設定專門助理。
- **Automation：** non-interactive prompt mode 與 CI usage 可讓 Claude Code 執行 scripted 或背景任務。
- **Enterprise deployment：** Anthropic 文件提供 Anthropic API、Amazon Bedrock 與 Google Vertex AI 等部署選項。

### 實務使用

安裝 CLI：

```bash
npm install -g @anthropic-ai/claude-code
cd your-project
claude
```

常見工作流：

- 在要求修改前，先請 Claude 說明 codebase 結構。
- 請 Claude 針對變更撰寫或更新測試。
- 讓 Claude 執行測試命令，再根據 failure 修補。
- Review 前請 Claude 總結變更檔案。
- 用 project settings 記錄 build、test、lint 與權限期待。
- MCP 只連接任務真正需要的來源與工具。

適合的第一批任務：

- 說明一個 module 或陌生 code path。
- 新增一個聚焦的 unit test。
- 修正 lint error。
- 更新既有 API 文件。
- 用已知 failing case 重現並修正小 bug。

### 學習檢核表

- [ ] 安裝 Claude Code，並在測試 repository 中執行 `claude`。
- [ ] 修改前先請 Claude 摘要 repository structure。
- [ ] 在 `.claude/settings.json` 設定 project-level settings。
- [ ] 理解 user、project、local、enterprise settings 的差異。
- [ ] 進行小修改並手動檢查 Git diff。
- [ ] 請 Claude 執行測試並說明 failures。
- [ ] 設定一個 MCP integration。
- [ ] 建立一個用於專門 review 或 test writing 的 project subagent。
- [ ] 用 non-interactive prompt mode 練習低風險 scripted task。
- [ ] 保留 human review 與 CI checks 作為 merge 或 deploy 前的必要 gate。

## References

- [Claude Code overview - Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Set up Claude Code - Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/getting-started)
- [Claude Code settings - Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Claude Code Docs](https://code.claude.com/docs)
- [Model Context Protocol](https://modelcontextprotocol.io/)
