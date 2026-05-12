# Desktop Extensions DXT

| Field | Details |
| --- | --- |
| Category | MCP packaging, desktop agent distribution |
| Current name | MCP Bundles (MCPB) |
| Legacy name | Desktop Extensions (DXT) |
| File extensions | `.mcpb` recommended for new bundles; `.dxt` legacy-compatible |
| Primary use | Package local MCP servers for one-click installation in desktop AI clients |
| Package format | Zip archive with `manifest.json`, server code, assets, and optional dependencies |
| Reference implementation | `modelcontextprotocol/mcpb` |
| Best fit | Developers distributing local MCP integrations to non-developer users |
| Last reviewed | 2026-04-29 |

## English

### Overview

Desktop Extensions, originally known as DXT, were introduced to make local MCP server installation easier for desktop users. The format has since been renamed MCP Bundles (MCPB). New packages should use the `.mcpb` extension, while existing `.dxt` packages continue to work where clients preserve compatibility.

An MCPB package is a zip archive that contains a local MCP server and a `manifest.json` file describing the extension, its runtime, user configuration, compatibility, and requested permissions. The goal is similar to browser or editor extensions: package a capability once, let users install it without manually editing MCP configuration files.

### Why it matters

- **Lower installation friction:** Users can install local MCP servers without cloning repos, editing JSON, or debugging runtime paths.
- **Better distribution:** Developers can ship a single bundle with metadata, icons, runtime requirements, and configuration prompts.
- **Safer setup:** Clients can inspect manifests, show permissions, and ask users for configuration before running server code.
- **Local-first integrations:** Desktop extensions are useful for file, app, and OS-level workflows that should stay on the user's machine.
- **Bridge from prototype to product:** A working MCP server can become a shareable desktop integration with packaging rather than a full hosted service.

### Architecture/Concepts

| Concept | Meaning |
| --- | --- |
| MCPB / DXT bundle | A compressed package containing a local MCP server and its metadata. |
| `manifest.json` | The required metadata and configuration file for the bundle. |
| Runtime | The execution environment required by the server, such as Node.js or Python. |
| User config | Install-time fields the client asks the user to provide, such as API keys or folder paths. |
| Compatibility | Host, platform, and version constraints that help clients decide whether the bundle can run. |
| Permissions | Declared capabilities or access expectations shown to the user before installation or execution. |
| CLI | Tooling for initializing, validating, packing, signing, and inspecting bundles. |

The manifest is the contract between the bundle author and the desktop host. It should tell the host what the extension is, how to launch it, which environment variables or user-provided values it needs, and which client or platform versions it supports.

DXT/MCPB does not replace MCP. It packages an MCP server. MCP defines the runtime protocol between client and server; MCPB defines a desktop-friendly distribution format for local servers.

### Practical usage

Use MCPB when a local MCP server should be easy for end users to install:

| Scenario | MCPB fit | Notes |
| --- | --- | --- |
| Local file or notes integration | Strong | Bundle the server and request a folder path during setup. |
| Desktop app automation | Strong | Clearly disclose permissions and supported OS versions. |
| API-backed local helper | Strong | Prompt for an API key or OAuth setup if supported by the client. |
| Remote-only SaaS connector | Maybe | A hosted remote MCP server may be easier to update and govern. |
| Enterprise deployment | Depends | Confirm client support, signing requirements, and admin controls. |

Practical authoring flow:

1. Build and test the MCP server directly.
2. Add a `manifest.json` with accurate name, version, runtime, launch command, compatibility, and user configuration.
3. Keep bundled dependencies minimal and reproducible.
4. Validate the bundle with the official CLI.
5. Install it in a clean desktop client profile and test first-run setup.
6. Document what data the server can access and which actions it can take.

Security tips:

- Treat every bundle as executable code.
- Do not hide network calls, file access, or shell execution behind vague descriptions.
- Request only the configuration and permissions the server actually needs.
- Avoid embedding secrets in the package; ask for user configuration at install time.
- Keep server updates versioned and auditable.

### Learning checklist

- [ ] Explain the difference between MCP and MCPB/DXT.
- [ ] Identify why `.mcpb` is preferred for new bundles.
- [ ] Inspect a bundle's `manifest.json`.
- [ ] Build and run the underlying MCP server before packaging.
- [ ] Package a minimal server with the official CLI.
- [ ] Validate runtime, platform, and user configuration fields.
- [ ] Test installation in a supported desktop client.
- [ ] Review bundle permissions and data access with a security mindset.

## 繁體中文

### 概覽

Desktop Extensions 最初稱為 DXT，目標是讓桌面使用者更容易安裝本機 MCP server。這個格式後來更名為 MCP Bundles（MCPB）。新的套件應使用 `.mcpb` 副檔名；既有 `.dxt` 套件在保留相容性的 client 中仍可使用。

