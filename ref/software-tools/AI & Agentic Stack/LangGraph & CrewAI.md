# LangGraph & CrewAI

| Field | Details |
| --- | --- |
| Category | AI agent orchestration and multi-agent workflow frameworks |
| Tools | LangGraph, CrewAI |
| Primary use | Build stateful agent workflows, human-in-the-loop loops, and multi-agent task automation |
| Languages | LangGraph: Python and JavaScript/TypeScript; CrewAI: Python |
| Licensing | LangGraph: MIT; CrewAI: MIT |
| Best fit | Teams moving beyond one-shot prompts into repeatable, observable, recoverable agent systems |
| Last reviewed | 2026-04-29 |

## English

### Overview

LangGraph and CrewAI are open-source frameworks for building agentic systems, but they optimize for different levels of control.

| Framework | Core idea | Strengths | Typical fit |
| --- | --- | --- | --- |
| LangGraph | Model an agent or workflow as a graph of stateful steps. | Durable execution, explicit state, branching, cycles, streaming, human review, memory, and low-level orchestration. | Production agent runtimes where control flow, recovery, and state inspection matter. |
| CrewAI | Define agents, tasks, crews, and flows for collaborative automation. | Role-based agent teams, task delegation, tools, memory, knowledge sources, guardrails, and event-driven flows. | Multi-agent task execution where clear roles and high-level collaboration abstractions help teams move quickly. |

LangGraph is best understood as a low-level runtime for stateful agent workflows. You define nodes, edges, state, and transitions directly. CrewAI is more opinionated: you describe agents, tasks, and collaboration patterns, then use Crews and Flows to orchestrate the work.

### Why it matters

Simple prompt chains are often enough for demos, but production agent systems usually need more:

- State that persists across turns, tools, users, and failures.
- Conditional paths when the next step depends on model output, tool results, or human approval.
- Loops for retry, critique, self-correction, research, planning, or evaluator-optimizer patterns.
- Observability for debugging tool calls, state changes, latency, and cost.
- Guardrails so autonomous systems can be interrupted, reviewed, resumed, or constrained.

LangGraph and CrewAI make these concerns explicit. They help developers turn loose LLM calls into auditable workflows with defined responsibilities, checkpoints, and integration points.

### Architecture/Concepts

#### LangGraph

Key concepts:

- **State**: shared data passed through the graph, such as messages, intermediate findings, tool outputs, or workflow metadata.
- **Nodes**: functions or agent steps that read state and return updates.
- **Edges**: transitions between nodes. Edges can be fixed or conditional.
- **Cycles**: loops that allow reflection, retry, refinement, or multi-step tool use.
- **Checkpointers and persistence**: stores that enable durable execution and resuming from saved state.
- **Human-in-the-loop**: interruption points where people can inspect or modify state before continuing.
- **LangSmith integration**: tracing and debugging support for complex agent behavior.

Common LangGraph patterns:

- Prompt chaining: break a task into ordered model calls.
- Routing: send work to different nodes based on classification or state.
- Parallelization: run independent subtasks and merge results.
- Orchestrator-worker: let one controller assign work to specialized workers.
- Evaluator-optimizer: loop between a generator and reviewer until quality criteria are met.
- Stateful agent: combine LLM calls, tools, memory, and graph control flow.

#### CrewAI

Key concepts:

- **Agent**: an actor with a role, goal, backstory, tools, memory, knowledge, and optional reasoning behavior.
- **Task**: a clear unit of work with a description, expected output, assigned agent, and optional structured output.
- **Crew**: a team of agents that collaborate to complete tasks.
- **Process**: the collaboration pattern for tasks, such as sequential or hierarchical execution.
- **Flow**: an event-driven workflow layer for stateful orchestration and controlled execution.
- **Tools and knowledge**: external capabilities and retrieval sources available to agents.
- **Guardrails and human review**: controls for validating or pausing execution.

CrewAI separates two useful mental models:

- **Crews** emphasize autonomous collaboration among specialized agents.
- **Flows** emphasize precise, event-driven orchestration, state management, and production control.

### Practical usage

Use **LangGraph** when:

- You need exact control over state transitions and branching.
- The workflow may run for a long time and must resume after interruption.
- You need human approval or state editing at specific points.
- You are building custom agent architectures rather than using a high-level pattern.
- You want graph-based debugging and explicit execution paths.

Use **CrewAI** when:

- The problem naturally maps to roles such as researcher, analyst, writer, reviewer, or planner.
- You want to define agents and tasks quickly in Python or configuration.
- You need delegation, collaboration, memory, knowledge sources, and tools.
- You want a higher-level abstraction for multi-agent workflows.
- You want to combine autonomous Crews with more controlled Flows.

