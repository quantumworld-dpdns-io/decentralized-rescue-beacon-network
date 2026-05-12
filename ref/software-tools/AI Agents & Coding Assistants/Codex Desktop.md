# Codex Desktop

| Field | Details |
| --- | --- |
| Category | Desktop command center for AI coding agents |
| Developer | OpenAI |
| Primary use | Supervise multiple Codex agents across projects, review diffs, use worktrees, and manage long-running coding tasks |
| Interfaces | Native desktop app, Codex CLI, IDE extensions, web/cloud Codex |
| Platforms | macOS launch in February 2026; Windows availability announced in March 2026 |
| Account model | ChatGPT plans with Codex access; availability and rate limits vary by plan and promotion |
| Best fit | Developers coordinating several agentic coding tasks across local projects and cloud environments |
| Last reviewed | 2026-04-29 |

## English

### Overview

Codex Desktop is OpenAI's native desktop interface for Codex, the agentic coding system available across app, CLI, IDE extension, and cloud surfaces. OpenAI introduced the Codex app for macOS on February 2, 2026, and later updated the announcement to state that Windows support became available on March 4, 2026.

The app is designed as a command center for coding agents. Instead of focusing on a single chat or autocomplete panel, it helps users run multiple agent tasks in parallel, keep work isolated with worktrees, review changes in context, comment on diffs, and continue work across the Codex CLI and IDE extension.

### Why it matters

Agentic coding shifted developer work from "ask for a snippet" to "delegate a scoped task and review the result." That creates coordination problems: several agents may work on the same repository, each task needs a review trail, and long-running changes need isolation from the developer's active branch.

Codex Desktop matters because it makes that supervision workflow explicit. The app gives developers a project/thread model for agent work, keeps changes separated, and uses the same Codex configuration and history as other Codex surfaces. For teams, the important design questions become repository access, approval rules, sandbox policy, review expectations, and when to delegate versus pair locally.

### Architecture/Concepts

- **Agent threads:** each delegated task runs in a thread with its own context, conversation, and change history.
- **Projects:** threads are organized by project so work can continue across repositories without losing state.
- **Worktree isolation:** agents can work in separate Git worktrees, allowing parallel changes without directly modifying the user's active checkout.
- **Diff review:** users can inspect changes, comment on diffs, and decide whether to continue, edit manually, or bring changes into their local workflow.
- **Shared Codex configuration:** the desktop app can pick up session history and configuration from the Codex CLI and IDE extension.
- **Sandboxing and approvals:** Codex uses system-level sandboxing and asks for elevated permission for actions such as broader filesystem or network access, depending on configuration.
- **Skills and automations:** Codex supports reusable capabilities and scheduled/background agent work for repeatable engineering tasks.

### Practical usage

Use Codex Desktop when you need to supervise several scoped coding tasks at once:

- Create a project for the repository or workspace.
- Start separate threads for independent tasks such as a bug fix, refactor, test expansion, or documentation update.
- Let each agent work in an isolated worktree.
- Review diffs before merging or applying changes.
- Open the work in an editor when human edits are faster than further prompting.
- Codify repeated team workflows as Skills where appropriate.
- Use automation only for low-risk recurring tasks with clear review gates.

Good first tasks:

- Add tests around an existing function.
- Fix a localized UI or API bug.
- Update documentation after a small code change.
- Investigate a CI failure and propose a patch.
- Refactor a small module with a clear acceptance criterion.

Avoid delegating broad, ambiguous rewrites until the repository has clear setup instructions, tests, approval rules, and review habits. Codex can move quickly, so the human review loop remains part of the engineering system.

### Learning checklist

- [ ] Install and sign in to the Codex desktop app.
- [ ] Confirm Codex CLI and IDE extension configuration is shared as expected.
- [ ] Start one project and one small task thread.
- [ ] Review a diff produced by an agent before applying it.
- [ ] Practice opening an agent worktree in the editor.
- [ ] Configure command approval rules for the project.
- [ ] Create or use one Skill for a recurring workflow.
- [ ] Try two independent tasks in parallel on the same repository.
- [ ] Document how your team should review Codex-produced changes.
- [ ] Track plan availability and rate limits because Codex access changes by subscription and rollout.

## 繁體中文

### 概覽