MCPB 套件是 zip archive，內含本機 MCP server 與 `manifest.json`。Manifest 描述 extension、runtime、使用者設定、相容性與所需權限。它的目標類似瀏覽器或編輯器 extension：把能力封裝一次，讓使用者不用手動修改 MCP 設定檔即可安裝。

### 為什麼重要

- **降低安裝門檻：** 使用者不必 clone repo、編輯 JSON 或處理 runtime path。
- **更容易發佈：** 開發者可用單一 bundle 提供 metadata、icon、runtime requirements 與設定提示。
- **設定更安全：** Client 可檢查 manifest、顯示權限，並在執行 server code 前要求使用者設定。
- **支援 local-first 整合：** 適合檔案、app 與 OS 層級工作流，讓資料留在使用者機器上。
- **從 prototype 走向產品：** 已可運作的 MCP server 可透過包裝變成可分享桌面整合，不一定要先做完整 hosted service。

### 架構/概念

| 概念 | 說明 |
| --- | --- |
| MCPB / DXT bundle | 包含本機 MCP server 與 metadata 的壓縮套件。 |
| `manifest.json` | Bundle 必要的 metadata 與設定檔。 |
| Runtime | Server 需要的執行環境，例如 Node.js 或 Python。 |
| User config | 安裝時 client 要求使用者提供的欄位，例如 API key 或資料夾路徑。 |
| Compatibility | Host、平台與版本限制，用來判斷 bundle 是否可執行。 |
| Permissions | 安裝或執行前顯示給使用者的能力或存取需求。 |
| CLI | 用於初始化、驗證、打包、簽署與檢查 bundle 的工具。 |

Manifest 是 bundle 作者與 desktop host 之間的合約。它應清楚說明 extension 是什麼、如何啟動、需要哪些環境變數或使用者提供值，以及支援哪些 client 或平台版本。

DXT/MCPB 不會取代 MCP。它是 MCP server 的封裝格式。MCP 定義 client 與 server 執行時的協定；MCPB 定義本機 server 的桌面友善發佈格式。

### 實務使用

當本機 MCP server 需要讓終端使用者容易安裝時，適合使用 MCPB：

| 場景 | MCPB 適合度 | 備註 |
| --- | --- | --- |
| 本機檔案或筆記整合 | 高 | 打包 server，並在設定時要求資料夾路徑。 |
| 桌面 app 自動化 | 高 | 清楚揭露權限與支援 OS 版本。 |
| API-backed 本機 helper | 高 | 依 client 能力提示 API key 或 OAuth 設定。 |
| 純遠端 SaaS connector | 視情況 | Hosted remote MCP server 可能更容易更新與治理。 |
| 企業部署 | 視情況 | 需確認 client 支援、簽署需求與管理員控制。 |

實務製作流程：

1. 先直接建置並測試 MCP server。
2. 加入 `manifest.json`，正確填寫名稱、版本、runtime、launch command、相容性與使用者設定。
3. 讓 bundled dependencies 維持最小且可重現。
4. 用官方 CLI 驗證 bundle。
5. 在乾淨的 desktop client profile 中安裝並測試首次設定。
6. 文件化 server 可存取哪些資料、可執行哪些動作。

安全建議：

- 將每個 bundle 都視為可執行程式碼。
- 不要用模糊描述隱藏網路呼叫、檔案存取或 shell execution。
- 只要求 server 實際需要的設定與權限。
- 不要把 secret 內嵌在 package；安裝時再要求使用者設定。
- 讓 server 更新有版本且可稽核。

### 學習檢核表

- [ ] 說明 MCP 與 MCPB/DXT 的差異。
- [ ] 說明為什麼新 bundle 應優先使用 `.mcpb`。
- [ ] 檢查 bundle 的 `manifest.json`。
- [ ] 在打包前先建置並執行底層 MCP server。
- [ ] 使用官方 CLI 打包最小 server。
- [ ] 驗證 runtime、platform 與 user configuration 欄位。
- [ ] 在支援的 desktop client 中測試安裝。
- [ ] 以安全角度審查 bundle 權限與資料存取。

## References

- [MCPB GitHub repository](https://github.com/modelcontextprotocol/mcpb)
- [MCPB manifest specification](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md)
- [MCPB CLI documentation](https://github.com/modelcontextprotocol/mcpb/blob/main/CLI.md)
- [Anthropic: Desktop Extensions announcement](https://www.anthropic.com/engineering/desktop-extensions)
- [Model Context Protocol documentation](https://modelcontextprotocol.io/docs/getting-started/intro)
