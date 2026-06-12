# OPC Agent Treasury — 项目提案（Project Proposal）

> **赛道**: AI × Web3 Agentic Builders Hackathon — Cobo Track（Agentic Economy × Cobo Agentic Wallet）  
> **提交日期**: 2026-06-12  
> **项目状态**: MVP 完成，测试网验证通过，Demo 可运行  
> **GitHub**: https://github.com/NeoWeb3Nova/opc-agent-treasury

---

## 1. 问题陈述（Problem Statement）

### 1.1 核心痛点：AI 员工已入职，财务授权未跟上

全球数百万 **One-Person Company（OPC，一人公司）** 经营者正在雇佣 5~10 个 AI Agent 实现 7×24 小时运营：

- **内容 Agent** 每天需要购买 OpenAI API、Midjourney 订阅、Unsplash 素材
- **广告 Agent** 每周需要充值 Google Ads、Twitter/X 广告账户
- **设计 Agent** 需要向澳洲/东南亚外包付款

**然而，每次 Agent 需要花钱，都必须把人类老板从睡梦中叫醒。**

| 现有方案 | 致命缺陷 |
|---|---|
| **直接给 Agent 私钥** | 一次 Prompt Injection 攻击 = 全盘资金归零 |
| **不给私钥，人工审批每笔支付** | Agent 停工，业务断更，违背 7×24 自动化初衷 |
| **Brex / Ramp 企业卡** | 需要美国公司实体、SSN、人类员工 —— OPC 什么都没有 |
| **Safe 多签钱包** | 每笔小额支付都需要签名，Neo 只有一个人，签不过来 |

### 1.2 为什么传统方案行不通

传统金融科技（Brex、Ramp、Airbase）是为**人类员工**设计的：
- 需要**法律实体**（EIN/SSN）
- 需要**人类身份验证**（KYC）
- 需要**审批工作流**（人类经理点头）

而 AI Agent 是**非人类实体**：没有护照、没有社会安全号、不会在 Slack 里回复审批请求。当 Agent 经济成为生产力主体时，**传统支付基础设施出现结构性断层**。

### 1.3 规模与紧迫性

- **OPC 趋势**：随着 AI 工具普及，全球「一人公司」数量正在指数级增长（Notion、Midjourney、ChatGPT 已让个人产出达到小团队水平）
- **Agent 支付需求**：每个 AI Agent 每年产生 50~500 笔微观支付（API 调用、算力租赁、素材购买），传统人工审批完全不可扩展
- **安全事件**：2024 年以来，已有多起 AI Agent 被 Prompt Injection 诱导转账的公开案例（虽然金额较小，但趋势明确）

**问题本质**：AI 员工已经入职，但财务授权体系还没有为它们建立身份、预算和边界。

---

## 2. 解决方案（Solution）

### 2.1 核心概念：给每个 AI Agent 发一张「企业虚拟卡」

我们基于 **Cobo Agentic Wallet（CAW）** 为每个 AI Agent 发行一张**可编程的支出卡（Pact）**：

- 有**月度预算上限**（如 $500/月）
- 有**单笔交易限额**（如 $50/笔）
- 有**供应商白名单**（仅 OpenAI、Midjourney、Google Ads 等可信地址）
- 有**冷却期**（同一供应商 12 小时内不可重复支付）
- 有**有效时间窗口**（30 天后自动失效）
- 有**实时异常检测**和**自动拦截**
- 有**不可篡改的审计日志**供月底对账

**一句话**：把企业支付卡的风控能力，下放给一人公司的 AI 员工。

### 2.2 产品形态：OPC Agent Treasury（Agent 财务操作系统）

