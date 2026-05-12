# Fermyon Spin

| Field | Details |
| --- | --- |
| Category | Serverless WebAssembly application framework and CLI |
| Primary use | Build, run, distribute, and deploy event-driven Wasm microservices and web applications |
| Interfaces | Spin CLI, `spin.toml` manifest, language SDKs, HTTP and Redis triggers, Spin plugins |
| Languages | Rust, JavaScript/TypeScript, Python, Go, .NET, and other WASI-compatible languages |
| Runtime model | WebAssembly components with sandboxed, capability-based execution |
| Best fit | Lightweight APIs, edge services, full-stack Wasm apps, serverless functions, and portable microservices |
| Last reviewed | 2026-04-29 |

## English

### Overview

Fermyon Spin is an open source framework and developer toolchain for building server-side applications as WebAssembly. It gives developers a serverless-style workflow: create an app from a template, compile components to Wasm, run the app locally, and deploy it to Fermyon Cloud, Kubernetes through SpinKube, or compatible Wasm platforms.

Spin focuses on microservices, APIs, websites, event handlers, and full-stack applications rather than general-purpose container replacement. Its main value is combining WebAssembly's small artifacts, fast startup, portability, and sandboxing with a practical developer experience built around `spin new`, `spin build`, `spin up`, and deployment commands.

### Why it matters

- It makes WebAssembly usable for everyday backend and edge application development.
- It gives serverless teams a portable packaging model that is not tied to one cloud function runtime.
- It can start lightweight request handlers quickly enough to support scale-to-zero and dense deployments.
- It lets teams mix languages in one application while keeping components isolated.
- It uses explicit capability declarations so components only receive the host access they need.
- It provides a path from local development to cloud, registry, or Kubernetes deployment without rewriting the app.

### Architecture/Concepts

| Concept | Meaning |
| --- | --- |
| Spin CLI | The developer command-line tool used to create, build, run, watch, package, and deploy applications. |
| Spin application | A collection of one or more Wasm components plus routing, triggers, build commands, and capability configuration. |
| `spin.toml` | The application manifest that defines components, sources, triggers, routes, build steps, variables, and allowed capabilities. |
| Component | A WebAssembly Component Model unit that handles an event, such as an HTTP request or Redis message. |
| Trigger | The event source that invokes a component. Common triggers include HTTP routing and Redis pub/sub. |
| Capability-based access | Host resources such as files, outbound network hosts, variables, key/value stores, SQLite, Redis, MySQL, and PostgreSQL must be declared rather than assumed. |
| WASI | The standards-oriented interface layer that lets Wasm code interact with host capabilities in a portable way. |
| Component composition | Spin 2.0 moves toward composing isolated components across language boundaries using WebAssembly Component Model interfaces. |
| Local runtime | `spin up` runs the application locally for testing, usually exposing HTTP routes on a local port. |
| Deployment targets | Spin apps can be deployed to Fermyon Cloud, pushed to registries, or run in Kubernetes-oriented environments such as SpinKube. |

Spin originally introduced a framework for writing server-side Wasm modules that answer HTTP requests and other events. Spin 1.0 stabilized the developer workflow and broadened language, database, registry, Kubernetes, key/value, and Vault-backed configuration support. Spin 2.0 made the Component Model a first-class part of the application model, improving portability, SDK ergonomics, and polyglot composition.

### Practical usage

Use Spin when:

- You are building small APIs, webhook handlers, websites, or event-driven services.
- You want serverless ergonomics with a portable Wasm artifact instead of a cloud-specific function bundle.
- Cold-start behavior, deployment density, and sandboxing matter.
- Different components are naturally written in different languages.
- You want local development, cloud deployment, and Kubernetes deployment to share the same app structure.

Basic workflow:

```bash
spin new
spin build
spin up
```

Typical development loop:

```bash
spin new hello-spin --template http-rust
cd hello-spin
spin build
spin up
curl http://127.0.0.1:3000/
```

