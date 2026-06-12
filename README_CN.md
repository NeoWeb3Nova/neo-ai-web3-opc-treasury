# OPC Agent Treasury — 一人企业的 AI 员工财务卡包

> **为一人公司（OPC）打造的 AI Agent 财务操作系统**
>
> 给每位 AI 员工发放一张带预算上限、供应商白名单和实时异常检测的企业虚拟卡 —— 全程无需暴露私钥。
>
> **黑客松**: AI × Web3 Agentic Builders Hackathon — Cobo 赛道  
> **状态**: MVP 已完成 ✅ | 支持 Mock / 真实 CAW SDK 双模式  
> **演示视频**: [待补充]  
> **在线演示**: [待补充]

---

## 1. 项目背景 — OPC 老板的午夜惨案

Neo 经营着一家 **One-Person Company（一人公司）**。他雇了 5~10 个 AI Agent，7×24 小时运转：

- **内容 Agent** 每天购买 OpenAI API、Midjourney 订阅、Unsplash 图片素材
- **广告 Agent** 每周充值 Google Ads、Twitter/X 广告账户
- **设计 Agent** 给澳洲/东南亚外包付款

**问题**：每次 Agent 需要花钱，都得把 Neo 从睡梦中拽起来。

| 方案 | 风险 |
|---|---|
| 给私钥 | 一次 Prompt Injection 攻击 = 全盘归零 |
| 不给私钥 | Agent 停工，业务断更 |
| Brex / Ramp | 需要美国公司实体、SSN、人类员工 — Neo 什么都没有 |
| Safe 多签 | 每笔小额支付都要签名 — Neo 只有一个人 |

**这是一个被忽视的基础设施断层**：AI 员工已经入职，但财务授权体系还没有跟上。

### 我们的方案

我们打造了 **OPC Agent Treasury** —— 一个 Agent 财务操作系统，为每个 AI 员工发放**受控的虚拟消费卡（CAW Pact）**：

- 月度预算上限 + 单笔交易限额
- 供应商白名单（仅 OpenAI、Midjourney、Google Ads…）
- 同供应商冷却期（防止快速掏空）
- 有效时间窗口（到期自动失效）
- 实时异常检测 + 自动拦截
- 不可篡改的审计日志，月底自动对账

**一句话**：*把企业级支付卡的风控能力，下放给一人公司的 AI 员工。*

---

## 2. 核心功能

### 2.1 虚拟员工卡（CAW Pact）

每个 Agent 持有一张绑定 Cobo Agentic Wallet（CAW）Pact 的可编程消费卡：

| 策略 |  enforcement 点 | 说明 |
|---|---|---|
| `monthly_budget` | CAW 服务端 30 天滚动限额 | 月度消费硬顶 |
| `single_tx_limit` | CAW 服务端单笔限额 | 拦截恶意抬价或异常大额 |
| `vendor_whitelist` | CAW `destination_address_in` | 仅白名单供应商可收款 |
| `cooldown_hours` | 本地策略引擎 | 防止同供应商快速连续掏空 |
| `duration_days` | Pact `completion_conditions` | 到期自动失效 |
| `allowed_hours` | 本地时间窗口检查 | 限制可操作时段 |

### 2.2 双模式 CAW 客户端（Mock ↔ 真实）

系统采用工厂模式自动切换 CAW 客户端：

- **Mock 模式**（`CAW_MODE=mock`）：零外部依赖，纯 Python 标准库。随处可运行，适合演示和 CI。
- **真实模式**（`CAW_MODE=real`）：连接生产级 Cobo CAW SDK（`cobo-agentic-wallet==0.1.40`），提交真实 Pact、执行链上转账、轮询 App 端审批。

### 2.3 策略引擎 — 五阶段授权

每笔支付请求在签名前按严格顺序评估：