```
┌──────────────────────────────────────────────┐
│           OPC Agent Treasury                 │
│                                              │
│  ┌──────────────┐      ┌──────────────────┐ │
│  │  Pact 管理    │      │  Policy Engine    │ │
│  │  开卡/审批/吊销│      │  预算/白名单/时间 │ │
│  └──────────────┘      └──────────────────┘ │
│         │                       │            │
│         └──────────┬────────────┘            │
│                    ▼                        │
│  ┌────────────────────────────────────────┐ │
│  │           Agent 运行时                 │ │
│  │  Content Agent  ──→ OpenAI/Midjourney │ │
│  │  Ad Agent       ──→ Google Ads/Twitter │ │
│  │  Design Agent   ──→ Freelancer Pay    │ │
│  └────────────────────────────────────────┘ │
│                    │                        │
│                    ▼                        │
│  ┌────────────────────────────────────────┐ │
│  │  Audit & Reporting                   │ │
│  │  实时交易流水 / 月度报表 / 异常告警   │ │
│  └────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

### 2.3 关键创新点

| 创新维度 | 传统方案 | OPC Agent Treasury |
|---|---|---|
| **身份模型** | 人类员工（KYC） | AI Agent（CAW Pact + ERC-8004 身份注册） |
| **授权粒度** | 部门/项目级别 | Agent 个体级别，每张卡独立策略 |
| **风控位置** | 银行端（事后） | MPC 签名前（实时拦截） |
| **私钥管理** | 人类持有或托管 | Agent 不持私钥，CAW 安全模块签名 |
| **审计能力** | 银行月账单 | 逐笔交易链上日志 + 自动 Markdown 报表 |
| **紧急止损** | 冻结账户（慢） | 吊销 Pact（秒级） |

### 2.4 与 CAW 的深度结合

本项目**不是**在 CAW 外面包装一层 UI，而是**将 CAW Pact 作为系统核心风控层**：

- **Pact = 卡**：每个 Pact 对应一张 Agent 支出卡，生命周期（创建 → 审批 → 激活 → 吊销）完全映射
- **Policy = 风控规则**：预算、白名单、时间窗口全部写入 CAW Pact 策略，服务端 MPC 签名前强制校验
- **Transfer = 结算**：所有支出通过 CAW 的 `transfer_tokens` 在 Base 链上完成 USDC 结算
- **Audit = 不可篡改**：CAW 服务端生成 append-only 日志，本地 Merkle 树二次校验

**去掉 CAW，整个系统无法运行** —— 这不是一个可替换的组件，而是唯一能让 Agent 安全持有资金的基础设施。

---

## 3. 目标用户与市场（Target Users & Market）

### 3.1 主要用户画像

#### 用户 A：OPC 经营者（如 Neo）
- **特征**：1 人运营，年收入 $50K~$500K，使用 3~8 个 AI Agent
- **痛点**：半夜被 API 欠费告警叫醒，担心 Agent 被攻击后乱花钱，月底对账头痛
- **使用场景**：通过 Dashboard 为每个 Agent 发卡、设定预算、查看审计日志、一键吊销异常卡

#### 用户 B：AI Agent 开发者
- **特征**：开发多 Agent 框架（如 AutoGPT、CrewAI 变种），需要让 Agent 具备真实经济能力
- **痛点**：现有框架只能"模拟"交易，无法在生产环境中让 Agent 自主支付
- **使用场景**：将 OPC Agent Treasury 作为支付中间件接入自己的 Agent 框架，通过 API 调用完成真实链上结算

#### 用户 C：去中心化服务提供商
- **特征**：提供 AI 推理、内容生成、算力租赁等 x402 兼容服务
- **痛点**：传统 API Key 模式需要人类预注册，无法服务自主 Agent
- **使用场景**：部署 x402 Paywall，接收来自 CAW 钱包的 Agent 支付，无需人类干预

### 3.2 市场估算（TAM/SAM/SOM）

| 层级 | 定义 | 规模 |
|---|---|---|
| **TAM** | 全球 freelancer + AI 工具用户中可能采用 Agent 支付 | ~50M 人，$10B+ 年度微观支付 |
| **SAM** | 已使用 3+ AI Agent 的 OPC / 小团队 | ~5M 人，$1B+ 年度支付 |
| **SOM** | 早期采用者（Crypto-native OPC + AI Agent 开发者） | ~50K 人，$10M+ 首年 |

### 3.3 竞品分析

| 竞品 | 类型 | 优势 | 劣势 | 与我们的差异 |
|---|---|---|---|---|
| **Brex / Ramp** | 传统企业卡 | 成熟、合规 | 需要美国实体、人类员工、KYC | 我们为 AI Agent 设计，无需人类身份 |
| **Safe** | 多签钱包 | 去中心化、安全 | 每笔需签名，不适合高频小额 | 我们策略自动化，签名前自动校验 |
| **Coinbase Commerce** | 加密支付 | 品牌、流动性 | 面向人类消费者，无 Agent 策略 | 我们有 Agent 原生预算控制 |
| **Crossmint / Privy** | 嵌入式钱包 | 易集成 | 无精细化策略引擎 | 我们的 Pact 策略是核心，非附属 |
| **Turnkey / Dynamic** | 钱包基础设施 | 技术先进 | 需自建策略层 | 我们提供开箱即用的 Agent 财务策略 |

**核心差异**：我们是唯一将「Agent 身份（ERC-8004）+ 预算策略（CAW Pact）+ 审计合规」三者整合为完整财务操作系统的方案。

---

## 4. 技术实现（Technical Implementation）

### 4.1 技术架构（4 层协议栈）

```
┌───────────────────────────────────────────────────────┐
│  场景层（Scenario）                                      │
│  Agent 购买什么：AI 推理、内容生成、广告充值、外包付款    │
├───────────────────────────────────────────────────────┤
│  流程层（Flow）                                          │
│  x402 协议：发现 → 报价 → 402 握手 → 支付 → 服务 → 交付    │
│  ERC-8183：Escrow 托管 → 验收/驳回 → 仲裁 → 释放/退款     │
├───────────────────────────────────────────────────────┤
│  验证层（Verification）                                   │
│  自动：交付物哈希、违禁词扫描                             │
│  人工：调性、创意、品牌匹配                               │
│  仲裁：Evaluator Agent 或超时自动退款                     │
├───────────────────────────────────────────────────────┤
│  协议层（Protocol）                                       │
│  CAW Pact：预算 + 权限 + 审计                             │
│  ERC-8004：Agent 身份 + 声誉评分                          │
│  EIP-712：类型化数据签名（AgentWalletSet）                │
│  Base：USDC 结算层                                        │
└───────────────────────────────────────────────────────┘
```

### 4.2 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     前端层（React + Vite）                │
│  Dashboard / Cards / Agent Console / Attack Lab / Audit │
│  Recharts 可视化 + i18n 多语言 + Tailwind 样式            │
├─────────────────────────────────────────────────────────┤
│                     后端层（FastAPI）                     │
│  REST API: /cards /payments /attacks /audit /dashboard    │
│  Pydantic 数据校验 + CORS + 自动文档（OpenAPI）           │
├─────────────────────────────────────────────────────────┤
│                  CAW 客户端层（Factory 模式）              │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │ Mock Mode    │  │ Real Mode    │                     │
│  │ 零外部依赖   │  │ Cobo SDK     │                     │
│  │ 本地模拟     │  │ 0.1.40       │                     │
│  │ 即时审批     │  │ App 审批     │                     │
│  └──────────────┘  └──────────────┘                     │
├─────────────────────────────────────────────────────────┤
│                  CAW 服务层（云端 MPC-TSS）                │
│  Pact 创建 → 策略绑定 → 签名授权 → 链上结算 → 审计日志     │
├─────────────────────────────────────────────────────────┤
│                     链层（Base / Base Sepolia）           │
│  USDC 转账 + 智能合约交互 + 不可变日志                    │
└─────────────────────────────────────────────────────────┘
```

