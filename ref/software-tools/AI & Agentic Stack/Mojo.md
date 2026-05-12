# Mojo

| Field | Details |
| --- | --- |
| Category | AI infrastructure, systems programming, heterogeneous computing |
| Developer | Modular |
| Primary use | High-performance AI infrastructure, CPU/GPU kernels, Python-adjacent systems code |
| Language model | Pythonic syntax with static systems-programming features |
| Runtime/tooling | `mojo` CLI, compiler, standard library, REPL, formatter, debugger, language server |
| Current status | Pre-1.0; stable docs show v26.2, released 2026-03-19, with nightly builds also available |
| Cost/licensing note | Installable as Modular-provided Python or Conda packages; consult Modular terms for SDK licensing |
| Best fit | Python teams that need lower-level performance, hardware portability, or custom AI kernels without switching wholesale to C++/CUDA |
| Last verified | 2026-04-29 |

## English

### Overview

Mojo is Modular's systems programming language for high-performance AI infrastructure and heterogeneous hardware. It keeps a Python-like surface syntax while adding compiled performance, explicit types, value ownership, traits, compile-time metaprogramming, and direct access to lower-level CPU and GPU programming patterns.

The central idea is not "replace Python overnight." Mojo is designed to let Python-oriented teams move performance-critical code into a compiled language that can still interoperate with the Python ecosystem. Modular describes Mojo as built on MLIR so the same language can target CPUs, GPUs, and other accelerator classes through compiler and library support.

### Why it matters

AI systems often split work across Python orchestration, C++ extensions, CUDA kernels, build tooling, and deployment-specific glue. That split is powerful but expensive: teams need multiple language skill sets, careful memory ownership, custom build systems, and separate performance debugging workflows.

Mojo matters because it tries to collapse more of that stack into one language. A model-serving or ML infrastructure team can prototype near Python ergonomics, then optimize hot paths with static types, ownership-aware memory management, SIMD, and GPU kernels. For agentic and AI application stacks, Mojo is most relevant below the product layer: custom operators, inference kernels, data preprocessing, accelerator experiments, and Python package extensions.

The tradeoff is maturity. Modular's FAQ says Mojo is still early, below 1.0, and source stability is not guaranteed. Treat it as a serious emerging systems language rather than a drop-in replacement for mature production languages in every context.

### Architecture/Concepts

- **Pythonic syntax and interoperability:** Mojo adopts and extends Python syntax. Mojo can call Python modules through CPython, and Python can call explicitly bound Mojo code.
- **Compiled systems language:** Mojo code is compiled and can be built, run, packaged, formatted, debugged, or used through a REPL with the `mojo` CLI.
- **MLIR foundation:** Mojo is built on MLIR, a compiler infrastructure intended for multiple hardware targets, which supports Modular's goal of portable CPU, GPU, and accelerator programming.
- **Struct-based type system:** Mojo standard types such as `Int` and `String` are structs, and user-defined structs participate in the same model.
- **Traits:** Traits define shared behavior with compile-time checking and are intended to provide abstraction without runtime dispatch overhead.
- **Value semantics and ownership:** Mojo defaults toward value semantics and uses ownership to reduce memory-safety bugs such as use-after-free, double-free, and leaks without relying on a garbage collector.
- **Compile-time metaprogramming:** Parameterization, generics, constraints, and compile-time evaluation support highly specialized code generation.
- **Hardware-aware libraries:** Mojo exposes CPU vectorization patterns such as `SIMD` and a `gpu` package for hardware-agnostic GPU programming.

### Practical usage

Install Mojo through a Python or Conda package workflow. Modular's install guide currently recommends Pixi for the most reliable experience, while also documenting `uv`.

Minimal project flow:

```bash
pixi init hello-world -c https://conda.modular.com/max-nightly/ -c conda-forge
cd hello-world
pixi add mojo
pixi run mojo --version
```

Minimal program:

```mojo
def main():
    print("Hello, World!")
```

Run it:

