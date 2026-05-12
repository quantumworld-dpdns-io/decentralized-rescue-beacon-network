# Qiskit

| Field | Details |
| --- | --- |
| Category | Quantum computing SDK and software stack |
| Maintainer / ecosystem | IBM Quantum and open-source Qiskit community |
| Primary use | Build, optimize, transpile, simulate, and execute quantum circuits and experiments |
| Typical users | Quantum software developers, researchers, educators, algorithm teams, HPC/quantum integration teams |
| Core interfaces | Python SDK, circuit API, transpiler, primitives, providers, visualization tools, OpenQASM/QPY serialization |
| Common targets | Local simulators, IBM Quantum systems, and third-party quantum hardware through provider plugins |
| Current note | IBM lists Qiskit v2.4 as the current release on the Qiskit product page reviewed for this file |
| Last reviewed | 2026-04-29 |

## English

### Overview

Qiskit is IBM Quantum's open-source software stack for circuit-level quantum computing, algorithm research, and utility-scale experiment development. It gives Python developers a practical workflow for constructing quantum circuits, compiling them for target hardware, executing them through primitives and providers, and analyzing results.

The SDK centers on explicit circuit construction with `QuantumCircuit`, quantum information utilities, transpilation and synthesis passes, primitive execution interfaces, backend/provider abstractions, result objects, visualization helpers, and serialization formats such as OpenQASM and QPY. IBM positions Qiskit as a backend-agnostic stack that can run across IBM Quantum hardware and other provider ecosystems.

### Why it matters

Quantum software has to bridge a large gap between abstract algorithms and constrained hardware. Real devices have limited connectivity, noisy operations, changing calibration data, queueing behavior, and backend-specific instruction sets. Qiskit matters because it makes that translation process explicit and programmable.

For learners, Qiskit is one of the most accessible ways to move from gates and measurement to executable programs. For researchers, it provides a common environment for testing algorithms, quantum information workflows, error-mitigation techniques, compilation strategies, and hardware-aware experiments. For platform teams, its provider and primitive model creates a path from local prototypes to managed execution on cloud-accessible quantum systems.

### Architecture/Concepts

Key concepts:

- **QuantumCircuit**: The main object for composing qubits, classical bits, gates, measurements, control flow, and higher-level circuit structures.
- **Circuit library**: Reusable circuits and gates for common algorithmic patterns, arithmetic, data preparation, and benchmarking.
- **Quantum information**: Operators, states, channels, Pauli objects, measures, and utilities for reasoning about circuits and results mathematically.
- **Transpiler**: Converts circuits into forms compatible with a target backend by applying layout, routing, basis translation, optimization, and scheduling passes.
- **Pass manager**: A configurable pipeline of transpiler passes; preset pass managers provide common optimization levels and backend-aware defaults.
- **Synthesis**: Decomposes higher-level operations into supported gate sets, often trading off depth, two-qubit gate count, and approximation quality.
- **Primitives**: Execution-oriented interfaces for common experiment patterns, especially sampling measurement outcomes and estimating observables.
- **Providers and backends**: Abstractions for connecting Qiskit code to simulators, fake/testing backends, IBM Quantum systems, and third-party hardware providers.
- **Results and visualization**: Data structures and plotting helpers for counts, distributions, state visualizations, circuit diagrams, and experiment inspection.
- **Serialization**: OpenQASM support for circuit interchange and QPY for Qiskit-native circuit persistence.

Qiskit's practical workflow is usually: model the problem, build a circuit, select or describe a target backend, transpile the circuit for that target, execute through an appropriate primitive or provider, then inspect and post-process results.

### Practical usage

Use Qiskit when:

- You need a Python-first SDK for building and analyzing quantum circuits.
- You want to learn quantum programming with a tool that maps cleanly from textbook gates to executable experiments.
- You need hardware-aware transpilation for IBM Quantum or other provider-backed systems.
- You are prototyping algorithms for optimization, simulation, quantum machine learning, chemistry, or quantum information science.
- You need to compare simulator results with runs on real quantum hardware.
- You want access to an ecosystem of tutorials, provider plugins, addons, and community extensions.