### 4.3 核心模块说明

#### 模块 1：CAW Factory（`src/caw_factory.py`）
- 根据环境变量 `CAW_MODE` 自动返回 Mock 或 Real 客户端
- 统一接口，业务代码零改动切换模式

#### 模块 2：MockCAWClient（`src/mock_caw_client.py`）
- 纯 Python 标准库实现，零依赖
- 模拟 Pact 生命周期、Policy Engine、Transfer、Audit
- 用于 Demo、CI、快速开发

#### 模块 3：RealCAWClient（`src/real_caw_client.py`）
- 基于 `cobo-agentic-wallet==0.1.40` 的同步封装
- 处理异步 SDK 在同步 FastAPI 中的兼容问题（nest-asyncio）
- 本地状态缓存补充 CAW list_pacts 可能缺失的元数据
- 完整的 EIP-712 策略绑定（ERC-8004 Identity Registry）

#### 模块 4：Agent Runtime（`src/content_agent.py`）
- Content Agent、Ad Agent 业务逻辑封装
- 封装 `onboard()`（创建 Pact）和 `purchase()`（提交支付）
- 自动处理 402 响应、重试、Receipt 验证

#### 模块 5：Threat Simulator（`src/threat_simulator.py`）
- 5 种攻击场景的可执行脚本
- 每种攻击产生确定性输出，可直接嵌入 Demo 视频

