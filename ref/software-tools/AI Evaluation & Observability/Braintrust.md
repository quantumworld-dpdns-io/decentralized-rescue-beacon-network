# Braintrust

| Field | Details |
| --- | --- |
| Category | AI evaluation, experiment tracking, observability, prompt testing |
| Maintainer / ecosystem | Braintrust |
| Primary use | Build datasets, run evals, trace production AI behavior, compare experiments, and improve prompts or agents |
| Typical users | AI product engineers, evaluation engineers, ML platform teams, QA and product teams |
| Interfaces | Web UI, TypeScript SDK, Python SDK, Go SDK, Ruby SDK, CLI, API, MCP server |
| Common integrations | OpenAI, Anthropic, Gemini, AI frameworks, OpenTelemetry-style tracing, Autoevals |
| Best fit | Teams that want evaluation-driven AI development with traceable production feedback loops |
| Last reviewed | 2026-04-29 |

## English

### Overview

Braintrust is an AI evaluation and observability platform for systematically testing and improving LLM applications. It combines datasets, evals, scorers, experiments, tracing, playgrounds, annotations, and production logging.

The central idea is evaluation-driven development: define representative data, run the application as a task, score outputs with code or model judges, compare experiments, and use production traces or human feedback to keep improving the test set.

### Why it matters

Prompt and model changes are easy to make but hard to trust. Without a repeatable evaluation loop, teams often rely on a few manual examples, which misses regressions and makes quality discussions subjective.

Braintrust helps by providing:

- Versioned datasets for test cases and production-derived examples.
- Evals that combine data, a task, and scorers.
- Experiments that compare versions and highlight regressions.
- Scorers using Autoevals, LLM-as-a-judge, or custom code.
- Tracing for LLM calls, tool calls, retrieval, business logic, latency, token usage, and cost.
- Playgrounds for testing prompts, workflows, models, scorers, and datasets.
- Annotation and feedback loops for improving eval coverage.

### Architecture/Concepts

Key concepts:

- **Dataset**: A versioned collection of examples, commonly with `input`, optional `expected`, metadata, and tags.
- **Eval**: A repeatable evaluation consisting of data, a task function, and one or more scorers.
- **Task**: The application behavior being tested, such as a prompt, RAG pipeline, tool-using agent, classifier, or workflow.
- **Scorer**: A function that measures output quality. Scorers can be deterministic code, Autoevals, or LLM-as-a-judge prompts.
- **Experiment**: The stored result of an eval run, including outputs, scores, metrics, traces, and comparison data.
- **Trace**: A production or evaluation execution broken into spans for model calls, tools, retrieval, and custom logic.
- **Span**: A unit of work inside a trace, with inputs, outputs, metadata, scores, and metrics.
- **Playground**: A no-code workspace for iterating on prompts, workflows, models, datasets, and scorers.

Braintrust treats evaluation and observability as connected. Production logs can become dataset examples, eval failures can be investigated through traces, and prompt changes can be promoted from playgrounds into experiments.

### Practical usage

Use Braintrust when:

- You need repeatable evals for AI features before deployment.
- You want to compare prompts, model providers, retrievers, tools, or agent workflows.
- You want production traces and evaluation results in the same workflow.
- You need versioned datasets and clear regression analysis.
- You want non-code teammates to inspect results, annotate outputs, or use playgrounds.

Typical workflow:

1. Create a dataset from curated examples, existing QA cases, production logs, or human feedback.
2. Define a task that runs the AI feature under test.
3. Attach scorers such as exact match, JSON schema validation, factuality, relevance, tone, safety, or custom business logic.
4. Run evals locally, in CI, remotely, or from the UI.
5. Compare experiments to identify regressions, improvements, latency changes, and cost changes.
6. Use tracing to debug individual bad cases.
7. Add failures and production edge cases back into the dataset.

Operational tips:

- Keep eval datasets versioned and review changes the same way you review code.
- Separate smoke evals for CI from larger benchmark evals that can run on a schedule.
- Prefer deterministic scorers for hard requirements such as JSON validity and policy constraints.
- Calibrate LLM-as-a-judge scorers against human labels for subjective quality.
- Log enough metadata to group results by model, prompt version, customer segment, route, language, or release.
- Treat prompts, traces, and production logs as sensitive data.

### Learning checklist

- [ ] Explain the relationship between datasets, tasks, scorers, evals, and experiments.
- [ ] Create a small dataset with inputs and expected outputs.
- [ ] Run an eval using one deterministic scorer.
- [ ] Add an LLM-as-a-judge scorer and inspect disagreements.
- [ ] Compare two experiments and identify regressions.
- [ ] Instrument production tracing and inspect a trace with spans.
- [ ] Promote a production failure into a dataset example.
- [ ] Decide which evals should run in CI and which should run offline or on a schedule.

## 繁體中文

### 概覽

