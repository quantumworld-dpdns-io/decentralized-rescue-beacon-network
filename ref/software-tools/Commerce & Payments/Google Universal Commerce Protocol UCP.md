# Google Universal Commerce Protocol (UCP)

| Field | Details |
| --- | --- |
| Category | Agentic commerce, checkout integration, retail protocol |
| Provider | Google / Universal Commerce Protocol ecosystem |
| Primary use | Enable direct buying and checkout flows from Google AI surfaces such as AI Mode in Search and Gemini |
| Integration paths | Native checkout; Embedded checkout for approved merchants with specialized flows |
| Key dependencies | Merchant Center product data, Google Pay payment handler, UCP profile, checkout APIs, order lifecycle updates |
| Related protocols | Agent Payments Protocol (AP2), Agent2Agent (A2A), Model Context Protocol (MCP) |
| Best fit | Merchants preparing for AI-assisted shopping, direct purchase flows, and agentic commerce channels |
| Last reviewed | 2026-04-29 |

## English

### Overview

Google Universal Commerce Protocol (UCP) is Google's developer-facing path for adopting the Universal Commerce Protocol on Google AI surfaces. UCP is an open standard for agentic commerce: it lets consumer surfaces, merchants, payment services, and identity or credential providers coordinate product discovery, checkout, payment, and post-purchase events through a common protocol.

On Google, UCP is positioned around direct buying from AI Mode in Search and Gemini. Instead of sending a shopper through a traditional multi-page checkout funnel, a merchant can expose checkout capabilities that Google can invoke inside the AI interaction flow. The merchant remains the Merchant of Record and keeps ownership of the customer relationship, transaction data, terms, and post-purchase experience.

Google's implementation is evolving. The documentation notes that not every feature in the broader UCP specification is available on Google's surfaces, so teams should use Google's implementation guides as the source of truth for launch readiness.

### Why it matters

UCP matters because AI assistants are becoming shopping surfaces, not just recommendation interfaces. If a user asks an AI system to compare, select, and buy a product, the commerce stack needs a trustworthy way to move from intent to checkout without losing merchant control or payment security.

For merchants, UCP can reduce checkout friction and expose high-intent demand on Google AI surfaces while preserving the merchant's role in the transaction. For platform teams, it creates a structured integration model for inventory checks, payment token handling, checkout state, order updates, and future account-linked experiences.

It is also important because it connects commerce to the broader agent protocol ecosystem. Google's UCP materials describe compatibility with AP2 for secure agent-led payments, A2A for agent-to-agent communication, and MCP-style tool/data integrations.

### Architecture/Concepts

| Concept | Meaning |
| --- | --- |
| UCP standard | The open commerce protocol that standardizes interactions between consumer surfaces and commerce ecosystem participants. |
| Google AI surfaces | Google entry points such as AI Mode in Search and Gemini where UCP-powered buying experiences can appear. |
| Merchant of Record | The merchant remains responsible for the sale, customer relationship, transaction data, terms, and post-purchase handling. |
| Merchant Center | The source for product feeds, brand assets, shipping, returns, policies, and business information used by Google shopping surfaces. |
| UCP profile | A published profile used by Google to discover merchant capabilities, payment handlers, and public keys for signature verification. |
| Native checkout | The default deeper integration where checkout logic is exposed directly to Google through APIs. |
| Embedded checkout | An optional path for approved merchants that need an iframe-based checkout experience for bespoke flows. |
| Payment handler | Google Pay payment-handler integration used to submit encrypted payment credentials to a payment service provider. |
| Order lifecycle | Events and webhooks used to keep order status, fulfillment, tracking, and transaction state synchronized. |
| Account linking | Optional OAuth 2.0 flow for identity-linked checkout and future loyalty or personalization scenarios. |

Google's implementation overview describes a launch path with these major steps:

1. Prepare Merchant Center data, including product feed, shipping, returns, brand assets, and contact information.
2. Join the UCP waitlist and receive Google approval before going live.
3. Set up the Google Pay payment handler.
4. Publish a UCP profile so Google can discover capabilities and verification keys.
5. Implement native checkout endpoints for session creation, updates, and completion.
6. Choose guest checkout or account-linked checkout.
7. Synchronize order status through webhooks.

### Practical usage

