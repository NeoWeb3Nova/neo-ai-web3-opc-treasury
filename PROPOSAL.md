# OPC Agent Treasury — Project Proposal

> 项目定位：一人公司的 AI 员工财务操作系统  
> 赛道：AI × Web3 Agentic Builders Hackathon / Cobo Agentic Wallet Track  
> 更新时间：2026-06-12  
> 当前状态：可运行 MVP；Mock 模式可本地完整演示；Real CAW 模式已完成 SDK/REST 对接与测试网验证记录  
> GitHub：`https://github.com/NeoWeb3Nova/opc-agent-treasury`

---

## 0. 执行摘要

AI Agent 正在从“写内容、查资料、跑脚本”的工具，变成一人公司（One-Person Company, OPC）的数字员工。它们会持续调用 API、购买数据、租用算力、支付广告和外包服务。但现有支付体系仍然假设付款主体是人类员工或传统公司：要么每笔都让老板手动审批，要么把私钥/API Key 交给 Agent。前者牺牲自动化，后者放大资金风险。

OPC Agent Treasury 的核心方案是：把 Cobo Agentic Wallet 的 Pact 抽象成“AI 员工支出卡”。老板为每个 Agent 配置预算、单笔限额、供应商白名单、有效期、冷却期和审计规则；Agent 可以在授权范围内自主支付 x402/API 服务，但永远不能接触私钥、不能绕过策略、不能隐藏被拒绝的交易。

本项目不是一个“AI + Web3 概念包装”，而是一个围绕真实痛点设计的财务控制层：

- 面向真实用户：OPC 经营者、Agent 开发者、x402 服务提供商；
- 面向真实资金风险：Prompt Injection、地址篡改、预算耗尽、错用权限、撤销后复用；
- 面向真实技术栈：FastAPI、React/Vite、Cobo CAW SDK/REST、CAW Pact Policy、x402、ERC-8004；
- 面向真实演示：本地 Mock 模式零凭证可跑，Real 模式保留 CAW 钱包/Pact/交易验证记录与 SOP。

---

## 1. 问题：AI 员工已经入职，财务授权体系没有跟上

### 1.1 核心矛盾

一人公司今天可以用多个 AI Agent 组成“数字团队”：


| AI 员工          | 典型任务                    | 会触发的支出               |
| -------------- | ----------------------- | -------------------- |
| Research Agent | 市场调研、协议监控、数据检索          | 搜索 API、数据 API、链上 RPC |
| Growth Agent   | 广告实验、社媒分发、线索 enrichment | 广告账户、社媒数据、增长工具       |
| Infra Agent    | 部署检查、RPC 监控、自动化运维       | RPC、云服务、监控服务         |
| Ops Agent      | 采购、报销、供应商协调             | API 订阅、外包服务、支付路由     |
| Audit Agent    | 对账、异常复核、月底报告            | 审计数据、报表导出、归档服务       |


问题在于：这些 Agent 可以 7×24 工作，但不能安全地 7×24 花钱。

### 1.2 现有方案为什么失败


| 方案                    | 表面上解决了什么     | 结构性缺陷                                        |
| --------------------- | ------------ | -------------------------------------------- |
| 把钱包私钥/API Key 给 Agent | Agent 可以立即付款 | 一次 Prompt Injection 或工具链污染就可能导致全额资金损失        |
| 每笔付款都人工审批             | 人类老板保持控制权    | Agent 的自主性消失，所有微支付都会卡在审批队列                   |
| 使用 Brex/Ramp 等企业卡     | 有成熟预算和对账能力   | 为法人公司和人类员工设计，不适合钱包原生 AI Agent                |
| 使用 Safe 多签            | 大额资金安全       | 对高频小额支付过重，OPC 只有一个老板时体验更差                    |
| 传统 API Key / 预充值      | 易于集成         | 每个服务都需要预注册，无法支持开放的 Agent-to-Service commerce |


本质上，传统系统解决的是“人类员工如何报销/刷卡”，而不是“非人类 Agent 如何在可审计、可撤销、可限制的边界内自主支付”。

