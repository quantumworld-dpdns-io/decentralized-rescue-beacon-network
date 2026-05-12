# NVIDIA CUDA-Q

| Field | Details |
| --- | --- |
| Category | Quantum computing framework and hybrid quantum-classical programming platform |
| Vendor | NVIDIA |
| Primary use | Building, simulating, optimizing, and running hybrid quantum-classical applications across CPUs, GPUs, simulators, and QPUs |
| Languages | Python and C++ |
| Execution targets | Local CPU simulation, GPU-accelerated simulation, multi-GPU workflows, cloud/provider QPUs, and custom backends |
| Core abstractions | Quantum kernels, qubits/qvectors, gates, measurements, targets/backends, sampling, running, observing expectation values, optimizers, and quantum operators |
| Best fit | Researchers and engineering teams that need one programming model for quantum algorithms, high-performance simulation, and QPU/hybrid HPC experimentation |

## English

### Overview

NVIDIA CUDA-Q is an open-source platform and programming model for accelerated quantum supercomputing. It lets developers express hybrid quantum-classical programs in Python or C++ and execute them on heterogeneous resources: CPUs, NVIDIA GPUs, quantum simulators, and physical quantum processing units.

The platform is designed to be QPU-agnostic. A CUDA-Q program can be developed against local simulators, scaled to GPU-accelerated simulation, and then retargeted to supported quantum hardware providers when appropriate. NVIDIA positions CUDA-Q as a bridge between near-term quantum algorithm development and longer-term fault-tolerant, quantum-centric supercomputing.

### Why it matters

CUDA-Q matters because useful quantum workloads are rarely only a quantum circuit. They usually combine classical preprocessing, parameter optimization, quantum kernel execution, measurement aggregation, simulation, and postprocessing. CUDA-Q puts those pieces in one programming model instead of forcing developers to stitch together unrelated circuit tools, HPC code, and hardware interfaces.

Important practical benefits include:

- Hybrid execution across CPU, GPU, and QPU resources from one application.
- GPU-accelerated state-vector, tensor-network, and noisy simulation for algorithm development before hardware is available or affordable.
- Python and C++ APIs, allowing notebooks and research prototypes to share concepts with performance-oriented production code.
- A kernel-based model that lets developers write quantum routines once and target different simulators or QPUs.
- Integration with compiler infrastructure such as MLIR, LLVM, and QIR for lowering, optimization, and backend execution.
- Support for algorithmic workflows such as VQE, QAOA, Hamiltonian simulation, quantum machine learning experiments, dynamics simulation, and quantum error-correction research.

For teams already using NVIDIA GPUs or HPC systems, CUDA-Q is especially relevant because it treats quantum acceleration as part of a broader heterogeneous computing stack rather than as a separate silo.

### Architecture/Concepts

CUDA-Q centers on a few core concepts:

- **Quantum kernels:** A kernel is the unit of quantum code. In C++, kernels are annotated with `__qpu__`; in Python, they are commonly declared with `@cudaq.kernel`. Kernels allocate qubits, apply gates, use supported classical control flow, and perform measurements.
- **Host and device roles:** Classical host code calls quantum kernels, manages parameters, runs optimizers, selects targets, and processes results. Kernel bodies describe the quantum work and a supported subset of classical logic.
- **Quantum data types:** Programs use qubits and registers such as `cudaq.qubit`, `cudaq.qvector`, `cudaq::qubit`, and `cudaq::qvector` to represent quantum state within kernels.
- **Quantum operations:** Gates, controlled operations, adjoint operations, custom operations, and measurements are expressed directly in the kernel language. Measurement can be used for sampling and, where supported, mid-circuit control.
- **Targets and backends:** CUDA-Q programs can target CPU simulators, NVIDIA GPU-accelerated simulators, multi-GPU simulation modes, cloud backends, and supported hardware providers.
- **Execution primitives:** `sample` is used for shot-based measurement counts, `run` supports workflows that return classical data from kernels, `observe` computes expectation values for operator/Hamiltonian workloads, and state APIs support simulator introspection.
- **Operators and optimizers:** CUDA-Q includes tools for constructing spin operators and running classical optimizers/gradients around parameterized quantum kernels.
- **Compiler/toolchain path:** CUDA-Q lowers high-level Python or C++ kernel code through a compiler stack that can optimize and transform quantum programs for the selected simulator or QPU target.
- **CUDA-QX libraries:** NVIDIA also exposes domain libraries such as CUDA-Q Solvers and CUDA-Q QEC for higher-level algorithm and error-correction workflows.

### Practical usage

For Python exploration, the current quick start uses `pip install cudaq` and a normal Python workflow. A minimal program typically imports `cudaq`, defines a decorated kernel, allocates a `qvector`, applies gates, measures, and calls `cudaq.sample`.

