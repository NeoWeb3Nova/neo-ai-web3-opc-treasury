<div align="center">
  <h1>OPC Agent Treasury</h1>
  <p><strong>AI Employee Finance OS for One-Person Companies</strong></p>
  <p>Issue programmable CAW spending cards to AI agents, let them pay x402 services, and keep every dollar scoped, revocable, and auditable.</p>
  <p>
    <img alt="Hackathon" src="https://img.shields.io/badge/Hackathon-AI%20%C3%97%20Web3%20Agentic%20Builders-6E56CF">
    <img alt="Track" src="https://img.shields.io/badge/Track-Cobo%20Agentic%20Wallet-111827">
    <img alt="Backend" src="https://img.shields.io/badge/Backend-FastAPI%20%2B%20Python%203.10%2B-009688">
    <img alt="Frontend" src="https://img.shields.io/badge/Frontend-React%2019%20%2B%20Vite%208-61DAFB">
    <img alt="Wallet" src="https://img.shields.io/badge/Wallet-Cobo%20CAW%20SDK%200.1.40-F59E0B">
    <img alt="Status" src="https://img.shields.io/badge/Status-MVP%20Ready-success">
  </p>
</div>

---

## 0. Hackathon Submission Summary

| Item | Status | Evidence |
|---|---:|---|
| GitHub repository README | Complete | This file |
| Project background / problem | Complete | Sections 1–2 |
| Installation and run guide | Complete | Section 7 |
| Core features | Complete | Section 3 |
| Technical architecture | Complete | Section 4 |
| APIs / SDKs / AI tools used | Complete | Section 5 |
| CAW key code and configuration | Complete | `src/real_caw_client.py`, `.env.example`, `docs/CAW-REAL-MODE-SOP.md` |
| Runnable prototype | Complete | FastAPI backend, React UI, Streamlit UI, CLI demo |
| On-chain / CAW evidence | Complete | Section 9, `docs/cobo-caw-research/report-v2.md` |
| Demo video | To be added | `demo/video/` |
| Live demo link | Local runnable | `http://localhost:5173`, `http://localhost:8000`, `http://localhost:8501` |

**Primary track:** Cobo Track — Agentic Economy × Cobo Agentic Wallet  
**Primary direction:** Agent-Native Payments + Agent Resource Procurement + A2A Economy  
**Submission posture:** runnable MVP with mock mode for judges and real CAW mode for verified wallet/Pact/payment flows.

---

## 1. Project Background — The OPC Midnight Problem

A one-person company (OPC) can now hire a team of AI employees: a research agent, a growth agent, an infrastructure agent, an operations agent, and a content agent. They can work 24/7, call APIs, buy data, run ads, and procure compute.

But money still has an old-world bottleneck:

> Either the founder wakes up to approve every micro-payment, or the founder gives an AI agent a private key and hopes prompt injection never happens.

That is not a business operating system. That is an accident waiting to happen.

| Existing option | Why it fails for AI employees |
|---|---|
| Give the agent a private key | One compromised prompt, plugin, or runtime can drain the wallet. |
| Keep all payments human-approved | The agent stops being autonomous; every 402/API/payment blocks the founder. |
| Use corporate cards like Brex/Ramp | Designed for human employees and jurisdictional company onboarding, not wallet-native agents. |
| Use a multisig | Secure for large treasury moves; too heavy for high-frequency micro-procurement. |
| Use an API key subscription model | Requires pre-registration with every vendor; incompatible with open agent commerce. |

**OPC Agent Treasury** solves the missing middle layer: AI agents can spend real money, but only inside owner-approved policies that are enforced by wallet infrastructure rather than agent self-discipline.

---

## 2. Solution — Corporate Cards for AI Employees

OPC Agent Treasury turns a Cobo Agentic Wallet Pact into a **virtual employee spending card**.

The owner defines a card once:

- Which AI employee may use it
- Which vendors / destination addresses are allowed
- Which chain and token are allowed
- Maximum monthly budget
- Maximum single transaction amount
- Cooldown / frequency constraints
- Expiration window
- Whether CAW App approval is required

Then the AI employee can autonomously pay x402/API/service providers without ever receiving a private key.

### Core principle

```text
Agent autonomy is useful only when the blast radius is mathematically bounded.
```