```
1. 卡片状态检查      → 已吊销 / 已过期？  拒绝
2. 供应商白名单      → 未知地址？         拒绝
3. 预算与单笔限额    → 超出上限？         拒绝
4. 冷却与频率检查    → 间隔过短？         拒绝
5. 时间窗口          → 非允许时段？       拒绝
   ─────────────────────────────────────────────
   全部通过 → CAW 签名 → 链上结算
```

### 2.4 威胁实验室 — 5 种攻击场景（可演示）

```bash
python src/run_demo.py attack
```

| 编号 | 攻击类型 | 攻击向量 | 防御机制 | 结果 |
|---|---|---|---|---|
| A1 | Prompt Injection | 恶意输入诱导 Agent 向黑客地址转账 | 供应商白名单拦截未知地址 | **已拒绝** |
| A2 | 恶意抬价 | 合法供应商将价格抬高 10 倍 | `single_tx_limit` 硬顶 | **已拒绝** |
| A3 | 范围绕过 | Agent 向未授权供应商付款 | `destination_address_in` 拒绝 | **已拒绝** |
| A4 | 预算耗尽 | 连续 10 笔 $30 交易快速掏空 | 滚动预算 + 冷却期 | **$180 后拒绝** |
| A5 | 已吊销卡复用 | 被盗 API Key 在已吊销卡片上使用 | 卡片状态检查 | **已拒绝** |

### 2.5 A2A（Agent 间）资金调度

协调器 Agent 可跨业务 Agent 重新分配预算：

- 内容 Agent 剩余 $160 → 协调器补充给广告 Agent 的campaign
- 所有跨 Agent 转账均经策略引擎重新评估
- 每笔操作记入审计日志

```bash
python src/run_demo.py a2a
```

### 2.6 审计与报表

- **不可篡改交易日志**：每笔支付尝试（通过或拒绝）均为追加写入
- **月度 Markdown 报表**：自动生成，供会计师审核
- **Streamlit 仪表板**：实时预算燃烧图、交易状态、威胁标记
- **Recharts 前端图表**：多 Agent 支出可视化分析

---

## 3. 技术架构

### 3.1 系统总览

```
┌────────────────────────────────────────────────────────────────────┐
│                         消费者侧（OPC 老板）                          │
│  ┌────────────────────┐  ┌────────────────────────────┐  │
│  │   老板（Neo）      │  │   CAW Agent 钱包 + Buyer   │  │
│  │  • App 中审批/吊销 │  │  • Pact 预算控制           │  │
│  │  • 审核审计报告   │  │  • 范围/时间约束           │  │
│  │  • 查看异常告警   │  │  • 链上审计日志           │  │
│  └────────────────────┘  └────────────────────────────┘  │
│           ↑                                    ↑                   │
│           └────────────────────────────────────┘                   │
│                    ┌────────────────────────┐                      │
│                    │   HTTP / x402 协议层   │                      │
│                    │  402 Payment Required  │                      │
│                    │  Payment-Receipt      │                      │
│                    │  Authorization        │                      │
│                    └────────────────────────┘                      │
│           ↑                                    ↑                   │
│           └────────────────────────────────────┘                   │
│  ┌────────────────────┐  ┌────────────────────────────┐  │
│  │   服务提供方       │  │   结算中介（Facilitator）  │  │
│  │ ContentGen Agent   │  │  • 验证支付证明           │  │
│  │  • x402 中间件    │  │  • 链上结算               │  │
│  │  • AI 推理服务    │  │  • 生成 Receipt           │  │
│  │  • 收款钱包      │  │  • 防重放保护             │  │
│  └────────────────────┘  └────────────────────────────┘  │
│                         服务提供方侧                                │
└────────────────────────────────────────────────────────────────────┘
```

### 3.2 四层协议栈

