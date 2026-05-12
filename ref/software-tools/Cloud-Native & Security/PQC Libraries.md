# PQC Libraries

| Metadata | Details |
| --- | --- |
| Category | Cloud-Native & Security |
| Topic | Post-Quantum Cryptography (PQC) libraries |
| Primary use | Testing, prototyping, and planning migration to quantum-resistant cryptography |
| Key algorithms | ML-KEM, ML-DSA, SLH-DSA, hybrid classical/PQC key establishment |
| Typical tools | Open Quantum Safe liboqs, OQS Provider for OpenSSL 3, Cloudflare CIRCL |
| License model | Mostly free and open source; confirm each project license before production use |
| Recommended audience | Security engineers, platform engineers, cloud architects, and applied cryptography learners |
| Production caution | Treat many PQC library integrations as evolving. Prefer standardized algorithms, supported platform releases, and vendor guidance for production systems. |

## English

### Overview

Post-Quantum Cryptography (PQC) libraries provide implementations of cryptographic algorithms designed to remain secure against attackers with future large-scale quantum computers. They are especially relevant for key establishment and digital signatures because widely deployed public-key systems such as RSA and elliptic-curve cryptography are threatened by cryptographically relevant quantum computers.

The current center of practical PQC work is migration readiness:

- Use NIST-standardized algorithms where available.
- Test hybrid key establishment that combines classical and post-quantum mechanisms.
- Inventory cryptographic dependencies before replacing production primitives.
- Keep systems crypto-agile so algorithms can be upgraded without redesigning the whole application.

Important algorithm names:

| Standard | Algorithm | Purpose | Origin |
| --- | --- | --- | --- |
| FIPS 203 | ML-KEM | Key encapsulation / shared-secret establishment | CRYSTALS-Kyber |
| FIPS 204 | ML-DSA | Digital signatures | CRYSTALS-Dilithium |
| FIPS 205 | SLH-DSA | Stateless hash-based digital signatures | SPHINCS+ |

### Why It Matters

PQC matters because of the "harvest now, decrypt later" risk. An attacker can record encrypted traffic today and wait until future quantum capabilities make some classical public-key cryptography breakable. This is most urgent for data that must remain confidential for many years, such as medical records, national security data, financial records, intellectual property, and long-term identity credentials.

For cloud-native systems, PQC readiness affects:

- TLS termination and service-to-service encryption.
- Certificate issuance, validation, and rotation.
- API gateways, ingress controllers, and service meshes.
- Secrets management and key management systems.
- Firmware signing, container signing, and software supply-chain verification.
- Compliance roadmaps for regulated sectors.

### Architecture/Concepts

PQC libraries usually appear in one of three layers:

| Layer | Role | Example |
| --- | --- | --- |
| Algorithm library | Implements KEMs, signatures, test vectors, benchmarks, and low-level APIs | liboqs, CIRCL |
| Crypto provider | Connects PQC algorithms to a general cryptographic framework | OQS Provider for OpenSSL 3 |
| Protocol integration | Exposes PQC through TLS, X.509, S/MIME, VPNs, service meshes, or application protocols | Hybrid TLS 1.3 experiments and provider-backed OpenSSL workflows |

Core concepts:

- **KEM (Key Encapsulation Mechanism):** A public-key method for establishing a shared secret. ML-KEM is the NIST-standardized KEM.
- **Digital signature:** A mechanism for authentication and integrity. ML-DSA and SLH-DSA are NIST-standardized signature schemes.
- **Hybrid mode:** Combines a classical algorithm, such as X25519 or ECDHE, with a PQC algorithm. The goal is to retain classical security while adding resistance to future quantum attacks.
- **Crypto-agility:** The ability to replace algorithms, parameter sets, and providers without major application rewrites.
- **Parameter set:** A named security/performance profile, such as ML-KEM-512, ML-KEM-768, or ML-KEM-1024.

Representative open-source libraries:

| Library | Language / Integration | Best fit | Notes |
| --- | --- | --- | --- |
| Open Quantum Safe liboqs | C library | Prototyping PQC KEM and signature algorithms | Provides common APIs, tests, and benchmarks for quantum-safe algorithms. |
| OQS Provider | OpenSSL 3 provider | Testing PQC through OpenSSL-compatible workflows | Enables PQC and hybrid KEM schemes in OpenSSL 3 contexts; follow project warnings before production use. |
| Cloudflare CIRCL | Go library | Go applications and protocol experiments | Includes PQC, elliptic-curve, hash, and protocol primitives; intended for experimental deployment and applied cryptography work. |

### Practical Usage

Use PQC libraries deliberately. They are not a drop-in fix for every security problem.

Recommended workflow:

1. **Inventory cryptography.** List where RSA, ECDSA, ECDH, X25519, TLS, certificates, SSH, JWT signing, code signing, and key wrapping are used.
2. **Classify data lifetime.** Prioritize systems protecting data that must remain confidential for years.
3. **Choose standardized algorithms first.** Prefer ML-KEM for key establishment and ML-DSA or SLH-DSA for signatures when the surrounding platform supports them.
4. **Test hybrid TLS.** Use lab environments to evaluate hybrid classical/PQC negotiation, certificate behavior, interoperability, latency, packet sizes, and CPU cost.
5. **Avoid custom protocols.** Use maintained libraries, providers, and protocol implementations instead of assembling cryptographic flows manually.
6. **Benchmark in context.** Measure handshake size, handshake latency, memory use, CPU cost, and failure behavior under realistic traffic.
7. **Plan rollback and upgrade paths.** PQC standards, provider behavior, and platform support are still evolving.

Example evaluation matrix:

| Question | What to Check |
| --- | --- |
| Is the algorithm standardized? | Confirm whether it maps to FIPS 203, FIPS 204, or FIPS 205. |
| Is the library maintained? | Check release history, security policy, issue activity, and supported platforms. |
| Is the API stable? | Read project warnings about experimental or non-production status. |
| Does it integrate with current infrastructure? | Validate OpenSSL, Go, TLS, Kubernetes ingress, service mesh, and certificate tooling support. |
| Can it be rotated? | Confirm configuration-driven algorithm selection and automated certificate/key rotation. |

### Learning Checklist

- Explain the difference between a KEM and a digital signature.
- Name the NIST-standardized PQC algorithms: ML-KEM, ML-DSA, and SLH-DSA.
- Describe why "harvest now, decrypt later" affects long-lived confidential data.
- Compare algorithm libraries, provider integrations, and protocol integrations.
- Build and run a small liboqs or CIRCL experiment in a lab environment.
- Test a hybrid TLS handshake and observe certificate, packet-size, and latency impacts.
- Document where a cloud-native system depends on RSA, ECDSA, ECDH, or X25519.
- Define a crypto-agility plan for algorithm replacement and emergency rollback.

## 繁體中文

### 概述

抗量子密碼學（Post-Quantum Cryptography, PQC）函式庫提供一組密碼演算法實作，目標是在未來出現大型量子電腦時，仍能抵抗相關攻擊。PQC 特別影響金鑰建立與數位簽章，因為目前廣泛使用的 RSA 與橢圓曲線密碼學，在具備足夠能力的量子電腦面前會面臨風險。

目前實務上的重點是遷移準備：

- 優先使用已由 NIST 標準化的演算法。
- 測試結合傳統密碼與 PQC 的混合式金鑰建立。
- 在替換正式環境密碼元件前，先盤點系統中的密碼依賴。
- 建立密碼敏捷性，讓演算法可以升級，而不需要重寫整個應用程式。

重要演算法名稱：

| 標準 | 演算法 | 用途 | 來源 |
| --- | --- | --- | --- |
| FIPS 203 | ML-KEM | 金鑰封裝 / 建立共享秘密 | CRYSTALS-Kyber |
| FIPS 204 | ML-DSA | 數位簽章 | CRYSTALS-Dilithium |
| FIPS 205 | SLH-DSA | 無狀態雜湊式數位簽章 | SPHINCS+ |

### 重要性

PQC 的重要性來自「現在截獲，以後破解」（harvest now, decrypt later）風險。攻擊者可以先錄下今天的加密流量，等到未來量子運算能力足以破解部分傳統公鑰密碼後，再回頭解密。這對需要多年保密的資料特別重要，例如醫療紀錄、國安資料、金融資料、智慧財產，以及長期身分憑證。

對雲原生系統來說，PQC 準備會影響：

- TLS 終止與服務間加密。
- 憑證簽發、驗證與輪替。
- API Gateway、Ingress Controller 與 Service Mesh。
- Secret 管理與金鑰管理系統。
- 韌體簽章、容器簽章與軟體供應鏈驗證。
- 受監管產業的合規遷移路線圖。

### 架構/概念

PQC 函式庫通常出現在三個層次：

| 層次 | 角色 | 範例 |
| --- | --- | --- |
| 演算法函式庫 | 實作 KEM、簽章、測試向量、效能測試與底層 API | liboqs、CIRCL |
| 密碼提供者 | 將 PQC 演算法接到通用密碼框架 | OpenSSL 3 的 OQS Provider |
| 協定整合 | 透過 TLS、X.509、S/MIME、VPN、Service Mesh 或應用協定使用 PQC | Hybrid TLS 1.3 實驗與 OpenSSL provider 工作流程 |

核心概念：

