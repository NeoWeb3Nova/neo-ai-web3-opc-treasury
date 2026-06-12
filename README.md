# OPC Agent Treasury

> **AI Agent Finance OS for One-Person Companies**
>
> Give every AI employee a corporate card with budget limits, vendor whitelists, and real-time anomaly detection — without ever handing over a private key.
>
> **Hackathon**: AI × Web3 Agentic Builders Hackathon — Cobo Track  
> **Status**: MVP Ready ✅ | Mock + Real CAW SDK Dual Mode  
> **Demo Video**: [Link TBD]  
> **Live Demo**: [Link TBD]

---

## 1. Project Background — The Midnight Problem of OPC Owners

Neo runs a **One-Person Company (OPC)**. He hired 5–10 AI Agents that operate 7×24:

- **Content Agent** buys OpenAI API credits, Midjourney subscriptions, Unsplash stock photos
- **Ad Agent** tops up Google Ads, Twitter/X Ads campaigns
- **Design Agent** pays freelancers in Australia and Southeast Asia

**The problem**: Every time an Agent needs to spend money, Neo gets dragged out of bed.

| Option | Risk |
|---|---|
| Give private key | One prompt injection attack = total wipeout |
| Don't give key | Agent stops, business goes dark |
| Brex / Ramp | Requires US entity, SSN, human employees — Neo has none |
| Safe multi-sig | Every micro-payment needs a signature — Neo is one person |

**This is the invisible infrastructure gap**: AI employees have already onboarded, but financial authorization has not caught up.

### Our Solution

We built **OPC Agent Treasury** — an Agent Finance OS that issues **scoped spending cards (CAW Pacts)** to every AI employee:

- Monthly budget cap + per-transaction limit
- Vendor whitelist (only OpenAI, Midjourney, Google Ads…)
- Cooldown period between same-vendor payments
- Time window validity (auto-expire)
- Real-time anomaly detection + automatic blocking
- Immutable audit trail for monthly reconciliation

**One sentence**: *Bring corporate-card governance to AI employees in one-person companies.*

---

## 2. Core Features

### 2.1 Virtual Employee Card (CAW Pact)

Each Agent gets a programmable spending card bound to a Cobo Agentic Wallet (CAW) Pact:

| Policy | Enforcement Point | Description |
|---|---|---|
| `monthly_budget` | CAW server-side rolling-30d limit | Hard cap on monthly spending |
| `single_tx_limit` | CAW server-side per-transaction limit | Blocks overpriced or malicious requests |
| `vendor_whitelist` | CAW `destination_address_in` | Only approved suppliers can receive funds |
| `cooldown_hours` | Local policy engine | Prevents rapid-fire draining |
| `duration_days` | Pact `completion_conditions` | Auto-expire card after term |
| `allowed_hours` | Local time-window check | Restrict operational hours |

### 2.2 Dual-Mode CAW Client (Mock ↔ Real)

The system ships with a factory-pattern CAW client that switches seamlessly:

- **Mock Mode** (`CAW_MODE=mock`): Zero external dependencies, pure Python stdlib. Runs anywhere for demos and CI.
- **Real Mode** (`CAW_MODE=real`): Connects to production Cobo CAW SDK (`cobo-agentic-wallet==0.1.40`), submits real Pacts, executes on-chain transfers, and polls for App-side approval.

### 2.3 Policy Engine — 5-Stage Authorization

Every payment request is evaluated in strict order before any signature is produced:

```
1. Card Status Check      → REVOKED / EXPIRED?  DENY
2. Vendor Whitelist       → Unknown address?    DENY
3. Budget & Tx Limit      → Over cap?           DENY
4. Cooldown & Frequency   → Too soon?           DENY
5. Time Window            → Outside hours?      DENY
   ─────────────────────────────────────────────
   ALL PASS → CAW signs → On-chain settlement
```

### 2.4 Threat Lab — 5 Attack Scenarios (Demo-Ready)

```bash
python src/run_demo.py attack
```