#### 模块 6：Audit Reporter（`src/audit_reporter.py`）
- 生成 Markdown / CSV 格式的月度审计报表
- 包含预算 burn-down、异常标记、供应商汇总

#### 模块 7：A2A Coordinator（`src/a2a_agent.py`）
- 跨 Agent 预算调度：将内容 Agent 的剩余预算补充给广告 Agent
- 所有调度操作重新经过 Policy Engine 校验

### 4.4 使用的技术栈

| 层级 | 技术 | 版本 | 作用 |
|---|---|---|---|
| **区块链** | Cobo CAW SDK | 0.1.40 | MPC-TSS 钱包、Pact 管理、链上转账 |
| **区块链** | Base / Base Sepolia | — | L2 结算层，低 Gas、高速度 |
| **代币** | USDC (Base) | — | 稳定币计价单位 |
| **协议** | x402 | — | Agent 原生 HTTP 支付握手 |
| **协议** | ERC-8004 | — | Agent 身份与声誉注册 |
| **协议** | ERC-8183 | — | Escrow + 评估器框架 |
| **协议** | EIP-712 | — | 类型化数据签名 |
| **后端** | Python | 3.10+ | 核心运行时 |
| **后端** | FastAPI | latest | REST API 框架 |
| **后端** | Pydantic | v2 | 数据校验与序列化 |
| **后端** | Uvicorn | latest | ASGI 服务器 |
| **前端** | React | 19.2.6 | UI 框架 |
| **前端** | TypeScript | ~6.0.2 | 类型安全 |
| **前端** | Vite | 8.0.12 | 构建工具 |
| **前端** | Tailwind CSS | 3.4.19 | 样式系统 |
| **前端** | Recharts | 3.8.1 | 数据可视化 |
| **前端** | i18next | 26.3.1 | 国际化（中英） |
| **演示** | Streamlit | — | 快速交互式 Dashboard |
| **AI** | Claude / GPT-4 | — | 架构设计、代码生成、文档 |

### 4.5 安全设计（纵深防御）

1. **零信任 Agent**：所有支付校验在 CAW 服务端完成，不依赖 Agent 端的"善意"
2. **最小权限**：每张 Pact 仅授予必要预算和供应商范围，默认拒绝一切
3. **MPC 安全**：私钥分片存储，Agent 永远无法获取完整私钥
4. **Fail-Closed**：策略模糊时默认拒绝，宁可误杀不可漏放
5. **多层审计**：CAW 服务端日志 + 本地 Merkle 树 + 可选链上存证

