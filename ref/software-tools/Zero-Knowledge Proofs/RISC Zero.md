# RISC Zero

| Field | Details |
| --- | --- |
| Category | Zero-knowledge virtual machine and verifiable computation platform |
| Project | RISC Zero |
| License | Apache-2.0 OR MIT |
| Core model | General-purpose zkVM based on zk-STARKs and the RISC-V microarchitecture |
| Primary languages | Rust, C, C++ through RISC-V compiler toolchains |
| Main artifacts | Method ELF, Image ID, journal, receipt, seal |
| Best fit | Proving correct execution of ordinary programs without writing custom ZK circuits |
| Last reviewed | 2026-04-29 |

## English

### Overview

RISC Zero is an open-source zero-knowledge virtual machine (zkVM) for verifiable general-purpose computation. Developers write normal programs, commonly in Rust, compile them to a RISC-V ELF, run them inside the zkVM, and produce a cryptographic receipt proving that the program executed correctly.

The central advantage is that application logic can be expressed as software instead of hand-designed arithmetic circuits. A verifier checks the receipt against the program's Image ID and reads only the public journal output. Private inputs and intermediate execution state remain hidden except for what the public output implies.

### Why it matters

RISC Zero makes zero-knowledge proofs more accessible to software teams. Instead of learning a circuit DSL for every computation, teams can reuse existing language tooling, libraries, tests, and code-review practices while gaining succinct verification of execution.

This is useful when the expensive or sensitive computation can run off-chain or off-server, but another party still needs confidence in the result. Typical domains include blockchain scaling, verifiable off-chain state transitions, privacy-preserving credentials, verifiable AI or ML inference, compliance checks, auctions, games, and workflows where a prover should not reveal private data.

### Architecture/Concepts

| Concept | Meaning |
| --- | --- |
| zkVM | A virtual machine that executes code and produces a zero-knowledge proof of correct execution. |
| RISC-V | The instruction-set architecture RISC Zero targets, allowing programs to compile from familiar languages. |
| Method | The guest program compiled into a RISC-V ELF with a special entry point. |
| Image ID | A cryptographic hash of the method ELF. Verifiers use it to know exactly which code was proven. |
| Guest | The program running inside the zkVM. It receives private inputs, computes, and commits public outputs. |
| Host | The outside program that prepares inputs, runs the prover, receives the receipt, and can verify it. |
| Journal | An append-only public output log written by guest code, commonly through `env::commit()`. |
| Receipt | The proof artifact returned by a successful run. It attests that the journal came from executing the expected method. |
| Seal | The opaque cryptographic proof data inside a receipt. |
| Prover | The component that executes the guest and generates the proof. It can run locally or through remote proving services. |
| Verifier | The party or program that checks a receipt against an expected Image ID and then decodes the journal. |

The normal flow is:

1. Write guest code for the computation that must be proven.
2. Compile the guest into a RISC-V ELF method and derive its Image ID.
3. Build a host program that supplies inputs and invokes the prover.
4. Run the method in the zkVM and receive a receipt containing the journal and seal.
5. Verify the receipt against the expected Image ID before trusting the journal output.

RISC Zero's proof system is based on zk-STARKs and supports recursive proof composition. The project also supports Groth16-related verification paths for compact verification use cases, especially where on-chain verification cost matters.

### Practical usage

Use RISC Zero when:

- You need proof that a computation ran correctly, but do not want to expose private inputs.
- Your logic is easier to maintain as Rust, C, or C++ than as a custom ZK circuit.
- A blockchain contract or external verifier should check a compact proof of off-chain work.
- You want a local open-source prover for private data or a remote prover for scalable workloads.
- You need verifiable computation for AI inference, identity checks, compliance rules, games, or cross-party workflows.

Implementation tips:

- Keep guest code deterministic and minimize unnecessary work; proving cost grows with execution.
- Treat the journal as public. Do not commit secrets unless disclosure is intended.
- Pin and review the Image ID used by verifiers, because it defines the trusted program.
- Use development mode only for testing; production verification must reject fake or skipped proofs.
- Start with local proving for development and private inputs, then evaluate remote proving or Boundless-style proving for heavier workloads.
- Design clear host/guest boundaries so serialization, inputs, outputs, and verification are easy to audit.
- Benchmark realistic inputs early; ordinary software that is fast natively can still be expensive to prove.

### Learning checklist

- [ ] Explain why a zkVM avoids writing a custom circuit for each application.
- [ ] Create a small RISC Zero project with `cargo risczero`.
- [ ] Write a guest method that reads private input and commits a public output.
- [ ] Understand how the method ELF and Image ID bind a proof to specific code.
- [ ] Generate a receipt from a host program.
- [ ] Verify the receipt and decode the journal.
- [ ] Distinguish local proving, development mode, and remote proving.
- [ ] Review privacy boundaries: private input, intermediate state, journal, receipt, and verifier-visible data.
- [ ] Benchmark proof time and proof verification for the target deployment environment.

## 繁體中文

### 概覽

RISC Zero 是開源的 zero-knowledge virtual machine（zkVM），用於可驗證的一般運算。開發者可以撰寫一般程式，常見是 Rust，將程式編譯成 RISC-V ELF，在 zkVM 中執行，並產生 cryptographic receipt，證明該程式確實正確執行。