Example use cases:

| Scenario | Suggested tool | Reason |
| --- | --- | --- |
| Code generation with test writer, implementer, and reviewer agents | CrewAI or LangGraph | CrewAI fits role-based collaboration; LangGraph fits tighter control over loops and checkpoints. |
| Customer support triage with escalation approval | LangGraph | Strong fit for stateful routing, persistence, and human-in-the-loop review. |
| Market research report with researcher and analyst agents | CrewAI | Clear roles, tasks, tools, and expected outputs. |
| Long-running data enrichment pipeline with resumable steps | LangGraph | Durable execution and explicit graph state are central. |
| Business workflow automation with events and agent teams | CrewAI | Flows can coordinate controlled execution while Crews handle agent collaboration. |

Practical implementation tips:

- Start with the smallest reliable workflow, then add autonomy only where it improves outcomes.
- Keep state schemas explicit and avoid passing unstructured blobs between steps.
- Treat tool permissions, API credentials, and file access as security boundaries.
- Add human review before irreversible actions such as sending email, changing records, or deploying code.
- Log inputs, outputs, tool calls, and decisions for later debugging and evaluation.
- Write evaluation cases for common successes, expected failures, and edge cases.

### Learning checklist

- [ ] Explain the difference between a prompt chain, workflow, and agent.
- [ ] Build a minimal LangGraph `StateGraph` with two nodes and a conditional edge.
- [ ] Add checkpointing to a LangGraph workflow and resume an interrupted run.
- [ ] Add a human review step before a sensitive tool call.
- [ ] Define a CrewAI agent with role, goal, task, and expected output.
- [ ] Run a CrewAI crew with at least two specialized agents.
- [ ] Compare CrewAI Crews and CrewAI Flows for the same small workflow.
- [ ] Add one external tool or knowledge source safely.
- [ ] Trace a run and identify where state, tools, and model outputs changed.
- [ ] Document failure modes, retry policy, and approval requirements.

## 繁體中文

### 概覽

LangGraph 與 CrewAI 都是用來建立 Agentic AI 系統的開源框架，但兩者的抽象層級不同。

| 框架 | 核心概念 | 優勢 | 適合情境 |
| --- | --- | --- | --- |
| LangGraph | 將 Agent 或工作流建模為具狀態的圖。 | 持久化執行、明確狀態、分支、循環、串流、人類審核、記憶與低階編排。 | 需要控制流程、恢復能力與狀態檢查的生產級 Agent Runtime。 |
| CrewAI | 定義 Agents、Tasks、Crews 與 Flows 來進行協作式自動化。 | 角色型 Agent 團隊、任務委派、工具、記憶、知識來源、Guardrails 與事件驅動流程。 | 需要快速建立多 Agent 協作任務，且角色與責任清楚的場景。 |

LangGraph 可以視為低階、可控的狀態式 Agent 編排 Runtime。開發者直接定義節點、邊、狀態與轉移邏輯。CrewAI 則提供較高階的抽象，讓開發者以角色、任務與協作方式描述工作，再透過 Crews 與 Flows 執行。

### 為什麼重要

簡單的 Prompt Chain 足以支撐展示，但真正上線的 Agent 系統通常需要更多能力：

- 狀態必須能跨回合、工具、使用者與失敗情境保存。
- 下一步可能取決於模型輸出、工具結果或人工批准。
- 系統需要循環來重試、評論、自我修正、研究、規劃或進行 evaluator-optimizer 流程。
- 團隊需要可觀測性來除錯工具呼叫、狀態變化、延遲與成本。
- 自主系統必須能被中斷、審核、恢復或限制。

LangGraph 與 CrewAI 讓這些需求成為架構的一部分。它們能把零散的 LLM 呼叫整理成可審計、有責任邊界、有檢查點的工作流。

### 架構/概念

#### LangGraph

核心概念：

- **State（狀態）**：在圖中傳遞的共享資料，例如訊息、工具輸出、中間結果或流程中繼資料。
- **Nodes（節點）**：讀取狀態並回傳更新的函式或 Agent 步驟。
- **Edges（邊）**：節點之間的轉移，可為固定轉移或條件轉移。
- **Cycles（循環）**：支援反思、重試、修正或多步工具使用。
- **Checkpointers 與 Persistence（持久化）**：讓工作流能保存進度並從中斷點恢復。
- **Human-in-the-loop（人在迴路中）**：讓人可以在指定節點檢查或修改狀態後再繼續。
- **LangSmith 整合**：支援追蹤與除錯複雜 Agent 行為。

常見 LangGraph 模式：