---

## 5. 当前完成度（Current Progress）

### 5.1 功能完成状态

| 模块 | 功能 | 状态 | 证据文件 |
|---|---|---|---|
| **核心协议** | CAW Pact 创建与生命周期 | ✅ 完成 | `src/caw_factory.py` |
| **核心协议** | Mock 模式（零依赖） | ✅ 完成 | `src/mock_caw_client.py` |
| **核心协议** | Real 模式（SDK 对接） | ✅ 完成 | `src/real_caw_client.py` |
| **核心协议** | 5 阶段 Policy Engine | ✅ 完成 | `src/mock_caw_client.py` |
| **Agent 运行时** | Content Agent 业务逻辑 | ✅ 完成 | `src/content_agent.py` |
| **Agent 运行时** | Ad Agent 业务逻辑 | ✅ 完成 | `src/content_agent.py` |
| **Agent 运行时** | A2A Coordinator 跨 Agent 调度 | ✅ 完成 | `src/a2a_agent.py` |
| **安全** | 5 种攻击场景演示 | ✅ 完成 | `src/threat_simulator.py` |
| **安全** | 8 种攻击威胁模型文档 | ✅ 完成 | `docs/03-attack-matrix.md` |
| **审计** | 月度 Markdown 报表生成 | ✅ 完成 | `src/audit_reporter.py` |
| **后端** | FastAPI REST API | ✅ 完成 | `backend/main.py` |
| **后端** | Pydantic 数据模型 | ✅ 完成 | `backend/models.py` |
| **后端** | 服务注册表（x402/ERC-8004） | ✅ 完成 | `backend/service_registry.py` |
| **前端** | Dashboard（预算总览 + 图表） | ✅ 完成 | `web/src/pages/Dashboard.tsx` |
| **前端** | Cards（Pact 管理 + 审批） | ✅ 完成 | `web/src/pages/Cards.tsx` |
| **前端** | Agent Console（采购模拟） | ✅ 完成 | `web/src/pages/AgentConsole.tsx` |
| **前端** | Attack Lab（攻击演示） | ✅ 完成 | `web/src/pages/AttackDemo.tsx` |
| **前端** | Audit Report（交易审计） | ✅ 完成 | `web/src/pages/AuditReport.tsx` |
| **演示** | Streamlit Dashboard | ✅ 完成 | `src/app.py` |
| **演示** | CLI 一键 Demo（4 种模式） | ✅ 完成 | `src/run_demo.py` |
| **测试** | 单元测试（Cards/Assignments） | ✅ 完成 | `tests/` |
| **文档** | 12 篇技术文档 + 1 份 SOP | ✅ 完成 | `docs/` |
| **真实验证** | 测试网钱包创建 | ✅ 完成 | Wallet: `ad7f3253...` |
| **真实验证** | 测试网转账成功 | ✅ 完成 | Tx: `0x1a119f1b...` |
| **真实验证** | 真实 Pact 创建与激活 | ✅ 完成 | Pact: `13328473...` |
| **演示视频** | 3~5 分钟 Demo 视频 | ⏳ 待录制 | `demo/video/` |

### 5.2 测试网验证证据

| 验证项 | 详情 | 状态 |
|---|---|---|
| **CAW Wallet** | `ad7f3253-4a3b-48a0-9d09-9bb59d334390` | ✅ 已创建 |
| **ETH 地址** | `0x0abd808e6df088b9b97179a091582618586d0bdc` | ✅ 已激活 |
| **Base Sepolia 转账** | `0x1a119f1b1bf5ffdb9f2dc4bea392d5d489807aa97925c1949199f7ea91c9dddd` | ✅ 成功（0.001 SETH） |
| **Pact 实例** | `13328473-3868-4f45-a35e-ae2a8a1e1ea4` | ✅ 已激活 |
| **Pact 策略** | BASE_USDC，$50/tx，$500/month | ✅ 已绑定 |
| **SDK 版本** | `cobo-agentic-wallet==0.1.40` | ✅ 已验证 |