Common operational patterns:

- Use templates to start with the right language and trigger.
- Keep each component small and focused on one route, event, or responsibility.
- Declare outbound hosts and data services explicitly in `spin.toml`.
- Use built-in KV or SQLite for lightweight persistence, and external databases for larger production data.
- Use `spin watch` during development and `spin doctor` when diagnosing local setup problems.
- Package or deploy through `spin cloud deploy`, registry workflows, or Kubernetes/SpinKube depending on the target platform.

Operational cautions:

- Spin is best for event-driven Wasm services; long-running background processes and OS-heavy workloads may still fit containers better.
- Language support depends on SDK maturity and WASI support, so verify the target language before committing.
- Capability restrictions are a security advantage, but they require deliberate manifest maintenance.
- Validate database, secrets, observability, and deployment target behavior in the actual runtime, not only with `spin up`.
- Treat Spin 1.x and Spin 2.x examples carefully because manifest structure and Component Model assumptions differ.

### Learning checklist

- [ ] Install the Spin CLI and create a template-based HTTP app.
- [ ] Build and run a Spin app locally with `spin build` and `spin up`.
- [ ] Read and modify `spin.toml` routes, components, build commands, and capabilities.
- [ ] Add a second component in another language and understand how requests route to each component.
- [ ] Use a built-in service such as key/value, SQLite, variables, or outbound HTTP.
- [ ] Learn how the WebAssembly Component Model changes Spin 2.x application structure.
- [ ] Deploy the same app to a target such as Fermyon Cloud, a registry flow, or Kubernetes with SpinKube.
- [ ] Decide when Spin is a better fit than containers, traditional serverless functions, or a general Wasm runtime like Wasmtime.

## 繁體中文

### 概覽

Fermyon Spin 是開源的 WebAssembly 後端應用框架與開發工具鏈。它提供類 serverless 的工作流程：從 template 建立應用、將 component 編譯成 Wasm、在本機執行測試，並部署到 Fermyon Cloud、透過 SpinKube 部署到 Kubernetes，或部署到相容的 Wasm 平台。

Spin 的重點不是取代所有 container，而是服務 microservice、API、網站、事件處理器與 full-stack 應用。它把 WebAssembly 的小型 artifact、快速啟動、可攜性與 sandboxing，包裝成以 `spin new`、`spin build`、`spin up` 與部署指令為核心的實用開發體驗。

### 為什麼重要

- 讓 WebAssembly 更容易用於日常後端與 edge 應用開發。
- 為 serverless 團隊提供不綁定單一雲端 function runtime 的可攜封裝模型。
- 輕量 request handler 的啟動速度適合 scale-to-zero 與高密度部署。
- 允許在同一個應用中混用不同語言，同時保持 component 隔離。
- 透過明確的 capability 宣告，讓 component 只取得必要的 host 存取權。
- 從本機開發到 cloud、registry 或 Kubernetes 部署，可以維持一致的應用結構。

### 架構/概念

| 概念 | 說明 |
| --- | --- |
| Spin CLI | 用於建立、建置、執行、watch、封裝與部署應用的開發者 CLI。 |
| Spin application | 由一個或多個 Wasm component，加上 routing、trigger、build command 與 capability 設定組成。 |
| `spin.toml` | 應用 manifest，定義 component、source、trigger、route、build step、variable 與允許的 capability。 |
| Component | WebAssembly Component Model 的執行單元，用來處理 HTTP request 或 Redis message 等事件。 |
| Trigger | 觸發 component 的事件來源，常見例子包括 HTTP routing 與 Redis pub/sub。 |
| Capability-based access | 檔案、outbound network host、variable、key/value store、SQLite、Redis、MySQL、PostgreSQL 等 host resource 必須明確宣告。 |
| WASI | 標準化介面層，讓 Wasm 程式能以可攜方式使用 host capability。 |
| Component composition | Spin 2.0 更正式地使用 WebAssembly Component Model interface，在不同語言的隔離 component 之間組合功能。 |
| 本機 runtime | `spin up` 在本機執行應用並提供測試用 route，通常會開啟本機 HTTP port。 |
| 部署目標 | Spin app 可部署到 Fermyon Cloud、推送到 registry，或在 SpinKube 等 Kubernetes-oriented 環境中執行。 |