Use Google UCP when a retail or marketplace team wants products to be purchasable directly inside Google AI experiences. It is especially relevant for merchants that already maintain high-quality Merchant Center feeds and want a path from product discovery to checkout without forcing users to abandon the AI surface.

Engineering teams should treat UCP as both a commerce integration and a trust boundary. Checkout endpoints need production-grade availability, real-time inventory validation, reliable tax and shipping updates, payment-token handling through a supported PSP, and clear auditability for order and transaction events.

Native checkout is the strategic path for most merchants because it unlocks richer agentic flows such as multi-item carts, account-linked experiences, and personalization. Embedded checkout may fit merchants with highly customized checkout UX or requirements that the native path does not yet support, but it is described as optional and approval-based.

Implementation tips:

- Keep Merchant Center data complete before starting technical integration.
- Model checkout state explicitly: session creation, address changes, shipping/tax recalculation, payment authorization, completion, cancellation, and errors.
- Implement real-time inventory checks immediately before the final purchase action.
- Identify Google UCP health checks using the documented `Google-UCP-Prober/1.0` user agent.
- Separate UCP traffic from normal web/app checkout traffic in analytics, fraud monitoring, support, and reconciliation.
- Validate payment-token support with your payment service provider before committing to a launch date.
- Review privacy, consent, customer support, and terms display because the merchant still owns the transaction.

### Learning checklist

- [ ] Explain why UCP is different from a normal product feed or checkout redirect.
- [ ] Identify the role of Merchant Center in product discovery and launch readiness.
- [ ] Compare Native checkout and Embedded checkout.
- [ ] Describe how UCP relates to AP2, A2A, and MCP.
- [ ] Map a checkout flow into session creation, update, completion, error handling, and order lifecycle events.
- [ ] Verify how payment tokens are processed by the merchant's payment service provider.
- [ ] Design real-time inventory, shipping, tax, and address update behavior.
- [ ] Document how UCP orders are reconciled against existing ecommerce, analytics, fraud, and support systems.
- [ ] Review privacy, consent, and customer-data ownership responsibilities.
- [ ] Track Google's implementation guides because feature support is still evolving.

## 繁體中文

### 概覽

Google Universal Commerce Protocol（UCP）是 Google 針對 Universal Commerce Protocol 在 Google AI 介面上的開發者整合路徑。UCP 是一個面向 agentic commerce 的開放標準，讓消費者介面、商家、付款服務、身分或憑證提供者，能以共同協定協調商品探索、結帳、付款與購後事件。

在 Google 的實作中，UCP 主要用於讓使用者能在 AI Mode in Search 與 Gemini 等 AI 介面中直接購買商品。商家不只是把使用者導回傳統多頁式結帳流程，而是暴露可由 Google 在 AI 互動流程中呼叫的結帳能力。商家仍然是 Merchant of Record，並保有客戶關係、交易資料、條款與購後體驗的所有權。

Google 的 UCP 支援仍在演進中。文件明確提醒，廣義 UCP 規格中的功能不一定全部已在 Google 介面上提供，因此實作團隊應以 Google 的 implementation guides 作為上線準備的依據。

### 為什麼重要

UCP 的重要性在於，AI 助理正在從商品推薦介面變成購物介面。當使用者要求 AI 比較、選擇並購買商品時，商務系統需要可信任的方式，把購買意圖安全地轉換成結帳與付款，同時不讓商家失去交易控制權。

對商家而言，UCP 可以降低結帳摩擦，並讓高意圖使用者在 Google AI 介面中直接完成購買，同時保留商家在交易中的核心角色。對平台團隊而言，UCP 提供一套結構化整合模型，用於庫存檢查、付款 token 處理、結帳狀態、訂單更新，以及未來的帳號連結體驗。

它也重要在於把商務流程接到更大的 agent protocol 生態系。Google UCP 文件說明它可與 AP2、A2A、MCP 等協定相容：AP2 處理安全的 agent-led payment，A2A 支援 agent-to-agent 通訊，MCP 則常用於工具與資料整合。

### 架構/概念

