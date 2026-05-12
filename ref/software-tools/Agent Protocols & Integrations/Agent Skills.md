# Agent Skills

| Field | Details |
| --- | --- |
| Category | Agent capability packaging, reusable instructions |
| Primary ecosystem | Open Agent Skills format, originally developed by Anthropic and used across skills-compatible agents |
| Primary use | Package domain expertise, workflows, scripts, templates, and reference materials for on-demand agent use |
| Core file | `SKILL.md` |
| Loading model | Progressive disclosure: metadata first, instructions when triggered, resources as needed |
| Best fit | Repeatable workflows that need more structure than a prompt but less integration overhead than a full tool server |
| Last reviewed | 2026-04-29 |

## English

### Overview

Agent Skills are modular capability packages that teach an agent how to perform a specialized task. The format was originally developed by Anthropic and has been published as an open, lightweight standard for skills-compatible agents. A Skill is a directory with a required `SKILL.md` file, YAML metadata, procedural instructions, and optional supporting files such as scripts, templates, examples, or reference documents.

Skills are different from one-off prompts. The agent discovers a Skill from its metadata, loads the full instructions only when relevant, and reads or executes supporting resources only when the task calls for them. This progressive-disclosure design lets teams install many Skills without putting all of their content into every conversation.

### Why it matters

- **Reusable expertise:** Teams can encode workflows once and reuse them across tasks.
- **Lower prompt repetition:** Users do not need to paste the same operating procedure into every session.
- **Context efficiency:** Only the matching Skill's instructions are loaded, and large resources stay out of context unless needed.
- **Deterministic helpers:** Scripts can perform reliable transformations, validation, rendering, or file operations.
- **Team consistency:** Project or organization Skills can capture style guides, compliance steps, build commands, and domain rules.

### Architecture/Concepts

| Concept | Meaning |
| --- | --- |
| `SKILL.md` | Required Markdown file containing YAML metadata and human-readable instructions. |
| `name` | Machine-readable Skill identifier, usually lowercase with hyphens. |
| `description` | Discovery text that tells the agent what the Skill does and when to use it. |
| Instructions | The main workflow guidance loaded when the Skill is triggered. |
| Resources | Supporting files such as schemas, templates, examples, policy docs, or detailed references. |
| Scripts | Executable helpers the agent can run for deterministic work. |
| Progressive disclosure | Loading only the metadata, instructions, and resources needed for the current task. |

A typical Skill structure:

```text
my-skill/
├── SKILL.md
├── references/
│   └── style-guide.md
├── templates/
│   └── report.md
└── scripts/
    └── validate.py
```

Good Skills read like onboarding notes for a capable teammate. They should say when to use the Skill, what workflow to follow, what files or scripts are available, and what quality bar must be met.

### Practical usage

Use a Skill when knowledge or workflow is reusable:

| Scenario | Skill fit | Notes |
| --- | --- | --- |
| Document generation | Strong | Combine instructions, templates, and validation scripts. |
| Project-specific coding workflow | Strong | Capture build commands, style rules, and review expectations. |
| Data analysis procedure | Strong | Include notebooks, scripts, schema notes, and chart conventions. |
| External API access | Maybe | Use a tool or MCP server when the agent must call live systems repeatedly. |
| High-risk automation | Use carefully | Add explicit approval steps and avoid hidden destructive scripts. |

Authoring tips:

- Make the `description` precise; it is the trigger surface.
- Keep `SKILL.md` focused and link to deeper references instead of loading everything upfront.
- Put repetitive or exact operations in scripts rather than prose.
- Include examples of good outputs and common failure cases.
- State prerequisites, expected inputs, generated outputs, and verification steps.
- Keep secrets out of Skill directories.
- Treat third-party Skills as untrusted code until reviewed.

### Learning checklist

- [ ] Explain how Skills differ from prompts, tools, and MCP servers.
- [ ] Create a minimal `SKILL.md` with `name` and `description`.
- [ ] Write trigger guidance that is specific but not overly broad.
- [ ] Add one reference file and load it only when needed.
- [ ] Add one deterministic script for validation or transformation.
- [ ] Test the Skill on a task that should trigger it and one that should not.
- [ ] Review a Skill for hidden data access, shell commands, and dependency risk.
- [ ] Decide whether a workflow belongs in a Skill, tool call, or MCP server.

## 繁體中文

### 概覽