Spin 最初提供的是撰寫 server-side Wasm module 的框架，讓 module 能回應 HTTP request 與其他事件。Spin 1.0 穩定了開發流程，並擴充語言、資料庫、registry、Kubernetes、key/value 與 Vault-backed configuration 支援。Spin 2.0 則將 Component Model 提升為一等公民，改善可攜性、SDK ergonomics 與多語言 component 組合。

### 實務使用

適合使用 Spin 的情境：

- 正在建立小型 API、webhook handler、網站或事件驅動服務。
- 想要 serverless 開發體驗，但希望 artifact 是可攜的 Wasm，而不是特定雲端的 function bundle。
- cold start、部署密度與 sandboxing 很重要。
- 不同 component 適合用不同程式語言撰寫。
- 希望本機開發、cloud 部署與 Kubernetes 部署共用相同 app structure。

基本流程：

```bash
spin new
spin build
spin up
```

典型開發流程：

```bash
spin new hello-spin --template http-rust
cd hello-spin
spin build
spin up
curl http://127.0.0.1:3000/
```

常見操作模式：

- 用 template 選擇合適的語言與 trigger。
- 讓每個 component 聚焦在單一路由、事件或責任。
- 在 `spin.toml` 明確宣告 outbound host 與資料服務。
- 輕量 persistence 可使用內建 KV 或 SQLite，較大型 production data 則使用外部資料庫。
- 開發時使用 `spin watch`，排查本機設定問題時使用 `spin doctor`。
- 依部署目標選擇 `spin cloud deploy`、registry workflow 或 Kubernetes/SpinKube。

營運注意事項：

- Spin 最適合事件驅動的 Wasm service；長時間背景程序或高度依賴 OS 的 workload 仍可能更適合 container。
- 語言支援取決於 SDK 成熟度與 WASI 支援，導入前要確認目標語言狀態。
- capability restriction 是安全優勢，但也代表 manifest 需要被有意識地維護。
- database、secret、observability 與部署目標行為應在實際 runtime 驗證，不只依賴 `spin up`。
- 閱讀 Spin 1.x 與 Spin 2.x 範例時要留意 manifest 結構與 Component Model 假設可能不同。

### 學習檢核表

- [ ] 安裝 Spin CLI，並用 template 建立 HTTP app。
- [ ] 使用 `spin build` 與 `spin up` 在本機建置並執行 Spin app。
- [ ] 閱讀並修改 `spin.toml` 中的 route、component、build command 與 capability。
- [ ] 加入第二個不同語言的 component，理解 request 如何路由到不同 component。
- [ ] 使用 key/value、SQLite、variable 或 outbound HTTP 等內建服務。
- [ ] 理解 WebAssembly Component Model 如何改變 Spin 2.x 的應用結構。
- [ ] 將同一個 app 部署到 Fermyon Cloud、registry workflow 或 Kubernetes with SpinKube 等目標。
- [ ] 判斷何時 Spin 比 container、傳統 serverless function 或 Wasmtime 這類 general Wasm runtime 更合適。

## References

- [Develop serverless WebAssembly apps with Spin](https://www.fermyon.com/spin)
- [Introducing Spin 2.0](https://www.fermyon.com/blog/introducing-spin-v2)
- [Spin 1.0 - The Developer Tool for Serverless WebAssembly](https://www.fermyon.com/blog/introducing-spin-v1)
- [Introducing Spin](https://www.fermyon.com/blog/introducing-spin)