| AI employee can | AI employee cannot |
|---|---|
| Pay approved vendors within budget | Export or access the private key |
| Use a Pact-scoped CAW permission | Spend outside the Pact policy |
| Trigger x402-style per-request payments | Change its own whitelist or limits |
| Execute repeatable business workflows | Revoke owner authority |
| Produce audit records for review | Hide denied attempts from the owner |

---

## 3. Core Features

### 3.1 CAW Permission Cards

Each card maps to a CAW Pact. In mock mode, the same interface is simulated locally for fast demos and tests. In real mode, the backend submits a real Pact to Cobo Agentic Wallet.

| Control | Implementation | Why it matters |
|---|---|---|
| Monthly budget | CAW `usage_limits.rolling_30d.amount_usd_gt` + local UI accounting | Prevents slow-drain attacks. |
| Single transaction cap | CAW `deny_if.amount_usd_gt` | Blocks inflated vendor requests. |
| Vendor allowlist | CAW `destination_address_in` | Prevents prompt-injected payments to attacker addresses. |
| Token / chain scope | CAW `token_in` and `chain_in` | Keeps spend on approved settlement rails. |
| Expiration | CAW `completion_conditions.time_elapsed` | Makes temporary employee permissions expire automatically. |
| Spend completion | CAW `completion_conditions.amount_spent_usd` | Ends a Pact after its budget is consumed. |
| ERC-8004 signing scope | CAW `message_sign` policy for `AgentWalletSet` EIP-712 typed data | Binds agent identity/reputation operations to allowed registry domains. |
| Cooldown | Local policy layer before transfer | Adds business-level anti-spam/frequency control. |
| Assignment | Backend requires an active card to be assigned to one digital employee before payment | Prevents a generic or wrong agent from using another employee’s card. |

### 3.2 Mock Mode and Real CAW Mode

| Mode | Use case | External dependency | Entry point |
|---|---|---|---|
| `CAW_MODE=mock` | Hackathon judging, CI, offline demo | None beyond Python dependencies | `src/mock_caw_client.py` |
| `CAW_MODE=real` | Real CAW wallet, Pact, balance, transfer, audit testing | Cobo CAW SDK/API/App | `src/real_caw_client.py` |

The factory in `src/caw_factory.py` keeps the rest of the system independent of the selected mode.

### 3.3 x402 + ERC-8004 Marketplace Context

The project includes a curated and live-updatable service registry for agent-commerce demos:

- `GET /providers/x402` returns x402-style service providers with wallet addresses and pricing metadata.
- `GET /erc8004/agents` returns x402-enabled ERC-8004 agent registry examples.
- `GET /erc8004/agents/search?q=...` searches the public 8004scan API with local fallback.
- `GET /marketplace/context` documents why x402 and ERC-8004 are the correct protocol targets.

This gives the UI a realistic path: select a vendor, issue a CAW card, bind it to an AI employee, then submit a payment.

### 3.4 Digital Employee Directory

OPC Agent Treasury models AI staff as first-class treasury actors:

| Employee | Agent ID | Role | Risk tier | Recommended policy |
|---|---|---|---|---|
| Watt Infrastructure Agent | `agent-watt-infra` | RPC, deployment checks, infrastructure monitoring | Low | $250/month, $25/tx, 2h cooldown |
| Vega Research Agent | `agent-vega-research` | Market and protocol research | Medium | $300/month, $40/tx, 4h cooldown |
| Lyra Growth Agent | `agent-lyra-growth` | Paid growth and campaign experiments | High | $800/month, $120/tx, 8h cooldown |
| Orion Operations Agent | `agent-orion-ops` | Procurement and payment orchestration | Medium | $500/month, $75/tx, 6h cooldown |
| Nova Operations Agent | `agent-nova-ops` | Cashflow, reconciliation, exception review | Medium | $400/month, $60/tx, 6h cooldown |

### 3.5 Payment Policy Engine

Every payment request is evaluated before CAW transfer submission:

```text
1. Card lifecycle check
   - ACTIVE required
   - REVOKED / EXPIRED / PENDING_APPROVAL denied

2. Employee assignment check
   - Card must be assigned
   - Requesting agent_id must match assigned_agent_id

3. Vendor and destination check
   - Vendor must exist in the card whitelist
   - Destination must be a valid EVM address

4. Business policy check
   - Cooldown window
   - Local budget estimate

5. CAW policy enforcement
   - Pact-scoped API key
   - src_addr + dst_addr transfer payload
   - CAW Policy Engine final allow / deny

6. Audit and dashboard update
   - Approved, denied, or on-chain error normalized for UI
```

