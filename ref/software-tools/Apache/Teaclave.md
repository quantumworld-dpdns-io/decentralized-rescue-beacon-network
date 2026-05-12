# Apache Teaclave

| Field | Details |
|---|---|
| Project | Apache Teaclave |
| Category | Confidential computing, Trusted Execution Environments (TEEs), secure application SDKs |
| License | Apache License 2.0 |
| Governance | Apache Software Foundation Top-Level Project |
| Primary languages | Rust, with SDK work also covering Java TEE experimentation |
| Main platforms | Intel SGX, Arm TrustZone, and other TEE-oriented environments |
| Typical users | Developers building privacy-preserving workloads, trusted applications, secure storage, attestation flows, and confidential cloud, edge, or embedded systems |
| Website | <https://teaclave.apache.org/> |

## English

### Overview

Apache Teaclave is an open source confidential-computing project for building memory-safe Trusted Applications on Trusted Execution Environments (TEEs). Its current focus is an ecosystem of SDKs and reusable components for platforms such as Intel SGX and Arm TrustZone, with Rust as the main language for memory-safe TEE development.

Teaclave originally became known for the Teaclave Function-as-a-Service (FaaS) framework: a general-purpose secure computing platform for running private computations on sensitive data. That FaaS framework is now legacy and no longer the active center of development. The project now emphasizes SDKs, crates, examples, and showcases that help developers build their own trusted applications directly.

### Why it matters

Sensitive-data workloads often need to run in environments where the infrastructure operator, cloud provider, or host operating system should not be able to inspect the plaintext data or tamper silently with the computation. TEEs address this by isolating selected code and data in hardware-backed protected execution contexts.

Teaclave matters because it packages that model into developer-facing building blocks. Instead of treating enclave development as a purely low-level systems task, it provides SDKs and reusable components for common confidential-computing concerns such as remote attestation, secure storage, key management, and trusted application structure.

Practical scenarios include privacy-preserving analytics over medical or financial data, secure inference, private set intersection, confidential data collaboration, and edge or embedded workloads where trusted code must run on constrained or shared infrastructure.

### Architecture/Concepts

Teaclave should be understood as an ecosystem rather than one single runtime:

- **Trusted Execution Environment (TEE):** A hardware-backed isolation boundary that protects selected code and data from the surrounding system.
- **Trusted Application (TA):** The application logic that runs inside a TEE and handles sensitive operations.
- **Remote attestation:** A protocol for proving to a remote party that expected code is running inside a genuine trusted environment before secrets or sensitive data are released.
- **Memory-safe development:** Teaclave emphasizes Rust-based development to reduce memory-safety vulnerabilities in trusted code.
- **SDKs and crates:** The current project provides SDKs and TEE-tailored dependencies for building applications on Intel SGX, Arm TrustZone, and related environments.
- **Legacy FaaS architecture:** The older Teaclave FaaS platform used services running inside TEEs and mutually attested channels to coordinate authentication, frontend access, management, access control, storage, and execution. It remains useful as an architectural reference, but new work should start from the active SDK ecosystem.

### Practical usage

Use Teaclave when you need to build software that processes sensitive data while reducing trust in the host environment. A typical adoption path is:

1. Identify the sensitive computation and minimize the code that must run inside the TEE.
2. Choose the relevant Teaclave SDK for the target platform, such as Intel SGX or Arm TrustZone.
3. Prototype locally with the project documentation, examples, and available Docker or emulation support when hardware is not immediately available.
4. Add attestation so clients can verify the trusted application before provisioning data, credentials, or keys.
5. Integrate secure storage and key-management patterns only for data that must remain protected across executions.
6. Treat the legacy FaaS documentation as historical background unless maintaining an existing Teaclave FaaS deployment.

Teaclave is most appropriate when confidentiality, integrity, and verifiable execution are central requirements. It is less appropriate as a general compute framework when ordinary process isolation, container security, or standard access controls are sufficient.

### Learning checklist

- Understand the difference between encryption at rest, encryption in transit, and computation inside a TEE.
- Learn the threat model of the target TEE platform, including what is and is not protected.
- Review remote attestation before designing data or key provisioning.
- Build a small trusted application with the Teaclave SGX SDK or TrustZone SDK.
- Keep the trusted computing base small; move non-sensitive orchestration outside the enclave or trusted application.
- Study the legacy FaaS materials for service design patterns, while using current SDK repositories for new implementation work.
- Review operational concerns such as hardware availability, cloud confidential-computing support, side-channel limitations, upgrade strategy, and dependency management.

## 繁體中文

### 概觀

Apache Teaclave 是一個開源的機密運算專案，用來在可信執行環境（Trusted Execution Environment, TEE）上建立具記憶體安全性的 Trusted Applications。它目前的重點是 SDK 生態系與可重用元件，支援 Intel SGX、Arm TrustZone 等平台，並以 Rust 作為主要的記憶體安全開發語言。

