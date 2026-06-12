# OPC Agent Treasury — Demo 链接与 3-5 分钟演示视频口播稿

> 建议时长：4 分 20 秒左右  
> 录制方式：屏幕录制 + 旁白  
> 推荐演示模式：`CAW_MODE=mock`，确保评委无需外部凭证即可完整复现  
> 目标：让评委在 5 分钟内看懂“问题真实、CAW 是核心、流程能跑、安全边界清楚”。

---

## 0. Demo 链接说明

如果提交平台要求填写 Demo Link，当前最稳妥的写法：

```text
Local runnable demo:
Frontend: http://localhost:5173
Backend API: http://localhost:8000
Backend Docs: http://localhost:8000/docs
Streamlit optional demo: http://localhost:8501

Default mode: CAW_MODE=mock, no private key or external credential required.
Real CAW mode is documented in docs/CAW-REAL-MODE-SOP.md with verified wallet/Pact/testnet evidence.
```

如果最终有线上部署，再把上面的本地链接替换成线上 URL；没有线上部署时，不要伪造 live demo link，直接写 “Local runnable demo”。

---

## 1. 录制前准备

### 1.1 启动后端

```bash
source .venv/bin/activate
cd backend
CAW_MODE=mock uvicorn main:app --reload --port 8000
```

检查：

```bash
curl http://localhost:8000/health
```

预期看到：

```json
{"status":"ok","caw_mode":"mock", ...}
```

### 1.2 启动前端

```bash
cd web
npm run dev
```

打开：

```text
http://localhost:5173
```

### 1.3 建议录制浏览器页面顺序

1. Dashboard：总览当前 Treasury 状态。
2. Cards：创建/展示 AI 员工支出卡。
3. Agent Console：AI 员工使用已分配卡片付款。
4. Attack Demo：展示攻击被拦截。
5. Audit Report：展示交易、拒绝原因、审计闭环。
6. README/Proposal 或终端：展示 Real CAW 证据和测试结果。

---

## 2. 4 分 20 秒版本口播稿

### 0:00 - 0:25 开场：一句话痛点

画面：Dashboard 或项目首页。

口播：

大家好，我是 Neo。这个项目叫 OPC Agent Treasury，是给一人公司的 AI 员工使用的财务操作系统。

今天 AI Agent 已经可以帮一个 solo founder 做研究、买数据、跑广告、调用 API，但只要它需要花钱，就会遇到一个很危险的二选一：

要么每一笔都叫醒老板审批，自动化失效；要么把钱包私钥或 API Key 交给 Agent，一次 Prompt Injection 就可能把钱花到攻击者地址。

OPC Agent Treasury 解决的是中间这一层：让 AI Agent 能花钱，但只能在老板预先授权的预算、供应商和策略范围内花钱。

---

### 0:25 - 0:55 解决方案：AI 员工支出卡

画面：切到 Cards 页面，展示卡片列表或创建卡片区域。

口播：

我们的核心设计很简单：给每个 AI Agent 发一张可编程的支出卡。

这张卡在底层对应 Cobo Agentic Wallet 的 Pact。老板可以设置月度预算、单笔限额、供应商白名单、有效期和冷却期。Agent 不会拿到私钥，也不能自己改规则。

所以这里的 CAW 不是登录组件，也不是普通钱包按钮。CAW Pact 是整个系统的风控核心：Pact 定义权限，CAW Policy Engine 在付款前执行边界，MPC 钱包负责保护私钥。

---

### 0:55 - 1:35 核心流程 1：创建并审批一张 AI 员工卡

画面：Cards 页面。演示创建一张卡，或展示已有 Active 卡。

建议操作：

- 点击 New Card / Create Card。
- 名称可用：`Vega Research Agent Card`。
- Budget：`300`。
- Single tx limit：`40`。
- Vendors：选择 `BlockRun AI Gateway` 或 `StableEnrich`。
- 创建后展示 Pending / Active 状态。
- 如果是 Mock 模式，可点击 Approve。

口播：

这里我给 Vega Research Agent 创建一张研究预算卡。

这张卡的月预算是 300 USDC，单笔最多 40 USDC，只能支付白名单里的 x402 服务。真实 CAW 模式下，这一步会提交一个 CAW Pact，并需要老板在 Cobo App 里审批；在今天的演示里，我使用 Mock 模式，让评委可以不依赖外部 App 和测试网状态完整跑通流程。

审批后，这张卡变成 Active。下一步，它必须被分配给一个具体的数字员工，不能成为所有 Agent 共用的万能付款凭证。

---