### 3.6 Threat Lab

The demo includes executable security scenarios rather than slide-only claims.

| ID | Attack | Defense | Demo endpoint / file |
|---|---|---|---|
| A1 | Prompt injection sends funds to attacker address | Vendor allowlist | `POST /attacks/a1`, `src/threat_simulator.py` |
| A2 | Legitimate vendor inflates price | Per-transaction cap | `POST /attacks/a2` |
| A3 | Scope bypass to unapproved service | Destination whitelist | `POST /attacks/a3` |
| A4 | Budget exhaustion via repeated small payments | Rolling budget + cooldown | `POST /attacks/a4` |
| A5 | Reuse of revoked card | Card status check | `POST /attacks/a5` |

The broader design documentation covers eight attack classes in `docs/03-attack-matrix.md`: replay, MITM/address tampering, budget exhaustion, rogue provider, privilege escalation, time-window bypass, signature forgery, and audit tampering.

### 3.7 Multi-Interface Demo

| Interface | Audience | Purpose |
|---|---|---|
| React + Vite web app | Hackathon judges / product demo | Dashboard, cards, employee assignment, agent console, attack demo, audit report |
| FastAPI backend | Developers / integrations | REST API around mock/real CAW clients |
| Streamlit dashboard | Fast local presentation | Pact manager, agent ops, threat lab, audit views |
| CLI demo | Terminal-first verification | Normal flow, attack flow, full flow, A2A coordination |

---

## 4. Technical Architecture

### 4.1 System Diagram

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         OPC Owner / Founder                          │
│  - Creates CAW wallet                                                │
│  - Approves / rejects Pacts in Cobo App                              │
│  - Reviews cards, denied attempts, audit trail                       │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ approve / revoke
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Cobo Agentic Wallet (CAW)                         │
│  MPC-TSS wallet │ Pact lifecycle │ Policy Engine │ Audit pipeline     │
│  - transfer policy: chain/token/destination/budget                   │
│  - message_sign policy: ERC-8004 AgentWalletSet EIP-712              │
│  - Pact-scoped API key after owner approval                          │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ scoped permission
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 OPC Agent Treasury Backend (FastAPI)                 │
│  Cards API │ Assignment API │ Payments API │ Attack API │ Audit API    │
│  MockCAWClient for offline demos │ RealCAWClient for live CAW calls    │
└──────────────┬────────────────────────────┬─────────────────────────┘
               │                            │
               ▼                            ▼
┌──────────────────────────────┐   ┌──────────────────────────────────┐
│ React / Streamlit UI          │   │ AI Employee Runtime / CLI Demo    │
│ - Dashboard                   │   │ - Content / Ad agents             │
│ - Cards                       │   │ - A2A Coordinator                 │
│ - Agent Console               │   │ - Threat simulator                │
│ - Attack Demo                 │   │ - Monthly audit reporter          │
└──────────────────────────────┘   └──────────────────┬───────────────┘
                                                       │ x402-style request
                                                       ▼
                                      ┌──────────────────────────────────┐
                                      │ x402 / API / Agent marketplace    │
                                      │ Provider receives scoped payment  │
                                      └──────────────────────────────────┘