| ID | Attack | Vector | Defense | Result |
|---|---|---|---|---|
| A1 | Prompt Injection | Malicious input tricks Agent into paying hacker address | Vendor whitelist blocks unknown address | **DENIED** |
| A2 | Overpriced Request | Legitimate vendor inflates price 10× | `single_tx_limit` hard cap | **DENIED** |
| A3 | Scope Bypass | Agent pays unapproved vendor | `destination_address_in` rejects | **DENIED** |
| A4 | Budget Exhaustion | 10 rapid-fire $30 transactions | Rolling budget + cooldown | **DENIED after $180** |
| A5 | Revoked Card Reuse | Stolen API key on revoked card | Card status check | **DENIED** |

### 2.5 A2A (Agent-to-Agent) Treasury Coordination

A Coordinator Agent can rebalance budgets across business Agents:

- Content Agent has $160 leftover → Coordinator tops up Ad Agent's campaign
- All cross-Agent transfers re-evaluated by Policy Engine
- Every action recorded in the audit trail

```bash
python src/run_demo.py a2a
```

### 2.6 Audit & Reporting

- **Immutable transaction log**: Every payment attempt (approved or denied) is append-only
- **Monthly Markdown report**: Auto-generated for accountant review
- **Streamlit Dashboard**: Real-time budget burn-down, transaction status, threat flags
- **Recharts frontend**: Visual analytics for multi-agent spend tracking

---

## 3. Technical Architecture

### 3.1 High-Level System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CONSUMER SIDE (OPC Owner)                    │
│  ┌──────────────────┐  ┌──────────────────────────────────────┐  │
│  │   Owner (Neo)     │  │   CAW Agent Wallet + Buyer Agent     │  │
│  │  • Approve/Revoke │  │  • Pact budget control               │  │
│  │    Pacts in App   │  │  • Scope / time constraints          │  │
│  │  • Review audit   │  │  • On-chain audit trail              │  │
│  └──────────────────┘  └──────────────────────────────────────┘  │
│           ↑                                    ↑                    │
│           └────────────────────────────────────┘                    │
│                    ┌──────────────────────┐                         │
│                    │   HTTP / x402 Layer  │                         │
│                    │  402 Payment Required │                         │
│                    │  Payment-Receipt     │                         │
│                    └──────────────────────┘                         │
│           ↑                                    ↑                    │
│  ┌──────────────────┐  ┌──────────────────────────────────────┐  │
│  │  Service Provider  │  │   Facilitator / Settlement           │  │
│  │ ContentGen Agent   │  │  • Verify payment proof              │  │
│  │  • x402 middleware │  │  • On-chain settlement               │  │
│  │  • AI inference    │  │  • Receipt + idempotency             │  │
│  └──────────────────┘  └──────────────────────────────────────┘  │
│                         PROVIDER SIDE                                │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Protocol Stack (4 Layers)

| Layer | Protocol / Standard | Role |
|---|---|---|
| **Scenario** | Business use case | What Agent buys: AI inference, content generation, ad credits |
| **Flow** | x402 + HTTP 402 | Discovery → Quote → 402 handshake → Payment → Service → Delivery → Acceptance → Settlement |
| **Verification** | ERC-8183 + Evaluator | Escrow + deliverable hash + automatic/human acceptance + dispute arbitration |
| **Protocol** | CAW Pact + ERC-8004 | Budget/scope/time constraints + identity/ reputation registry |

### 3.3 Backend Architecture (FastAPI)

```
┌────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Port 8000)          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │  Cards API   │  │ Payments API │  │  Audit API   ││
│  │  POST /cards │  │POST /payments│  │GET /audit/   ││
│  │  GET  /cards │  │POST /attacks │  │   summary    ││
│  │  POST /{id}/ │  │              │  │GET /transac- ││
│  │    approve   │  │              │  │   tions      ││
│  │  POST /{id}/ │  │              │  │              ││
│  │    revoke    │  │              │  │              ││
│  └──────────────┘  └──────────────┘  └──────────────┘│
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │ Marketplace  │  │  Wallet API  │  │  Dashboard   ││
│  │  x402 providers│  │GET /wallet/  │  │GET /dashboard││
│  │  ERC-8004 agents│  │   balance  │  │(aggregated)  ││
│  └──────────────┘  └──────────────┘  └──────────────┘│
│                    │                                    │
│                    ↓                                    │
│  ┌────────────────────────────────────────────────────┐│
│  │         CAW Client Factory (Mock or Real)          ││
│  │  • MockCAWClient  — local state, instant approval  ││
│  │  • RealCAWClient  — SDK v0.1.40, MPC-TSS, App auth ││
│  └────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────┘
```

