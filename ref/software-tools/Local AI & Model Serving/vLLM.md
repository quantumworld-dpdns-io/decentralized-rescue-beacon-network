# vLLM

| Field | Details |
| --- | --- |
| Category | High-throughput LLM inference and serving engine |
| Primary use | Serve Hugging Face-compatible language and multimodal models with efficient GPU utilization |
| Core techniques | Paged KV cache, continuous batching, optimized kernels, distributed inference |
| Interfaces | Python API, OpenAI-compatible server, CLI, Docker/Kubernetes deployments |
| Hardware | NVIDIA GPUs, AMD GPUs, CPUs, Gaudi, TPU, AWS Trainium/Inferentia, and other supported backends depending on version |
| Best fit | Production model serving where throughput, latency, batching, and GPU memory efficiency matter |
| Last reviewed | 2026-04-29 |

## English

### Overview

vLLM is an inference and serving engine designed for efficient LLM serving. It began in the UC Berkeley Sky Computing Lab and is now a community-driven project used for both research and production deployments.

The central idea is to make GPU memory and request scheduling more efficient. vLLM is known for PagedAttention-style KV cache management, continuous batching of incoming requests, optimized model execution, streaming responses, OpenAI-compatible endpoints, and support for distributed inference.

### Why it matters

- LLM serving cost is often dominated by GPU utilization and KV cache memory.
- Real workloads arrive continuously, not as neat static batches.
- Production APIs need streaming, cancellation, metrics, model limits, and compatibility with existing clients.
- Multi-GPU and multi-node serving require clear tensor, pipeline, data, or expert parallelism choices.
- Quantization, speculative decoding, prefix caching, and LoRA serving can change cost and latency significantly.

### Architecture/Concepts

| Concept | Role |
| --- | --- |
| Engine | Schedules requests, manages model execution, and coordinates memory. |
| Paged KV cache | Stores attention keys and values in blocks to reduce memory waste and support larger effective batches. |
| Continuous batching | Dynamically mixes prefill and decode work from many requests instead of waiting for fixed batches. |
| OpenAI-compatible server | Exposes familiar `/v1/chat/completions`, `/v1/completions`, embeddings, and related APIs depending on model support. |
| Prefix caching | Reuses shared prompt prefixes to avoid repeated prefill work. |
| Speculative decoding | Uses draft-model or related strategies to reduce generation latency when configured correctly. |
| Quantization | Supports formats such as GPTQ, AWQ, INT4, INT8, and FP8 depending on model and hardware. |
| Parallelism | Tensor, pipeline, data, and expert parallelism options help serve larger models or higher traffic. |
| LoRA serving | Multi-LoRA support enables adapter-based serving on top of a base model. |

### Practical usage

Use vLLM when:

- You need a production-grade OpenAI-compatible endpoint for one or more models.
- GPU throughput and cost per token are important.
- You serve many concurrent users or long-context requests.
- You need distributed inference for models larger than one GPU.
- You want to integrate Hugging Face model artifacts with a high-performance serving layer.

Example server shape:

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

Production checks:

- Confirm the exact model architecture, tokenizer, quantization, and context length are supported.
- Benchmark prefill-heavy, decode-heavy, and long-context traffic separately.
- Size GPU memory for weights, KV cache, batch concurrency, and fragmentation margin.
- Set request limits, authentication, network controls, and observability before exposing the server.
- Validate OpenAI-compatible behavior for tool calls, structured outputs, embeddings, or multimodal inputs if your app depends on them.

### Learning checklist

- [ ] Explain why KV cache memory dominates LLM serving.
- [ ] Run one model with the OpenAI-compatible vLLM server.
- [ ] Send streaming and non-streaming chat requests.
- [ ] Compare throughput with different max batch, context, and concurrency settings.
- [ ] Test prefix caching or speculative decoding on a suitable workload.
- [ ] Try one quantized model and compare quality, memory, and latency.
- [ ] Understand tensor parallelism before serving a model across multiple GPUs.