```

### 4.2 Protocol Stack

| Layer | Protocol / component | Project role |
|---|---|---|
| Business scenario | OPC digital employees | Defines who is allowed to spend and why. |
| Payment discovery | x402 / HTTP 402 pattern | Agent receives a payment requirement and pays per request. |
| Agent identity | ERC-8004 | Provider/employee identity and reputation context. |
| Wallet authorization | Cobo CAW Pact | Owner-approved, scoped wallet permission. |
| Policy enforcement | CAW Policy Engine + local business checks | Final guardrail before funds move. |
| Settlement | CAW transfer APIs on Base / supported chains | Executes token transfers in real mode. |
| Audit | CAW audit logs + local transaction records | Produces reviewable evidence for the owner. |

### 4.3 Backend API Surface

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Backend and CAW mode health check |
| `GET` | `/config` | Default chain/token and mode |
| `GET` | `/providers/x402` | Curated/live x402 provider list |
| `GET` | `/erc8004/agents` | ERC-8004 agent registry examples |
| `GET` | `/erc8004/agents/search?q=...` | Live 8004scan search with fallback |
| `GET` | `/marketplace/context` | x402scan and ERC-8004 ecosystem context |
| `GET` | `/agents/digital-employees` | OPC AI employee directory |
| `GET` | `/wallet/balance` | Real CAW wallet balance, if configured |
| `POST` | `/cards` | Create a CAW card/Pact |
| `GET` | `/cards` | List cards with recomputed spend |
| `POST` | `/cards/{card_id}/approve` | Wait for mock/real Pact activation |
| `POST` | `/cards/{card_id}/assign` | Assign an active card to one digital employee |
| `POST` | `/cards/{card_id}/revoke` | Revoke locally or request CAW revoke flow |
| `POST` | `/payments` | Submit scoped payment from assigned agent |
| `GET` | `/transactions` | List transaction records |
| `GET` | `/audit/summary` | Monthly spending and anomaly summary |
| `POST` | `/attacks/{attack_id}` | Execute one threat scenario |
| `GET` | `/dashboard` | Aggregated cards + transactions + summary |
| `POST` | `/demo/reset` | Reset mock demo state |

### 4.4 Repository Structure

```text
.
├── README.md                         # Hackathon-facing project README
├── README_CN.md                      # Chinese README from previous iteration
├── PROPOSAL.md                       # Project proposal / pitch narrative
├── .env.example                      # Root backend + CAW environment template
├── backend/
│   ├── main.py                       # FastAPI application and REST endpoints
│   ├── models.py                     # Pydantic request/response schemas
│   └── requirements.txt              # Backend dependencies
├── src/
│   ├── caw_factory.py                # Mock/real CAW client selector
│   ├── mock_caw_client.py            # Offline CAW simulator for judging/CI
│   ├── real_caw_client.py            # Cobo CAW SDK/REST wrapper
│   ├── service_registry.py           # x402 + ERC-8004 marketplace context
│   ├── content_agent.py              # Content and ad agent demo logic
│   ├── a2a_agent.py                  # Agent-to-agent coordination demo
│   ├── threat_simulator.py           # Attack scenarios
│   ├── audit_reporter.py             # Monthly audit report generator
│   ├── app.py                        # Streamlit dashboard
│   ├── requirements-ui.txt           # Streamlit dependencies
│   └── run_demo.py                   # CLI demo entry point
├── web/
│   ├── package.json                  # React/Vite/Tailwind app manifest
│   ├── .env.example                  # Vite API URL template
│   ├── PRODUCT.md                    # Product and design principles
│   └── src/
│       ├── App.tsx                   # Router
│       ├── api/client.ts             # FastAPI client wrapper
│       └── pages/                    # Dashboard, Cards, Agent, Attack, Audit
├── tests/
│   ├── test_cards_api.py             # Cards, real CAW wrappers, policy tests
│   ├── test_card_assignment_api.py   # Employee assignment and payment scoping
│   └── test_marketplace_api.py       # x402/ERC-8004 registry behavior
├── docs/
│   ├── 01-hackathon-rules.md         # Official rules and track alignment
│   ├── 03-attack-matrix.md           # Threat model
│   ├── 04-architecture.md            # System architecture
│   ├── 05-flow.md                    # End-to-end payment flow
│   ├── 06-risks.md                   # Risk boundaries and mitigations
│   ├── 07-interfaces.md              # API/interface notes
│   ├── 10-vc-perspective.md          # Judge/investor framing
│   ├── 11-prizes-and-judging.md      # Scoring strategy
│   ├── CAW-REAL-MODE-SOP.md          # Real CAW mode runbook
│   └── cobo-caw-research/report-v2.md# CAW deep research report
└── demo/
    ├── screenshots/
    └── video/