- Prompt chaining：將任務拆成有順序的模型呼叫。
- Routing：依分類或狀態將工作導向不同節點。
- Parallelization：平行執行獨立子任務並合併結果。
- Orchestrator-worker：由控制者分派工作給專門的 Worker。
- Evaluator-optimizer：在產生器與審核器之間循環，直到品質達標。
- Stateful agent：結合 LLM、工具、記憶與圖形控制流程。

#### CrewAI

核心概念：

- **Agent**：具備角色、目標、背景、工具、記憶、知識與可選推理能力的執行者。
- **Task**：具有描述、預期輸出、指派 Agent 與可選結構化輸出的工作單位。
- **Crew**：由多個 Agent 組成、協作完成任務的團隊。
- **Process**：任務協作方式，例如 sequential 或 hierarchical。
- **Flow**：事件驅動的工作流層，用於狀態式編排與受控執行。
- **Tools 與 Knowledge**：Agent 可使用的外部能力與檢索來源。
- **Guardrails 與人工審核**：用於驗證、中止或審核執行結果。

CrewAI 有兩個重要心智模型：

- **Crews** 著重於專門 Agent 之間的自主協作。
- **Flows** 著重於精確的事件驅動編排、狀態管理與生產控制。

### 實務使用

適合使用 **LangGraph** 的情境：

- 需要精準控制狀態轉移與分支。
- 工作流可能長時間執行，且必須能從中斷點恢復。
- 需要在特定步驟加入人工批准或狀態修改。
- 要建立自訂 Agent 架構，而不是套用高階模式。
- 需要以圖形化、明確路徑來除錯執行流程。

適合使用 **CrewAI** 的情境：

- 問題自然對應到研究員、分析師、撰寫者、審查者或規劃者等角色。
- 想用 Python 或設定檔快速定義 Agents 與 Tasks。
- 需要任務委派、協作、記憶、知識來源與工具。
- 想使用較高階的多 Agent 工作流抽象。
- 想把自主 Crews 與更可控的 Flows 結合。

應用範例：

| 場景 | 建議工具 | 原因 |
| --- | --- | --- |
| 由測試撰寫、程式實作與 Code Review Agent 組成的程式生成流程 | CrewAI 或 LangGraph | CrewAI 適合角色協作；LangGraph 適合更嚴格的循環與檢查點控制。 |
| 客服分類與升級審核 | LangGraph | 適合狀態式路由、持久化與人工審核。 |
| 市場研究報告，由研究員與分析師協作 | CrewAI | 角色、任務、工具與預期輸出清楚。 |
| 可恢復的長時間資料補強流程 | LangGraph | 持久化執行與明確圖狀態是核心需求。 |
| 企業流程自動化，包含事件與 Agent 團隊 | CrewAI | Flows 可控制流程，Crews 可處理 Agent 協作。 |

實作建議：

- 從最小且可靠的工作流開始，只在確實改善結果時加入自主性。
- 明確定義狀態結構，避免在步驟間傳遞不透明的大型文字塊。
- 將工具權限、API 金鑰與檔案存取視為安全邊界。
- 在寄信、修改資料、部署程式等不可逆操作前加入人工審核。
- 記錄輸入、輸出、工具呼叫與決策，以便除錯與評估。
- 為常見成功案例、預期失敗與邊界情境建立評測案例。

### 學習檢查清單

- [ ] 說明 Prompt Chain、Workflow 與 Agent 的差異。
- [ ] 建立一個包含兩個節點與條件邊的最小 LangGraph `StateGraph`。
- [ ] 為 LangGraph 工作流加入 checkpoint，並從中斷點恢復。
- [ ] 在敏感工具呼叫前加入人工審核步驟。
- [ ] 定義 CrewAI Agent 的角色、目標、任務與預期輸出。
- [ ] 執行一個至少包含兩個專門 Agent 的 CrewAI Crew。
- [ ] 用同一個小型工作流比較 CrewAI Crews 與 CrewAI Flows。
- [ ] 安全地加入一個外部工具或知識來源。
- [ ] 追蹤一次執行，指出狀態、工具與模型輸出在哪些地方改變。
- [ ] 文件化失敗模式、重試策略與人工批准需求。

## References

- [LangGraph overview - LangChain Docs](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph durable execution - LangChain Docs](https://docs.langchain.com/oss/python/langgraph/durable-execution)
- [LangGraph workflows and agents - LangChain Docs](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
- [LangGraph GitHub repository](https://github.com/langchain-ai/langgraph)
- [LangGraph product page - LangChain](https://www.langchain.com/langgraph)
- [CrewAI documentation](https://docs.crewai.com/en)
- [CrewAI introduction](https://docs.crewai.com/en/introduction)
- [CrewAI open-source page](https://www.crewai.com/open-source)
- [CrewAI GitHub repository](https://github.com/crewAIInc/crewAI)