### 1.3 需要被解决的三个底层问题

1. 身份问题：谁在付款？是哪个 Agent？是否绑定到一个可验证身份或声誉上下文？
2. 授权问题：这个 Agent 可以向谁付款、花多少钱、在什么时间窗口内付款？
3. 审计问题：哪些交易通过了，哪些被拦截了，为什么被拦截，老板能否复盘？

没有这三层，Agentic Economy 只能停留在模拟交易或中心化托管账户，无法进入真实商业场景。

---

## 2. 解决方案：给每个 AI 员工发一张可编程支出卡

### 2.1 产品一句话

OPC Agent Treasury 使用 Cobo Agentic Wallet Pact 为每个 AI Agent 发行一张可编程、可撤销、可审计的虚拟支出卡，让 Agent 能在老板设定的边界内自主支付。

### 2.2 关键设计原则

```text
Agent 的自主性只有在资金风险被数学化约束后才有商业价值。
```


| 设计原则        | 项目实现                                                      |
| ----------- | --------------------------------------------------------- |
| Agent 不持有私钥 | Agent 通过 CAW Pact-scoped 权限触发支付，私钥由 CAW/MPC 基础设施保护        |
| 默认最小权限      | 每张卡绑定预算、供应商、链、Token、有效期和 Agent 身份                         |
| 策略先于转账      | 后端本地业务检查 + CAW Policy Engine 在付款前执行                       |
| 拒绝也是审计资产    | 被拦截的攻击/异常交易会进入交易记录和审计摘要                                   |
| 可快速撤销       | Pact/Card 可以被吊销；Real 模式中 Owner 侧撤销通过 CAW App/Owner Key 完成 |


### 2.3 产品形态

```text
OPC Owner
  │
  │ 创建 / 审批 / 吊销 Agent 支出卡
  ▼
OPC Agent Treasury
  ├─ Cards / Pacts：每个 AI 员工一张支出卡
  ├─ Policy Engine：预算、单笔限额、白名单、冷却期、有效期
  ├─ Agent Console：Agent 发起 x402/API 服务采购
  ├─ Attack Lab：演示攻击如何被拦截
  └─ Audit Report：月底对账、异常复盘、交易明细
  │
  ▼
Cobo Agentic Wallet
  ├─ Pact lifecycle
  ├─ Transfer policy
  ├─ Message-sign policy for ERC-8004 EIP-712
  ├─ Pact-scoped API key
  └─ CAW audit / transaction APIs
  │
  ▼
x402 / API / Agent Marketplace Providers
```

### 2.4 用户视角的完整闭环

1. 老板选择一个 AI 员工，例如 Vega Research Agent。
2. 老板创建一张支出卡：月预算 300 USDC、单笔 40 USDC、只允许指定 x402 数据/API 服务。
3. Real 模式下，CAW 创建 Pact，老板在 Cobo App 中审批后变为 Active。
4. 老板把 Active Card 分配给 Vega。
5. Vega 在 Agent Console 或外部 Agent Runtime 中请求支付服务。
6. 后端检查卡状态、员工绑定、供应商白名单、金额、冷却期。
7. Real 模式下，CAW 使用 Pact policy 与 Pact-scoped API key 执行最终权限校验和转账。
8. 成功、拒绝、异常和链上错误都会进入审计记录。

### 2.5 与 Cobo CAW 的关系

本项目中 CAW 不是可替换的“钱包登录组件”，而是核心控制平面：


| CAW 能力                | 在项目中的角色                   |
| --------------------- | ------------------------- |
| Pact                  | 虚拟支出卡的生命周期和权限容器           |
| Policy Engine         | 链、Token、目标地址、预算、签名范围的强制边界 |
| MPC-TSS 钱包            | 私钥不暴露给 Agent Runtime      |
| Pact-scoped API Key   | 支付请求被绑定到具体 Pact，而不是泛化钱包权限 |
| App/Owner Key         | 老板保留审批、撤销和最终控制权           |
| Transaction/Audit API | 为审计和 Dashboard 提供真实数据来源   |


---