## 繁體中文

### 概覽

vLLM 是為高效率 LLM serving 設計的推論與服務引擎。它起源於 UC Berkeley Sky Computing Lab，現在是由社群推動、同時用於研究與生產環境的專案。

它的核心價值是提升 GPU 記憶體與請求排程效率。vLLM 以 PagedAttention 類型的 KV cache 管理、continuous batching、最佳化模型執行、串流回應、OpenAI-compatible endpoint 與分散式推論支援而聞名。

### 為什麼重要

- LLM serving 成本通常受 GPU 使用率與 KV cache 記憶體主導。
- 真實流量是連續到達，不會自然形成固定 batch。
- 生產 API 需要串流、取消、指標、模型限制與既有 client 相容性。
- 多 GPU 與多節點 serving 需要清楚選擇 tensor、pipeline、data 或 expert parallelism。
- 量化、speculative decoding、prefix caching 與 LoRA serving 都可能大幅影響成本與延遲。

### 架構/概念

| 概念 | 角色 |
| --- | --- |
| Engine | 排程請求、管理模型執行並協調記憶體。 |
| Paged KV cache | 以 block 儲存 attention key/value，降低記憶體浪費並支援更大的有效 batch。 |
| Continuous batching | 動態混合多個請求的 prefill 與 decode 工作，而不是等待固定 batch。 |
| OpenAI-compatible server | 依模型支援暴露 `/v1/chat/completions`、`/v1/completions`、embeddings 等 API。 |
| Prefix caching | 重用共享 prompt prefix，避免重複 prefill 計算。 |
| Speculative decoding | 在正確設定下利用 draft model 等策略降低生成延遲。 |
| Quantization | 依模型與硬體支援 GPTQ、AWQ、INT4、INT8、FP8 等格式。 |
| Parallelism | Tensor、pipeline、data 與 expert parallelism 可支援更大模型或更高流量。 |
| LoRA serving | Multi-LoRA 支援讓多個 adapter 可共用 base model serving。 |

### 實務使用

適合使用 vLLM 的情境：

- 需要生產級 OpenAI-compatible endpoint。
- GPU 吞吐量與每 token 成本很重要。
- 要服務大量並發使用者或長 context 請求。
- 模型大到需要分散式推論。
- 想把 Hugging Face 模型與高效 serving layer 整合。

範例 server：

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

生產檢查：

- 確認模型架構、tokenizer、量化格式與 context length 被目前版本支援。
- 分別 benchmark prefill-heavy、decode-heavy 與 long-context 流量。
- 為 weights、KV cache、batch concurrency 與碎片化餘裕規劃 GPU 記憶體。
- 對外開放前設定請求限制、認證、網路控管與可觀測性。
- 若應用依賴 tool calls、structured outputs、embeddings 或 multimodal input，需驗證 OpenAI 相容行為。

### 學習檢核表

- [ ] 解釋為什麼 KV cache 記憶體會主導 LLM serving。
- [ ] 用 vLLM OpenAI-compatible server 執行一個模型。
- [ ] 發送串流與非串流 chat request。
- [ ] 比較不同 batch、context 與 concurrency 設定下的吞吐量。
- [ ] 在適合的工作負載測試 prefix caching 或 speculative decoding。
- [ ] 嘗試一個量化模型並比較品質、記憶體與延遲。
- [ ] 在多 GPU serving 前理解 tensor parallelism。

## References

- [vLLM documentation](https://docs.vllm.ai/)
- [vLLM OpenAI-compatible server](https://docs.vllm.ai/en/stable/serving/openai_compatible_server/)
- [vLLM Paged Attention documentation](https://docs.vllm.ai/en/stable/design/paged_attention/)
- [NVIDIA vLLM overview](https://docs.nvidia.com/deeplearning/frameworks/vllm-release-notes/overview.html)
- [vLLM GitHub repository](https://github.com/vllm-project/vllm)