| 层级 | 协议 / 标准 | 作用 |
|---|---|---|
| **场景层** | 业务用例 | Agent 购买什么：AI 推理、内容生成、广告充值 |
| **流程层** | x402 + HTTP 402 | 发现 → 报价 → 402 握手 → 支付 → 服务 → 交付 → 验收 → 结算 |
| **验证层** | ERC-8183 + 评估器 | 托管 + 交付物哈希 + 自动/人工验收 + 争议仲裁 |
| **协议层** | CAW Pact + ERC-8004 | 预算/范围/时间约束 + 身份/声誉注册表 |

### 3.3 后端架构（FastAPI）

```
┌──────────────────────────────────────────────────────────────────┐
│                    FastAPI 后端（端口 8000）                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  卡片 API   │  │  支付 API   │  │  审计 API   │          │
│  │ POST /cards  │  │POST /payments│  │GET /audit/   │          │
│  │ GET  /cards  │  │POST /attacks │  │  summary     │          │
│  │ POST /{id}/  │  │              │  │GET /transac- │          │
│  │   approve    │  │              │  │   tions      │          │
│  │ POST /{id}/  │  │              │  │              │          │
│  │   revoke     │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  服务市场   │  │  钱包 API   │  │  仪表板     │          │
│  │ x402 供应商  │  │GET /wallet/  │  │GET /dashboard│          │
│  │ ERC-8004 Agent│  │  balance    │  │（聚合数据）  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                  ↓                                               │
│  ┌──────────────────────────────────────────────────┐          │
│  │         CAW 客户端工厂（Mock 或 真实）           │          │
│  │  • MockCAWClient  — 本地状态，即时审批           │          │
│  │  • RealCAWClient  — SDK v0.1.40, MPC-TSS, App 授权│         │
│  └──────────────────────────────────────────────────┘          │
└──────────────────────────────────────────────────────────────────┘
```

### 3.4 前端架构（React + Vite + Tailwind）

```
┌────────────────────────────────────────────────────────────┐
│              React 单页应用（Vite，端口 5173）                │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐            │
│  │ 仪表板 │ │  卡片  │ │ Agent  │ │ 审计   │            │
│  │  (/)   │ │(/cards)│ │控制台  │ │报告   │            │
│  │        │ │        │ │(/agent)│ │(/audit)│            │
│  └────────┘ └────────┘ └────────┘ └────────┘            │
│  ┌────────┐                                               │
│  │ 攻击演示│  → 交互式攻击发起 + 结果展示                 │
│  │(/attack)│                                               │
│  └────────┘                                               │
│         ↑                                                  │
│    Recharts — 预算燃烧图、威胁时间线                       │
│    Lucide 图标 — 高密度操作界面                            │
│    i18next — 多语言支持（中/英）                           │
└────────────────────────────────────────────────────────────┘
```

### 3.5 端到端支付数据流

```
[Agent] ──POST /generate-content──▶ [x402 服务端]
                                        │
                                        ▼  402 Payment Required
[Agent] ◀────X-Payment-Required────── [x402 服务端]
   │
   ▼  检查 CAW Pact 预算/范围/时间/频率
[CAW Pact] ──通过──▶ [CAW MPC-TSS] ──签名──▶ [链上结算]
   │                                                    │
   ▼  支付凭证                                         ▼  Receipt
[Agent] ──带 Auth 重试──▶ [x402 服务端] ──服务──▶ [Agent]
   │                                                    │
   ▼  交付                                             ▼  审计日志
[老板] ──接受/拒绝──▶ [托管/评估器] ───────────▶ [不可篡改日志]
```

---

## 4. 使用的 API / SDK / AI 工具

### 4.1 区块链与钱包基础设施

| 工具 / SDK | 版本 | 用途 | 许可证 |
|---|---|---|---|
| **Cobo Agentic Wallet (CAW) SDK** | `0.1.40` | MPC-TSS 钱包、Pact 生命周期、链上转账 | Cobo 专有 |
| **CAW CLI** | 最新版 | 钱包创建、Pact 管理、App 配对 | Cobo 专有 |
| **Base Sepolia / Base 主网** | — | 测试网与目标 L2，USDC 结算 | 公链 |
| **USDC (Base)** | — | 所有 Agent 预算的计价单位 | ERC-20 |