Teaclave 早期最知名的是 Teaclave Function-as-a-Service（FaaS）框架，也就是用來在敏感資料上執行私密運算的通用安全運算平台。不過，FaaS 框架現在已屬於 legacy，並非主要維護方向。現階段的 Teaclave 更著重於 SDK、crates、範例與 showcase，協助開發者直接建立自己的可信應用程式。

### 為什麼重要

敏感資料工作負載常常需要在不完全信任基礎設施管理者、雲端供應商或主機作業系統的情況下執行。TEE 透過硬體支援的隔離邊界，保護特定程式碼與資料，降低外部環境讀取明文資料或暗中竄改運算結果的風險。

Teaclave 的價值在於把這種安全模型包裝成開發者可使用的建構元件。它不只要求開發者直接面對底層 enclave 細節，也提供 SDK 與可重用模組，涵蓋遠端證明、 secure storage、金鑰管理，以及可信應用程式的基本結構。

常見應用情境包含醫療或金融資料的隱私保護分析、安全模型推論、private set intersection、跨組織機密資料協作，以及在雲端、邊緣或嵌入式環境中執行需要可信保護的工作負載。

### 架構與概念

Teaclave 應視為一個生態系，而不是單一執行環境：

- **可信執行環境（TEE）：** 由硬體支援的隔離邊界，用來保護特定程式碼與資料不受周邊系統影響。
- **Trusted Application（TA）：** 在 TEE 內執行、處理敏感邏輯的應用程式。
- **遠端證明（remote attestation）：** 在釋出機密資料、憑證或金鑰之前，讓遠端使用者確認預期程式碼確實執行於可信環境中的機制。
- **記憶體安全開發：** Teaclave 強調使用 Rust 等記憶體安全語言，降低可信程式碼中的記憶體安全漏洞。
- **SDK 與 crates：** 目前專案提供針對 Intel SGX、Arm TrustZone 與相關 TEE 場景的 SDK，以及適合 TEE 使用的相依套件。
- **Legacy FaaS 架構：** 舊版 Teaclave FaaS 平台曾以執行於 TEE 內的多個服務與 mutual-attested channels 協調 authentication、frontend、management、access control、storage 與 execution。它仍可作為架構參考，但新專案應優先從目前維護中的 SDK 生態系開始。

### 實務使用

當你需要在降低對主機環境信任的前提下處理敏感資料時，可以考慮 Teaclave。典型導入流程如下：

1. 先界定真正敏感的運算，並盡量縮小需要放入 TEE 的程式碼範圍。
2. 依目標平台選擇適合的 Teaclave SDK，例如 Intel SGX 或 Arm TrustZone。
3. 透過官方文件、範例，以及可用的 Docker 或模擬支援進行本機原型開發。
4. 加入遠端證明，讓客戶端在提供資料、憑證或金鑰前能驗證可信應用程式。
5. 僅針對需要跨執行階段保護的資料整合 secure storage 與金鑰管理模式。
6. 除非需要維護既有 Teaclave FaaS 部署，否則應把 FaaS 文件視為歷史與架構參考。

Teaclave 最適合用在機密性、完整性與可驗證執行是核心需求的場景。如果一般行程隔離、容器安全或標準存取控制已足夠，則不一定需要引入 TEE 與 Teaclave。

### 學習檢核表

- 理解靜態加密、傳輸加密，以及在 TEE 中進行運算三者的差異。
- 研究目標 TEE 平台的 threat model，確認哪些風險有被保護、哪些沒有。
- 在設計資料或金鑰佈署前，先理解遠端證明流程。
- 使用 Teaclave SGX SDK 或 TrustZone SDK 建立一個小型 Trusted Application。
- 保持 trusted computing base 精簡，將非敏感的編排邏輯放在 enclave 或 TA 外部。
- 以 legacy FaaS 資料學習服務設計模式，但以目前 SDK repository 作為新實作的主要依據。
- 評估硬體可用性、雲端機密運算支援、side-channel 限制、升級策略與相依套件管理等營運議題。

## References

- Apache Teaclave official website: <https://teaclave.apache.org/>
- Apache Teaclave overview: <https://teaclave.apache.org/overview/>
- Apache Teaclave documentation: <https://teaclave.apache.org/docs/>
- Apache Teaclave ecosystem documentation: <https://teaclave.apache.org/teaclave-docs/>
- Apache Teaclave FaaS legacy documentation: <https://teaclave.apache.org/teaclave-faas-legacy/>
- ASF announcement of Apache Teaclave as a Top-Level Project: <https://news.apache.org/foundation/entry/the-apache-software-foundation-announces-new-top-level-projects-4>