```

---

## 5. APIs, SDKs and AI Tools Used

### 5.1 Blockchain / Wallet / Agent-Commerce Stack

| Tool / API / SDK | Version / source | Used for | Where |
|---|---|---|---|
| Cobo Agentic Wallet Python SDK | `cobo-agentic-wallet>=0.1.40` | Submit Pacts, read Pacts, transfer tokens, inspect balances/transactions | `backend/requirements.txt`, `src/real_caw_client.py` |
| Cobo CAW REST API | `AGENT_WALLET_API_URL` | Sync HTTP fallback for balances, Pacts, transfers, transactions | `src/real_caw_client.py` |
| Cobo CAW App | Mobile owner approval | Approve/reject/revoke Pacts and protect owner key share | `docs/CAW-REAL-MODE-SOP.md` |
| CAW Pact Policy Engine | CAW platform | Transfer policy, message-sign policy, budget limits, destination allowlists | `src/real_caw_client.py` |
| CAW CLI | `caw` | Wallet onboarding, API key retrieval, Pact operations, faucet | `docs/CAW-REAL-MODE-SOP.md` |
| x402 | Protocol pattern / marketplace context | Agent-native pay-per-request payment flow | `src/service_registry.py`, `docs/05-flow.md` |
| ERC-8004 | Identity/reputation standard | Agent identity, reputation context, EIP-712 `AgentWalletSet` policy | `src/real_caw_client.py`, `src/service_registry.py` |
| ERC-8183 | Escrow/evaluator design layer | Future conditional acceptance, dispute, and escrow layer | `docs/04-architecture.md`, `docs/06-risks.md` |
| Base / Base Sepolia | Chain context | USDC settlement target and verified testnet evidence | `.env.example`, Section 9 |
| USDC | `BASE_USDC` | Default spending denomination | `.env.example`, `src/real_caw_client.py` |

### 5.2 Backend Stack

| Technology | Version / constraint | Purpose |
|---|---|---|
| Python | 3.10+ | Backend, CAW client, demo agents |
| FastAPI | `>=0.111.0` | REST API |
| Uvicorn | `>=0.30.0` | ASGI server |
| Pydantic | `>=2.7.0` | API schema validation |
| python-dotenv | `>=1.0.0` | `.env` loading |
| nest-asyncio | `>=1.6.0` | Async SDK bridge when needed |
| Streamlit | `>=1.35.0` | Alternative live demo UI |
| pandas | `>=2.0.0` | Dashboard tables / reporting |
| pytest + FastAPI TestClient | Test dependencies used in repo | API and policy regression tests |

### 5.3 Frontend Stack

| Technology | Version from `web/package.json` | Purpose |
|---|---:|---|
| React | `^19.2.6` | SPA UI |
| React DOM | `^19.2.6` | DOM rendering |
| Vite | `^8.0.12` | Dev server and build tool |
| TypeScript | `~6.0.2` | Type-safe frontend |
| Tailwind CSS | `^3.4.19` | Utility styling |
| React Router DOM | `^7.17.0` | Routing |
| Recharts | `^3.8.1` | Budget and audit charts |
| Lucide React | `^1.17.0` | Icon system |
| i18next / react-i18next | `^26.3.1` / `^17.0.8` | English/Chinese UI language support |
| clsx / tailwind-merge | `^2.1.1` / `^3.6.0` | Conditional class composition |

### 5.4 AI Tools and Agent Roles

| Tool / role | How it is used in this project |
|---|---|
| AI coding assistants | Assisted full-stack implementation, debugging, refactoring, and documentation under human review. |
| Content Agent | Demo employee that buys OpenAI/Midjourney/Unsplash-like services inside a card budget. |
| Ad Agent | Demo employee that buys Google Ads / Twitter Ads-like services. |
| A2A Coordinator Agent | Demonstrates agent-to-agent task dispatch and budget rebalancing. |
| Threat Simulation Agent | Executes adversarial scenarios to prove policy boundaries. |

The project does **not** require an LLM API key to run the default mock demo. AI-agent behavior in the repository is deterministic Python demo logic so judges can reproduce it quickly.

---

## 6. Security Model and Risk Boundaries

### 6.1 Zero-Trust Agent Model

OPC Agent Treasury assumes the agent runtime may be compromised. Therefore the product does not rely on the agent promising to behave.

Security is enforced at three layers:

| Layer | Enforces | Example |
|---|---|---|
| CAW infrastructure | Wallet permission, signing, destination, token, rolling budget | Unknown destination address is denied by Pact policy. |
| Backend business logic | Employee assignment, cooldown, UX-friendly errors, local audit | `agent-lyra-growth` cannot use Vega’s card. |
| Owner controls | App approval, revocation, wallet backup, real-mode key management | Owner approves a Pact before it becomes active. |

### 6.2 Key Design Decisions

| Decision | Reason |
|---|---|
| No private key in agent code | Agents only operate through CAW credentials and scoped Pacts. |
| Pact per employee / task | Reduces blast radius and makes revocation precise. |
| Vendor whitelist is mandatory | The most important defense against prompt injection and address tampering. |
| Assignment required before payment | Prevents an active card from becoming a generic shared credential. |
| Denied transactions are first-class audit records | A blocked attack is valuable evidence, not noise. |
| Mock mode is kept | Judges and CI can reproduce the full product without external credentials. |
| Real mode is kept | Proves this is not just a mockup; the same API shape can hit CAW. |

### 6.3 Known MVP Boundaries

| Boundary | Current state | Production hardening path |
|---|---|---|
| x402 payment server | Flow and provider registry are modeled; old prototype lives under `src/_archive/` | Integrate a production x402 middleware/facilitator endpoint. |
| ERC-8183 escrow | Architecture and risk model documented | Add escrow contract integration and evaluator workflow. |
| On-chain audit immutability | CAW and local transaction records are used | Persist Merkle roots / receipts to chain or durable storage. |
| Real vendor addresses | `.env.example` uses placeholders | Configure verified vendor addresses before real transfers. |
| Mainnet funds | Demo uses testnet/sandbox posture | Start with low limits, owner approval, monitoring, and emergency revoke runbook. |

---

## 7. Installation and Run Guide

### 7.1 Prerequisites

| Tool | Required for | Recommended version |
|---|---|---|
| Git | Clone repo | Latest |
| Python | Backend, CLI, Streamlit | 3.10+ |
| Node.js + npm | React frontend | Node 18+ |
| Cobo CAW CLI/App | Real mode only | Latest from Cobo docs |

### 7.2 Clone

```bash
git clone https://github.com/NeoWeb3Nova/opc-agent-treasury.git
cd opc-agent-treasury
```

If you are already inside the repository, start from the project root.

### 7.3 Backend Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Optional Streamlit UI dependencies:

```bash
pip install -r src/requirements-ui.txt
```

### 7.4 Environment Configuration

```bash
cp .env.example .env
```

For default hackathon demo mode, keep:

```bash
CAW_MODE=mock
VITE_API_URL=http://localhost:8000
```

For real CAW mode, fill the CAW values in `.env`:

| Variable | Required | Description |
|---|---:|---|
| `CAW_MODE` | Yes | `mock` or `real` |
| `AGENT_WALLET_API_URL` | Real mode | Cobo Agentic Wallet API base URL |
| `AGENT_WALLET_API_KEY` | Real mode | CAW API key from `caw wallet current --show-api-key` |
| `AGENT_WALLET_WALLET_ID` | Real mode | CAW wallet UUID |
| `CAW_DEFAULT_CHAIN` | Real mode | Default chain, e.g. `BASE_ETH` |
| `CAW_DEFAULT_TOKEN` | Real mode | Default token, e.g. `BASE_USDC` |
| `CAW_SRC_ADDR` / `AGENT_WALLET_ADDRESS` | Real transfers if balance API cannot infer source address | Source wallet address for CAW `transfer` payload |
| `VENDOR_*_ADDR` | Real transfers | Real destination addresses for vendors |
| `VITE_API_URL` | Frontend | Backend URL for Vite app |

Never commit `.env` or real API keys.

### 7.5 Run FastAPI Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Verify in another terminal:

```bash
curl http://localhost:8000/health
```

Expected shape:

```json
{"status":"ok","caw_mode":"mock","sdk_available":true,"wallet_uuid":null}
```

`sdk_available` depends on whether `cobo-agentic-wallet` installed successfully in your environment.

### 7.6 Run React Frontend

```bash
cd web
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

