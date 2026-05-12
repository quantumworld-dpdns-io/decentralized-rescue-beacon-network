# Cilium Tetragon

| Field | Details |
| --- | --- |
| Category | Cloud-native security, runtime observability, runtime enforcement |
| Project | Cilium Tetragon |
| Maintainer / ecosystem | Cilium project; CNCF project ecosystem |
| License | Apache-2.0 |
| Core technology | eBPF on Linux; Kubernetes-aware policy and event correlation |
| Primary use cases | Process execution monitoring, system call activity, file and network access observability, runtime policy enforcement |
| Interfaces | JSON event logs, gRPC stream, `tetra` CLI, Kubernetes `TracingPolicy` CRDs, Prometheus metrics |
| Current note | GitHub lists Tetragon `v1.6.1` as the latest release on March 31, 2026; verify release notes before production upgrades. |

## English

### Overview

Cilium Tetragon is an open source, eBPF-based security observability and runtime enforcement tool. It observes security-relevant activity from inside the Linux kernel and enriches those events with process, container, pod, namespace, node, and cluster context where available.

In Kubernetes, Tetragon is Kubernetes-aware: policies and events can be related to workloads rather than only to raw host processes. Outside Kubernetes, it can also be used on virtual machines and bare-metal Linux systems for process, file, network, and system-call visibility.

Tetragon is best understood as a runtime signal and enforcement layer. It does not replace image scanning, admission control, network policy, SIEM, or EDR workflows; it provides high-fidelity runtime events and optional kernel-level actions that those workflows can use.

### Why it matters

Modern attacks often happen after deployment: an unexpected shell is spawned, a binary is dropped into `/tmp`, credentials are read, a fileless payload executes, or a process attempts suspicious outbound network access. Static controls can reduce those risks, but they cannot fully describe what a workload actually does at runtime.

Tetragon matters because it can:

- Attribute runtime behavior to the responsible binary, process tree, container, pod, and namespace.
- Reduce observability overhead by applying filters in eBPF before events are sent to user space.
- Detect activity such as process execution, system calls, file access, network activity, privilege changes, kernel module activity, and fileless execution patterns.
- Enforce selected policies close to the event source, including blocking or killing processes in supported policy actions.
- Feed existing operations and security pipelines through JSON logs, gRPC, and metrics.

The practical value is shorter investigation time: instead of asking only "which pod talked to this address?", teams can ask "which binary inside which pod opened this connection, with which arguments, and what parent process launched it?"

### Architecture/Concepts

Tetragon runs an agent on each observed node, typically as a Kubernetes DaemonSet. The agent loads eBPF programs into the kernel and uses them to observe selected hooks. Events are exported to user space after policy filtering and enrichment.

Key concepts:

- **eBPF sensors**: Kernel-resident programs collect and filter runtime activity with low overhead compared with forwarding every event to a user-space agent.
- **Process lifecycle events**: Tetragon emits process execution and exit events, which form the base for attributing later activity to a binary and process tree.
- **TracingPolicy**: A Kubernetes custom resource used to define what kernel or user-space hooks should be observed and what selectors, filters, and actions should apply.
- **Hook points**: Policies can use kernel `kprobes` and `tracepoints`, and user-space `uprobes`. Official docs caution that syscall hooks can introduce time-of-check/time-of-use risk when arguments point to user memory; later kernel hooks such as LSM `security_` hooks can avoid that class of issue.
- **Kubernetes identity enrichment**: Tetragon can attach namespace, pod, workload, node, and container context to events so security rules map to workloads.
- **Runtime enforcement**: Policies can move from observation to action, for example alerting, overriding a return value, or terminating a process depending on the policy and hook.
- **Export and integration**: Events are available as JSON logs and through gRPC; metrics are exposed for Prometheus-compatible systems.

Tetragon is strongest when policies are specific. A broad "trace everything" approach can create noise and cost; high-value policies target suspicious execution paths, unexpected privilege transitions, sensitive file access, and workload-specific behaviors.

### Practical usage

Install on Kubernetes with Helm:

```bash
helm repo add cilium https://helm.cilium.io
helm repo update
helm install tetragon cilium/tetragon -n kube-system
kubectl rollout status -n kube-system ds/tetragon -w
```

