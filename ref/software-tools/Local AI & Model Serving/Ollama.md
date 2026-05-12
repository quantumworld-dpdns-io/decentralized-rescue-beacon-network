# Ollama

| Field | Details |
| --- | --- |
| Category | Local AI runtime and model manager |
| Primary use | Download, run, customize, and serve open models on developer machines and small servers |
| Interfaces | CLI, local REST API, OpenAI-compatible API, Python library, JavaScript library |
| Default API | `http://localhost:11434/api` |
| Model format | Primarily GGUF-based packaged models distributed through Ollama libraries |
| Best fit | Fast local experimentation, privacy-sensitive prototypes, offline assistants, and lightweight app integration |
| Last reviewed | 2026-04-29 |

## English

### Overview

Ollama is a local AI runtime that makes open-weight model usage feel like a package manager plus a local inference server. A user can pull a model, run it from the CLI, and expose it through a local API without manually wiring tokenizers, quantized model files, inference backends, and server processes.

It is strongest when the priority is simplicity: getting models such as Llama, Gemma, Qwen, DeepSeek, Mistral, or embedding models running quickly on macOS, Windows, Linux, workstations, and small servers.

### Why it matters

- It lowers the setup cost for local LLM development.
- It gives teams a local endpoint for privacy-sensitive testing before using cloud inference.
- It standardizes model lifecycle tasks such as pull, list, show, copy, delete, and run.
- It supports streaming generation and chat APIs that are easy to wire into tools.
- It can act as a local backend for editors, agents, notebooks, and internal apps.

### Architecture/Concepts

| Concept | Meaning |
| --- | --- |
| Ollama daemon | Local service that manages loaded models and serves API requests. |
| CLI | Commands such as `ollama run`, `ollama pull`, `ollama list`, and `ollama rm`. |
| Model tag | Model names use a `model:tag` pattern; omitted tags default to `latest`. |
| Modelfile | Configuration for creating customized model variants with parameters, templates, adapters, or system prompts. |
| Local API | REST API for generation, chat, embeddings, model management, and running-model inspection. |
| OpenAI-compatible API | Compatibility layer for clients that expect OpenAI-style chat/completion endpoints. |
| Quantization | Smaller model representations reduce memory use and make local inference practical. |

### Practical usage

Use Ollama when:

- You want the fastest path from "install" to a working local model.
- You are building a prototype that should run on a laptop or single workstation.
- You need simple local APIs for chat, generation, or embeddings.
- You want users to manage models with familiar CLI commands.
- You value operational simplicity over maximum serving throughput.

Basic workflow:

```bash
ollama pull gemma3
ollama run gemma3
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3",
  "prompt": "Explain local model serving in one paragraph."
}'
```

Operational cautions:

- Check model memory requirements before distributing a local workflow.
- Pin model tags for reproducible demos and tests.
- Do not expose the local API on a network without access controls.
- Benchmark with the exact context length and quantization level you plan to use.
- Use vLLM or SGLang instead when multi-GPU throughput and production batching are the main goal.

### Learning checklist

- [ ] Install Ollama and run one chat model locally.
- [ ] Pull, list, inspect, and delete models with the CLI.
- [ ] Call `/api/generate` and `/api/chat` from a script.
- [ ] Understand model tags and why pinning matters.
- [ ] Create a simple customized model with a Modelfile.
- [ ] Compare latency and memory use across two quantization levels or model sizes.
- [ ] Decide when Ollama is enough and when a production serving engine is needed.

## 繁體中文

### 概覽

Ollama 是本機 AI runtime，將開源模型的使用體驗簡化成「模型套件管理器」加「本機推論伺服器」。使用者可以拉取模型、用 CLI 執行，並透過本機 API 供應服務，不需要手動組合 tokenizer、量化模型檔、推論 backend 與 server process。

它最適合追求簡單快速的情境，例如在 macOS、Windows、Linux、工作站或小型伺服器上快速執行 Llama、Gemma、Qwen、DeepSeek、Mistral 或 embedding 模型。

### 為什麼重要

- 降低本機 LLM 開發的設定成本。
- 讓團隊能先用本機 endpoint 測試隱私敏感工作流。
- 標準化模型拉取、列表、檢視、複製、刪除與執行。
- 支援容易整合到工具中的串流生成與聊天 API。
- 可作為編輯器、Agent、Notebook 與內部應用的本機 backend。

### 架構/概念

| 概念 | 說明 |
| --- | --- |
| Ollama daemon | 管理已載入模型並提供 API 的本機服務。 |
| CLI | `ollama run`、`ollama pull`、`ollama list`、`ollama rm` 等指令。 |
| Model tag | 模型名稱採用 `model:tag` 格式；省略 tag 時預設為 `latest`。 |
| Modelfile | 用於建立客製模型變體，可設定參數、template、adapter 或 system prompt。 |
| 本機 API | 提供生成、聊天、embedding、模型管理與執行中模型查詢的 REST API。 |
| OpenAI-compatible API | 讓 OpenAI 風格 client 可連接 Ollama 的相容介面。 |
| Quantization | 透過較小的模型表示降低記憶體需求，使本機推論更可行。 |

### 實務使用

適合使用 Ollama 的情境：

- 想用最短路徑從安裝進到可用的本機模型。
- 要建立可在 laptop 或單機工作站執行的原型。
- 需要簡單的本機聊天、生成或 embedding API。
- 希望使用者能用熟悉的 CLI 管理模型。
- 操作簡單比極限吞吐量更重要。

基本流程：

```bash
ollama pull gemma3
ollama run gemma3
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3",
  "prompt": "Explain local model serving in one paragraph."
}'
```

營運注意事項：

- 發布本機工作流前，先確認模型記憶體需求。
- 為可重現的展示與測試固定 model tag。
- 不要在沒有存取控制的情況下把本機 API 暴露到網路。
- 用實際要使用的 context length 與量化等級 benchmark。
- 若主要目標是多 GPU 吞吐量與生產級 batching，應改評估 vLLM 或 SGLang。

### 學習檢核表

- [ ] 安裝 Ollama 並在本機執行一個聊天模型。
- [ ] 使用 CLI 拉取、列出、檢視與刪除模型。
- [ ] 從 script 呼叫 `/api/generate` 與 `/api/chat`。
- [ ] 理解 model tag 以及固定版本的重要性。
- [ ] 用 Modelfile 建立簡單客製模型。
- [ ] 比較兩種量化等級或模型大小的延遲與記憶體使用。
- [ ] 判斷何時 Ollama 足夠，何時需要生產級 serving engine。

## References

- [Ollama documentation](https://docs.ollama.com/)
- [Ollama API introduction](https://docs.ollama.com/api/introduction)
- [Ollama GitHub repository](https://github.com/ollama/ollama)