Frontend pages:

| Route | Page |
|---|---|
| `/` | Dashboard |
| `/cards` | CAW cards / Pacts |
| `/agent` | Agent payment console |
| `/attack` | Threat lab |
| `/audit` | Audit report |

### 7.7 Run Streamlit Demo UI

```bash
source .venv/bin/activate
cd src
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

### 7.8 Run CLI Demos

```bash
source .venv/bin/activate
cd src

python3 run_demo.py normal   # Issue cards, simulate purchases, print audit
python3 run_demo.py attack   # Run threat simulation
python3 run_demo.py full     # Normal + attack flow
python3 run_demo.py a2a      # Agent-to-agent coordination
```

---

## 8. Real CAW Mode

Real mode is documented in detail in `docs/CAW-REAL-MODE-SOP.md`.

High-level flow:

```bash
# 1. Install / verify Cobo CAW CLI using the Cobo instructions
caw --version

# 2. Onboard and pair wallet
caw onboard --wait
caw wallet current --show-api-key

# 3. Configure .env
CAW_MODE=real
AGENT_WALLET_API_URL=https://api.agenticwallet.cobo.com
AGENT_WALLET_API_KEY=your_caw_api_key_here
AGENT_WALLET_WALLET_ID=your_wallet_uuid_here
CAW_DEFAULT_CHAIN=BASE_ETH
CAW_DEFAULT_TOKEN=BASE_USDC

