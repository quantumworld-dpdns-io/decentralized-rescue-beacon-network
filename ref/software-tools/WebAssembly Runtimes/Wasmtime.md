# Wasmtime

| Field | Details |
| --- | --- |
| Name | Wasmtime |
| Category | WebAssembly runtime, WASI runtime, embeddable sandbox |
| Project | Bytecode Alliance |
| License | Apache License 2.0 with LLVM exception |
| Primary use | Running WebAssembly outside the browser and embedding Wasm safely inside host applications |
| Typical users | Platform engineers, runtime developers, plugin-system authors, edge/serverless teams, security-conscious application developers |
| Interfaces | CLI, Rust crate, C API, C++, Python, .NET, Go, Ruby |
| Key technologies | WebAssembly, WASI, Component Model, Cranelift, capability-based host access |
| Last verified | 2026-04-29 |

## English

### Overview

Wasmtime is a fast, secure, standalone runtime for WebAssembly outside the browser. It can be used as a command-line tool for running `.wasm` files or as an embeddable runtime inside larger applications.

The project is part of the Bytecode Alliance and supports WebAssembly modules, WASI, and the WebAssembly Component Model. In practice, this makes Wasmtime useful both for simple command-line execution and for product architectures that need portable plugins, tenant isolation, or language-neutral components.

Wasmtime uses Cranelift as its optimizing code generator and can execute JIT-compiled or ahead-of-time compiled WebAssembly. Its Rust embedding API exposes the main runtime primitives for compiling modules or components, instantiating them, linking host functions, configuring resources, and calling exported Wasm functions.

### Why it matters

- **Safe extension points:** Applications can run third-party or user-provided logic in a WebAssembly sandbox instead of loading native plugins directly.
- **Portable execution:** Code compiled to WebAssembly can run across operating systems and CPU architectures with a consistent runtime contract.
- **Server-side WebAssembly:** WASI gives Wasm programs controlled access to filesystems, clocks, randomness, networking, and other host capabilities.
- **Fast startup and density:** Wasm modules are usually smaller and cheaper to instantiate than full container images, which matters for edge, serverless, plugin, and multi-tenant workloads.
- **Embeddability:** Wasmtime is not only a CLI. It is also a library for Rust, C, Python, Go, .NET, Ruby, and other host environments.
- **Standards alignment:** Wasmtime tracks WebAssembly standards work and supports both core modules and the newer Component Model direction.

### Architecture/Concepts

- **Engine:** The global compilation and runtime environment. It is configured with `Config`, can be shared across threads, and is commonly created once per process.
- **Store:** Owns runtime state for WebAssembly objects such as functions, instances, memories, and tables. Host-specific state can be stored in `Store<T>` and accessed from host functions.
- **Module:** A compiled core WebAssembly module. Compilation is relatively expensive, so compiled modules can be reused and may be serialized for faster loading.
- **Component:** A compiled WebAssembly Component Model artifact. Components support interface-driven, cross-language composition.
- **Instance:** A live instantiation of a module or component. Exports such as functions and memories are retrieved from instances.
- **Func / TypedFunc:** Callable WebAssembly functions or host-defined functions exposed to Wasm. Typed function wrappers provide safer and faster calls.
- **Linker:** Connects imports requested by a module or component to host-provided functions, memories, WASI interfaces, or other definitions.
- **Memory, Table, Global, Resource:** Runtime objects that model WebAssembly state and host/component resources.
- **WASI:** The WebAssembly System Interface. Wasmtime uses the separate `wasmtime-wasi` crate for WASI support in Rust embeddings.
- **Component Model:** A higher-level Wasm architecture for portable interfaces and cross-language composition. Wasmtime exposes this through `wasmtime::component`.
- **Cranelift:** The optimizing code generator used by Wasmtime to produce machine code quickly.

Wasmtime's security model depends on WebAssembly isolation plus explicit host capabilities. A Wasm guest cannot directly access the host operating system unless the embedder links in host functions or WASI capabilities that grant that access. Resource controls, async execution, interruption, deterministic execution options, and memory configuration are important when running untrusted or multi-tenant code.

### Practical usage

Use the CLI when you want to run a Wasm program directly:

```bash
rustup target add wasm32-wasip1
rustc hello.rs --target wasm32-wasip1
wasmtime hello.wasm
```

Use the embedding API when Wasmtime is part of a larger product. A typical Rust embedding flow is:

1. Create an `Engine`, optionally with a custom `Config`.
2. Compile a core `Module` or Component Model `Component`.
3. Create a `Store<T>` for per-instance state and resource ownership.
4. Populate a `Linker` with host functions, WASI imports, or component interfaces.
5. Instantiate the module or component.
6. Retrieve exported functions, memories, or resources.
7. Call exports and handle traps, errors, fuel/timeout policies, and cleanup.

Common production patterns include:

- Embedding user-defined policy, transformation, or automation scripts as Wasm plugins.
- Running language-neutral business logic compiled from Rust, C/C++, Go, .NET, or other toolchains.
- Building edge/serverless platforms where cold start, isolation, and portability matter.
- Executing untrusted code with explicit filesystem, network, clock, and environment permissions.
- Precompiling or caching modules to reduce startup latency.
- Using WASI for portable system interfaces and the Component Model for typed, cross-language APIs.

Operational cautions:

- Treat WebAssembly sandboxing as one layer of defense, not the whole security model.
- Grant the minimum required WASI capabilities and host imports.
- Bound CPU time, memory, file access, network access, and long-running calls for untrusted workloads.
- Pin Wasmtime and language binding versions in production; runtime, WASI, and Component Model behavior can evolve.
- Test both successful execution and traps, guest memory misuse, cancellation, and resource cleanup.

### Learning checklist

- Install the Wasmtime CLI and run a minimal WASI `.wasm` program.
- Explain the difference between core WebAssembly modules and Component Model components.
- Understand `Engine`, `Store`, `Module`, `Component`, `Instance`, `Func`, `Memory`, and `Linker`.
- Write one host function and expose it to a Wasm guest.
- Run a WASI program with explicitly granted filesystem or environment access.
- Compare JIT-style compilation, serialized modules, and ahead-of-time deployment workflows.
- Learn how traps, errors, fuel/epoch interruption, async host functions, and resource limits work.
- Evaluate whether a workload should use raw modules, WASI Preview 1, WASI Preview 2, or the Component Model.

## 繁體中文

### 概觀

Wasmtime 是一個快速、安全、可獨立使用的 WebAssembly runtime，用於在瀏覽器之外執行 Wasm。它可以作為命令列工具執行 `.wasm` 檔案，也可以嵌入到大型應用程式中作為 sandboxed execution layer。

Wasmtime 是 Bytecode Alliance 專案，支援 WebAssembly modules、WASI 與 WebAssembly Component Model。實務上，它既適合直接執行 Wasm 程式，也適合用在需要 portable plugins、tenant isolation 或跨語言元件的產品架構。

Wasmtime 使用 Cranelift 作為 optimizing code generator，可以執行 JIT-compiled 或 ahead-of-time compiled WebAssembly。其 Rust embedding API 提供編譯 module 或 component、建立 instance、連接 host functions、設定資源與呼叫 Wasm exports 所需的主要 runtime primitives。

### 為什麼重要

- **安全的擴充點：** 應用程式可以在 WebAssembly sandbox 中執行第三方或使用者提供的邏輯，而不是直接載入 native plugins。
- **可攜式執行：** 編譯成 WebAssembly 的程式可以在不同作業系統與 CPU 架構上，以一致的 runtime contract 執行。
- **伺服器端 WebAssembly：** WASI 讓 Wasm 程式能以受控方式使用 filesystem、clock、randomness、networking 等 host capabilities。
- **快速啟動與高密度：** Wasm modules 通常比完整 container images 更小、啟動成本更低，適合 edge、serverless、plugin 與 multi-tenant workloads。
- **易於嵌入：** Wasmtime 不只是 CLI，也可透過 Rust、C、Python、Go、.NET、Ruby 等 host environment 作為 library 使用。
- **貼近標準：** Wasmtime 跟進 WebAssembly 標準化工作，支援 core modules，也支援新的 Component Model 方向。

### 架構/概念

