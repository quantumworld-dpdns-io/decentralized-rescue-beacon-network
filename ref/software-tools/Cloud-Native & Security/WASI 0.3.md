# WASI 0.3

| Field | Details |
| --- | --- |
| Category | Cloud-native runtime, WebAssembly, security sandbox |
| Status | Forthcoming / preview release |
| Primary audience | Platform engineers, edge/serverless developers, runtime/toolchain maintainers |
| Key capability | Native asynchronous WebAssembly components through the Component Model |
| Main interfaces | Clocks, random, filesystem, sockets, CLI, HTTP |
| Reference runtimes | Wasmtime 37+ previews; broader runtime support should be verified per runtime |

## English

### Overview

WASI 0.3 is the next major step in the WebAssembly System Interface after WASI 0.2. WASI defines modular APIs that let WebAssembly programs interact with host capabilities such as files, clocks, randomness, sockets, command-line environments, and HTTP while preserving WebAssembly's sandboxed execution model.

The central theme of WASI 0.3 is native async support for the WebAssembly Component Model. Instead of representing asynchronous host I/O through ad hoc polling patterns or runtime-specific glue, WASI 0.3 introduces component-level asynchrony in the Canonical ABI, including explicit `stream<T>` and `future<T>` types.

WASI.dev currently describes WASI 0.3 as a forthcoming release, with previews available in Wasmtime 37+. Treat it as a preview target for experimentation, portability testing, and toolchain preparation rather than a stable production contract unless your runtime and language toolchain document support for the exact version you use.

### Why it matters

- **Better server-side WebAssembly:** Async I/O is a baseline requirement for network services, proxies, serverless functions, edge workloads, and high-concurrency systems.
- **Cleaner component composition:** Components written in different languages can expose asynchronous contracts through shared WIT interfaces instead of bespoke host adapters.
- **More practical edge and plugin runtimes:** WASI combines small WebAssembly binaries, capability-based access, and fast instantiation with host-managed resources.
- **Stronger portability story:** The goal is to move async behavior into the common component ABI so runtimes and tools can converge on the same semantics.
- **Security by capability:** WASI APIs are intended to expose only capabilities granted by the host, which is useful for plugin systems and multi-tenant execution.

### Architecture/Concepts

| Concept | Meaning |
| --- | --- |
| WebAssembly module | A core Wasm binary. WASI 0.1 / Preview 1 is commonly used with modules and remains widely deployed. |
| WebAssembly component | A Component Model binary that can use WIT-defined interfaces and compose with components from other languages. |
| WIT | WebAssembly Interface Type, the IDL used to describe Component Model interfaces. |
| Canonical ABI | The Component Model ABI layer that defines how interface types cross component boundaries. WASI 0.3 adds async semantics here. |
| `future<T>` | A typed value representing an asynchronous result. |
| `stream<T>` | A typed value representing asynchronous streams of data. |
| Capability-based access | The host grants explicit access to resources such as directories, sockets, clocks, or HTTP clients. |

WASI 0.3 is iterative relative to WASI 0.2. It refactors the WASI 0.2-era interfaces to take advantage of native async rather than replacing the Component Model direction. The proposed draft interface areas are:

- Clocks
- Random
- Filesystem
- Sockets
- CLI
- HTTP

### Practical usage

- Use WASI 0.3 today for prototypes, runtime evaluation, and early integration tests.
- Check the exact runtime support matrix before relying on it. Wasmtime 37+ exposes WASI 0.3 preview support, but Wasmtime's own documentation marks WASIp3 support as experimental, unstable, and incomplete.
- Prefer components and WIT when designing new cross-language APIs. WASI 0.3 is aligned with the Component Model rather than the older WASI 0.1 module-only style.
- Keep WASI 0.2 compatibility in mind for production systems until the runtime, language bindings, and deployment platform you use all document stable WASI 0.3 support.
- Test async semantics directly: streaming, cancellation behavior, backpressure, host resource cleanup, and inter-component calls are the areas most likely to expose portability gaps.
- Pin toolchain versions in CI. WASI 0.3 preview behavior may change across runtime, bindings-generator, and WIT package releases.

Example evaluation workflow:

| Step | Action |
| --- | --- |
| 1 | Choose a runtime with documented WASI 0.3 preview support, such as Wasmtime 37+. |
| 2 | Model the API boundary in WIT and decide which functions should return `future<T>` or use `stream<T>`. |
| 3 | Build a small component that exercises HTTP, filesystem, or socket I/O under realistic load. |
| 4 | Run component-level tests for success, error, cancellation, and resource cleanup cases. |
| 5 | Record runtime flags, bindings versions, and known incompatibilities before expanding usage. |

### Learning checklist

- Explain the difference between WASI 0.1 modules and WASI 0.2/0.3 components.
- Read a simple WIT file and identify imports, exports, resources, records, variants, and worlds.
- Describe why async belongs in the Canonical ABI rather than only in host-specific adapters.
- Compare `future<T>` and `stream<T>` and identify common use cases for each.
- Understand how capability-based access limits filesystem, network, and host-resource exposure.
- Build or run a minimal WASI component in a runtime that documents Component Model support.
- Verify the maturity level of a runtime before using WASI 0.3 in production.

## 繁體中文

### 概覽