For C++ development, CUDA-Q uses the `nvq++` compiler. A typical C++ kernel includes `<cudaq.h>`, marks quantum code with `__qpu__`, allocates a `cudaq::qvector`, applies operations, measures, and compiles with `nvq++`.

Common usage patterns:

- Start locally with a small circuit and `sample` to validate measurement distributions.
- Increase qubit count or circuit depth on GPU-accelerated targets when simulation becomes CPU-bound.
- Use `observe` for Hamiltonian expectation values in chemistry, materials, VQE, and QAOA-style workflows.
- Use parameterized kernels plus CUDA-Q or third-party optimizers for hybrid variational algorithms.
- Add noisy simulation to test robustness against device-like error models.
- Move from local simulation to supported QPU providers once credentials, topology, queueing, shot budgets, and backend constraints are understood.
- Use multi-GPU or multi-QPU modes when workloads can be batched or distributed across processors.

Operational caveats: CUDA-Q does not require a GPU for basic use, but GPU acceleration is Linux-focused and depends on compatible NVIDIA drivers, CUDA, and target support. Multi-GPU workflows add MPI and environment requirements. Hardware-provider execution also depends on provider accounts, backend availability, credentials, and device-specific limitations.

### Learning checklist

- Explain CUDA-Q's role as a hybrid quantum-classical programming model rather than only a circuit SDK.
- Write a basic Python kernel with `@cudaq.kernel`, `cudaq.qvector`, gates, `mz`, and `cudaq.sample`.
- Write the same idea in C++ with `__qpu__`, `cudaq::qvector`, and `nvq++`.
- Distinguish `sample`, `run`, `observe`, and state retrieval.
- Understand how targets/backends change execution without rewriting the algorithm.
- Know when CPU simulation is enough and when GPU or multi-GPU simulation is justified.
- Build a parameterized kernel and connect it to an optimizer for VQE or QAOA.
- Construct simple spin operators or Hamiltonians and compute expectation values.
- Test noisy simulations before assuming ideal-circuit results transfer to hardware.
- Check installation, CUDA, MPI, provider credentials, and backend constraints before planning production runs.

## 繁體中文

### 概覽

NVIDIA CUDA-Q 是開源的量子開發平台與程式設計模型，目標是加速量子超級運算。開發者可以用 Python 或 C++ 描述混合量子-classical 程式，並在 CPU、NVIDIA GPU、量子模擬器與實體 QPU 上執行。

CUDA-Q 的設計重點是 QPU-agnostic。開發者可以先用本機模擬器開發，再擴展到 GPU 加速模擬，最後在條件成熟時切換到支援的量子硬體供應商。NVIDIA 將它定位為連接近期量子演算法開發與長期 fault-tolerant、quantum-centric supercomputing 的工具鏈。

### 為什麼重要

CUDA-Q 重要的原因在於，有用的量子工作負載通常不只是單一量子電路。實務上會同時包含 classical 前處理、參數最佳化、量子 kernel 執行、量測統計、模擬與後處理。CUDA-Q 將這些流程放進同一個程式模型中，降低把電路工具、HPC 程式與硬體介面拼接在一起的成本。

主要實務價值包括：

- 可在同一應用中協調 CPU、GPU 與 QPU 資源。
- 提供 GPU 加速的 state-vector、tensor-network 與 noisy simulation，方便在硬體可用或成本可接受前先開發演算法。
- 同時支援 Python 與 C++，讓 notebook 研究原型與高效能程式碼使用相近概念。
- 以 kernel 為核心的模型，讓量子 routine 可以寫一次再切換不同模擬器或 QPU。
- 與 MLIR、LLVM、QIR 等 compiler infrastructure 整合，用於 lowering、最佳化與 backend 執行。
- 支援 VQE、QAOA、Hamiltonian simulation、量子機器學習實驗、dynamics simulation，以及量子錯誤校正研究等工作流。

對已經使用 NVIDIA GPU 或 HPC 系統的團隊來說，CUDA-Q 特別有價值，因為它把量子加速視為 heterogeneous computing stack 的一部分，而不是獨立孤島。

### 架構/概念

CUDA-Q 的核心概念如下：