Observe process execution events from the Tetragon DaemonSet on a single-node cluster:

```bash
kubectl exec -ti -n kube-system ds/tetragon -c tetragon -- \
  tetra getevents -o compact
```

Common first policies and checks:

- Monitor execution from writable paths such as `/tmp`.
- Detect shells or package managers running inside production application containers.
- Alert on SUID, file capability, or setuid-related privilege transitions.
- Detect fileless execution patterns such as anonymous memory-backed binaries.
- Monitor outbound connections from workloads that should be network-quiet.
- Enable process credential visibility when investigating privilege changes.
- Export events to a log pipeline and correlate them with Kubernetes audit logs, Cilium/Hubble flow logs, and application telemetry.

Operational guidance:

- Start in observation mode before enabling enforcement actions.
- Scope policies by namespace, pod labels, container name, binary path, and arguments to reduce noise.
- Test policies on representative workloads and kernels; kernel hook availability and semantics can vary.
- Review release notes before upgrades, especially for Helm values, CRDs, event schemas, and metrics.
- Treat Tetragon as one layer in a defense-in-depth program, not as the only control.

### Learning checklist

- Explain what eBPF contributes to Tetragon's low-overhead runtime visibility.
- Distinguish process execution events from custom `TracingPolicy` events.
- Install Tetragon with Helm and verify the DaemonSet rollout.
- Use `tetra getevents` to inspect process events.
- Read a Tetragon JSON event and identify binary, arguments, parent process, pod, namespace, and node.
- Write or adapt a policy that monitors a sensitive behavior without overwhelming the event stream.
- Understand when a policy should alert only and when enforcement is justified.
- Know the upgrade-sensitive areas: Helm values, CRDs, metrics names, event schemas, and kernel compatibility.

## 繁體中文

### 概覽

Cilium Tetragon 是一個開源、以 eBPF 為核心的安全可觀測性與執行期防護工具。它從 Linux 核心內部觀察具安全意義的行為，並在可用時補上行程、容器、Pod、Namespace、節點與叢集等脈絡。

在 Kubernetes 環境中，Tetragon 具備 Kubernetes 感知能力：事件與政策可以對應到工作負載，而不只是主機上的原始行程。在 Kubernetes 之外，它也可以用於虛擬機與裸機 Linux，提供行程、檔案、網路與系統呼叫層級的可視性。

可以把 Tetragon 視為執行期訊號與執行期防護層。它不取代映像檔掃描、Admission Control、Network Policy、SIEM 或 EDR；它提供高品質的執行期事件，以及可選的核心層級處置能力，讓這些流程能做出更準確的判斷。

### 為什麼重要

許多現代攻擊發生在部署之後：非預期的 shell 被啟動、二進位檔被寫入 `/tmp` 後執行、憑證被讀取、fileless payload 被執行，或某個行程嘗試可疑的對外連線。靜態控制能降低風險，但無法完整描述工作負載在執行期實際做了什麼。

Tetragon 的價值在於它可以：

- 將執行期行為歸因到實際的 binary、行程樹、容器、Pod 與 Namespace。
- 透過 eBPF 在事件送到使用者空間前先做過濾，降低可觀測性成本。
- 偵測行程執行、系統呼叫、檔案存取、網路活動、權限變更、核心模組活動與 fileless execution 等行為。
- 在支援的政策動作中，靠近事件源頭進行阻擋或終止行程等處置。
- 透過 JSON logs、gRPC 與 metrics 串接既有的維運與資安管線。

它最實際的好處是縮短調查時間：團隊不只問「哪個 Pod 連到這個位址？」，而是能問「哪個 Pod 裡的哪個 binary、帶著哪些參數、由哪個父行程啟動，並開了這條連線？」

### 架構/概念

Tetragon 會在每個被觀察的節點上執行 agent，Kubernetes 中通常以 DaemonSet 部署。Agent 會將 eBPF 程式載入核心，並用它們觀察指定 hook。事件經政策過濾與脈絡補強後，再匯出到使用者空間。

核心概念：