Agent Skills 是模組化能力套件，用來教 agent 執行特定專業任務。這個格式最初由 Anthropic 發展，後來作為開放、輕量的標準提供給相容的 agents 使用。一個 Skill 是包含必要 `SKILL.md` 的資料夾，並可包含 YAML metadata、流程指引、scripts、templates、範例或參考文件。

Skills 不同於一次性 prompts。Agent 先透過 metadata 發現 Skill，只有在相關時才載入完整指引，並在任務需要時才讀取或執行支援資源。這種 progressive disclosure 設計讓團隊可以安裝許多 Skills，而不必把所有內容塞進每次對話。

### 為什麼重要

- **可重用專業知識：** 團隊可把工作流編碼一次，之後重複使用。
- **降低重複提示：** 使用者不必每次都貼上相同 SOP。
- **節省 context：** 只有符合任務的 Skill 指引會被載入，大型資源只有需要時才進入 context。
- **可預測 helper：** Scripts 可負責穩定的轉換、驗證、渲染或檔案操作。
- **團隊一致性：** Project 或 organization Skills 可保存 style guide、合規步驟、build commands 與領域規則。

### 架構/概念

| 概念 | 說明 |
| --- | --- |
| `SKILL.md` | 必要 Markdown 檔，包含 YAML metadata 與人可讀指引。 |
| `name` | 機器可讀 Skill 識別碼，通常使用小寫與 hyphen。 |
| `description` | Discovery 文字，告訴 agent Skill 做什麼、何時使用。 |
| Instructions | Skill 被觸發時載入的主要流程指引。 |
| Resources | 支援檔案，例如 schemas、templates、examples、policy docs 或詳細參考。 |
| Scripts | Agent 可執行的 deterministic helpers。 |
| Progressive disclosure | 只載入當前任務需要的 metadata、instructions 與 resources。 |

典型 Skill 結構：

```text
my-skill/
├── SKILL.md
├── references/
│   └── style-guide.md
├── templates/
│   └── report.md
└── scripts/
    └── validate.py
```

好的 Skill 應像寫給有能力隊友的 onboarding notes。它應說明何時使用、遵循什麼流程、有哪些檔案或 scripts 可用，以及品質標準是什麼。

### 實務使用

當知識或流程可重複使用時，適合使用 Skill：

| 場景 | Skill 適合度 | 備註 |
| --- | --- | --- |
| 文件產生 | 高 | 結合 instructions、templates 與 validation scripts。 |
| 專案特定 coding workflow | 高 | 保存 build commands、style rules 與 review expectations。 |
| 資料分析程序 | 高 | 包含 notebooks、scripts、schema notes 與圖表慣例。 |
| 外部 API 存取 | 視情況 | 若 agent 需反覆呼叫 live systems，工具或 MCP server 更適合。 |
| 高風險自動化 | 謹慎使用 | 加入明確批准步驟，避免隱藏破壞性 scripts。 |

撰寫建議：

- 讓 `description` 精準，因為它是觸發依據。
- 讓 `SKILL.md` 聚焦，將深入內容連到其他 reference，而不是一次載入全部。
- 將重複或需要精確執行的操作放進 scripts，而不是只靠文字描述。
- 提供好輸出範例與常見失敗情境。
- 寫明 prerequisites、expected inputs、generated outputs 與 verification steps。
- 不要把 secrets 放進 Skill 目錄。
- 第三方 Skills 在審查前都應視為不可信程式碼。

### 學習檢核表

- [ ] 說明 Skills 與 prompts、tools、MCP servers 的差異。
- [ ] 建立含 `name` 與 `description` 的最小 `SKILL.md`。
- [ ] 撰寫明確但不過度寬泛的觸發說明。
- [ ] 加入一個 reference file，且只在需要時載入。
- [ ] 加入一個用於驗證或轉換的 deterministic script。
- [ ] 用應觸發與不應觸發的任務測試 Skill。
- [ ] 檢查 Skill 是否隱含資料存取、shell commands 與 dependency 風險。
- [ ] 判斷某個 workflow 應放在 Skill、tool call 或 MCP server。

## References

- [Claude Docs: Agent Skills overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Agent Skills open format](https://agentskills.io/)
- [Claude Docs: Agent Skills in Claude Code](https://docs.claude.com/en/docs/claude-code/skills)
- [Claude API Docs: Skills](https://platform.claude.com/docs/en/managed-agents/skills)
- [Anthropic Engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Model Context Protocol: Build with Agent Skills](https://modelcontextprotocol.io/docs/develop/build-with-agent-skills)