## 3. 目标用户

### 3.1 第一类用户：一人公司经营者（OPC Owner）


| 画像   | 描述                                         |
| ---- | ------------------------------------------ |
| 典型状态 | 一个人经营内容、咨询、SaaS、Web3 服务或自动化业务              |
| 已有工具 | ChatGPT/Claude、自动化脚本、Agent 框架、订阅 API、云服务   |
| 核心痛点 | 不想让 Agent 乱花钱，也不想半夜审批每一笔 0.01-10 USDC 的微支付 |
| 使用场景 | 给不同 Agent 发放不同预算卡，查看支出、拦截异常、一键撤销           |


### 3.2 第二类用户：AI Agent / Multi-Agent 框架开发者


| 画像   | 描述                                                     |
| ---- | ------------------------------------------------------ |
| 典型状态 | 构建 CrewAI、LangGraph、AutoGPT 类 Agent 系统或垂直 Agent 应用     |
| 核心痛点 | Agent 可以决策和执行任务，但缺少安全的真实付款能力                           |
| 使用场景 | 把 OPC Agent Treasury 作为支付中间层，让 Agent 调用付费 API、数据源或链上服务 |


### 3.3 第三类用户：x402 / Agent 服务提供商


| 画像   | 描述                                     |
| ---- | -------------------------------------- |
| 典型状态 | 提供按次付费 API、AI 推理、链上数据、搜索、RPC、增长数据服务    |
| 核心痛点 | 传统 API Key 模式依赖人类注册和预充值，不适合开放 Agent 市场 |
| 使用场景 | 通过 x402 收款，接受来自 CAW 控制的钱包原生 Agent 支付   |


### 3.4 早期切入点

优先选择 Crypto-native OPC 和 Agent 开发者，而不是一开始进入传统企业财务系统。原因：

- 他们已经理解钱包、USDC、x402 和链上支付；
- 他们更愿意接受测试网/MVP/开发者工具形态；
- 他们的支付频率高、金额小、风险边界清晰，适合用 Pact 方式做最小可行验证；
- 他们对“AI 员工”有真实使用场景，而不是概念兴趣。

---

## 4. 技术实现

### 4.1 总体架构