- **KEM（金鑰封裝機制）：** 用公鑰方式建立共享秘密。ML-KEM 是 NIST 標準化的 KEM。
- **數位簽章：** 用於身分驗證與完整性保護。ML-DSA 與 SLH-DSA 是 NIST 標準化的簽章演算法。
- **混合模式：** 將 X25519 或 ECDHE 等傳統演算法與 PQC 演算法結合，目標是在保留傳統安全性的同時，增加對未來量子攻擊的抵抗力。
- **密碼敏捷性：** 不大幅重寫應用程式，就能替換演算法、參數組與 provider 的能力。
- **參數組：** 命名的安全性與效能設定，例如 ML-KEM-512、ML-KEM-768、ML-KEM-1024。

代表性開源函式庫：

| 函式庫 | 語言 / 整合 | 適合用途 | 說明 |
| --- | --- | --- | --- |
| Open Quantum Safe liboqs | C 函式庫 | 原型設計與測試 PQC KEM、簽章演算法 | 提供量子安全演算法的共同 API、測試與 benchmark。 |
| OQS Provider | OpenSSL 3 Provider | 透過 OpenSSL 相容流程測試 PQC | 在 OpenSSL 3 情境中啟用 PQC 與混合式 KEM；正式使用前需遵循專案警告。 |
| Cloudflare CIRCL | Go 函式庫 | Go 應用程式與協定實驗 | 包含 PQC、橢圓曲線、雜湊與協定 primitives；適合實驗部署與應用密碼學研究。 |

### 實務使用

PQC 函式庫應該被有計畫地導入。它們不是所有安全問題的直接替代解。

建議流程：

1. **盤點密碼使用。** 列出 RSA、ECDSA、ECDH、X25519、TLS、憑證、SSH、JWT 簽章、程式碼簽章與金鑰包裝的使用位置。
2. **分類資料保密期限。** 優先處理需要多年保密的資料與系統。
3. **優先選擇標準化演算法。** 在平台支援的前提下，金鑰建立優先考慮 ML-KEM，簽章優先考慮 ML-DSA 或 SLH-DSA。
4. **測試混合式 TLS。** 在實驗環境評估混合式傳統/PQC 協商、憑證行為、互通性、延遲、封包大小與 CPU 成本。
5. **避免自訂協定。** 使用維護中的函式庫、provider 與協定實作，不要自行拼裝密碼流程。
6. **在真實情境 benchmark。** 測量握手大小、握手延遲、記憶體用量、CPU 成本與故障行為。
7. **規劃回復與升級路徑。** PQC 標準、provider 行為與平台支援仍在演進。

評估矩陣範例：

| 問題 | 檢查項目 |
| --- | --- |
| 演算法是否已標準化？ | 確認是否對應 FIPS 203、FIPS 204 或 FIPS 205。 |
| 函式庫是否持續維護？ | 檢查 release 歷史、安全政策、issue 活動與支援平台。 |
| API 是否穩定？ | 閱讀專案是否標示實驗性或不建議正式使用。 |
| 是否能整合現有基礎設施？ | 驗證 OpenSSL、Go、TLS、Kubernetes Ingress、Service Mesh 與憑證工具支援。 |
| 是否能輪替？ | 確認可透過設定選擇演算法，並支援自動化憑證與金鑰輪替。 |

### 學習檢核表

- 說明 KEM 與數位簽章的差異。
- 說出 NIST 標準化的 PQC 演算法：ML-KEM、ML-DSA、SLH-DSA。
- 解釋「現在截獲，以後破解」為何會影響長期保密資料。
- 比較演算法函式庫、provider 整合與協定整合。
- 在實驗環境建立並執行一個 liboqs 或 CIRCL 小型測試。
- 測試混合式 TLS 握手，觀察憑證、封包大小與延遲影響。
- 文件化雲原生系統中依賴 RSA、ECDSA、ECDH 或 X25519 的位置。
- 定義演算法替換與緊急回復的密碼敏捷性計畫。

## References

- [NIST: Announcing approval of FIPS 203, FIPS 204, and FIPS 205](https://www.nist.gov/news-events/news/2024/08/announcing-approval-three-federal-information-processing-standards-fips)
- [NIST CSRC: FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard](https://csrc.nist.gov/pubs/fips/203/final)
- [NIST: First three finalized post-quantum encryption standards](https://www.nist.gov/node/1856616)
- [Open Quantum Safe: liboqs](https://openquantumsafe.org/liboqs/)
- [Open Quantum Safe GitHub: liboqs](https://github.com/open-quantum-safe/liboqs)
- [Open Quantum Safe GitHub: OQS Provider for OpenSSL 3](https://github.com/open-quantum-safe/oqs-provider)
- [Cloudflare Research: CIRCL](https://research.cloudflare.com/projects/applied-cryptography/circl/)
- [Cloudflare GitHub: CIRCL](https://github.com/cloudflare/circl)