- **Engine：** 全域 compilation 與 runtime environment。透過 `Config` 設定，可跨 threads 共用，通常每個 process 建立一個。
- **Store：** 擁有 WebAssembly objects 的 runtime state，例如 functions、instances、memories 與 tables。`Store<T>` 可保存 host-specific state，並讓 host functions 存取。
- **Module：** 已編譯的 core WebAssembly module。編譯成本相對高，因此 compiled modules 可重用，也可序列化以加快載入。
- **Component：** 已編譯的 WebAssembly Component Model artifact。Components 支援以 interface 為中心的跨語言組合。
- **Instance：** Module 或 component 的實際執行個體。Functions、memories 等 exports 會從 instance 取得。
- **Func / TypedFunc：** 可呼叫的 WebAssembly functions，或提供給 Wasm 的 host-defined functions。Typed wrappers 可提供更安全且更有效率的呼叫。
- **Linker：** 將 module 或 component 要求的 imports 連接到 host functions、memories、WASI interfaces 或其他 definitions。
- **Memory, Table, Global, Resource：** 表示 WebAssembly state 與 host/component resources 的 runtime objects。
- **WASI：** WebAssembly System Interface。Rust embedding 中通常透過獨立的 `wasmtime-wasi` crate 加入 WASI 支援。
- **Component Model：** 較高階的 Wasm architecture，用於 portable interfaces 與跨語言組合。Wasmtime 透過 `wasmtime::component` 暴露相關 API。
- **Cranelift：** Wasmtime 用來快速產生 machine code 的 optimizing code generator。

Wasmtime 的安全模型建立在 WebAssembly isolation 與明確 host capabilities 之上。Wasm guest 不能任意存取 host operating system；只有 embedder 連接 host functions 或授權 WASI capabilities 時，guest 才能使用對應能力。當執行 untrusted 或 multi-tenant code 時，resource controls、async execution、interruption、deterministic execution options 與 memory configuration 都很重要。

### 實務用法

若只是要直接執行 Wasm 程式，可使用 CLI：

```bash
rustup target add wasm32-wasip1
rustc hello.rs --target wasm32-wasip1
wasmtime hello.wasm
```

若 Wasmtime 是大型產品的一部分，則使用 embedding API。典型 Rust embedding 流程如下：

1. 建立 `Engine`，必要時搭配自訂 `Config`。
2. 編譯 core `Module` 或 Component Model `Component`。
3. 建立 `Store<T>`，保存 per-instance state 並管理資源 ownership。
4. 在 `Linker` 中加入 host functions、WASI imports 或 component interfaces。
5. 建立 module 或 component instance。
6. 取得 exported functions、memories 或 resources。
7. 呼叫 exports，並處理 traps、errors、fuel/timeout policies 與 cleanup。

常見 production patterns 包括：

- 將使用者定義的 policy、transformation 或 automation scripts 作為 Wasm plugins 嵌入。
- 執行由 Rust、C/C++、Go、.NET 或其他 toolchains 編譯出的 language-neutral business logic。
- 建立重視 cold start、isolation 與 portability 的 edge/serverless platforms。
- 在明確授權 filesystem、network、clock 與 environment permissions 的情況下執行 untrusted code。
- 預先編譯或快取 modules，以降低 startup latency。
- 使用 WASI 建立 portable system interfaces，並用 Component Model 建立 typed cross-language APIs。

營運注意事項：

- 將 WebAssembly sandboxing 視為多層防禦的一層，而不是完整安全模型。
- 只授權最低必要的 WASI capabilities 與 host imports。
- 對 untrusted workloads 限制 CPU time、memory、file access、network access 與 long-running calls。
- 在 production 中鎖定 Wasmtime 與 language binding versions；runtime、WASI 與 Component Model 行為仍會演進。
- 同時測試成功執行、traps、guest memory misuse、cancellation 與 resource cleanup。

### 學習檢核表

- 安裝 Wasmtime CLI，並執行最小 WASI `.wasm` 程式。
- 說明 core WebAssembly modules 與 Component Model components 的差異。
- 理解 `Engine`、`Store`、`Module`、`Component`、`Instance`、`Func`、`Memory` 與 `Linker`。
- 撰寫一個 host function，並暴露給 Wasm guest 使用。
- 在明確授權 filesystem 或 environment access 的情況下執行 WASI program。
- 比較 JIT-style compilation、serialized modules 與 ahead-of-time deployment workflows。
- 學習 traps、errors、fuel/epoch interruption、async host functions 與 resource limits。
- 評估 workload 應使用 raw modules、WASI Preview 1、WASI Preview 2 或 Component Model。

## References

- [Wasmtime official site](https://wasmtime.dev/)
- [Wasmtime documentation](https://docs.wasmtime.dev/)
- [Wasmtime Rust API reference](https://docs.wasmtime.dev/api/wasmtime/)
