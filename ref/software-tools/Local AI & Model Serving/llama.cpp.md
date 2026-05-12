# llama.cpp

| Field | Details |
| --- | --- |
| Category | Portable local LLM inference engine and tooling |
| Primary use | Run quantized models on CPUs, consumer GPUs, Apple Silicon, and edge/server hardware |
| Implementation | C/C++ with ggml/gguf ecosystem |
| Interfaces | `llama-cli`, `llama-server`, libraries, examples, and bindings from the wider ecosystem |
| Model format | GGUF |
| Best fit | Maximum portability, low-dependency local inference, quantization experiments, and embedded/offline deployments |
| Last reviewed | 2026-04-29 |

## English

### Overview

llama.cpp is a portable C/C++ inference project for running LLMs with minimal setup across a wide range of hardware. It is closely tied to the ggml tensor library and the GGUF model format, which is widely used for quantized local models.

The project is a foundation layer for many local AI tools. Desktop apps, local servers, wrappers, and model managers often rely on llama.cpp or GGUF-compatible artifacts even when users do not interact with llama.cpp directly.

### Why it matters

- It makes useful LLM inference possible on commodity laptops and offline machines.
- GGUF plus quantization lets larger models fit into smaller RAM or VRAM budgets.
- The project supports CPU, Apple Metal, CUDA, HIP, Vulkan, SYCL, and other backends depending on build options.
- It provides both command-line inference and a local server path.
- It is often the fastest way to test whether a model can run on constrained hardware.

### Architecture/Concepts

| Concept | Meaning |
| --- | --- |
| ggml | Low-level tensor library used by the llama.cpp ecosystem. |
| GGUF | Model file format that stores weights and metadata for local inference. |
| Quantization | Lower-bit weight formats such as 1.5-bit through 8-bit variants reduce memory and can improve speed. |
| `llama-cli` | Command-line tool for local text generation and experiments. |
| `llama-server` | Local HTTP server with OpenAI-compatible behavior for app integration. |
| GPU offload | Moves selected layers or operations to GPU while keeping the rest on CPU if needed. |
| Context window | Number of tokens kept for prompt and conversation state; memory cost grows with context. |
| Grammar/constrained decoding | Mechanisms for restricting output format, often used for JSON-like results. |

### Practical usage

Use llama.cpp when:

- You need the broadest local hardware compatibility.
- You want to run GGUF models without a heavy Python serving stack.
- You are optimizing for small devices, offline environments, or edge machines.
- You need direct control over quantization, context, threads, GPU layers, and sampling.
- You are building a tool that should work even without a large GPU.

Example workflow:

```bash
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF
llama-server -hf ggml-org/gemma-3-1b-it-GGUF --port 8080
```

Operational cautions:

- Model quality varies by quantization level; test task quality, not only speed.
- CPU-only inference can be useful but may be too slow for interactive large models.
- Build flags matter: Metal, CUDA, HIP, Vulkan, and SYCL support depend on the compiled binary.
- Long context increases memory pressure even when model weights fit.
- For high-concurrency production APIs, evaluate vLLM or SGLang after proving model fit with llama.cpp.

### Learning checklist

- [ ] Run a GGUF model with `llama-cli`.
- [ ] Start `llama-server` and send a local API request.
- [ ] Compare two quantization levels for speed, memory, and output quality.
- [ ] Tune context length, thread count, and GPU offload settings.
- [ ] Understand the difference between model weights memory and KV cache memory.
- [ ] Build from source with the backend relevant to your hardware.
- [ ] Decide when llama.cpp is the serving layer versus a portability test tool.

## 繁體中文

### 概覽

llama.cpp 是可攜式 C/C++ 推論專案，用於在多種硬體上以最少設定執行 LLM。它與 ggml tensor library 和 GGUF 模型格式密切相關；GGUF 也是本機量化模型最常見的格式之一。

許多本機 AI 工具都以 llama.cpp 為基礎層。即使使用者不直接操作 llama.cpp，桌面應用、本機伺服器、wrapper 與模型管理器也常依賴 llama.cpp 或 GGUF-compatible artifact。

### 為什麼重要

- 讓一般 laptop 與離線機器也能進行有用的 LLM 推論。
- GGUF 加量化可讓較大模型放入較小 RAM 或 VRAM。
- 依 build options 支援 CPU、Apple Metal、CUDA、HIP、Vulkan、SYCL 等 backend。
- 同時提供命令列推論與本機 server 路徑。
- 常是測試模型能否在受限硬體上執行的最快方式。

### 架構/概念

| 概念 | 說明 |
| --- | --- |
| ggml | llama.cpp 生態使用的低階 tensor library。 |
| GGUF | 儲存本機推論 weights 與 metadata 的模型檔格式。 |
| Quantization | 1.5-bit 到 8-bit 等低位元 weight 格式，可降低記憶體並可能提升速度。 |
| `llama-cli` | 用於本機文字生成與實驗的命令列工具。 |
| `llama-server` | 提供 OpenAI-compatible 行為的本機 HTTP server。 |
| GPU offload | 視需求將部分 layer 或 operation 移到 GPU，其餘留在 CPU。 |
| Context window | prompt 與對話狀態可保留的 token 數；context 越長記憶體成本越高。 |
| Grammar/constrained decoding | 限制輸出格式的機制，常用於 JSON 類結果。 |

### 實務使用

適合使用 llama.cpp 的情境：

- 需要最廣泛的本機硬體相容性。
- 想在沒有大型 Python serving stack 的情況下執行 GGUF 模型。
- 針對小型裝置、離線環境或 edge machine 最佳化。
- 需要直接控制量化、context、threads、GPU layers 與 sampling。
- 要建立即使沒有大型 GPU 也能運作的工具。

範例流程：

```bash
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF
llama-server -hf ggml-org/gemma-3-1b-it-GGUF --port 8080
```

營運注意事項：

- 模型品質會受量化等級影響；應測任務品質，而不只測速度。
- CPU-only 推論有價值，但大型模型互動可能太慢。
- Build flags 很重要：Metal、CUDA、HIP、Vulkan、SYCL 支援取決於編譯出的 binary。
- 即使 weights 放得下，長 context 仍會提高記憶體壓力。
- 若要高並發生產 API，先用 llama.cpp 證明模型可運行，再評估 vLLM 或 SGLang。

### 學習檢核表

- [ ] 用 `llama-cli` 執行一個 GGUF 模型。
- [ ] 啟動 `llama-server` 並送出本機 API request。
- [ ] 比較兩種量化等級的速度、記憶體與輸出品質。
- [ ] 調整 context length、thread count 與 GPU offload 設定。
- [ ] 理解 model weights memory 與 KV cache memory 的差異。
- [ ] 針對自己的硬體 backend 從 source build。
- [ ] 判斷 llama.cpp 應作為 serving layer 還是可攜性測試工具。

## References

- [llama.cpp GitHub repository](https://github.com/ggml-org/llama.cpp)
- [llama.cpp server example and usage](https://github.com/ggml-org/llama.cpp/tree/master/examples/server)
- [GGUF format documentation](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)