### 1:35 - 2:20 核心流程 2：Agent Console 发起一次合法支付

画面：Agent Console 页面。

建议操作：

- 选择 Vega Research Agent。
- 选择刚才的 Active Card。
- 如果页面支持 assignment，先 Assign card。
- Vendor 选择卡片白名单里的 provider。
- Amount 输入 `1` 或 `5`。
- Purpose 输入 `x402 research data request`。
- 点击 Submit Payment。
- 展示 APPROVED 和各阶段检查通过。

口播：

现在进入 Agent Console。假设 Vega 需要购买一次研究数据 API，它会提交一个付款请求。

系统会先检查：这张卡是不是 Active；这张卡是不是分配给 Vega；供应商是不是在白名单里；金额有没有超过单笔和月度预算；有没有违反冷却期。

如果是在 Real CAW 模式下，最后还会带上 pact_id、src_addr、dst_addr、token_id、chain_id 和 request_id，通过 Pact-scoped API Key 交给 CAW 做最终的转账权限校验。

这里可以看到，这笔请求通过了所有检查，状态是 Approved。关键点是：Agent 完成了付款动作，但从头到尾没有接触私钥，也没有拿到无限钱包权限。

---

### 2:20 - 3:05 核心流程 3：攻击演示 — Prompt Injection / 越权支付被拦截

画面：Attack Demo 页面。

建议操作：

- 选择一张 Active 且已分配的卡。
- 运行 A1 或 A2：
  - A1：Prompt injection sends funds to attacker address。
  - A2：Legitimate vendor inflates price。
- 展示 DENIED、failed stage、failed checks。

口播：

真正重要的不是正常支付能通过，而是被攻击时系统会不会 fail closed。

这里我运行一个典型攻击：Agent 被 Prompt Injection 诱导，把钱打到攻击者地址，或者把金额提高到远超单笔限额。

可以看到交易被拒绝了。拒绝原因不是前端写死的提示，而是来自后端策略检查：可能是 scope_denied、per_tx_exceeded、agent_not_assigned，或者 cooldown_violation。

这说明系统不相信 Agent 自己会永远诚实。它默认把 Agent 当成可能被攻破的执行环境，把真正的资金边界放在 Card/Pact 和 CAW Policy 层。

---

### 3:05 - 3:35 审计闭环：老板月底能复盘

画面：Audit Report 页面。

建议操作：

- 展示 approved / denied 交易。
- 展示 denied reason、agent、vendor、amount。
- 展示 summary 或 anomaly 区域。

口播：

所有通过和被拒绝的请求都会进入审计记录。

这对一人公司很关键。老板不需要实时盯着每一笔小额支付，但月底必须能回答三个问题：哪个 Agent 花了钱，花给谁，为什么有些请求被拒绝。

所以 OPC Agent Treasury 不只是支付按钮，它也是 Agent 财务审计层。被拦截的攻击不是噪音，而是风险证据。

---

### 3:35 - 4:00 Real CAW 证据：不是纯 Mock

画面：README 的 Verified CAW / On-Chain Evidence 区域，或 PROPOSAL 当前完成度区域。

口播：

为了保证演示稳定，默认 Demo 使用 Mock 模式。但项目已经实现了 Real CAW 客户端，并保留了真实验证记录。

这里包括 CAW Wallet UUID、钱包地址、Base Sepolia 测试交易哈希、已激活的 Pact ID，以及 cobo-agentic-wallet SDK 0.1.40 的对接代码。

Real 模式的操作 SOP 在 `docs/CAW-REAL-MODE-SOP.md`，核心代码在 `src/real_caw_client.py`。

---

### 4:00 - 4:20 收尾：为什么这个项目重要

画面：回到 Dashboard 或 README 顶部。

口播：

总结一下，OPC Agent Treasury 解决的不是“怎么让 AI 自动点付款”，而是更底层的问题：AI Agent 如何在真实商业里拥有受控、可撤销、可审计的资金权限。

未来的一人公司会有很多 AI 员工。它们不应该拥有无限钱包，而应该拥有像企业卡一样的策略化支出权限。

这就是 OPC Agent Treasury：AI 员工的财务卡包，也是 Agentic Economy 进入真实支付场景前必须补上的安全层。谢谢。

---

## 3. 3 分钟压缩版口播稿

如果提交平台限制更严格，可以使用这个版本。

### 0:00 - 0:20

OPC Agent Treasury 是给一人公司 AI 员工使用的财务操作系统。今天 Agent 可以帮老板做研究、买数据、跑广告，但一旦涉及付款，要么每笔都人工审批，要么把私钥交给 Agent。前者牺牲自动化，后者非常危险。