Braintrust 是一個 AI evaluation 與 observability 平台，用於系統化測試與改善 LLM 應用。它結合 datasets、evals、scorers、experiments、tracing、playgrounds、annotations 與 production logging。

核心想法是 evaluation-driven development：定義具代表性的資料，將應用作為 task 執行，用程式或模型 judge 對 outputs 評分，比較 experiments，並用 production traces 或 human feedback 持續改善測試集。

### 為什麼重要

Prompt 與 model 變更很容易，但很難確認品質。若沒有可重複的 evaluation loop，團隊常只靠少數手動案例，容易漏掉 regressions，也讓品質討論變得主觀。

Braintrust 的價值包括：

- 使用 versioned datasets 管理測試案例與 production-derived examples。
- 用 data、task 與 scorers 組成 evals。
- 用 experiments 比較版本並找出 regressions。
- 支援 Autoevals、LLM-as-a-judge 與 custom code scorers。
- 追蹤 LLM calls、tool calls、retrieval、business logic、latency、token usage 與 cost。
- 用 playgrounds 測試 prompts、workflows、models、scorers 與 datasets。
- 透過 annotation 與 feedback loops 改善 eval coverage。

### 架構/概念

核心概念：

- **Dataset**：版本化案例集合，通常包含 `input`、可選的 `expected`、metadata 與 tags。
- **Eval**：可重複的評估，由 data、task function 與一個或多個 scorers 組成。
- **Task**：被測試的應用行為，例如 prompt、RAG pipeline、會使用工具的 agent、classifier 或 workflow。
- **Scorer**：衡量 output quality 的函式，可為 deterministic code、Autoevals 或 LLM-as-a-judge prompts。
- **Experiment**：eval run 的儲存結果，包含 outputs、scores、metrics、traces 與比較資料。
- **Trace**：production 或 evaluation execution，可拆成 model calls、tools、retrieval 與 custom logic 的 spans。
- **Span**：trace 中的一個工作單位，包含 inputs、outputs、metadata、scores 與 metrics。
- **Playground**：無程式碼工作區，用於迭代 prompts、workflows、models、datasets 與 scorers。

Braintrust 將 evaluation 與 observability 視為同一個流程的一部分。Production logs 可以變成 dataset examples，eval failures 可以透過 traces 調查，prompt changes 可以從 playgrounds 推進到 experiments。

### 實務使用

適合使用 Braintrust 的情境：

- 需要在部署前為 AI features 建立可重複 evals。
- 想比較 prompts、model providers、retrievers、tools 或 agent workflows。
- 想把 production traces 與 evaluation results 放在同一套流程中。
- 需要 versioned datasets 與清楚的 regression analysis。
- 希望非工程成員也能檢查結果、標註 outputs 或使用 playgrounds。

常見流程：

1. 從 curated examples、既有 QA cases、production logs 或 human feedback 建立 dataset。
2. 定義執行待測 AI feature 的 task。
3. 加上 scorers，例如 exact match、JSON schema validation、factuality、relevance、tone、safety 或 custom business logic。
4. 在本機、CI、remote environment 或 UI 執行 evals。
5. 比較 experiments，找出 regressions、improvements、latency changes 與 cost changes。
6. 用 tracing 除錯個別壞案例。
7. 將 failures 與 production edge cases 加回 dataset。

維運建議：

- Eval datasets 應版本化，並像程式碼一樣審查變更。
- 將 CI 用的 smoke evals 與排程執行的大型 benchmark evals 分開。
- JSON validity 與 policy constraints 等硬性需求優先使用 deterministic scorers。
- 對 subjective quality，應用 human labels 校準 LLM-as-a-judge scorers。
- 記錄足夠 metadata，以便依 model、prompt version、customer segment、route、language 或 release 分組。
- Prompts、traces 與 production logs 都應視為敏感資料。

### 學習檢核表

- [ ] 說明 datasets、tasks、scorers、evals 與 experiments 的關係。
- [ ] 建立包含 inputs 與 expected outputs 的小型 dataset。
- [ ] 使用一個 deterministic scorer 執行 eval。
- [ ] 加入 LLM-as-a-judge scorer 並檢查 disagreement。
- [ ] 比較兩個 experiments 並找出 regressions。
- [ ] Instrument production tracing 並檢查包含 spans 的 trace。
- [ ] 將 production failure 轉成 dataset example。
- [ ] 決定哪些 evals 應在 CI 執行，哪些應離線或排程執行。

## References

- [Braintrust evaluation quickstart](https://www.braintrust.dev/docs/evaluation)
- [Braintrust tracing quickstart](https://www.braintrust.dev/docs/observability)
- [Braintrust datasets](https://www.braintrust.dev/docs/guides/datasets)
- [Braintrust scorers](https://www.braintrust.dev/docs/evaluate/write-scorers)
- [Braintrust playgrounds](https://www.braintrust.dev/docs/platform/playground)
- [Braintrust run evaluations](https://www.braintrust.dev/docs/guides/evals/write)