它的核心價值是讓應用邏輯可以用一般軟體方式撰寫，而不是為每個問題手工設計 ZK circuit。Verifier 會用程式的 Image ID 檢查 receipt，並只讀取公開的 journal output。Private inputs 與中間執行狀態不會被揭露，除非它們可由公開輸出推得。

### 為什麼重要

RISC Zero 讓軟體團隊更容易使用 zero-knowledge proofs。團隊不必為每段邏輯都學習 circuit DSL，而可以沿用既有語言工具、函式庫、測試與 code review 流程，同時取得可驗證的程式執行結果。

當昂貴或敏感的運算可以在鏈下或伺服器外完成，但另一方仍需要信任結果時，RISC Zero 特別有用。常見場景包含 blockchain scaling、可驗證的鏈下 state transition、隱私保護 credential、可驗證 AI/ML inference、合規檢查、拍賣、遊戲，以及不想揭露私有資料的跨方工作流。

### 架構/概念

| 概念 | 說明 |
| --- | --- |
| zkVM | 可執行程式並產生正確執行證明的 virtual machine。 |
| RISC-V | RISC Zero 採用的指令集架構，讓熟悉語言可透過 toolchain 編譯後執行。 |
| Method | 編譯成 RISC-V ELF 的 guest program，包含特殊 entry point。 |
| Image ID | Method ELF 的 cryptographic hash。Verifier 用它確認被證明的是哪一份程式。 |
| Guest | 在 zkVM 內執行的程式，讀取私有輸入、計算，並提交公開輸出。 |
| Host | 外部程式，負責準備輸入、呼叫 prover、取得 receipt，並可執行 verification。 |
| Journal | Guest 寫入的 append-only 公開輸出紀錄，常透過 `env::commit()` 產生。 |
| Receipt | 成功執行後得到的 proof artifact，證明 journal 來自預期 method 的正確執行。 |
| Seal | Receipt 內部的不透明 cryptographic proof data。 |
| Prover | 執行 guest 並產生 proof 的元件，可在本機或遠端 proving service 上執行。 |
| Verifier | 檢查 receipt 是否符合預期 Image ID，並解讀 journal 的一方或程式。 |

典型流程如下：

1. 撰寫需要被證明的 guest code。
2. 將 guest 編譯成 RISC-V ELF method，並產生 Image ID。
3. 撰寫 host program，提供輸入並呼叫 prover。
4. 在 zkVM 中執行 method，取得包含 journal 與 seal 的 receipt。
5. 在信任 journal output 前，先用預期 Image ID 驗證 receipt。

RISC Zero 的 proof system 以 zk-STARKs 為基礎，並支援 recursive proof composition。專案也支援 Groth16 相關驗證路徑，適合需要更精簡驗證成本的情境，特別是 on-chain verification。

### 實務使用

適合使用 RISC Zero 的情境：

- 需要證明某段運算正確執行，但不想揭露 private inputs。
- 業務邏輯用 Rust、C 或 C++ 維護，比改寫成 custom ZK circuit 更合理。
- Blockchain contract 或外部 verifier 需要檢查鏈下運算的精簡 proof。
- 需要本機 open-source prover 處理私有資料，或需要遠端 prover 支援較大的 workload。
- 需要為 AI inference、身分檢查、合規規則、遊戲或跨方流程加入可驗證運算。

實作建議：

- Guest code 應保持 deterministic，並避免不必要工作；proving cost 會隨執行量增加。
- 將 journal 視為公開資料。除非刻意揭露，否則不要 commit secrets。
- 固定並審查 verifier 使用的 Image ID，因為它定義了被信任的程式版本。
- Development mode 只能用於測試；production verification 必須拒絕假的或跳過的 proof。
- 開發與私有輸入可先使用 local proving，再依 workload 評估 remote proving 或 Boundless 類型的 proving。
- 清楚設計 host/guest 邊界，讓 serialization、inputs、outputs 與 verification 容易稽核。
- 及早用真實輸入 benchmark；一般執行很快的軟體，證明時仍可能成本很高。

### 學習檢核表

- [ ] 說明 zkVM 如何避免為每個應用撰寫 custom circuit。
- [ ] 使用 `cargo risczero` 建立小型 RISC Zero 專案。
- [ ] 撰寫一個讀取 private input 並 commit public output 的 guest method。
- [ ] 理解 method ELF 與 Image ID 如何把 proof 綁定到特定程式碼。
- [ ] 從 host program 產生 receipt。
- [ ] 驗證 receipt 並解讀 journal。
- [ ] 區分 local proving、development mode 與 remote proving。
- [ ] 檢查隱私邊界：private input、intermediate state、journal、receipt 與 verifier 可見資料。
- [ ] 針對目標部署環境 benchmark proof time 與 verification time。

## References

- [RISC Zero official site](https://risczero.com/)
- [RISC Zero GitHub repository](https://github.com/risc0/risc0)
- [RISC Zero zkVM overview](https://www.mintlify.com/risc0/risc0/concepts/zkvm-overview)
