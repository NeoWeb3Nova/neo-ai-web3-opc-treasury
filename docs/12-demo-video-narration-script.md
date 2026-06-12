# OPC Agent Treasury — 演示视频纯口播稿（按页面分段）

> 建议时长：4 分 20 秒  
> 录制方式：屏幕录制 + 旁白  
> 推荐模式：CAW_MODE=mock

---

## 页面：Dashboard / 开场

大家好，我是 Neo。这次黑客松参赛的项目叫 OPC Agent Treasury，是给一人公司的 AI 员工使用的财务操作系统。

今天 AI Agent 已经可以帮一个 solo founder 做研究、买数据、跑广告、调用 API，但只要它需要花钱，就会遇到一个很危险的二选一：

要么每一笔都叫醒老板审批，自动化失效；要么把钱包私钥或 API Key 交给 Agent，一次 Prompt Injection 就可能把钱花到攻击者地址。

OPC Agent Treasury 解决的是中间这一层：让 AI Agent 能花钱，但只能在老板预先授权的预算、供应商和策略范围内花钱。

---

## 页面：Cards（方案介绍）

我们的核心设计很简单：给每个 AI Agent 发一张可编程的支出卡。

这张卡在底层对应 Cobo Agentic Wallet 的 Pact。老板可以设置月度预算、单笔限额、供应商白名单、有效期和冷却期。Agent 不会拿到私钥，也不能自己改规则。

所以这里的 CAW 不是登录组件，也不是普通钱包按钮。CAW Pact 是整个系统的风控核心：Pact 定义权限，CAW Policy Engine 在付款前执行边界，MPC 钱包负责保护私钥。

---

## 页面：Cards（创建并审批卡片）

这里我给 Vega Research Agent 创建一张研究预算卡。

这张卡的月预算是 300 USDC，单笔最多 40 USDC，只能支付白名单里的 x402 服务。真实 CAW 模式下，这一步会提交一个 CAW Pact，并需要老板在 Cobo App 里审批；在今天的演示里，我使用 Mock 模式，让评委可以不依赖外部 App 和测试网状态完整跑通流程。

审批后，这张卡变成 Active。下一步，它必须被分配给一个具体的数字员工，不能成为所有 Agent 共用的万能付款凭证。

---

## 页面：Agent Console（合法支付）

现在进入 Agent Console。假设 Vega 需要购买一次研究数据 API，它会提交一个付款请求。

系统会先检查：这张卡是不是 Active；这张卡是不是分配给 Vega；供应商是不是在白名单里；金额有没有超过单笔和月度预算；有没有违反冷却期。

如果是在 Real CAW 模式下，最后还会带上 pact_id、src_addr、dst_addr、token_id、chain_id 和 request_id，通过 Pact-scoped API Key 交给 CAW 做最终的转账权限校验。

这里可以看到，这笔请求通过了所有检查，状态是 Approved。关键点是：Agent 完成了付款动作，但从头到尾没有接触私钥，也没有拿到无限钱包权限。

---

## 页面：Attack Demo（攻击拦截）

真正重要的不是正常支付能通过，而是被攻击时系统会不会 fail closed。

这里我运行一个典型攻击：Agent 被 Prompt Injection 诱导，把钱打到攻击者地址，或者把金额提高到远超单笔限额。

可以看到交易被拒绝了。拒绝原因不是前端写死的提示，而是来自后端策略检查：可能是 scope_denied、per_tx_exceeded、agent_not_assigned，或者 cooldown_violation。

这说明系统不相信 Agent 自己会永远诚实。它默认把 Agent 当成可能被攻破的执行环境，把真正的资金边界放在 Card/Pact 和 CAW Policy 层。

---

## 页面：Audit Report（审计闭环）

所有通过和被拒绝的请求都会进入审计记录。

这对一人公司很关键。老板不需要实时盯着每一笔小额支付，但月底必须能回答三个问题：哪个 Agent 花了钱，花给谁，为什么有些请求被拒绝。

所以 OPC Agent Treasury 不只是支付按钮，它也是 Agent 财务审计层。被拦截的攻击不是噪音，而是风险证据。

---

## 页面：Real CAW 证据

为了保证演示稳定，默认 Demo 使用 Mock 模式。但项目已经实现了 Real CAW 客户端，并保留了真实验证记录。

这里包括 CAW Wallet UUID、钱包地址、Base Sepolia 测试交易哈希、已激活的 Pact ID，以及 cobo-agentic-wallet SDK 0.1.40 的对接代码。

Real 模式的操作 SOP 在 docs/CAW-REAL-MODE-SOP.md，核心代码在 src/real_caw_client.py。

---

## 页面：Dashboard / 收尾

总结一下，OPC Agent Treasury 解决的不是“怎么让 AI 自动点付款”，而是更底层的问题：AI Agent 如何在真实商业里拥有受控、可撤销、可审计的资金权限。

未来的一人公司会有很多 AI 员工。它们不应该拥有无限钱包，而应该拥有像企业卡一样的策略化支出权限。

这就是 OPC Agent Treasury：AI 员工的财务卡包，也是 Agentic Economy 进入真实支付场景前必须补上的安全层。谢谢。