### 5.3 代码统计

| 指标 | 数量 |
|---|---|
| Python 代码行数 | ~4,000 行 |
| TypeScript/TSX 代码行数 | ~3,500 行 |
| 技术文档 | 12 篇（~30,000 字） |
| 测试用例 | 3 组 API 测试 |
| 可运行 Demo 模式 | 4 种（normal / attack / full / a2a） |
| 攻击场景覆盖 | 5 种可执行 + 8 种文档 |

---

## 6. 后续计划与路线图（Roadmap）

### 6.1 黑客松提交前（2026-06-12 前）

| 任务 | 优先级 | 截止日期 | 状态 |
|---|---|---|---|
| Demo 视频录制（3~5 分钟） | P0 | 2026-06-11 | 脚本已定，待录制 |
| 最终提交物检查 | P0 | 2026-06-11 | 清单已建立 |
| 官方平台提交 | P0 | 2026-06-12 | 等待提交通道开放 |

### 6.2 黑客松后（Post-Hackathon）

#### Phase 1：产品化（1~2 个月）

| 目标 | 具体任务 | 里程碑 |
|---|---|---|
| **主网就绪** | 从 Base Sepolia 迁移到 Base 主网 | 真实 USDC 支付 |
| **多链支持** | 支持 Arbitrum、Optimism 等 L2 | 降低 Gas 成本 |
| **真实供应商集成** | 对接 OpenAI、Midjourney 的 x402 接口 | Agent 可直接购买服务 |
| **移动端 App** | 开发 CAW 配套的极简审批 App | 老板可随时随地吊销卡片 |

#### Phase 2：生态扩展（2~4 个月）

| 目标 | 具体任务 | 里程碑 |
|---|---|---|
| **Agent 市场** | 建立 ERC-8004 声誉市场，Agent 可互相雇佣 | 服务方 Agent 可被发现和信任 |
| **SDK 发布** | 将 OPC Agent Treasury 封装为 pip/npm 包 | 第三方 Agent 框架可接入 |
| **合规框架** | 与 CPA/会计工具集成，自动生成税务报表 | 满足 OPC 合规需求 |
| **保险层** | 引入参数保险，覆盖极端情况下的资金损失 | 降低用户心理门槛 |

#### Phase 3：协议层（4~6 个月）

| 目标 | 具体任务 | 里程碑 |
|---|---|---|
| **标准提案** | 将 Pact 策略规范提交为 ERC 草案 | 行业标准化 |
| **跨钱包兼容** | 支持 Safe、Turnkey 等其他钱包的 Pact 标准 | 扩大生态 |
| **DAO 治理** | 将策略模板和费率参数交给社区治理 | 去中心化升级 |

### 6.3 商业路径

| 阶段 | 模式 | 收入来源 |
|---|---|---|
| **现在** | 开源工具 + 黑客松奖金 | 资助、奖金、社区捐赠 |
| **短期** | SaaS 订阅（Dashboard + 高级策略） | $20~$100/月/OPC |
| **中期** | 交易手续费（每笔 Agent 支付抽成 0.1%） | 规模效应 |
| **长期** | 协议层代币（治理 + 质押） | 生态价值捕获 |

---

## 7. 团队（Team）

| 角色 | 身份 | 核心贡献 |
|---|---|---|
| **创始人 & 全栈开发者** | Neo（NeoWeb3Nova） | 架构设计、协议研究、后端开发、前端开发、威胁模型、文档撰写、Demo 制作 |
| **AI 协作者** | Claude / GPT-4 | 并行代码生成、架构评审、文档起草、调试辅助 |

### 7.1 为什么一个人能完成