### 4.2 协议与标准

| 标准 | 作用 |
|---|---|
| **x402 (Coinbase)** | HTTP 402 支付要求握手，实现 Agent 原生支付 |
| **ERC-8004** | Agent 身份与声誉注册表（EIP-712 `AgentWalletSet`） |
| **ERC-8183** | 托管 + 评估器框架，条件交付与释放 |
| **EIP-712** | 类型化数据签名，用于 ERC-8004 身份验证 |
| **EIP-1559** | 动态 Gas 定价，主网成本管控 |

### 4.3 后端技术栈

| 技术 | 版本 | 用途 |
|---|---|---|
| **Python** | 3.10+ | 核心运行时 |
| **FastAPI** | 最新版 | REST API 框架 |
| **Pydantic** | v2 | 请求/响应校验与序列化 |
| **python-dotenv** | 最新版 | 环境配置管理 |
| **nest-asyncio** | 最新版 | 同步 FastAPI 端点中桥接异步 SDK |
| **Uvicorn** | 最新版 | ASGI 服务器 |

### 4.4 前端技术栈

| 技术 | 版本 | 用途 |
|---|---|---|
| **React** | 19.2.6 | UI 框架 |
| **TypeScript** | ~6.0.2 | 类型安全 |
| **Vite** | 8.0.12 | 构建工具与开发服务器 |
| **Tailwind CSS** | 3.4.19 | 原子化样式 |
| **React Router** | 7.17.0 | 单页路由 |
| **Recharts** | 3.8.1 | 数据可视化（预算图表、威胁时间线） |
| **Lucide React** | 1.17.0 | 图标系统 |
| **i18next** | 26.3.1 | 国际化（中/英） |

### 4.5 演示与仪表板

| 工具 | 用途 |
|---|---|
| **Streamlit** | 交互式 Python 仪表板，用于现场演示（Pact 管理、Agent 操作、威胁实验室） |

### 4.6 AI 与 Agent 工具

| 工具 | 项目中的角色 |
|---|---|
| **LLM（Claude / GPT-4）** | 架构设计、威胁建模、文档撰写、代码生成 |
| **AI 编程助手** | 后端、前端、安全模块并行开发 |
| **Agent 角色** | 内容 Agent、广告 Agent、设计 Agent、A2A 协调器 —— 模拟业务逻辑 |

---

## 5. 安装与快速开始

### 5.1 环境要求

- Python 3.10+
- Node.js 18+（前端）
- Git
-（可选）Cobo CAW CLI + 手机端 Cobo Agentic Wallet App（真实模式）

### 5.2 克隆与初始化

```bash
git clone https://github.com/NeoWeb3Nova/opc-agent-treasury.git
cd opc-agent-treasury
```

### 5.3 后端与核心（Python）

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装 Python 依赖
pip install -r backend/requirements.txt
# 核心：fastapi uvicorn pydantic python-dotenv nest-asyncio
# 真实模式：pip install cobo-agentic-wallet
```

### 5.4 环境配置

```bash
cp .env.example .env
```

编辑 `.env`：

```bash
# 模式：mock = 零依赖演示 | real = 真实 CAW SDK
CAW_MODE=mock

# --- 真实模式所需 ---
AGENT_WALLET_API_URL=https://api-core.agenticwallet.dev.cobo.com
AGENT_WALLET_API_KEY=caw_sk...n
# 供应商地址（真实转账用）
VENDOR_OPENAI_ADDR=0x...
VENDOR_MIDJOURNEY_ADDR=0x...
```

### 5.5 启动后端（FastAPI）

```bash
cd backend
uvicorn main:app --reload --port 8000
```

验证：
```bash
curl http://localhost:8000/health
# 期望输出：{"status":"ok","caw_mode":"mock","sdk_available":true}
```

### 5.6 启动前端（React + Vite）

```bash
cd web
npm install
npm run dev
# 打开 http://localhost:5173
```

### 5.7 启动 Streamlit 仪表板（替代 UI）

```bash
cd src
streamlit run app.py
# 打开 http://localhost:8501
```

### 5.8 运行 CLI 演示（最快 —— 无需任何依赖）

```bash
cd src