# 4. Start backend from backend/
uvicorn main:app --reload --port 8000

# 5. Create a card/Pact from React UI or API
# 6. Approve the Pact in Cobo Agentic Wallet App
# 7. Assign the active card to a digital employee
# 8. Submit a payment from that assigned employee
```

Important real-mode implementation notes:

- `RealCAWClient` uses a fresh SDK client for Pact submission to avoid cross-event-loop issues in synchronous FastAPI endpoints.
- Read-only CAW calls such as balances and Pact lists prefer synchronous REST helpers to avoid `aiohttp` event-loop reuse problems.
- Transfers include `pact_id`, `src_addr`, `dst_addr`, `chain_id`, `token_id`, `amount`, and `request_id`.
- Pact-scoped API keys are fetched from CAW Pact detail when available; using a generic/default key can cause `INSUFFICIENT_PERMISSION`.
- Agent keys can read Pacts but may not be allowed to revoke them. Owner-side revoke may need the CAW App or owner API key.

---

## 9. Verified CAW / On-Chain Evidence

These records are kept from the project’s CAW real-mode validation and proposal materials.

| Evidence | Value |
|---|---|
| CAW Wallet UUID | `ad7f3253-4a3b-48a0-9d09-9bb59d334390` |
| Wallet ETH address | `0x0abd808e6df088b9b97179a091582618586d0bdc` |
| Successful transfer transaction | `0x1a119f1b1bf5ffdb9f2dc4bea392d5d489807aa97925c1949199f7ea91c9dddd` |
| Transfer amount | `0.001 SETH` on Base Sepolia test environment |
| CAW Pact instance | `13328473-3868-4f45-a35e-ae2a8a1e1ea4` |
| Pact policy summary | `BASE_USDC`, `$50/tx`, `$500/month` |
| SDK version | `cobo-agentic-wallet>=0.1.40` |
| Detailed report | `docs/cobo-caw-research/report-v2.md` |

Testnet / sandbox posture: no mainnet funds are required for judging the default demo.

---

## 10. Testing and Verification

### 10.1 Backend tests

```bash
source .venv/bin/activate
pytest tests
```

The test suite covers:

- Card schema validation
- Null/real CAW response normalization
- Mock card lifecycle
- Card assignment requirements
- Payment rejection for unassigned/wrong agents
- x402 provider metadata preservation
- ERC-8004 policy construction
- CAW transfer payload requirements such as `src_addr` and `pact_id`
- Marketplace context endpoints

### 10.2 Frontend build

```bash
cd web
npm run build
```

### 10.3 Manual smoke checks

With backend running:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/providers/x402
curl http://localhost:8000/agents/digital-employees
curl http://localhost:8000/marketplace/context
```

---

## 11. Why This Project Is Competitive

### 11.1 It directly matches the Cobo track

The Cobo track requires an agent funding scenario where CAW is essential, not decorative. In OPC Agent Treasury, CAW is the core control plane:

| Track requirement | Project answer |
|---|---|
| Agent performs funds operation | AI employees submit scoped payment requests. |
| Uses Cobo Agentic Wallet | Real CAW SDK/REST client creates Pacts and transfers tokens. |
| Demonstrates permission control | Pacts enforce chain/token/destination/budget/message-sign scopes. |
| Runnable demo | Mock mode runs locally; real mode has SOP and validation evidence. |
| Shows risk boundaries | Threat lab, risk docs, fail-closed policy model, audit logs. |