Typical workflow:

1. Install the SDK with `pip install qiskit`.
2. Create a `QuantumCircuit`, add gates, and include measurements where needed.
3. Use local simulators or testing backends while developing small circuits.
4. Choose a real or simulated target backend and transpile the circuit for its constraints.
5. Execute through primitives or provider APIs, depending on the experiment and runtime environment.
6. Analyze counts, expectation values, distributions, circuit depth, two-qubit gate count, and error-sensitive behavior.
7. Iterate on circuit design, transpiler settings, error mitigation, and post-processing.

Implementation tips:

- Treat transpilation as part of the program, not a final mechanical step; layout, routing, and basis choices can change experiment quality.
- Track circuit depth, two-qubit gate count, measurement count, and backend topology before running on hardware.
- Use fake/testing backends and simulators to validate structure, but do not assume simulator behavior predicts noisy hardware results.
- Prefer primitives for standard sampling and observable-estimation workflows.
- Pin package versions for reproducible research and record backend, calibration, transpiler settings, and seed values where relevant.
- Check IBM Quantum documentation for API changes because the SDK, runtime, primitives, and platform services evolve quickly.

### Learning checklist

- [ ] Install Qiskit and create a Bell-state circuit.
- [ ] Add measurements and inspect result counts from a simulator.
- [ ] Explain qubits, classical bits, gates, measurements, and circuit diagrams.
- [ ] Use `QuantumCircuit` and at least one circuit-library component.
- [ ] Transpile a circuit for a target backend and compare depth and two-qubit gate count before and after.
- [ ] Explain what a backend, provider, primitive, transpiler pass, and pass manager do.
- [ ] Run or review a primitive-based sampling or observable-estimation example.
- [ ] Export or inspect a circuit with OpenQASM or QPY.
- [ ] Review IBM Quantum learning material and current API documentation before using hardware.

## 繁體中文

### 概覽

Qiskit 是 IBM Quantum 維護的開源量子運算軟體堆疊，主要用於 circuit-level quantum programming、演算法研究，以及 utility-scale experiments。它讓 Python 開發者可以建立 quantum circuits、針對目標硬體進行編譯、透過 primitives 與 providers 執行實驗，並分析結果。

SDK 的核心包含 `QuantumCircuit` 電路建模、quantum information 工具、transpilation 與 synthesis passes、primitive execution interfaces、backend/provider abstractions、result objects、visualization helpers，以及 OpenQASM、QPY 等序列化格式。IBM 將 Qiskit 定位為 backend-agnostic 的量子軟體 stack，可連接 IBM Quantum hardware，也可透過 provider plugins 對接其他硬體生態系。

### 為什麼重要

量子軟體必須把抽象演算法轉換成受硬體限制的可執行實驗。真實量子裝置會受到 qubit connectivity、noise、calibration、queueing、backend-specific instruction sets 等因素影響。Qiskit 的價值在於把這個轉換流程變成可觀察、可設定、可程式化的工作流。

對學習者而言，Qiskit 是從 quantum gates、measurement 到實際程式執行的常見入口。對研究者而言，它提供測試 algorithms、quantum information workflows、error mitigation、compilation strategies 與 hardware-aware experiments 的共同環境。對平台團隊而言，provider 與 primitive model 則提供從本機 prototype 走向 cloud quantum execution 的路徑。

### 架構/概念

核心概念：