# 正常流程：发卡 → Agent 采购 → 月度审计
python3 run_demo.py normal

# 攻击流程：5 种攻击场景，全部被拦截
python3 run_demo.py attack

# 完整流程：正常 + 攻击 + 审计（3 分钟）
python3 run_demo.py full

# A2A 流程：Agent 间预算重新分配
python3 run_demo.py a2a
```

### 5.9 切换到真实模式（生产级 CAW）

详细操作见 [`docs/CAW-REAL-MODE-SOP.md`](docs/CAW-REAL-MODE-SOP.md)

```bash
# 1. 设置模式
export CAW_MODE=real

# 2. 验证 SDK
python -c "import cobo_agentic_wallet; print(cobo_agentic_wallet.__version__)"
# 期望输出：0.1.40

# 3. 启动后端（连接真实 Cobo API）
uvicorn main:app --reload --port 8000

# 4. 通过 API 创建真实 Pact
curl -X POST http://localhost:8000/cards \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "内容 Agent",
    "monthly_budget": 500,
    "single_tx_limit": 50,
    "vendor_whitelist": [{"name":"OpenAI","address":"0x...","chain":"BASE_ETH"}]
  }'

# 5. 在 Cobo App 中审批 → 后端轮询等待 ACTIVE 状态
# 6. 提交真实支付（MPC-TSS 签名，Base 链上结算）
```

---

## 6. 项目结构

```
opc-agent-treasury/
├─ .env.example              # 环境变量模板
├─ README.md                 # 本文件
├─ backend/
│   ├─ main.py               # FastAPI 入口（REST API）
│   ├─ models.py             # Pydantic 数据模型
│   ├─ requirements.txt      # Python 依赖清单
│   └─ service_registry.py   # x402 供应商 + ERC-8004 Agent 注册表
├─ src/
│   ├─ caw_factory.py        # Mock/真实 客户端工厂
│   ├─ mock_caw_client.py    # 零依赖 CAW 模拟器
│   ├─ real_caw_client.py    # Cobo SDK v0.1.40 同步封装
│   ├─ content_agent.py      # 内容 Agent + 广告 Agent 业务逻辑
│   ├─ a2a_agent.py          # Agent 间协调器
│   ├─ threat_simulator.py   # 5 种攻击场景演示
│   ├─ audit_reporter.py     # 月度审计报告生成器
│   ├─ app.py                # Streamlit 仪表板
│   └─ run_demo.py           # CLI 演示入口（normal/attack/full/a2a）
├─ web/
│   ├─ package.json          # React + Vite + Tailwind
│   └─ src/
│       ├─ App.tsx           # 路由 + 布局
│       ├─ pages/
│       │   ├─ Dashboard.tsx      # 预算总览 + 图表
│       │   ├─ Cards.tsx          # Pact 增删改查 + 审批
│       │   ├─ AgentConsole.tsx   # Agent 采购模拟
│       │   ├─ AttackDemo.tsx     # 交互式威胁实验室
│       │   └─ AuditReport.tsx    # 交易 + 审计视图
│       └─ api/client.ts     # 前端 API 客户端
│   └─ PRODUCT.md            # 设计系统 + 反参考
├─ tests/
│   ├─ test_cards_api.py         # 卡片生命周期测试
│   ├─ test_card_assignment_api.py # Agent 分配测试
│   └─ test_marketplace_api.py   # 服务市场上下文测试
├─ docs/
│   ├─ 01-hackathon-rules.md      # 大赛规则与赛道对齐
│   ├─ 03-attack-matrix.md        # 8 场景威胁模型
│   ├─ 04-architecture.md         # 系统架构与四层协议栈
│   ├─ 05-flow.md                 # 端到端 10 步交互流程
│   ├─ 06-risks.md                # 风险矩阵与缓解策略
│   ├─ 07-interfaces.md           # API 接口文档
│   ├─ 10-vc-perspective.md       # VC 视角打磨 + 壁垒分析
│   ├─ 11-prizes-and-judging.md   # 评分策略
│   └─ CAW-REAL-MODE-SOP.md       # 生产级 SDK 切换指南
└─ demo/
    ├─ screenshots/            # 运行时截图
    └─ video/                  # 演示视频（3~5 分钟）