```text
┌──────────────────────────────────────────────────────────────┐
│ Frontend: React + Vite + TypeScript                           │
│ Dashboard / Cards / Agent Console / Attack Demo / Audit       │
└──────────────────────────────┬───────────────────────────────┘
                               │ REST
┌──────────────────────────────▼───────────────────────────────┐
│ Backend: FastAPI + Pydantic                                   │
│ /cards /payments /attacks /audit /dashboard /providers        │
└──────────────────────────────┬───────────────────────────────┘
                               │ Factory Pattern
┌──────────────────────────────▼───────────────────────────────┐
│ CAW Client Layer                                               │
│ MockCAWClient: offline simulation                              │
│ RealCAWClient: Cobo CAW SDK + sync REST fallback               │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ Cobo Agentic Wallet                                            │
│ Pact / Policy Engine / MPC transfer / audit / owner approval   │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│ Agent Commerce Context                                         │
│ x402 providers / ERC-8004 identity & reputation / Base USDC    │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 协议栈


| 层级    | 技术/协议                               | 项目职责                                    | 证据                                          |
| ----- | ----------------------------------- | --------------------------------------- | ------------------------------------------- |
| 业务层   | OPC Digital Employees               | 定义 Agent 员工、角色、风险等级、推荐预算                | `src/service_registry.py`                   |
| 支付发现层 | x402 / HTTP 402 pattern             | 表达按次付费 API/服务采购流程                       | `docs/05-flow.md`, `/providers/x402`        |
| 身份层   | ERC-8004                            | Agent 身份、声誉、EIP-712 AgentWalletSet 签名范围 | `src/real_caw_client.py`                    |
| 授权层   | Cobo CAW Pact                       | 每张卡的预算、白名单、生命周期、审批状态                    | `src/real_caw_client.py`                    |
| 风控层   | CAW Policy + local policy           | 付款前做状态、员工绑定、供应商、金额、冷却期检查                | `src/mock_caw_client.py`, `backend/main.py` |
| 结算层   | CAW transfer on Base / Base Sepolia | 真实模式下提交 token transfer                  | `src/real_caw_client.py`                    |
| 审计层   | CAW transactions + local records    | Dashboard、Audit Summary、异常交易记录          | `backend/main.py`, `src/audit_reporter.py`  |


### 4.3 后端模块


| 模块               | 职责                                                             | 文件                        |
| ---------------- | -------------------------------------------------------------- | ------------------------- |
| FastAPI API      | 对前端和外部集成暴露 REST 接口                                             | `backend/main.py`         |
| Pydantic Models  | 请求/响应校验，统一卡片、交易、审计结构                                           | `backend/models.py`       |
| CAW Factory      | 根据 `CAW_MODE` 切换 Mock / Real                                   | `src/caw_factory.py`      |
| MockCAWClient    | 离线模拟 CAW Pact、Policy、Transaction、Audit                         | `src/mock_caw_client.py`  |
| RealCAWClient    | 对接 `cobo-agentic-wallet>=0.1.40`、CAW REST、Pact-scoped transfer | `src/real_caw_client.py`  |
| Service Registry | x402 providers、ERC-8004 agents、Digital Employees               | `src/service_registry.py` |
| Threat Simulator | 攻击演示脚本                                                         | `src/threat_simulator.py` |
| Audit Reporter   | Markdown/CSV 审计报表生成                                            | `src/audit_reporter.py`   |
| A2A Coordinator  | Agent-to-Agent 预算调度演示                                          | `src/a2a_agent.py`        |


### 4.4 前端模块


| 页面            | 作用                        | 文件                               |
| ------------- | ------------------------- | -------------------------------- |
| Dashboard     | 总预算、卡片、交易、支出图表            | `web/src/pages/Dashboard.tsx`    |
| Cards         | 创建 Pact/Card、审批状态、员工分配、撤销 | `web/src/pages/Cards.tsx`        |
| Agent Console | 指定 Agent 发起付款请求           | `web/src/pages/AgentConsole.tsx` |
| Attack Demo   | 执行攻击场景并展示拦截原因             | `web/src/pages/AttackDemo.tsx`   |
| Audit Report  | 月度审计、异常交易、交易明细            | `web/src/pages/AuditReport.tsx`  |
| i18n          | 中英文界面文本                   | `web/src/i18n/`                  |


### 4.5 核心支付校验流程

```text
Payment Request
  │
  ├─ 1. Card lifecycle check
  │     ACTIVE 才允许付款；PENDING / REVOKED / EXPIRED 一律拒绝
  │
  ├─ 2. Employee assignment check
  │     请求中的 agent_id 必须等于卡片 assigned_agent_id
  │
  ├─ 3. Vendor scope check
  │     vendor name/address 必须在该卡自己的 whitelist 中
  │
  ├─ 4. Business policy check
  │     单笔限额、月预算、本地冷却期、金额合法性
  │
  ├─ 5. CAW policy enforcement (real mode)
  │     Pact-scoped API Key + src_addr + dst_addr + token/chain + pact_id
  │
  └─ 6. Audit result
        APPROVED / DENIED / on-chain error 都写入记录