- **QuantumCircuit**：用來組合 qubits、classical bits、gates、measurements、control flow 與高階電路結構的主要物件。
- **Circuit library**：提供常見 algorithmic patterns、arithmetic、data preparation 與 benchmarking 的可重用 circuits/gates。
- **Quantum information**：包含 operators、states、channels、Pauli objects、metrics 與相關工具，用於數學上分析 circuits 與 results。
- **Transpiler**：透過 layout、routing、basis translation、optimization、scheduling 等 passes，將 circuit 轉成符合 target backend 的形式。
- **Pass manager**：可設定的 transpiler pipeline；preset pass managers 提供常見 optimization levels 與 backend-aware defaults。
- **Synthesis**：將高階 operations 分解成目標 gate set，通常需要在 depth、two-qubit gate count 與 approximation quality 之間取捨。
- **Primitives**：面向實驗執行的介面，常用於 sampling measurement outcomes 與 estimating observables。
- **Providers and backends**：把 Qiskit code 連到 simulators、fake/testing backends、IBM Quantum systems 與第三方 hardware providers 的抽象層。
- **Results and visualization**：用於 counts、distributions、state visualizations、circuit diagrams 與實驗檢查的資料結構與繪圖工具。
- **Serialization**：OpenQASM 用於 circuit interchange，QPY 則用於 Qiskit-native circuit persistence。

Qiskit 的常見流程是：建模問題、建立 circuit、選擇或描述 target backend、為該 backend transpile circuit、用合適的 primitive 或 provider 執行，最後檢查與後處理 results。

### 實務使用

適合使用 Qiskit 的情境：

- 需要 Python-first SDK 來建立與分析 quantum circuits。
- 想用能從教科書 gates 對應到可執行 experiments 的工具學習量子程式設計。
- 需要針對 IBM Quantum 或其他 provider-backed systems 做 hardware-aware transpilation。
- 正在 prototype optimization、simulation、quantum machine learning、chemistry 或 quantum information science 演算法。
- 需要比較 simulator results 與 real quantum hardware runs。
- 想使用 tutorials、provider plugins、addons 與 community extensions 的生態系。

常見流程：

1. 用 `pip install qiskit` 安裝 SDK。
2. 建立 `QuantumCircuit`，加入 gates，並依需求加入 measurements。
3. 開發小型 circuits 時先使用 local simulators 或 testing backends。
4. 選擇真實或模擬 target backend，並依其限制 transpile circuit。
5. 依實驗與 runtime 環境，透過 primitives 或 provider APIs 執行。
6. 分析 counts、expectation values、distributions、circuit depth、two-qubit gate count 與對 noise 敏感的行為。
7. 反覆調整 circuit design、transpiler settings、error mitigation 與 post-processing。

實作建議：

- 將 transpilation 視為程式的一部分，而不是最後的機械步驟；layout、routing 與 basis choices 會影響實驗品質。
- 上硬體前先追蹤 circuit depth、two-qubit gate count、measurement count 與 backend topology。
- 用 fake/testing backends 與 simulators 驗證結構，但不要假設 simulator behavior 一定能預測 noisy hardware results。
- 標準 sampling 與 observable-estimation workflows 優先考慮 primitives。
- 研究重現性需要 pin package versions，並記錄 backend、calibration、transpiler settings 與 seed values。
- SDK、runtime、primitives 與平台服務變動快，使用硬體或新 API 前應查 IBM Quantum 最新文件。

### 學習檢核表

- [ ] 安裝 Qiskit 並建立 Bell-state circuit。
- [ ] 加入 measurements，並從 simulator 檢查 result counts。
- [ ] 說明 qubits、classical bits、gates、measurements 與 circuit diagrams。
- [ ] 使用 `QuantumCircuit` 與至少一個 circuit-library component。
- [ ] 針對 target backend transpile circuit，並比較前後 depth 與 two-qubit gate count。
- [ ] 說明 backend、provider、primitive、transpiler pass 與 pass manager 的角色。
- [ ] 執行或閱讀一個 primitive-based sampling 或 observable-estimation 範例。
- [ ] 使用 OpenQASM 或 QPY 匯出或檢查 circuit。
- [ ] 使用硬體前，先閱讀 IBM Quantum learning material 與 current API documentation。

## References

- [IBM Quantum Qiskit product page](https://www.ibm.com/quantum/qiskit)
- [Qiskit SDK API documentation](https://quantum.cloud.ibm.com/docs/api/qiskit)
- [IBM Quantum learning path: Getting started with Qiskit](https://learning.quantum.ibm.com/learning-path/getting-started-with-qiskit) - this supplied URL currently redirects to a notice that the page no longer exists and that updated learning pathways will be available soon.