WASI 0.3 是 WebAssembly System Interface 在 WASI 0.2 之後的重要演進。WASI 提供一組模組化 API，讓 WebAssembly 程式可以在沙箱模型下使用主機能力，例如檔案、時鐘、亂數、Socket、命令列環境與 HTTP。

WASI 0.3 的核心重點是替 WebAssembly Component Model 加入原生非同步能力。過去非同步主機 I/O 常需要輪詢、手寫狀態機或執行期專用轉接層；WASI 0.3 則把非同步語意放進 Canonical ABI，並引入明確的 `stream<T>` 與 `future<T>` 型別。

依 WASI.dev 目前說明，WASI 0.3 仍屬即將推出的預覽目標，Wasmtime 37+ 已提供預覽支援。除非你使用的執行期與語言工具鏈明確標示支援特定版本，否則應把它視為實驗、可攜性測試與工具鏈準備用途，而不是穩定的正式生產合約。

### 為什麼重要

- **更適合伺服器端 WebAssembly：** 網路服務、Proxy、Serverless Function、邊緣工作負載與高併發系統都需要非同步 I/O。
- **元件組合更乾淨：** 不同語言寫成的元件可以透過共同 WIT 介面暴露非同步合約，減少客製化主機轉接層。
- **邊緣與外掛執行環境更實用：** WASI 結合小型 Wasm 二進位、能力式存取控制與快速啟動，適合外掛與多租戶場景。
- **可攜性更清楚：** 非同步行為進入共同 Component ABI 後，執行期與工具鏈較容易收斂到一致語意。
- **以能力為基礎的安全模型：** WASI API 原則上只暴露主機授權的能力，有助於限制檔案、網路與系統資源存取。

### 架構/概念

| 概念 | 說明 |
| --- | --- |
| WebAssembly module | 核心 Wasm 二進位。WASI 0.1 / Preview 1 常與 module 搭配，至今仍廣泛使用。 |
| WebAssembly component | 符合 Component Model 的二進位，可使用 WIT 介面並與不同語言產生的元件組合。 |
| WIT | WebAssembly Interface Type，用來描述 Component Model 介面的 IDL。 |
| Canonical ABI | Component Model 的 ABI 層，定義介面型別如何跨越元件邊界；WASI 0.3 在此加入非同步語意。 |
| `future<T>` | 代表非同步結果的型別。 |
| `stream<T>` | 代表非同步資料串流的型別。 |
| 能力式存取 | 主機明確授權目錄、Socket、時鐘或 HTTP client 等資源，元件不能任意存取未授權資源。 |

相較於 WASI 0.2，WASI 0.3 是漸進式演進。它延續 Component Model 方向，並把 WASI 0.2 時期的介面重構為可利用原生非同步能力。預計的草案介面範圍包括：

- Clocks
- Random
- Filesystem
- Sockets
- CLI
- HTTP

### 實務使用

- 現階段適合用 WASI 0.3 做原型、執行期評估與早期整合測試。
- 依賴前先確認精確的執行期支援狀態。Wasmtime 37+ 提供 WASI 0.3 預覽，但 Wasmtime 文件也標示 WASIp3 支援仍是 experimental、unstable、incomplete。
- 新的跨語言 API 設計應優先採用 component 與 WIT。WASI 0.3 對齊 Component Model，而不是早期 WASI 0.1 的 module-only 風格。
- 在生產系統中，若執行期、語言綁定與部署平台尚未明確提供穩定 WASI 0.3 支援，仍應保留 WASI 0.2 相容性。
- 直接測試非同步語意：串流、取消、背壓、主機資源清理與元件間呼叫，是最容易出現可攜性差異的區域。
- 在 CI 中鎖定工具鏈版本。WASI 0.3 預覽行為可能隨執行期、bindings generator 或 WIT package 版本變動。

範例評估流程：

| 步驟 | 行動 |
| --- | --- |
| 1 | 選擇明確標示 WASI 0.3 預覽支援的執行期，例如 Wasmtime 37+。 |
| 2 | 用 WIT 建模 API 邊界，決定哪些函式應回傳 `future<T>` 或使用 `stream<T>`。 |
| 3 | 建立小型 component，針對 HTTP、filesystem 或 socket I/O 做接近真實情境的負載測試。 |
| 4 | 撰寫元件層級測試，涵蓋成功、錯誤、取消與資源清理。 |
| 5 | 記錄執行期旗標、綁定版本與已知不相容處，再逐步擴大使用。 |

### 學習檢核表

- 能說明 WASI 0.1 module 與 WASI 0.2/0.3 component 的差異。
- 能閱讀簡單 WIT 檔案，辨識 imports、exports、resources、records、variants 與 worlds。
- 能解釋為什麼非同步應進入 Canonical ABI，而不只是主機專用 adapter。
- 能比較 `future<T>` 與 `stream<T>`，並列出常見使用情境。
- 理解能力式存取如何限制檔案、網路與主機資源暴露。
- 能在支援 Component Model 的執行期建置或執行最小 WASI component。
- 在導入生產前，能確認執行期與工具鏈的成熟度。

## References

- [WASI.dev: Interfaces](https://wasi.dev/interfaces)
- [WASI.dev: Roadmap](https://wasi.dev/roadmap)
- [WebAssembly/WASI GitHub repository](https://github.com/WebAssembly/WASI)
- [Wasmtime WASI crate documentation](https://docs.wasmtime.dev/api/wasmtime_wasi/)
- [WebAssembly specifications](https://webassembly.org/specs/)