- **eBPF sensors**：在核心中收集與過濾執行期活動，相較於把所有事件都送到使用者空間 agent，通常成本更低。
- **行程生命週期事件**：Tetragon 會產生行程執行與結束事件，這是將後續活動歸因到 binary 與行程樹的基礎。
- **TracingPolicy**：Kubernetes 自訂資源，用來定義要觀察哪些核心或使用者空間 hook，以及要套用哪些 selector、filter 與 action。
- **Hook points**：政策可使用核心的 `kprobes`、`tracepoints`，以及使用者空間的 `uprobes`。官方文件提醒，直接 hook system call 時，如果參數指向使用者空間記憶體，可能有 TOCTOU 風險；較後段的核心 hook，例如 LSM `security_` hook，可避免這類問題。
- **Kubernetes 身分補強**：Tetragon 可在事件中加入 namespace、pod、workload、node 與 container 脈絡，讓安全規則能對應到工作負載。
- **執行期防護**：政策可從觀察升級到處置，例如告警、覆寫回傳值，或依政策與 hook 終止行程。
- **匯出與整合**：事件可透過 JSON logs 與 gRPC 取得；metrics 可提供給 Prometheus 相容系統。

Tetragon 最適合用在明確的政策上。廣泛地「全部追蹤」容易造成雜訊與成本；高價值政策應聚焦在可疑執行路徑、非預期權限提升、敏感檔案存取，以及特定工作負載的異常行為。

### 實務用法

使用 Helm 安裝到 Kubernetes：

```bash
helm repo add cilium https://helm.cilium.io
helm repo update
helm install tetragon cilium/tetragon -n kube-system
kubectl rollout status -n kube-system ds/tetragon -w
```

在單節點叢集中，從 Tetragon DaemonSet 觀察行程執行事件：

```bash
kubectl exec -ti -n kube-system ds/tetragon -c tetragon -- \
  tetra getevents -o compact
```

常見的起始政策與檢查：

- 監控 `/tmp` 等可寫入路徑中的 binary 執行。
- 偵測 production application container 內是否啟動 shell 或 package manager。
- 針對 SUID、file capability、setuid 相關的權限變更發出告警。
- 偵測匿名記憶體 backed binary 等 fileless execution 型態。
- 監控原本不應有對外連線的工作負載。
- 調查權限變更時，啟用 process credential 可視性。
- 將事件匯出到 log pipeline，並與 Kubernetes audit logs、Cilium/Hubble flow logs、應用程式 telemetry 交叉比對。

維運建議：

- 先以觀察模式部署，再啟用阻擋或終止等 enforcement action。
- 依 namespace、pod labels、container name、binary path 與 arguments 縮小政策範圍，降低雜訊。
- 在具代表性的工作負載與 kernel 版本上測試政策；kernel hook 的可用性與語義可能因版本而異。
- 升級前檢查 release notes，特別是 Helm values、CRDs、event schemas 與 metrics。
- 將 Tetragon 視為多層防禦的一層，而不是唯一控制點。

### 學習檢核表

- 說明 eBPF 如何協助 Tetragon 以較低成本取得執行期可視性。
- 區分行程執行事件與自訂 `TracingPolicy` 事件。
- 使用 Helm 安裝 Tetragon 並驗證 DaemonSet rollout。
- 使用 `tetra getevents` 檢查行程事件。
- 讀懂一筆 Tetragon JSON event，並找出 binary、arguments、父行程、Pod、Namespace 與節點。
- 撰寫或調整一個能監控敏感行為、但不會淹沒事件流的政策。
- 判斷什麼時候只需告警，什麼時候才適合啟用 enforcement。
- 理解升級敏感項目：Helm values、CRDs、metrics 名稱、event schema 與 kernel 相容性。

## References

- [Tetragon official site](https://tetragon.io/)
- [Tetragon documentation overview](https://tetragon.io/docs/overview/)
- [Deploy Tetragon on Kubernetes](https://tetragon.io/docs/installation/kubernetes/)
- [Tetragon Helm chart reference](https://tetragon.io/docs/reference/helm-chart/)
- [Execution monitoring guide](https://tetragon.io/docs/getting-started/execution/)
- [TracingPolicy hook points](https://tetragon.io/docs/concepts/tracing-policy/hooks/)
- [Tetragon policy library: observability policies](https://tetragon.io/docs/policy-library/observability/)
- [Tetragon GitHub repository and releases](https://github.com/cilium/tetragon)