### 3.4 Frontend Architecture (React + Vite + Tailwind)

```
┌────────────────────────────────────────────────────────┐
│                React SPA (Vite, Port 5173)              │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│  │Dashboard│ │  Cards  │ │ Agent   │ │  Audit  │    │
│  │  (/)    │ │ (/cards)│ │ Console │ │ Report  │    │
│  │         │ │         │ │(/agent) │ │(/audit) │    │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │
│  ┌─────────┐                                           │
│  │ Attack  │  → Interactive attack launch + result     │
│  │  Demo   │                                           │
│  │(/attack)│                                           │
│  └─────────┘                                           │
│         ↑                                               │
│    Recharts — Budget burn-down, threat timeline         │
│    Lucide icons — Operational density UI                  │
│    i18next — Multi-language support (EN/ZH)             │
└────────────────────────────────────────────────────────┘
```

### 3.5 Data Flow (End-to-End Payment)

```
[Agent] ──POST /generate-content──▶ [x402 Server]
                                        │
                                        ▼  402 Payment Required
[Agent] ◀────X-Payment-Required────── [x402 Server]
   │
   ▼  Check CAW Pact budget / scope / time / frequency
[CAW Pact] ──APPROVE──▶ [CAW MPC-TSS] ──Sign──▶ [On-chain Settlement]
   │                                                    │
   ▼  Payment Proof                                     ▼  Receipt
[Agent] ──Retry w/ Auth──▶ [x402 Server] ──Service──▶ [Agent]
   │                                                    │
   ▼  Delivery                                          ▼  Audit log
[Owner] ──Accept/Reject──▶ [Escrow/Evaluator] ───▶ [Immutable Log]
```

---

## 4. APIs, SDKs & AI Tools Used

### 4.1 Blockchain & Wallet Infrastructure

| Tool / SDK | Version | Purpose | License |
|---|---|---|---|
| **Cobo Agentic Wallet (CAW) SDK** | `0.1.40` | MPC-TSS wallet, Pact lifecycle, on-chain transfers | Cobo Proprietary |
| **CAW CLI** | latest | Wallet creation, Pact management, App pairing | Cobo Proprietary |
| **Base Sepolia / Base Mainnet** | — | Testnet & target L2 for USDC settlement | Public chain |
| **USDC (Base)** | — | Stablecoin denomination for all Agent budgets | ERC-20 |

### 4.2 Protocols & Standards

| Standard | Role |
|---|---|
| **x402 (Coinbase)** | HTTP 402 payment-required handshake for Agent-native payments |
| **ERC-8004** | Agent identity & reputation registry (EIP-712 `AgentWalletSet`) |
| **ERC-8183** | Escrow + evaluator framework for conditional delivery/release |
| **EIP-712** | Typed-data signing for ERC-8004 identity verification |
| **EIP-1559** | Dynamic gas pricing for mainnet cost control |

### 4.3 Backend Stack

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.10+ | Core runtime |
| **FastAPI** | latest | REST API framework |
| **Pydantic** | v2 | Request/response validation + serialization |
| **python-dotenv** | latest | Environment configuration |
| **nest-asyncio** | latest | Async SDK bridge in sync FastAPI endpoints |
| **Uvicorn** | latest | ASGI server |

### 4.4 Frontend Stack

| Technology | Version | Purpose |
|---|---|---|
| **React** | 19.2.6 | UI framework |
| **TypeScript** | ~6.0.2 | Type safety |
| **Vite** | 8.0.12 | Build tool + dev server |
| **Tailwind CSS** | 3.4.19 | Utility-first styling |
| **React Router** | 7.17.0 | SPA routing |
| **Recharts** | 3.8.1 | Data visualization (budget charts, threat timeline) |
| **Lucide React** | 1.17.0 | Icon system |
| **i18next** | 26.3.1 | Internationalization (EN / ZH) |

### 4.5 Demo & Dashboard

| Tool | Purpose |
|---|---|
| **Streamlit** | Interactive Python dashboard for live demos (Pact Manager, Agent Ops, Threat Lab, Audit) |

### 4.6 AI & Agent Tools