Codex Desktop 是 OpenAI 為 Codex 提供的原生桌面介面。Codex 是可跨 app、CLI、IDE extension 與 cloud 使用的 agentic coding system。OpenAI 在 2026 年 2 月 2 日推出 macOS 版 Codex app，並在公告更新中說明 Windows 版已於 2026 年 3 月 4 日開放。

這個 app 的定位是 coding agents 的 command center。它不是單一聊天窗或 autocomplete 面板，而是讓使用者平行執行多個 Agent 任務、用 worktrees 隔離變更、檢視 diff、在 diff 上留言，並延續 CLI 與 IDE extension 的工作流。

### 為什麼重要

Agentic coding 讓開發者從「請 AI 寫一段程式」轉向「把明確任務委派給 Agent，然後審查結果」。這會帶來協調問題：多個 Agent 可能同時處理同一個 repository，每個任務需要 review trail，長時間工作也需要和開發者目前分支隔離。

Codex Desktop 的重要性在於把監督多個 Agent 的工作流明確化。它提供 project/thread 模型、隔離變更，並沿用 Codex CLI 與 IDE extension 的設定與歷史。對團隊而言，重點會變成 repository access、approval rules、sandbox policy、review expectations，以及哪些工作該委派、哪些該在本機 pair。

### 架構/概念

- **Agent threads：** 每個委派任務都有自己的 thread、脈絡、對話與變更歷史。
- **Projects：** threads 依 project 組織，方便跨 repository 延續工作。
- **Worktree isolation：** Agent 可在獨立 Git worktree 中工作，平行變更不會直接修改使用者目前 checkout。
- **Diff review：** 使用者可檢查變更、評論 diff，並決定繼續提示、手動修改或帶回本機流程。
- **共享 Codex 設定：** Desktop app 可沿用 Codex CLI 與 IDE extension 的 session history 與 configuration。
- **Sandboxing 與 approvals：** Codex 使用系統層級 sandboxing，對較高權限動作依設定要求批准，例如更廣 filesystem 或 network access。
- **Skills 與 automations：** Codex 支援可重用能力與排程/背景 Agent 工作，用於重複工程任務。

### 實務使用

適合在需要同時監督多個清楚範圍的 coding tasks 時使用 Codex Desktop：

- 為 repository 或 workspace 建立 project。
- 為 bug fix、refactor、test expansion 或 documentation update 建立獨立 threads。
- 讓每個 Agent 在隔離 worktree 中工作。
- 合併或套用前先 review diff。
- 當手動修改比繼續提示更快時，在 editor 中開啟工作。
- 將重複團隊流程整理成 Skills。
- 只對低風險、具明確 review gate 的例行工作使用 automation。

適合的第一批任務：

- 為既有函式補測試。
- 修正局部 UI 或 API bug。
- 在小型程式變更後更新文件。
- 調查 CI failure 並提出 patch。
- 依明確 acceptance criteria 重構小模組。

在 repository 尚未具備清楚 setup instructions、tests、approval rules 與 review habits 前，不建議委派範圍過大或含糊的重寫。Codex 可以很快產生變更，因此人工 review 仍然是工程系統的一部分。

### 學習檢核表

- [ ] 安裝並登入 Codex desktop app。
- [ ] 確認 Codex CLI 與 IDE extension 設定能如預期共享。
- [ ] 建立一個 project 與一個小型 task thread。
- [ ] 在套用前 review Agent 產生的 diff。
- [ ] 練習在 editor 中開啟 Agent worktree。
- [ ] 為專案設定 command approval rules。
- [ ] 建立或使用一個 recurring workflow 的 Skill。
- [ ] 在同一 repository 上平行執行兩個獨立任務。
- [ ] 記錄團隊如何 review Codex 產生的變更。
- [ ] 追蹤 plan availability 與 rate limits，因為 Codex access 會依訂閱與 rollout 改變。

## References

- [Introducing the Codex app - OpenAI](https://openai.com/index/introducing-the-codex-app/)
- [Codex - OpenAI](https://openai.com/codex)
- [Using Codex with your ChatGPT plan - OpenAI Help Center](https://help.openai.com/en/articles/11369540)
- [OpenAI Codex CLI - Getting Started](https://help.openai.com/en/articles/11096431-openai-codex-ci-getting-started)
- [Codex use cases - OpenAI Developers](https://developers.openai.com/codex/use-cases)