```

### 4.6 技术栈


| 分类       | 技术                                   | 版本/约束                      | 来源                                                  |
| -------- | ------------------------------------ | -------------------------- | --------------------------------------------------- |
| Wallet   | Cobo Agentic Wallet SDK              | `>=0.1.40`                 | `backend/requirements.txt`                          |
| Backend  | Python                               | `3.10+`                    | README / requirements                               |
| Backend  | FastAPI                              | `>=0.111.0`                | `backend/requirements.txt`                          |
| Backend  | Pydantic                             | `>=2.7.0`                  | `backend/requirements.txt`                          |
| Backend  | Uvicorn                              | `>=0.30.0`                 | `backend/requirements.txt`                          |
| Backend  | nest-asyncio                         | `>=1.6.0`                  | `backend/requirements.txt`                          |
| Frontend | React                                | `^19.2.6`                  | `web/package.json`                                  |
| Frontend | Vite                                 | `^8.0.12`                  | `web/package.json`                                  |
| Frontend | TypeScript                           | `~6.0.2`                   | `web/package.json`                                  |
| Frontend | Tailwind CSS                         | `^3.4.19`                  | `web/package.json`                                  |
| Frontend | Recharts                             | `^3.8.1`                   | `web/package.json`                                  |
| Frontend | i18next / react-i18next              | `^26.3.1` / `^17.0.8`      | `web/package.json`                                  |
| Demo     | Streamlit                            | `>=1.35.0`                 | `src/requirements-ui.txt`                           |
| Chain    | Base / Base Sepolia                  | configured via env         | `.env.example`                                      |
| Protocol | x402 / ERC-8004 / ERC-8183 / EIP-712 | integration + architecture | `docs/04-architecture.md`, `src/real_caw_client.py` |


---

## 5. 当前完成度

### 5.1 总体状态


| 维度          | 状态      | 说明                                                            |
| ----------- | ------- | ------------------------------------------------------------- |
| 产品概念        | 已完成     | 目标用户、问题、卡片模型、CAW 映射清晰                                         |
| 本地可运行 MVP   | 已完成     | Mock 模式无需外部凭证即可演示完整流程                                         |
| Real CAW 对接 | 已完成主要路径 | SDK/REST 客户端、Pact 创建、审批轮询、transfer payload、余额/交易读取已实现         |
| 前端演示        | 已完成     | Dashboard、Cards、Agent Console、Attack Demo、Audit Report        |
| 后端 API      | 已完成     | Cards、Payments、Attack、Audit、Marketplace、Digital Employees 等接口 |
| 测试覆盖        | 已有基础覆盖  | Cards、Assignment、Marketplace、RealCAW policy 构造/回归测试           |
| 文档          | 已有完整材料  | README、Proposal、架构、流程、风险、SOP、CAW 研究报告                         |
| Demo 视频     | 未完成     | `demo/video/` 当前只有 `.gitkeep`，需要录制最终提交视频                      |
| 截图素材        | 未完成     | `demo/screenshots/` 当前只有 `.gitkeep`，需要补充 UI 截图                |
| 生产可用        | 未完成     | 尚需真实 x402 中间件、持久化 DB、主网风控、审计与合规加固                             |


### 5.2 已实现功能清单


| 模块              | 功能                                                 | 状态     | 证据                                           |
| --------------- | -------------------------------------------------- | ------ | -------------------------------------------- |
| CAW 抽象          | Mock / Real 双模式切换                                  | 完成     | `src/caw_factory.py`                         |
| Mock 模式         | Pact 生命周期、Policy、Audit、A2A 调度模拟                    | 完成     | `src/mock_caw_client.py`                     |
| Real 模式         | CAW SDK 初始化、Pact 创建、HTTP fallback、transfer payload | 完成主要路径 | `src/real_caw_client.py`                     |
| Cards API       | 创建、列表、详情、审批、分配、撤销                                  | 完成     | `backend/main.py`                            |
| Payments API    | Agent 付款、员工绑定校验、失败原因归一化                            | 完成     | `backend/main.py`                            |
| Marketplace API | x402 providers、ERC-8004 agent search/context       | 完成     | `src/service_registry.py`                    |
| Attack Lab      | 5 种可执行攻击场景                                         | 完成     | `backend/main.py`, `src/threat_simulator.py` |
| Threat Model    | 8 类攻击矩阵                                            | 已文档化   | `docs/03-attack-matrix.md`                   |
| Audit           | 交易记录、月度 summary、报表生成器                              | 完成     | `src/audit_reporter.py`, `/audit/summary`    |
| React UI        | 5 个核心页面                                            | 完成     | `web/src/pages/`                             |
| Streamlit UI    | 本地演示入口                                             | 完成     | `src/app.py`                                 |
| CLI Demo        | normal / attack / full / a2a                       | 完成     | `src/run_demo.py`                            |


### 5.3 Real CAW / 测试网验证记录

项目材料中保留以下 Real CAW 验证记录，用于证明该项目不是纯 Mock：


| 验证项                             | 记录                                                                   |
| ------------------------------- | -------------------------------------------------------------------- |
| CAW Wallet UUID                 | `ad7f3253-4a3b-48a0-9d09-9bb59d334390`                               |
| Wallet ETH address              | `0x0abd808e6df088b9b97179a091582618586d0bdc`                         |
| Successful transfer transaction | `0x1a119f1b1bf5ffdb9f2dc4bea392d5d489807aa97925c1949199f7ea91c9dddd` |
| Transfer amount                 | `0.001 SETH` on Base Sepolia test environment                        |
| CAW Pact instance               | `13328473-3868-4f45-a35e-ae2a8a1e1ea4`                               |
| Pact policy summary             | `BASE_USDC`, `$50/tx`, `$500/month`                                  |
| SDK dependency                  | `cobo-agentic-wallet>=0.1.40`                                        |
| SOP                             | `docs/CAW-REAL-MODE-SOP.md`                                          |


说明：默认评审演示建议使用 Mock 模式保证可复现；Real 模式用于证明 CAW 集成深度和真实钱包路径，但不建议评审过程依赖外部移动 App 审批和测试网状态。

### 5.4 代码与文档规模


| 指标                                          | 当前值   |
| ------------------------------------------- | ----- |
| Python 代码行数（`src/` + `backend/` + `tests/`） | 6,864 |
| TypeScript/TSX 代码行数（`web/src/`）             | 4,937 |
| Markdown 文档数量                               | 18    |
| 后端测试文件                                      | 3     |
| 前端核心页面                                      | 5     |
| 可执行 Demo 模式                                 | 4     |


### 5.5 当前 MVP 边界


| 边界       | 当前状态                          | 为什么可以接受                   | 后续处理                               |
| -------- | ----------------------------- | ------------------------- | ---------------------------------- |
| x402 服务端 | 当前以 provider registry 和流程模拟为主 | 黑客松重点是 CAW 权限与 Agent 支付控制 | 接入生产 x402 middleware / facilitator |
| 持久化存储    | Mock 状态在内存，Real 模式有本地非敏缓存     | 演示和测试足够                   | 引入 SQLite/Postgres 和事件表            |
| 真正供应商地址  | `.env.example` 使用占位地址         | 防止误转账和泄露                  | 生产前逐个验证 vendor address             |
| 审计不可篡改   | 本地记录 + CAW 交易/日志读取            | MVP 可复盘                   | Merkle root / receipt 上链或对象存储      |
| 主网资金     | 当前定位测试网/低限额验证                 | 避免未经审计的资金风险               | 第三方审计、额度灰度、监控告警                    |


---

## 6. 后续计划

### 6.1 提交前 P0


| 任务                    | 优先级 | 结果标准                                                                 |
| --------------------- | --- | -------------------------------------------------------------------- |
| 录制 3-5 分钟 Demo 视频     | P0  | `demo/video/` 中有最终视频或提交平台链接                                          |
| 补充核心 UI 截图            | P0  | `demo/screenshots/` 中至少包含 Dashboard、Cards、Agent Console、Attack、Audit |
| 最终 README/Proposal 校验 | P0  | 不夸大 Demo/截图/生产状态；命令、路径、版本准确                                          |
| 本地演示烟测                | P0  | 后端 health、前端 build、pytest 通过                                         |


### 6.2 Phase 1：产品化 MVP


| 方向          | 具体工作                                                                | 目标                       |
| ----------- | ------------------------------------------------------------------- | ------------------------ |
| 真实 x402 集成  | 接入生产 x402 middleware / facilitator，支持真实 402 → payment proof → retry | 从“支付控制演示”升级为“真实按次付费服务采购” |
| 持久化         | 增加 SQLite/Postgres，保存 cards、assignments、transactions、audit events   | 演示状态可恢复，审计可追踪            |
| Real CAW UX | 优化 App 审批、Pact 状态同步、Owner revoke 提示                                 | 降低真实模式操作摩擦               |
| 事件通知        | SSE/WebSocket 或轮询通知 pending、approved、denied、revoked                 | 老板能及时看到异常                |
| Vendor 验证   | 供应商地址验证、风险等级、可信来源标记                                                 | 降低地址投毒风险                 |


### 6.3 Phase 2：Agent 财务平台


| 方向                       | 具体工作                                     | 目标                   |
| ------------------------ | ---------------------------------------- | -------------------- |
| Card Templates           | 按岗位提供 Research/Growth/Infra/Ops/Audit 模板 | 老板不用从零设计策略           |
| Agent Framework Adapters | 为 LangGraph、CrewAI、AutoGen 等提供接入样例       | 让开发者快速把 Agent 接入支付能力 |
| ERC-8004 深化              | 使用身份、声誉和验证数据动态调整额度/审批阈值                  | 从固定白名单升级为声誉感知风控      |
| Accounting Export        | CSV、Markdown、会计工具导出                      | 面向 OPC 的月度对账和税务准备    |
| 安全测试                     | 扩展攻击脚本、加入回放测试和地址篡改测试                     | 建立可验证安全基线            |


### 6.4 Phase 3：协议与生态


| 方向                   | 具体工作                                  | 目标                          |
| -------------------- | ------------------------------------- | --------------------------- |
| ERC-8183 Escrow      | 增加交付验收、争议、Evaluator Agent、超时退款        | 支持外包/内容/服务类支付，而不只是即时 API 调用 |
| 多钱包兼容                | 抽象 Pact/Card 策略模型，探索 Safe、Turnkey 等后端 | 避免单一基础设施绑定，同时保留 CAW 优先实现    |
| Hosted Dashboard     | 提供托管版多租户 Dashboard                    | 从黑客松项目进入真实用户试用              |
| Risk Policy Standard | 输出 Agent spending policy schema       | 推动 Agent 支付风控标准化            |


---

## 7. 商业路径

### 7.1 为什么现在做

Agent 经济正在出现两个同步变化：

1. Agent 能力从“建议”走向“执行”：它们不只生成文本，还会调用工具、创建任务、采购服务。
2. Web3 支付从“人类钱包转账”走向“机器可读的按次支付”：x402、CAW、ERC-8004 等协议让 Agent commerce 有了基础设施雏形。

当这两个趋势交汇时，最先爆发的不是复杂金融产品，而是小额、高频、可控、可审计的业务支出。OPC 是最适合的早期市场。

### 7.2 商业模式假设


| 阶段      | 模式                             | 收入来源                     |
| ------- | ------------------------------ | ------------------------ |
| 开源/MVP  | 开源工具 + 黑客松展示                   | 奖金、资助、生态合作               |
| 早期 SaaS | 托管 Dashboard + 高级策略模板          | 月订阅，如 $20-$100 / OPC     |
| 开发者平台   | SDK、Agent 框架 adapter、API usage | 开发者套餐、用量计费               |
| 交易层     | 真实 x402/CAW 支付编排               | 小比例 transaction fee 或服务费 |
| 企业/团队版  | 多 Agent、多 Owner、合规审计           | 团队订阅、定制部署                |


### 7.3 护城河


| 护城河               | 说明                                                                  | 证据                                                    |
| ----------------- | ------------------------------------------------------------------- | ----------------------------------------------------- |
| 场景聚焦              | 不是泛化钱包，而是 OPC + AI 员工支出控制                                           | 产品模型围绕 Cards、Employees、Audit 展开                       |
| CAW 深度            | Pact、Policy、Pact-scoped key、Owner revoke、event-loop workaround 均有处理 | `src/real_caw_client.py`                              |
| 安全思维              | 从一开始设计攻击演示和拦截原因，而不是事后补安全                                            | `docs/03-attack-matrix.md`, `src/threat_simulator.py` |
| 双模式工程             | Mock 保证可复现，Real 保证不是纸面方案                                            | `src/caw_factory.py`                                  |
| Agent commerce 语境 | 连接 x402 provider、ERC-8004 agent、CAW policy                          | `src/service_registry.py`                             |


---

## 8. 团队与执行方式


| 角色                 | 贡献                                                |
| ------------------ | ------------------------------------------------- |
| Neo / NeoWeb3Nova  | 产品方向、OPC 场景定义、协议研究、架构、前后端实现、CAW Real 模式验证、文档与演示设计 |
| AI Coding Partners | 辅助代码生成、调试、测试补充、文档初稿和结构化整理；最终由人类开发者审查和整合           |


这是一个符合 OPC 方法论的项目：用 AI 增强单人执行力，但不让 AI 替代商业判断。项目的关键不是“用了 AI”，而是把 AI Agent 作为未来真实员工来设计财务权限、风控和审计。

---

## 9. 风险与应对


| 风险                          | 影响                  | 当前应对                                  | 后续加强                      |
| --------------------------- | ------------------- | ------------------------------------- | ------------------------- |
| Agent 被 Prompt Injection 操控 | 向攻击者地址付款            | 供应商白名单、员工绑定、CAW policy、Attack Lab     | 内容隔离、工具调用沙箱、策略模板审计        |
| 供应商地址被投毒                    | 合法服务名对应错误地址         | 卡片使用自身 whitelist 地址；未知地址拒绝            | 地址验证、签名声明、可信 registry     |
| Pact 撤销权限不清                 | Agent key 无法 revoke | 前端提示 Owner/App 侧操作，后端同步状态             | Owner key flow、Webhook 同步 |
| CAW SDK async loop 问题       | FastAPI 同步接口不稳定     | fresh SDK client + sync REST fallback | 官方 SDK 更新后简化实现            |
| Demo 依赖外部服务                 | 评审时不稳定              | Mock 模式默认零外部依赖                        | 录制视频 + 本地 fixture         |
| 生产资金风险                      | 未审计代码处理真实资金         | 默认测试网/低限额；风险免责声明                      | 第三方审计、监控告警、保险/限额策略        |


---

## 10. 提交物清单


| 提交物           | 状态    | 位置/说明                                 |
| ------------- | ----- | ------------------------------------- |
| GitHub Repo   | 完成    | 项目根目录                                 |
| README        | 完成    | `README.md`                           |
| 中文 README     | 存在    | `README_CN.md`                        |
| Proposal      | 本次已重写 | `PROPOSAL.md`                         |
| 架构文档          | 完成    | `docs/04-architecture.md`             |
| 流程文档          | 完成    | `docs/05-flow.md`                     |
| 风险文档          | 完成    | `docs/06-risks.md`                    |
| Attack Matrix | 完成    | `docs/03-attack-matrix.md`            |
| Real CAW SOP  | 完成    | `docs/CAW-REAL-MODE-SOP.md`           |
| CAW 研究报告      | 完成    | `docs/cobo-caw-research/report-v2.md` |
| 后端代码          | 完成    | `backend/`, `src/`                    |
| 前端代码          | 完成    | `web/`                                |
| 测试            | 已有    | `tests/`                              |
| Demo 视频       | 待补充   | `demo/video/` 当前只有 `.gitkeep`         |
| UI 截图         | 待补充   | `demo/screenshots/` 当前只有 `.gitkeep`   |


---

## 11. 结论

OPC Agent Treasury 解决的是 Agent 经济进入真实商业前必须补上的一层基础设施：资金权限。

如果没有它，AI Agent 要么不能付款，要么危险地持有私钥；要么被人工审批拖慢，要么在攻击面前没有边界。通过 CAW Pact、策略化支出卡、员工绑定、供应商白名单、x402 支付语境和审计闭环，本项目把“一人公司的 AI 员工”从工具推进到可管理、可约束、可复盘的经济参与者。

这个项目的价值不在于做了一个 Dashboard，而在于提出并验证了一种新的财务原语：

```text
AI Agent 不应该拥有无限钱包。
AI Agent 应该拥有可撤销、可审计、可策略化的支出权限。
```

OPC Agent Treasury 就是这个权限层的最小可行实现。