- **Quantum kernels：** kernel 是量子程式碼的基本單位。C++ 使用 `__qpu__` 標註；Python 通常使用 `@cudaq.kernel`。kernel 會配置 qubit、套用 gate、使用支援的 classical control flow，並執行量測。
- **Host 與 device 角色：** classical host code 呼叫 quantum kernel、管理參數、執行 optimizer、選擇 target，並處理結果。kernel body 則描述量子工作與受支援的 classical 邏輯子集。
- **量子資料型別：** 程式使用 `cudaq.qubit`、`cudaq.qvector`、`cudaq::qubit`、`cudaq::qvector` 等 qubit 與 register 型別，在 kernel 中表示量子狀態。
- **量子操作：** gate、controlled operation、adjoint operation、自訂 operation 與 measurement 都可以直接在 kernel language 中描述。量測可用於 sampling，也可在支援情境中用於 mid-circuit control。
- **Targets 與 backends：** CUDA-Q 程式可切換到 CPU 模擬器、NVIDIA GPU 加速模擬器、多 GPU 模擬模式、cloud backend，以及支援的硬體供應商。
- **執行 primitive：** `sample` 用於 shot-based 量測統計，`run` 支援從 kernel 回傳 classical data 的流程，`observe` 用於 operator/Hamiltonian 的 expectation value，state API 則支援模擬器狀態檢查。
- **Operators 與 optimizers：** CUDA-Q 提供 spin operator 建構工具，以及可搭配 parameterized quantum kernel 的 classical optimizer/gradient 工具。
- **Compiler/toolchain 路徑：** CUDA-Q 會將高階 Python 或 C++ kernel code 經由 compiler stack lowering，並依選定的模擬器或 QPU target 做最佳化與轉換。
- **CUDA-QX libraries：** NVIDIA 也提供 CUDA-Q Solvers、CUDA-Q QEC 等 domain libraries，用於更高階的演算法與錯誤校正工作流。

### 實務使用

Python 探索流程目前可依 quick start 使用 `pip install cudaq`，再用一般 Python 方式執行。最小程式通常會 import `cudaq`、定義 decorated kernel、配置 `qvector`、套用 gate、量測，最後呼叫 `cudaq.sample`。

C++ 開發則使用 CUDA-Q 的 `nvq++` compiler。典型 C++ kernel 會 include `<cudaq.h>`，以 `__qpu__` 標記量子程式碼，配置 `cudaq::qvector`，套用操作、量測，並用 `nvq++` 編譯。

常見使用模式：

- 先在本機用小型電路與 `sample` 驗證量測分布。
- 當 qubit 數或 circuit depth 讓 CPU 模擬變慢時，切換到 GPU 加速 target。
- 在 chemistry、materials、VQE、QAOA 類工作流中，用 `observe` 計算 Hamiltonian expectation value。
- 將 parameterized kernel 搭配 CUDA-Q 或第三方 optimizer，建立 hybrid variational algorithm。
- 加入 noisy simulation，測試演算法對 device-like error model 的穩健性。
- 在理解 credentials、topology、queueing、shot budget 與 backend 限制後，再從本機模擬移到支援的 QPU provider。
- 當工作負載可 batch 或分散到多個 processor 時，使用 multi-GPU 或 multi-QPU 模式。

實務注意事項：基本使用不需要 GPU，但 GPU 加速主要面向 Linux，且取決於相容的 NVIDIA driver、CUDA 與 target 支援。Multi-GPU 工作流會增加 MPI 與環境變數需求。硬體 provider 執行也取決於帳號、backend availability、credentials 與 device-specific 限制。

### 學習檢核表

- 說明 CUDA-Q 是 hybrid quantum-classical programming model，而不只是 circuit SDK。
- 使用 `@cudaq.kernel`、`cudaq.qvector`、gate、`mz`、`cudaq.sample` 寫出基本 Python kernel。
- 用 C++ 的 `__qpu__`、`cudaq::qvector` 與 `nvq++` 寫出相同概念。
- 分辨 `sample`、`run`、`observe` 與 state retrieval。
- 理解 target/backend 如何在不重寫演算法的情況下改變執行位置。
- 判斷何時 CPU 模擬足夠，何時需要 GPU 或 multi-GPU 模擬。
- 建立 parameterized kernel，並串接 optimizer 實作 VQE 或 QAOA。
- 建構簡單 spin operator 或 Hamiltonian，並計算 expectation value。
- 在假設 ideal-circuit 結果可轉移到硬體前，先測試 noisy simulation。
- 在規劃正式執行前，檢查安裝、CUDA、MPI、provider credentials 與 backend 限制。

## References

- [NVIDIA Developer: CUDA-Q](https://developer.nvidia.com/cuda-q)
- [NVIDIA CUDA-Q documentation](https://nvidia.github.io/cuda-quantum/latest/index.html)
- [CUDA-Q Quick Start](https://nvidia.github.io/cuda-quantum/latest/using/quick_start.html)
- [CUDA-Q Language Specification](https://nvidia.github.io/cuda-quantum/latest/specification/cudaq.html)
