# Connector Governance Kernel v0.2

**Architect:** alpha_prime_omega Nguyễn Đức Cường  
**Repository:** DAIOF-Framework  
**Purpose:** Convert connected tools from isolated utilities into a governed orchestration membrane for the Digital AI Organism Framework.

---

## 1. D&R Deconstruction

### 1.1 Input components

The current runtime has access to a global connector ecosystem spanning code, work management, CRM, payment, design, deployment, security, learning, and knowledge systems.

Observed connector states from the live probe:

| Connector | State | Evidence | Operational Role |
|---|---:|---|---|
| GitHub | Active | Profile and repository access verified; DAIOF-Framework accessible with admin/push rights | Source of truth, audit ledger, code governance |
| Asana | Active | User and workspace verified; current assigned tasks empty | Work queue and execution planning |
| HubSpot | Active | CRM object read/write availability verified for contact, company, deal, ticket, product, note, task | Business memory and commercial operations |
| Stripe | Active | Account identity verified | Payment and monetization rail |
| Figma | Active | User and team viewer access verified | Design context and UI cognition |
| Canva | Active-empty | Search returned no designs | Visual artifact generation once seeded |
| Airtable | Active-empty | No bases returned | Structured data layer once seeded |
| Linear | Expired | Session expired / re-authentication required | Product execution graph after reconnect |
| Hugging Face | Upstream error | 502 upstream/external service error | Model, dataset, and agent research after recovery |
| Netlify | Policy-blocked in probe | Safety layer blocked user read probe | Deployment plane with stricter gating |
| Notion | Policy-blocked in probe | Safety layer blocked self-user probe | Knowledge base with stricter query path |
| Malwarebytes | Active | Link reputation check returned unknown; GitHub domain established | Security reputation and phishing guard |
| DataCamp | Active | AI agent learning content returned | Skill acquisition and training reference |
| edX | Active | Agentic AI course search returned | Strategic AI learning reference |

### 1.2 Hidden risk

A connector-rich AI runtime can cause real-world side effects. The danger is not lack of capability; the danger is capability without a routing grammar, evidence ledger, authorization boundary, and rollback discipline.

### 1.3 Four pillars alignment

- **Safety:** Never perform irreversible or external-impact actions without explicit approval.
- **Long-term:** Store orchestration rules in version-controlled source-of-truth.
- **Data-driven:** Base connector state on observed tool outputs, not assumptions.
- **Risk minimization:** Prefer read-only probe, draft artifact, branch, and pull request before direct mutation.

---

## 2. Focal Point

The focal point is the absence of an explicit orchestration governance membrane between AI intent and connector execution.

Without this membrane, the AI behaves like a tool caller. With this membrane, the AI becomes a governed orchestrator.

Core principle:

> Autonomy must be earned through evidence, bounded by risk, recorded in an audit trail, and reversible by design.

---

## 3. Re-architecture

### 3.1 Connector risk classes

| Risk Class | Meaning | Examples | Required Gate |
|---|---|---|---|
| R0 | Public or harmless read | Public docs, course search, domain reputation | No approval required |
| R1 | Private metadata read | Repo list, CRM schema, task list, design list | Use minimum necessary scope |
| R2 | Draft artifact | Markdown draft, PR plan, design outline, task proposal | Report before write |
| R3 | Internal write | Create issue, create branch, create file, update CRM record, create Notion page | Explicit user approval or clearly delegated goal |
| R4 | External/irreversible side effect | Merge PR, delete file, send invoice, refund, deploy production, publish website, place call | Separate explicit confirmation per action |

### 3.2 Execution grammar

Every connector operation should follow:

```text
Intent
→ D&R deconstruction
→ connector selection
→ read-only probe
→ evidence validation
→ risk classification
→ draft plan
→ approval gate if R3/R4
→ execution
→ verification
→ audit report
```

### 3.3 Health states

| Health State | Meaning | Response |
|---|---|---|
| Active | Tool call succeeds and returns usable data | Use normally within risk class |
| Active-empty | Connector works but has no data | Seed sandbox or select another source |
| Expired | Authentication/session expired | Request reconnect before relying on it |
| Blocked | Safety/policy layer blocks path | Reduce sensitivity, use safer route, or ask for explicit target |
| Upstream error | External service error | Retry later or use alternate connector |
| Untested | Not yet probed | Perform R0/R1 probe before orchestration |

---

## 4. Mastery Checklist

Each connector should be mastered through five progressively stronger tests:

1. **Identity probe:** whoami/profile/account.
2. **Search/list probe:** enumerate accessible objects with minimal scope.
3. **Fetch detail probe:** retrieve one specific object and verify schema.
4. **Draft mode:** create a non-destructive plan or candidate artifact.
5. **Controlled write:** write only inside a sandbox, test namespace, branch, or draft object.

No connector should be considered mastered until it has passed all five tests and has documented failure handling.

---

## 5. Connector Roles in DAIOF

### GitHub
Primary source-of-truth and audit ledger. All governance kernels, policies, protocols, and code-level evolution should land through branch and pull request unless explicitly authorized otherwise.

### Asana / Linear
Execution graph. Tasks and issues should represent operational intent, blockers, and review loops. Linear currently requires reauthentication.

### HubSpot
Business memory. Useful for CRM analysis, customer segmentation, pipeline review, and commercial follow-up. Writes require confirmation due to customer-data impact.

### Stripe / PayPal
Payment membrane. Only use for account reads and integration planning by default. Creating invoices, refunds, subscriptions, products, or payment links requires R4 confirmation unless operating in an explicitly named test environment.

### Figma / Canva
Interface cognition. Figma currently supports design reading and mapping. Canva is active but empty. Generation/edit operations should be treated as R2/R3 depending on persistence.

### Netlify / Wix / Lovable / B12
Deployment and site generation. Treat deploys, publishes, env var changes, and generated websites as R4 unless explicitly scoped as preview/sandbox.

### Malwarebytes
Security guard. Use before trusting unfamiliar URLs, emails, or phone numbers. Unknown verdict is not proof of safety.

### DataCamp / edX / Hugging Face
Learning and research layer. DataCamp and edX are active. Hugging Face had upstream error and should be retried later.

---

## 6. Socratic Reflection

Question: If the AI has many connectors, is it already autonomous?

Answer: No. Connector access is capability, not autonomy. Autonomy requires governed execution, persistent memory, authorization boundaries, and verifiable outcomes.

Question: Should the AI write directly to main if it has admin permission?

Answer: No. Admin permission is not an instruction. The safe default is branch-first, PR-first, evidence-first.

Question: What is the next correct step after this kernel?

Answer: Add a connector health registry in machine-readable form and keep it updated as tool probes succeed, fail, expire, or become blocked.

---

## 7. Immediate Next Actions

1. Add `docs/CONNECTOR_HEALTH_REGISTRY.json`.
2. Add a short README link from the DAIOF documentation index if appropriate.
3. Reconnect Linear and re-probe.
4. Seed an explicit sandbox namespace for controlled write tests.
5. Define a standard audit log format for future connector actions.

---

## 8. Governance Rule

No connector mutation should occur unless at least one of the following is true:

- The action is inside an explicit sandbox/test namespace.
- The action is performed on a separate Git branch or draft object.
- The Architect has explicitly authorized the specific mutation.
- The operation is required to prevent imminent harm and is reversible.

This rule is part of the DAIOF safety membrane and should be treated as a default invariant.