```bash
mojo hello.mojo
```

Common commands:

- `mojo hello.mojo` runs a Mojo file directly.
- `mojo build hello.mojo` builds an executable.
- `mojo` starts the REPL when no command is supplied.
- `mojo format` formats source files.
- `mojo package` compiles a Mojo package.
- `mojo --version` prints the installed version.

Good first use cases:

- Rewrite a small Python bottleneck as Mojo and call it from Python.
- Prototype a custom numerical kernel.
- Work through Modular's GPU vector-add tutorial to understand blocks, grids, memory movement, kernel compilation, and asynchronous execution.
- Use Mojo where Python ergonomics matter but the implementation needs stronger control over types, memory, and hardware.

Avoid assuming that older examples still compile unchanged. Modern Mojo syntax has changed over time; for example, `def` is now the standard function declaration keyword, while `fn` is deprecated in current changelog notes.

### Learning checklist

- Understand where Mojo fits relative to Python, C++, CUDA, Triton, and Rust.
- Install the `mojo` package and verify `mojo --version`.
- Run a single-file `def main()` program.
- Learn variables, explicit types, structs, methods, traits, and modules.
- Practice value semantics, ownership, borrowing conventions, references, and destructors.
- Use Python interop in both directions: calling Python from Mojo and exposing Mojo to Python.
- Build and run a small package with the `mojo` CLI.
- Learn compile-time parameters, generics, constraints, and `comptime` constructs.
- Write a CPU-optimized loop using static types and SIMD-aware APIs.
- Complete the official GPU tutorial before writing custom kernels.
- Track the changelog before upgrading because Mojo is still evolving quickly.

## 繁體中文

### 概述

Mojo 是 Modular 推出的系統程式語言，目標是支援高效能 AI 基礎設施與異質硬體。它保留接近 Python 的語法，同時加入編譯式效能、明確型別、值擁有權、traits、編譯期 metaprogramming，以及較底層的 CPU/GPU 程式設計能力。

它的核心定位不是立刻取代 Python，而是讓熟悉 Python 的團隊能把效能關鍵路徑移到可編譯、可最佳化的語言中，並且仍能和 Python 生態互通。Modular 說明 Mojo 建立在 MLIR 之上，因此同一套語言與工具鏈可朝 CPU、GPU 與其他加速器目標發展。

### 為什麼重要

AI 系統常常同時使用 Python 做 orchestration、C++ extension 做效能、CUDA kernel 做 GPU 加速，再加上各種建置與部署 glue code。這種組合很強，但成本也高：團隊需要多種語言能力、記憶體管理知識、客製 build 流程，以及分散的效能除錯方式。

Mojo 的重要性在於它嘗試把更多層次整合到同一個語言模型中。模型服務、ML infrastructure 或 agentic AI stack 的團隊，可以用接近 Python 的方式開發，再針對熱點路徑使用靜態型別、ownership-aware 記憶體管理、SIMD 與 GPU kernel 進行最佳化。對 AI 應用來說，Mojo 最適合放在產品層下方：自訂 operator、推論 kernel、資料前處理、加速器實驗，以及 Python 套件 extension。

需要注意的是成熟度。Modular FAQ 指出 Mojo 仍在早期、尚未達 1.0，而且不保證 source stability。應把它視為有潛力且發展快速的新興系統語言，而不是所有 production 場景都能直接替換既有成熟語言的選項。

### 架構/概念