| 概念 | 說明 |
| --- | --- |
| UCP standard | 標準化消費者介面與商務生態參與者互動的開放商務協定。 |
| Google AI surfaces | 例如 AI Mode in Search 與 Gemini 等可呈現 UCP 購買體驗的 Google 入口。 |
| Merchant of Record | 商家仍負責銷售、客戶關係、交易資料、條款與購後服務。 |
| Merchant Center | Google 購物介面所需商品 feed、品牌素材、運送、退貨、政策與商家資訊來源。 |
| UCP profile | 讓 Google 探索商家能力、payment handler 與簽章驗證公鑰的公開設定。 |
| Native checkout | 預設且較深入的整合方式，商家透過 API 將結帳邏輯提供給 Google。 |
| Embedded checkout | 需要 iframe 型結帳體驗的特定核准商家可使用的選擇性路徑。 |
| Payment handler | Google Pay payment handler 整合，用於將加密付款憑證提交給 PSP。 |
| Order lifecycle | 用於同步訂單狀態、出貨、追蹤與交易狀態的事件與 webhook。 |
| Account linking | 選擇性的 OAuth 2.0 流程，用於帳號連結結帳與未來會員、個人化情境。 |

Google 的實作概覽列出主要上線步驟：

1. 準備 Merchant Center 資料，包含商品 feed、運送、退貨、品牌素材與聯絡資訊。
2. 加入 UCP waitlist，並在上線 Google AI Mode 與 Gemini 前取得 Google 核准。
3. 設定 Google Pay payment handler。
4. 發布 UCP profile，讓 Google 探索能力與驗證金鑰。
5. 實作 native checkout 所需的 session creation、update、completion 端點。
6. 選擇 guest checkout 或 account-linked checkout。
7. 透過 webhook 同步訂單狀態。

### 實務使用

當零售商或 marketplace 團隊希望商品能在 Google AI 體驗中被直接購買時，可以評估 Google UCP。它特別適合已經維護高品質 Merchant Center feed，並希望從商品探索到結帳都留在 AI 互動流程中的商家。

工程團隊應把 UCP 視為商務整合與信任邊界。結帳端點需要具備正式環境等級的可用性、即時庫存驗證、可靠的稅金與運費更新、透過支援 PSP 處理付款 token，以及清楚可稽核的訂單與交易事件。

Native checkout 是多數商家的策略性路徑，因為它能支援更完整的 agentic flow，例如多商品購物車、帳號連結體驗與個人化。Embedded checkout 則適合具有高度客製結帳 UX，或 native path 尚無法支援特殊需求的商家，但 Google 文件將其描述為選擇性且需核准的路徑。

實作建議：

- 技術整合前，先確保 Merchant Center 資料完整。
- 明確建模結帳狀態：建立 session、地址變更、運費與稅金重算、付款授權、完成、取消與錯誤。
- 在最後購買動作前執行即時庫存檢查。
- 使用文件中的 `Google-UCP-Prober/1.0` user agent 辨識 Google UCP health check。
- 在分析、詐欺監控、客服與對帳中，將 UCP 流量與一般網站或 app 結帳流量分開。
- 在承諾上線日期前，先確認付款服務提供者能處理對應 payment token。
- 審查隱私、同意、客服與條款呈現，因為商家仍然擁有交易責任。

### 學習檢核表

- [ ] 說明 UCP 與一般商品 feed 或 checkout redirect 的差異。
- [ ] 辨識 Merchant Center 在商品探索與上線準備中的角色。
- [ ] 比較 Native checkout 與 Embedded checkout。
- [ ] 說明 UCP 與 AP2、A2A、MCP 的關係。
- [ ] 將結帳流程映射到 session creation、update、completion、錯誤處理與 order lifecycle events。
- [ ] 驗證商家的付款服務提供者如何處理 payment token。
- [ ] 設計即時庫存、運送、稅金與地址更新行為。
- [ ] 文件化 UCP 訂單如何與既有 ecommerce、分析、詐欺監控與客服系統對帳。
- [ ] 審查隱私、同意與客戶資料所有權責任。
- [ ] 持續追蹤 Google implementation guides，因為功能支援仍在演進。

## References

- [Google for Developers: Getting started with Universal Commerce Protocol on Google](https://developers.google.com/merchant/ucp)
- [Google for Developers: UCP implementation overview](https://developers.google.com/merchant/ucp/guides)
- [Google for Developers: UCP FAQ](https://developers.google.com/merchant/ucp/faq)
- [Universal Commerce Protocol standard](https://ucp.dev/)
- [Universal Commerce Protocol GitHub organization](https://github.com/ucp-spec)
