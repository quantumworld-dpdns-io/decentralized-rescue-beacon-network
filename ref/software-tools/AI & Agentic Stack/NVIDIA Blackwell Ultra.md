# NVIDIA Blackwell Ultra

| Field | Details |
| --- | --- |
| Category | AI accelerator hardware and systems platform |
| Vendor | NVIDIA |
| Generation | Blackwell Ultra / GB300 Grace Blackwell Ultra |
| Primary use | Large-scale AI training, reasoning inference, long-context LLM serving, multimodal AI, and AI factory infrastructure |
| Access model | Paid hardware through NVIDIA systems, OEM partners, cloud providers, and data center platforms |
| Key hardware signals | Up to 288 GB HBM3E per Blackwell Ultra GPU by SKU; fifth-generation Tensor Cores; NVFP4 4-bit floating-point acceleration; NVLink 5; NVLink-C2C with Grace CPU in Grace Blackwell systems |
| Best fit | Teams that need very high memory capacity, token throughput, low-latency reasoning inference, or rack-scale accelerated compute |

## English

### Overview

NVIDIA Blackwell Ultra is an extension of the NVIDIA Blackwell architecture aimed at the most demanding AI workloads: frontier-model training, long-context inference, reasoning models, and production AI factories. It is not a single product only; the name appears across GPU chips, Grace Blackwell Ultra superchips, DGX systems, and rack-scale platforms such as GB300 NVL72.

At the chip level, NVIDIA describes Blackwell Ultra as a dual-reticle GPU built with 208 billion transistors and connected internally by NVIDIA High-Bandwidth Interface. Depending on the SKU, Blackwell Ultra GPUs can provide up to 288 GB of HBM3E memory. NVIDIA positions the platform around fifth-generation Tensor Cores, NVFP4 low-precision AI compute, larger memory capacity, and attention-layer acceleration for reasoning inference.

### Why it matters

Blackwell Ultra matters because modern AI bottlenecks are no longer only about raw matrix multiplication. Reasoning models, agentic systems, multimodal models, and long-context applications spend significant time and memory on attention, KV cache, orchestration, and serving many concurrent users.

The platform targets those constraints in several ways:

- More local GPU memory reduces the need to offload model weights or KV cache to slower memory tiers.
- NVFP4 can improve inference throughput and memory efficiency when models tolerate low-precision execution.
- Faster attention-layer operations help with long prompts, long generated outputs, and test-time scaling workloads.
- NVLink, NVLink-C2C, and rack-scale NVLink switching allow many GPUs and Grace CPUs to behave like a tightly integrated AI compute fabric.
- Enterprise features such as MIG partitioning, confidential computing support, and reliability tooling make the hardware more practical for shared production environments.

For buyers and architects, the main point is that Blackwell Ultra is designed for total AI service output, not just benchmark peak FLOPS. It is especially relevant when cost per token, latency per user, memory residency, and power efficiency determine whether a model can run economically.

### Architecture/Concepts

Blackwell Ultra builds on several architecture concepts:

- **Dual-reticle GPU design:** NVIDIA presents the Blackwell Ultra GPU as two large dies operating as one CUDA-programmable accelerator. This preserves the familiar CUDA software model while increasing silicon area and compute resources.
- **Fifth-generation Tensor Cores:** Tensor Cores accelerate matrix operations used heavily by transformer models. Blackwell Ultra adds strong support for NVFP4, FP8, FP6, BF16, TF32, and other AI/HPC precisions depending on workload and SKU.
- **NVFP4:** NVIDIA's 4-bit floating-point format is intended to lower memory footprint and increase AI throughput while preserving useful model accuracy for supported inference workflows.
- **Large HBM3E memory:** Up to 288 GB HBM3E per Blackwell Ultra GPU is important for larger models, longer contexts, higher batch sizes, and less KV-cache offloading. Product SKUs may expose less memory; for example, NVIDIA's current DGX Station specification lists 252 GB HBM3e GPU memory plus 496 GB LPDDR5X CPU memory, for 748 GB coherent memory.
- **Attention acceleration:** NVIDIA highlights doubled special-function throughput for key attention-layer operations versus Blackwell GPUs, improving transformer softmax-heavy workloads.
- **NVLink 5 and NVLink-C2C:** NVLink 5 connects GPUs at high bandwidth, while NVLink-C2C provides coherent CPU-GPU connectivity between Grace CPUs and Blackwell Ultra GPUs in Grace Blackwell systems.
- **Rack-scale systems:** GB300 NVL72 integrates 72 Blackwell Ultra GPUs and 36 Grace CPUs in a liquid-cooled rack-scale platform for reasoning inference and AI factory deployment.