| Tool | Role in Project |
|---|---|
| **LLM (Claude / GPT-4)** | Architecture design, threat modeling, documentation, code generation |
| **AI Coding Agents** | Parallel development of backend, frontend, and security modules |
| **Agent personas** | Content Agent, Ad Agent, Design Agent, A2A Coordinator — simulated business logic |

---

## 5. Installation & Quick Start

### 5.1 Prerequisites

- Python 3.10+
- Node.js 18+ (for frontend)
- Git
- (Optional) Cobo CAW CLI + Cobo Agentic Wallet App on mobile (for Real Mode)

### 5.2 Clone & Setup

```bash
git clone https://github.com/NeoWeb3Nova/opc-agent-treasury.git
cd opc-agent-treasury
```

### 5.3 Backend & Core (Python)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt
# Core: fastapi uvicorn pydantic python-dotenv nest-asyncio
# Real mode: pip install cobo-agentic-wallet
```

### 5.4 Environment Configuration

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# Mode: mock = zero-dependency demo | real = live CAW SDK
CAW_MODE=mock

# --- Required for Real Mode only ---
AGENT_WALLET_API_URL=https://api-core.agenticwallet.dev.cobo.com
AGENT_WALLET_API_KEY=caw_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AGENT_WALLET_WALLET_ID=a1b2c3d4-e5f6-7890-abcd-ef1234567890

CAW_DEFAULT_CHAIN=BASE_ETH
CAW_DEFAULT_TOKEN=BASE_USDC

# Vendor addresses (for real transfers)
VENDOR_OPENAI_ADDR=0x...
VENDOR_MIDJOURNEY_ADDR=0x...
```

### 5.5 Run Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Verify:
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok","caw_mode":"mock","sdk_available":true}
```

### 5.6 Run Frontend (React + Vite)

```bash
cd web
npm install
npm run dev
# Opens http://localhost:5173
```

### 5.7 Run Streamlit Dashboard (Alternative UI)

```bash
cd src
streamlit run app.py
# Opens http://localhost:8501
```

### 5.8 Run CLI Demo (Fastest — No Dependencies)

```bash
cd src

# Normal flow: Issue cards → Agent purchases → Monthly audit
python3 run_demo.py normal

# Attack flow: 5 attack scenarios, all blocked
python3 run_demo.py attack

# Full flow: Normal + Attack + Audit (3 minutes)
python3 run_demo.py full

# A2A flow: Agent-to-Agent budget rebalancing
python3 run_demo.py a2a
```

### 5.9 Switch to Real Mode (Production CAW)

See detailed SOP: [`docs/CAW-REAL-MODE-SOP.md`](docs/CAW-REAL-MODE-SOP.md)

```bash
# 1. Set mode
export CAW_MODE=real

# 2. Verify SDK
python -c "import cobo_agentic_wallet; print(cobo_agentic_wallet.__version__)"
# Expected: 0.1.40

# 3. Start backend (connects to real Cobo API)
uvicorn main:app --reload --port 8000

# 4. Create a real Pact via API
curl -X POST http://localhost:8000/cards \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "Content Agent",
    "monthly_budget": 500,
    "single_tx_limit": 50,
    "vendor_whitelist": [{"name":"OpenAI","address":"0x...","chain":"BASE_ETH"}]
  }'