### 11.2 It solves a real pain, not a sci-fi demo

The user is not “an autonomous AGI.” The user is a practical solo operator who wants AI employees to buy APIs, data, ads, and infrastructure without losing treasury control.

This is why the product uses the language of employee cards, limits, vendors, approvals, and audit reports. It is finance ops infrastructure for the agent era.

### 11.3 It has technical depth beyond CRUD

| Depth area | Evidence |
|---|---|
| CAW policy mapping | `src/real_caw_client.py` maps card controls into CAW transfer and message-sign policies. |
| Real SDK integration | SDK and REST calls handle balances, Pacts, transfers, transactions, and API-key scope issues. |
| x402 / ERC-8004 context | `src/service_registry.py` connects payment providers with agent identity/reputation metadata. |
| Security modeling | `docs/03-attack-matrix.md`, `docs/06-risks.md`, `src/threat_simulator.py` |
| Full-stack product | FastAPI + React + Streamlit + CLI + tests |

### 11.4 It is demo-ready

The project gives judges multiple ways to verify it:

1. Read the README and architecture docs.
2. Run mock mode without credentials.
3. Watch the UI issue cards and block attacks.
4. Inspect tests for policy boundaries.
5. Review real CAW evidence and SOP.

---

## 12. Roadmap

| Phase | Goal | Key work |
|---|---|---|
| Hackathon MVP | Prove safe AI employee spending | Mock/real CAW client, cards, assignment, payments, threat lab, dashboard |
| Post-hackathon P0 | Productionize payment path | Real x402 middleware, facilitator verification, robust idempotency, persistent DB |
| Phase 1 | Real OPC beta | Vendor onboarding, owner notification, SSE event stream, CAW App runbook, better audit exports |
| Phase 2 | Protocol integrations | ERC-8183 escrow/evaluator, richer ERC-8004 trust scoring, service quality proofs |
| Phase 3 | Developer platform | npm/pip SDK, card templates, agent-framework adapters, hosted demo |
| Phase 4 | Treasury OS | Multi-wallet support, recurring budgets, accounting export, compliance policies |

---

## 13. Documentation Index

| Document | Purpose |
|---|---|
| `docs/01-hackathon-rules.md` | Official rules and requirement mapping |
| `docs/02-sprint-tracker.md` | Build-period execution tracking |
| `docs/03-attack-matrix.md` | Threat model and attack coverage |
| `docs/04-architecture.md` | Architecture diagrams and protocol layers |
| `docs/05-flow.md` | End-to-end interaction and x402 flow |
| `docs/06-risks.md` | Risk boundaries and mitigations |
| `docs/07-interfaces.md` | Interface/API design notes |
| `docs/08-rules-gap-analysis.md` | Cobo rules versus project mapping |
| `docs/09-open-day-insights.md` | Hackathon open-day notes |
| `docs/10-vc-perspective.md` | Judge/investor positioning |
| `docs/11-prizes-and-judging.md` | Scoring and demo strategy |
| `docs/CAW-REAL-MODE-SOP.md` | Real CAW operation SOP |
| `docs/cobo-caw-research/report-v2.md` | Deep CAW technical research |

---

## 14. Team

| Role | Contributor | Contribution |
|---|---|---|
| Founder / developer | Neo / NeoWeb3Nova | Product idea, architecture, CAW research, backend, frontend, demo flows, docs, threat model |
| AI coding partners | Claude / GPT-class coding assistants | Implementation acceleration, refactoring support, test/debug assistance, documentation drafts under human review |

---

## 15. License and Risk Disclaimer

This repository is a hackathon MVP and reference implementation. It is designed for testnet, sandbox, and low-limit validation flows unless explicitly hardened for production.

Before using real funds:

- Use the CAW App and owner-controlled keys for approval/revocation.
- Start with low budgets and strict vendor allowlists.
- Verify every vendor destination address.
- Keep API keys out of git and logs.
- Back up CAW wallet/key-share materials according to the Cobo runbook.
- Monitor denied attempts, pending operations, and audit logs.
- Review `docs/06-risks.md` and `docs/CAW-REAL-MODE-SOP.md`.

License: not declared in this repository yet. Add a `LICENSE` file before production or public distribution if the hackathon submission requires an explicit license.

---

> Because giving your AI employee a private key is not a business plan.