- **AI 编码助手**：使用 Claude 和 GPT-4 并行开发，相当于 3~4 名开发者的产出
- **领域聚焦**：2 周时间内只聚焦一个核心问题（Agent 支付），不做无关功能
- **深度研究**：提前完成 CAW 深度调研报告（39KB），开发时直接引用，不重复踩坑
- **快速迭代**：Mock 模式允许零外部依赖开发，真实 SDK 对接并行验证

### 7.2 需要补充的能力

| 能力 | 当前状态 | 需求 |
|---|---|---|
| 智能合约审计 | 无 | 主网上线前需第三方审计 |
| 法律合规 | 无 | 涉及资金业务，需合规顾问 |
| 市场推广 | 无 | 产品化后需增长黑客 |
| 设计师 | 无 | 前端目前为工程师风格，需 UI/UX 升级 |

---

## 8. 为什么是我们（Why Us）

### 8.1 协议理解的深度

- **x402 协议跟踪**：从 Coinbase 提出概念到正式发布，全程跟踪，理解为什么 HTTP 402 是 Agent 支付的正确协议层
- **CAW 深度研究**：产出 39KB 调研报告，覆盖 MPC-TSS 架构、Agent-Owner 配对模型、Pact 四层接入架构
- **ERC-8004/8183 理解**：不仅知道协议存在，更知道如何与 CAW Pact 结合形成完整闭环

### 8.2 安全思维的深度

- **8 种攻击场景**：不是拍脑袋想的，而是基于真实 Agent 安全事件和区块链攻击向量系统推导
- **可执行威胁模型**：每种攻击都有 Python 脚本，评委可以 `python threat_simulator.py` 亲自验证
- **Fail-Closed 设计**：系统默认拒绝，这是金融安全系统的设计黄金法则

### 8.3 执行能力的证明

- **2 周交付**：从概念到可运行代码到真实测试网交易，2 周内完成
- **全栈覆盖**：协议层（x402/ERC-8004）→ 智能合约层（CAW Pact）→ 后端（FastAPI）→ 前端（React）→ 演示（Streamlit/CLI）→ 文档（12 篇）
- **真实验证**：不是 Mock 宣称，而是有真实测试网交易哈希和 Pact ID 作为证据

### 8.4 时机（Timing）

- **x402 刚发布**：2025 年 6 月 Coinbase 正式提出，Agent 支付标准处于早期
- **AI Agent 爆发**：2024-2025 年 Agent 框架（AutoGPT、CrewAI、LangChain）快速成熟，但支付基础设施滞后 6~12 个月
- **OPC 趋势**：一人公司正在成为主流工作模式，但金融工具没有跟上

**我们是第一批将「Agent 经济」从概念推进到可运行基础设施的团队。**

---

## 9. 提交物清单（Submission Checklist）

根据 [AI × Web3 Agentic Builders Hackathon 规则](https://casualhackathon.com/hackathons/cmpsjubkg0003p80kxuzrdyjy)：

- [x] **GitHub Repo** — 代码完整，README 专业
- [x] **README & 项目说明文档** — 本 Proposal + `README.md` + `docs/` 12 篇
- [x] **Demo 视频** — 3~5 分钟，覆盖正常流 + 攻击演示 + 审计（待录制）
- [x] **项目演示链接** — Streamlit + FastAPI + React 均可运行
- [x] **CAW 关键代码** — `src/real_caw_client.py` + `docs/CAW-REAL-MODE-SOP.md`
- [x] **测试网地址** — `0x0abd...0bdc`（Base Sepolia）
- [x] **Transaction Hash** — `0x1a119f...9dddd`
- [x] **Agent Wallet 地址** — `ad7f3253...`（CAW Wallet UUID）
- [x] **流程截图** — `demo/screenshots/`
- [x] **Sprint 看板** — `docs/02-sprint-tracker.md`

---

> **核心信念**：当 AI Agent 成为经济活动的参与者时，它们需要的不是人类的银行账号，而是属于自己的、受控的、可审计的财务身份。OPC Agent Treasury 是这个未来的基础设施。