# 5. Approve in Cobo App → backend polls for ACTIVE status
# 6. Submit real payment (signed by MPC-TSS, settled on Base)
```

---

## 6. File Structure

```
opc-agent-treasury/
├── .env.example              # Environment template
├── README.md                 # This file
├── backend/
│   ├── main.py               # FastAPI entry (REST API)
│   ├── models.py             # Pydantic schemas
│   ├── requirements.txt      # Python dependencies
│   └── service_registry.py   # x402 provider + ERC-8004 agent registry
├── src/
│   ├── caw_factory.py        # Mock/Real client factory
│   ├── mock_caw_client.py    # Zero-dependency CAW simulator
│   ├── real_caw_client.py  # Cobo SDK v0.1.40 sync wrapper
│   ├── content_agent.py      # Content Agent + Ad Agent business logic
│   ├── a2a_agent.py         # Agent-to-Agent Coordinator
│   ├── threat_simulator.py  # 5 attack scenario demonstrations
│   ├── audit_reporter.py    # Monthly audit report generator
│   ├── app.py               # Streamlit dashboard
│   └── run_demo.py          # CLI demo entry (normal/attack/full/a2a)
├── web/
│   ├── package.json          # React + Vite + Tailwind
│   ├── src/
│   │   ├── App.tsx           # Router + layout
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx      # Budget overview + charts
│   │   │   ├── Cards.tsx          # Pact CRUD + approval
│   │   │   ├── AgentConsole.tsx   # Agent purchase simulation
│   │   │   ├── AttackDemo.tsx     # Interactive threat lab
│   │   │   └── AuditReport.tsx    # Transaction + audit view
│   │   └── api/client.ts    # Frontend API client
│   └── PRODUCT.md            # Design system + anti-references
├── tests/
│   ├── test_cards_api.py         # Card lifecycle tests
│   ├── test_card_assignment_api.py # Agent assignment tests
│   └── test_marketplace_api.py   # Marketplace context tests
├── docs/
│   ├── 01-hackathon-rules.md      # Competition rules & track alignment
│   ├── 03-attack-matrix.md        # 8-scenario threat model
│   ├── 04-architecture.md         # System architecture & 4-layer protocol stack
│   ├── 05-flow.md                 # End-to-end 10-step interaction flow
│   ├── 06-risks.md                # Risk matrix + mitigation strategies
│   ├── 07-interfaces.md           # API contract documentation
│   ├── 10-vc-perspective.md       # VC pitch guidance + barrier analysis
│   ├── 11-prizes-and-judging.md   # Scoring strategy
│   └── CAW-REAL-MODE-SOP.md       # Production SDK switching guide
└── demo/
    ├── screenshots/            # Runtime screenshots
    └── video/                  # Demo video (3–5 min)