### Practical usage

Blackwell Ultra is most practical when the workload can exploit its memory, interconnect, and low-precision acceleration:

- Run very large LLMs and multimodal models with fewer compromises around model residency and context length.
- Serve reasoning models where user-visible latency and tokens per second per watt matter.
- Fine-tune, post-train, or evaluate large models with high-bandwidth GPU memory and fast GPU-to-GPU communication.
- Use DGX Station for local development, fine-tuning, inference, and team-shared AI workstations before deploying to data center or cloud infrastructure.
- Use GB300 NVL72 or DGX GB300-style systems when the requirement is rack-scale inference capacity rather than a single workstation.

Practical evaluation should focus on the exact system SKU, not only the architecture name. Confirm HBM capacity, coherent memory size, power envelope, networking, supported software stack, availability, and whether the model/runtime stack supports NVFP4 efficiently. For many teams, cloud access or managed DGX infrastructure will be more realistic than direct hardware ownership.

### Learning checklist

- Understand the difference between Blackwell, Blackwell Ultra, GB300 Grace Blackwell Ultra, DGX Station, and GB300 NVL72.
- Explain why HBM capacity and bandwidth matter for model weights, activations, and KV cache.
- Know when NVFP4 is useful and when accuracy validation is required before production use.
- Compare single-node, workstation, and rack-scale deployments.
- Check whether your inference stack supports Blackwell Ultra features through CUDA, TensorRT-LLM, NVIDIA NIM, or the relevant framework backend.
- Estimate cost per token, latency, throughput per watt, and memory residency before choosing hardware.
- Validate exact SKU specifications from NVIDIA or the system vendor because memory capacity and performance vary by product.

## 繁體中文

### 概覽

NVIDIA Blackwell Ultra 是 NVIDIA Blackwell 架構的延伸，面向最高階的 AI 工作負載，包括前沿模型訓練、長上下文推論、推理型模型，以及生產級 AI factory。它不只是單一 GPU 產品；Blackwell Ultra 這個名稱會出現在 GPU 晶片、Grace Blackwell Ultra Superchip、DGX 系統，以及 GB300 NVL72 這類機櫃級平台中。

在晶片層級，NVIDIA 將 Blackwell Ultra 描述為雙 reticle GPU，包含 2080 億個電晶體，並透過 NVIDIA High-Bandwidth Interface 連接成單一 CUDA 可程式化加速器。依 SKU 不同，Blackwell Ultra GPU 最高可配備 288 GB HBM3E 記憶體。NVIDIA 將此平台定位在第五代 Tensor Core、NVFP4 低精度 AI 運算、更大記憶體容量，以及針對推理型推論的 attention layer 加速。

### 為什麼重要

Blackwell Ultra 重要的原因在於，現代 AI 的瓶頸已不只是矩陣乘法的峰值效能。推理型模型、agentic 系統、多模態模型與長上下文應用，會在 attention、KV cache、任務編排，以及多使用者並行服務上消耗大量時間與記憶體。

此平台主要針對這些限制：

- 更大的 GPU 本地記憶體可降低模型權重或 KV cache 被迫卸載到較慢記憶體層的機率。
- 在模型可接受低精度執行時，NVFP4 可提升推論吞吐量與記憶體效率。
- Attention layer 操作加速有助於長 prompt、長輸出，以及 test-time scaling 工作負載。
- NVLink、NVLink-C2C 與機櫃級 NVLink switching 讓多顆 GPU 與 Grace CPU 可組成高整合度的 AI 運算 fabric。
- MIG 分割、confidential computing 支援與可靠性工具，讓硬體更適合共享式生產環境。

對採購者與架構師來說，重點是 Blackwell Ultra 不是只追求峰值 FLOPS，而是以整體 AI 服務輸出為目標。當每 token 成本、單一使用者延遲、模型常駐記憶體，以及能源效率決定模型能否經濟化部署時，它特別相關。

### 架構/概念

Blackwell Ultra 建立在幾個關鍵架構概念上：