- **Pythonic syntax 與互通性：** Mojo 採用並延伸 Python 語法。Mojo 可透過 CPython 呼叫 Python module，Python 也能呼叫明確宣告 binding 的 Mojo 程式碼。
- **編譯式系統語言：** Mojo 程式會被編譯，並可透過 `mojo` CLI 執行、建置、封裝、格式化、除錯或進入 REPL。
- **MLIR 基礎：** Mojo 建立在 MLIR 上，這是面向多種硬體目標的 compiler infrastructure，支撐 Modular 對 CPU、GPU 與加速器可攜程式設計的願景。
- **以 struct 為核心的型別系統：** `Int`、`String` 等標準型別也是 struct，自訂 struct 使用同一套模型。
- **Traits：** Traits 用來定義共享行為，透過編譯期檢查提供抽象能力，並避免執行期 dispatch 成本。
- **值語意與 ownership：** Mojo 偏向值語意，並用 ownership 降低 use-after-free、double-free、memory leak 等記憶體安全問題，而不依賴 garbage collector。
- **編譯期 metaprogramming：** Parameterization、generics、constraints 與 compile-time evaluation 可用來產生高度特化的程式碼。
- **硬體感知函式庫：** Mojo 提供如 `SIMD` 的 CPU vectorization 模式，也提供 `gpu` package 支援硬體無關的 GPU programming。

### 實務使用

Mojo 可透過 Python 或 Conda package workflow 安裝。Modular 的安裝文件目前建議 Pixi 作為最可靠的體驗，同時也提供 `uv` 安裝方式。

最小專案流程：

```bash
pixi init hello-world -c https://conda.modular.com/max-nightly/ -c conda-forge
cd hello-world
pixi add mojo
pixi run mojo --version
```

最小程式：

```mojo
def main():
    print("Hello, World!")
```

執行：

```bash
mojo hello.mojo
```

常用命令：

- `mojo hello.mojo` 直接執行 Mojo 檔案。
- `mojo build hello.mojo` 建置 executable。
- `mojo` 在未提供命令時啟動 REPL。
- `mojo format` 格式化原始碼。
- `mojo package` 編譯 Mojo package。
- `mojo --version` 顯示目前安裝版本。

適合的第一批使用情境：

- 將小型 Python 效能瓶頸改寫成 Mojo，並從 Python 呼叫。
- 原型化自訂數值 kernel。
- 依照 Modular 官方 GPU vector-add 教學，理解 blocks、grids、memory movement、kernel compilation 與 asynchronous execution。
- 在需要 Python 開發手感，但實作層又需要更強型別、記憶體與硬體控制的地方使用 Mojo。

不要假設舊範例一定能在新版 Mojo 直接編譯。例如目前 changelog 已說明 `def` 是標準函式宣告關鍵字，而 `fn` 已被 deprecated。

### 學習檢核表

- 理解 Mojo 相對於 Python、C++、CUDA、Triton、Rust 的定位。
- 安裝 `mojo` package，並用 `mojo --version` 確認版本。
- 執行單檔 `def main()` 程式。
- 學會 variables、明確型別、structs、methods、traits、modules。
- 練習 value semantics、ownership、borrowing conventions、references、destructors。
- 練習雙向 Python interop：從 Mojo 呼叫 Python，以及從 Python 呼叫 Mojo。
- 使用 `mojo` CLI 建置並執行小型 package。
- 學習 compile-time parameters、generics、constraints 與 `comptime` constructs。
- 用靜態型別與 SIMD-aware API 寫一個 CPU 最佳化 loop。
- 在撰寫自訂 GPU kernel 前，先完成官方 GPU tutorial。
- 升級前追蹤 changelog，因為 Mojo 仍快速演進。

## References

- [Mojo Manual - Modular](https://docs.modular.com/mojo/manual/)
- [Install Mojo - Modular](https://docs.modular.com/mojo/manual/install/)
- [Mojo changelog - Modular](https://docs.modular.com/mojo/changelog/)
- [Mojo CLI - Modular](https://docs.modular.com/mojo/cli/)
- [Python interoperability - Modular](https://docs.modular.com/mojo/manual/python/)
- [Get started with GPU programming - Modular](https://docs.modular.com/mojo/manual/gpu/intro-tutorial/)
- [Mojo vision - Modular](https://docs.modular.com/mojo/vision/)
- [Mojo roadmap - Modular](https://docs.modular.com/mojo/roadmap/)
- [Mojo FAQ - Modular](https://docs.modular.com/mojo/faq/)