### 0:20 - 0:50

我们的方案是：给每个 AI Agent 发一张可编程支出卡。底层使用 Cobo Agentic Wallet Pact，老板设置预算、单笔限额、供应商白名单、有效期和冷却期。Agent 可以在授权范围内支付，但永远不能接触私钥，也不能修改自己的规则。

### 0:50 - 1:30

这里我在 Cards 页面创建一张 Research Agent Card，月预算 300 USDC，单笔 40 USDC，只允许访问白名单里的 x402 服务。Mock 模式下可以一键审批；Real CAW 模式下，这一步会提交 Pact，并由老板在 Cobo App 中审批。

### 1:30 - 2:05

进入 Agent Console。Vega Research Agent 使用这张卡购买一次研究数据 API。系统会检查卡状态、Agent 分配、供应商白名单、预算、单笔限额和冷却期。通过后，付款被 Approved。Agent 完成了支付，但没有拿到无限钱包权限。

### 2:05 - 2:35

接下来运行攻击演示。攻击试图让 Agent 向攻击者地址付款，或者提交超额付款。系统返回 Denied，并展示失败阶段和失败原因，例如 scope_denied 或 per_tx_exceeded。这证明系统默认不信任 Agent Runtime，而是把边界放在 Card/Pact 和 CAW Policy 层。

### 2:35 - 2:50

最后看 Audit Report。所有通过和被拒绝的交易都会记录下来，老板可以看到哪个 Agent、向谁付款、金额多少、为什么被拒绝。这形成了完整的财务审计闭环。

### 2:50 - 3:00

OPC Agent Treasury 的核心价值是：让 AI Agent 拥有受控、可撤销、可审计的资金权限，而不是无限钱包。它是 Agentic Economy 进入真实支付场景前需要的安全层。

---

## 4. 录屏镜头清单

| 时间 | 页面 | 操作 | 评委应该看到什么 |
|---|---|---|---|
| 0:00-0:25 | Dashboard / README | 展示项目名和总览 | 问题明确，不先堆技术 |
| 0:25-0:55 | Cards | 展示卡片策略字段 | CAW Pact = AI 员工支出卡 |
| 0:55-1:35 | Cards | 创建/审批/展示 Active Card | 预算、限额、供应商白名单 |
| 1:35-2:20 | Agent Console | 合法支付 | Approved + 多阶段检查通过 |
| 2:20-3:05 | Attack Demo | 运行 A1/A2 攻击 | Denied + 明确失败原因 |
| 3:05-3:35 | Audit Report | 查看交易和异常 | 审计闭环 |
| 3:35-4:00 | README / Proposal | 展示 CAW evidence | 不是纯 Mock，有 Real 模式证据 |
| 4:00-4:20 | Dashboard | 收尾 | 价值主张清晰 |

---

## 5. 评审提交描述模板

提交表单如果有 “Demo Description / Video Description”，可以粘贴：

```text
This 3-5 minute demo shows OPC Agent Treasury, a Cobo Agentic Wallet powered finance OS for AI employees in a one-person company. The demo covers: issuing a programmable CAW Pact spending card, assigning it to a specific AI employee, submitting an x402-style payment request, blocking prompt-injection / over-limit attacks, and reviewing the audit trail. The default demo runs in mock mode for reproducibility, while the repository also includes Real CAW SDK/REST integration, verified wallet/Pact/testnet evidence, and a real-mode SOP.
```

中文版本：

```text
这个 3-5 分钟 Demo 展示 OPC Agent Treasury：一个基于 Cobo Agentic Wallet 的一人公司 AI 员工财务操作系统。演示内容包括：创建可编程 CAW Pact 支出卡、分配给指定 AI 员工、发起 x402 风格支付、拦截 Prompt Injection / 超额支付攻击，以及查看审计记录。默认演示使用 Mock 模式以保证评委可复现；仓库同时包含 Real CAW SDK/REST 对接、钱包/Pact/测试网验证记录和真实模式 SOP。
```

---

## 6. 录制注意事项

- 不要从技术栈开场，先讲痛点。
- 视频必须控制在 5 分钟内；宁可少讲细节，也要完整展示正常流 + 攻击流 + 审计流。
- 默认使用 Mock 模式，避免录制时卡在移动 App 审批、测试网网络或外部 API。
- Real CAW 证据只展示 20-25 秒，不要现场尝试真实转账。
- 如果页面加载失败，直接切到 CLI：`python3 src/run_demo.py full`，保证录制不中断。
- 不要展示 `.env`、API Key、私钥、助记词或任何真实 credential。