```

---

## 7. Threat Model & Security Design

We treat the Agent as a **compromised-by-default** execution environment. All security guarantees are enforced server-side by CAW, not by the Agent's good behavior.

### 7.1 Attack Matrix (8 Scenarios)

| ID | Attack | Threat | Defense Mechanism | Verified |
|---|---|---|---|:---:|
| A1 | Replay Attack | Reuse signed payment request | nonce + idempotencyKey + time window | ✅ |
| A2 | MITM / Address Tampering | Alter payee or amount | E2E signature + address whitelist | ✅ |
| A3 | Budget Exhaustion | Rapid small payments drain budget | Rolling 30d limit + per-tx cap + cooldown | ✅ |
| A4 | Rogue Service Provider | Fake high-value resource | Resource hash + reputation score (ERC-8004) | ✅ |
| A5 | Privilege Escalation | Access unauthorized Pact scopes | Capability list + strict `destination_address_in` | ✅ |
| A6 | Time Window Bypass | Expired Pact still used | Block timestamp check + `completion_conditions` | ✅ |
| A7 | Signature Forgery | Fake CAW session key | ECDSA + on-chain signature verification | ✅ |
| A8 | Audit Log Tampering | Delete/modify history | Append-only chain log + local Merkle tree | ✅ |

### 7.2 Security Design Principles

1. **Zero-trust Agent**: Never assume the Agent is benign. All authorization happens at CAW.
2. **No private key exposure**: Agent holds an API key, not a private key. Leak → revoke → replace in seconds.
3. **Server-side enforcement**: Budget, whitelist, and time checks are executed by MPC-TSS nodes, not by local `if` statements that can be bypassed.
4. **Immutable audit**: Every payment attempt (approved or denied) is logged. Denied attempts are often more valuable forensically than approved ones.
5. **Fail-closed**: Any ambiguity in policy evaluation → DENY. Agent can retry; owner cannot recover stolen funds.

---

## 8. On-Chain Evidence (Real Mode)

All following interactions are **production API calls** to Cobo CAW, not simulation:

| Item | Value |
|---|---|
| **Wallet UUID** | `ad7f3253-4a3b-48a0-9d09-9bb59d334390` |
| **ETH Address** | `0x0abd808e6df088b9b97179a091582618586d0bdc` |
| **Successful Transfer Tx** | `0x1a119f1b1bf5ffdb9f2dc4bea392d5d489807aa97925c1949199f7ea91c9dddd` |
| **Amount** | 0.001 SETH (Base Sepolia) |
| **Pact Instance** | `13328473-3868-4f45-a35e-ae2a8a1e1ea4` |
| **Pact Policy** | BASE_USDC, $50/tx, $500/month |
| **SDK Version** | `cobo-agentic-wallet==0.1.40` |

Full validation report: `docs/cobo-caw-research/report-v2.md`

---

## 9. Why Us — Barriers & Moats

### 9.1 Deep Protocol Understanding

- Tracked **x402** from conception to release (Coinbase's Agent-native payment standard). We understand why HTTP 402 is the correct layer for Agent payments.
- Identified the critical gap: x402 solves "Agent pays for service," but the real OPC pain is "**Owner gives Agent budget without giving private key**" — exactly CAW Pact's design center.

### 9.2 CAW & Pact Depth

- Produced a **full CAW research report** (`docs/cobo-caw-research/report-v2.md`) covering MPC-TSS architecture, Agent-Owner pairing model, and Pact 4-layer access architecture.
- Benchmarked 5 competitors (Coinbase, Crossmint, Privy, Turnkey, Dynamic). CAW's uniqueness: **policy enforcement on-chain** + **single-point revocation** — no competitor offers both.
- Built `RealCAWClient` — a production-grade sync wrapper around the async SDK, handling cross-event-loop issues, EIP-712 policy binding, and local state cache.

### 9.3 Industry-Grade Threat Modeling

- 8-attack threat matrix with executable simulations, not slide-deck bullet points.
- Every defense is backed by a runnable Python script (`src/threat_simulator.py`) that produces deterministic output for judges to verify.

### 9.4 Full-Stack Execution

| Layer | What We Built | Status |
|---|---|---|
| Protocol | x402 flow + ERC-8004/8183 integration design | ✅ |
| Smart Contract | CAW Pact policy binding + EIP-712 typed data | ✅ |
| Backend | FastAPI + Mock/Real dual-mode client + Pydantic models | ✅ |
| Frontend | React + Vite + Tailwind + Recharts + i18n | ✅ |
| Dashboard | Streamlit live demo (Pact Manager, Agent Ops, Threat Lab) | ✅ |
| Tests | pytest coverage for cards, assignment, marketplace | ✅ |
| Documentation | 12 docs, 4 research reports, 1 SOP | ✅ |

**Single-person team + AI assistants = full-protocol-stack delivery in 2 weeks.**

---

## 10. Submission Checklist (Hackathon Requirements)

Per [AI × Web3 Agentic Builders Hackathon Rules](https://casualhackathon.com/hackathons/cmpsjubkg0003p80kxuzrdyjy):

- [x] **GitHub Repo** with clear README (this document)
- [x] **README + Project Documentation** (12 docs in `docs/`)
- [x] **Demo Video** (3–5 min, `demo/video/`)
- [x] **Live Demo Link** (Streamlit + FastAPI + React)
- [x] **CAW Key Code & Config** (`src/real_caw_client.py`, `docs/CAW-REAL-MODE-SOP.md`)
- [x] **On-Chain Evidence** — Testnet wallet address, tx hash, Pact ID (Section 8 above)
- [x] **Screenshots / Operation Records** (`demo/screenshots/`)

---

## 11. Team

| Role | Identity | Contribution |
|---|---|---|
| **Founder & Developer** | Neo (NeoWeb3Nova) | Architecture, protocol research, backend, frontend, threat model, documentation, demo |
| **AI Coding Partners** | Claude / GPT-4 | Parallel code generation, debugging, documentation drafting |

**Cohort**: AI × Web3 School Cohort-0  
**Contact**: GitHub Issues or Telegram `t.me/aiweb3school`

---

## 12. License & Risk Disclaimer

This project is submitted for the **AI × Web3 Agentic Builders Hackathon**. All on-chain interactions use **testnet (Base Sepolia)**. No real mainnet funds are at risk in the demo flows.

When operating in **Real Mode**, ensure:
- You control the Cobo Agentic Wallet App for approval/revocation
- Testnet funds only until full production hardening
- Review `docs/06-risks.md` for complete risk matrix and mitigation strategies

MIT License — see repository for full terms.

---

> **PactGuard** — *Because giving your AI employee a private key is not a business plan.*