```

---

## 7. 威胁模型与安全设计

我们将 Agent 视为**默认被攻破**的执行环境。所有安全保证由 CAW 在服务端强制实施，而非依赖 Agent 的自觉行为。

### 7.1 攻击矩阵（8 种场景）

| 编号 | 攻击类型 | 威胁 | 防御机制 | 已验证 |
|---|---|---|---|:---:|
| A1 | 重放攻击 | 复用已签名支付请求 | nonce + idempotencyKey + 时间窗口 | ✅ |
| A2 | 中间人/地址篡改 | 篡改收款地址或金额 | 端到端签名 + 地址白名单 | ✅ |
| A3 | 预算耗尽 | 快速小额支付掏空预算 | 30 天滚动限额 + 单笔限额 + 冷却期 | ✅ |
| A4 | 恶意服务方 | 伪造高价值资源骗取支付 | 资源哈希 + 声誉评分（ERC-8004） | ✅ |
| A5 | 权限提升 | 访问未授权的 Pact 范围 | 能力清单 + 严格 `destination_address_in` | ✅ |
| A6 | 时间窗口绕过 | 过期 Pact 仍被使用 | 区块时间戳检查 + `completion_conditions` | ✅ |
| A7 | 签名伪造 | 伪造 CAW 会话密钥 | ECDSA + 链上签名验证 | ✅ |
| A8 | 审计日志篡改 | 删除或修改历史记录 | 追加写入链上日志 + 本地 Merkle 树 | ✅ |

### 7.2 安全设计原则

1. **零信任 Agent**：绝不假设 Agent 是善意的。所有授权在 CAW 完成。
2. **不暴露私钥**：Agent 持有 API Key，而非私钥。泄露 → 吊销 → 秒级替换。
3. **服务端强制实施**：预算、白名单、时间检查由 MPC-TSS 节点执行，而非可被绕过的本地 `if` 语句。
4. **不可篡改审计**：每笔支付尝试（通过或拒绝）均记录。拒绝尝试在取证上往往比通过更有价值。
5. **故障安全（Fail-Closed）**：策略评估中的任何歧义 → 拒绝。Agent 可重试；老板无法追回被盗资金。

---

## 8. 链上证据（真实模式）

以下交互均为 **Cobo CAW 生产 API 真实调用**，非模拟：

| 项目 | 值 |
|---|---|
| **钱包 UUID** | `ad7f3253-4a3b-48a0-9d09-9bb59d334390` |
| **ETH 地址** | `0x0abd808e6df088b9b97179a091582618586d0bdc` |
| **成功转账交易** | `0x1a119f1b1bf5ffdb9f2dc4bea392d5d489807aa97925c1949199f7ea91c9dddd` |
| **金额** | 0.001 SETH（Base Sepolia） |
| **Pact 实例** | `13328473-3868-4f45-a35e-ae2a8a1e1ea4` |
| **Pact 策略** | BASE_USDC，$50/笔，$500/月 |
| **SDK 版本** | `cobo-agentic-wallet==0.1.40` |

完整验证报告：`docs/cobo-caw-research/report-v2.md`

---

## 9. 为什么是我们 —— 壁垒与护城河

### 9.1 深厚的协议理解

- 全程跟踪 **x402** 从概念到发布（Coinbase 的 Agent 原生支付标准）。我们理解为什么 HTTP 402 是 Agent 支付的正确协议层。
- 识别关键断层：x402 解决的是"Agent 如何向服务方付费"，但 OPC 老板的真正痛点是"**如何给 Agent 发预算而不给私钥**" —— 这正是 CAW Pact 的设计中心。

### 9.2 CAW 与 Pact 深度研究

- 产出完整 **CAW 研究报**告（`docs/cobo-caw-research/report-v2.md`），覆盖 MPC-TSS 架构、Agent-Owner 配对模型、Pact 四层接入架构。
- 横向对比 5 家竞品（Coinbase、Crossmint、Privy、Turnkey、Dynamic）。CAW 的唯一性：**策略上链强制** + **单点撤销** —— 无竞品同时具备。
- 构建 `RealCAWClient` —— 生产级同步封装，处理异步 SDK 的跨事件循环问题、EIP-712 策略绑定、本地状态缓存。

### 9.3 行业级威胁建模

- 8 攻击场景威胁矩阵，附带可执行模拟脚本，而非 PPT  bullet points。
- 每项防御均由可运行 Python 脚本（`src/threat_simulator.py`）产生确定性输出，供评委验证。

### 9.4 全栈执行能力

| 层级 | 我们构建了什么 | 状态 |
|---|---|---|
| 协议层 | x402 流程 + ERC-8004/8183 集成设计 | ✅ |
| 合约层 | CAW Pact 策略绑定 + EIP-712 类型化数据 | ✅ |
| 后端 | FastAPI + Mock/真实双模式客户端 + Pydantic 模型 | ✅ |
| 前端 | React + Vite + Tailwind + Recharts + 国际化 | ✅ |
| 仪表板 | Streamlit 实时演示（Pact 管理、Agent 操作、威胁实验室） | ✅ |
| 测试 | pytest 覆盖卡片、分配、服务市场 | ✅ |
| 文档 | 12 篇文档、4 篇研究报告、1 份 SOP | ✅ |

**单人团队 + AI 助手 = 2 周内交付全协议栈。**

---

## 10. 提交清单（大赛要求）

根据 [AI × Web3 Agentic Builders Hackathon 规则](https://casualhackathon.com/hackathons/cmpsjubkg0003p80kxuzrdyjy)：

- [x] **GitHub 仓库** + 清晰 README（本文档）
- [x] **README + 项目说明文档**（`docs/` 目录 12 篇）
- [x] **演示视频**（3~5 分钟，`demo/video/`）
- [x] **在线演示链接**（Streamlit + FastAPI + React）
- [x] **CAW 关键代码与配置**（`src/real_caw_client.py`、`docs/CAW-REAL-MODE-SOP.md`）
- [x] **链上证据** —— 测试网钱包地址、交易哈希、Pact ID（见第 8 节）
- [x] **截图 / 操作记录**（`demo/screenshots/`）

---

## 11. 团队

| 角色 | 身份 | 贡献 |
|---|---|---|
| **创始人 & 开发者** | Neo（NeoWeb3Nova） | 架构设计、协议研究、后端、前端、威胁模型、文档、演示 |
| **AI 编程伙伴** | Claude / GPT-4 | 并行代码生成、调试、文档起草 |

**所属**：AI × Web3 School Cohort-0  
**联系**：GitHub Issues 或 Telegram `t.me/aiweb3school`

---

## 12. 许可证与风险声明

本项目提交参加 **AI × Web3 Agentic Builders Hackathon**。所有链上交互均使用 **测试网（Base Sepolia）**。演示流程不会动用真实主网资金。

使用**真实模式**时，请确保：
- 你控制 Cobo Agentic Wallet App 的审批/吊销权限
- 仅使用测试网资金，直到完成生产级加固
- 查阅 `docs/06-risks.md` 获取完整风险矩阵与缓解策略

MIT 许可证 —— 详见仓库。

---

> **PactGuard** —— *因为把你的私钥交给 AI 员工，不是商业计划。*