- **雙 reticle GPU 設計：** NVIDIA 將 Blackwell Ultra GPU 描述為兩個大型 die 以單一 CUDA 可程式化加速器運作，在保留 CUDA 軟體模型的同時增加晶片面積與運算資源。
- **第五代 Tensor Core：** Tensor Core 加速 transformer 模型大量使用的矩陣運算。Blackwell Ultra 強化 NVFP4，並依工作負載與 SKU 支援 FP8、FP6、BF16、TF32 等 AI/HPC 精度。
- **NVFP4：** NVIDIA 的 4-bit floating-point 格式，目標是在支援的推論流程中降低記憶體占用、提升 AI 吞吐量，並維持可用的模型準確度。
- **大型 HBM3E 記憶體：** 每顆 Blackwell Ultra GPU 最高可達 288 GB HBM3E，對大型模型、長上下文、更高 batch size，以及降低 KV-cache offloading 都很重要。實際產品 SKU 可能較低；例如 NVIDIA 目前的 DGX Station 規格列出 252 GB HBM3e GPU 記憶體與 496 GB LPDDR5X CPU 記憶體，合計 748 GB coherent memory。
- **Attention 加速：** NVIDIA 強調 Blackwell Ultra 相比 Blackwell GPU，針對關鍵 attention layer 指令提供加倍的 special-function throughput，可改善 transformer softmax 密集型工作負載。
- **NVLink 5 與 NVLink-C2C：** NVLink 5 提供 GPU 間高頻寬連接；NVLink-C2C 則在 Grace Blackwell 系統中提供 Grace CPU 與 Blackwell Ultra GPU 之間的 coherent CPU-GPU 連接。
- **機櫃級系統：** GB300 NVL72 將 72 顆 Blackwell Ultra GPU 與 36 顆 Grace CPU 整合在液冷機櫃級平台中，用於推理型推論與 AI factory 部署。

### 實務使用

當工作負載能善用其記憶體、互連與低精度加速時，Blackwell Ultra 最具實務價值：

- 以較少的模型常駐與上下文長度妥協，執行超大型 LLM 與多模態模型。
- 服務推理型模型，尤其是使用者可感知延遲與每瓦 tokens/sec 很重要的情境。
- 透過高頻寬 GPU 記憶體與高速 GPU-to-GPU 通訊，進行大型模型微調、後訓練或評測。
- 使用 DGX Station 在本地進行開發、微調、推論與團隊共享工作站，再部署到資料中心或雲端。
- 當需求是機櫃級推論容量而非單一工作站時，使用 GB300 NVL72 或 DGX GB300 類型系統。

實務評估時應聚焦在確切系統 SKU，而不只是架構名稱。需要確認 HBM 容量、coherent memory 大小、功耗、網路、支援的軟體堆疊、供貨狀態，以及模型/runtime 是否能有效使用 NVFP4。對許多團隊而言，雲端或受管理的 DGX 基礎設施，會比直接購買硬體更實際。

### 學習檢核表

- 分清楚 Blackwell、Blackwell Ultra、GB300 Grace Blackwell Ultra、DGX Station 與 GB300 NVL72 的差異。
- 說明 HBM 容量與頻寬為何會影響模型權重、activations 與 KV cache。
- 理解 NVFP4 何時有用，以及正式上線前為何需要準確度驗證。
- 比較單節點、工作站與機櫃級部署。
- 檢查推論堆疊是否透過 CUDA、TensorRT-LLM、NVIDIA NIM 或相關 framework backend 支援 Blackwell Ultra 功能。
- 在選擇硬體前估算每 token 成本、延遲、每瓦吞吐量與模型常駐記憶體需求。
- 由 NVIDIA 或系統供應商確認確切 SKU 規格，因為記憶體容量與效能會依產品而異。

## References

- [NVIDIA Technical Blog: Inside NVIDIA Blackwell Ultra: The Chip Powering the AI Factory Era](https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era/)
- [NVIDIA Blackwell Architecture](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/)
- [NVIDIA GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)
- [NVIDIA DGX Station](https://www.nvidia.com/en-us/products/workstations/dgx-station/)
- [NVIDIA press release: NVIDIA Launches AI-First DGX Personal Computing Systems With Global Computer Makers](https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Launches-AI-First-DGX-Personal-Computing-Systems-With-Global-Computer-Makers/default.aspx)
