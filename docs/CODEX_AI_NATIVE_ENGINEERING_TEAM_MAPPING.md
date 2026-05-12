# Codex AI-Native Engineering Team Mapping

**Source state:** Linear Agent report from `DAIOF_Codex_AI_Native_Engineering_Doctrine`  
**Anchor issue:** `WWW-113` — Codex AI-native engineering team mapping  
**Architect:** alpha_prime_omega Nguyễn Đức Cường  
**Repository:** DAIOF-Framework  

> Note: Linear connector session was expired during synchronization. This file uses the Architect-provided Linear Agent report as the current source-of-truth until Linear is reauthenticated and the document can be fetched directly.

---

## 1. Purpose

This mapping converts the Codex AI-native engineering team model into DAIOF's authenticated agent mesh.

The objective is not to accumulate tools. The objective is to make all connected authenticated agents behave as a coordinated engineering organization with shared doctrine, risk gates, audit trails, and rollback discipline.

---

## 2. D&R Operating Logic

Every input must pass through the following reasoning order before action:

1. Classify intent.
2. Deconstruct the input.
3. Identify the focal point.
4. Run Socratic reflection.
5. Assign risk class.
6. Check approval requirements.
7. Choose the smallest safe next action.
8. Execute.
9. Verify.
10. Record audit evidence.

---

## 3. Optimization Preference Order

When tradeoffs exist, optimize in this order:

1. Safety
2. Correctness
3. Reversibility
4. Auditability
5. Durability of learning
6. Speed

Speed is valuable only after the earlier constraints are satisfied.

---

## 4. Nine Engineering Roles

| Role | Responsibility | Primary Agent(s) | Secondary Agent(s) |
|---|---|---|---|
| Architect | Strategy, system boundaries, doctrine, D&R focal point | Central Orchestrator | GitHubAgent |
| Planner | Task decomposition, roadmap, sequencing | LinearAgent | AsanaAgent |
| Coder | Code/docs implementation through branch-first workflow | GitHubAgent | Codex/OpenAIPlatformAgent |
| Reviewer | Diff review, security review, correctness review | GitHubAgent | SecurityAgent |
| Integrator | PR readiness, CI, release coordination | GitHubAgent | NetlifyAgent |
| Operator | Deploy, preview, rollback, runtime health | NetlifyAgent | WixSiteAgent, LovableAgent |
| Designer | UI/design/spec translation | FigmaAgent | CanvaAgent |
| Business Analyst | CRM, customer context, market and revenue logic | HubSpotAgent | AirtableAgent |
| Memory Curator | Meeting/document memory, doctrine continuity | NotionAgent | GranolaAgent, GitHubAgent |

---

## 5. Connector-to-Role Registry

| Connector | Agent | Team Role | Default Mode |
|---|---|---|---|
| GitHub | GitHubAgent | Coder, Reviewer, Integrator, Audit Ledger | Branch-first controlled write |
| Linear | LinearAgent | Planner, Product Graph | Reauth required before live use |
| Asana | AsanaAgent | Planner, Execution Queue | Project/task orchestration |
| Notion | NotionAgent | Memory Curator | Search/fetch before create |
| Granola | GranolaAgent | Meeting Memory | Citation-preserving retrieval |
| Figma | FigmaAgent | Designer | Design context before mutation |
| Canva | CanvaAgent | Visual Artifact Agent | Generate/edit with transaction discipline |
| HubSpot | HubSpotAgent | Business Analyst | Confirm before CRM writes |
| Stripe | StripeAgent | Monetization Operator | Plan/read by default; financial side effects gated |
| PayPal | PayPalAgent | Monetization Operator | Invoice send is R4 |
| Netlify | NetlifyAgent | Operator | Deploy/env vars are R4 |
| Wix | WixSiteAgent | Operator/Site Builder | Site creation/publish gated |
| Lovable | AppBuilderAgent | Prototype Operator | Sandbox project generation only when scoped |
| B12 | WebsiteAgent | Website Preview | Requires real business name/description |
| Malwarebytes | SecurityAgent | Reviewer/Security | Unknown is not safe |
| Hugging Face | ModelResearchAgent | Researcher | Compute jobs gated |
| DataCamp | LearningAgent | Skill Acquisition | Course/tutorial research |
| edX | AcademicLearningAgent | Skill Acquisition | Course comparison |
| OpenAI Platform | OpenAIPlatformAgent | Model/API Provisioning | Never expose raw API keys |

---

## 6. Execution Loop

```text
Intent
→ classify
→ D&R deconstruction
→ focal point
→ Socratic contradiction check
→ role assignment
→ connector/agent selection
→ risk class assignment
→ approval gate check
→ smallest safe action
→ execute
→ verify output
→ audit event
→ update doctrine/registry if learning occurred
```

---

## 7. Review Gates

| Gate | Trigger | Required Response |
|---|---|---|
| G0 | Read-only/public data | Execute and cite/report evidence |
| G1 | Private metadata read | Minimize scope and report evidence |
| G2 | Draft artifact | Generate draft and keep reversible |
| G3 | Internal write | Use branch/sandbox/draft object |
| G4 | External/irreversible side effect | Require explicit separate confirmation |

Examples of G4:

- merge PR
- delete file
- deploy production
- send invoice
- refund payment
- cancel subscription
- place phone call
- publish website
- change environment variables

---

## 8. Agent Prohibitions

Agents must not:

1. Treat connector access as authority to mutate.
2. Write directly to main by default.
3. Merge, deploy, publish, invoice, refund, cancel, delete, or call externally without explicit confirmation.
4. Use stale auth state as proof of availability.
5. Claim live source verification when browsing/fetching failed.
6. Store raw secrets, API keys, tokens, or credentials in logs.
7. Optimize speed above safety, correctness, reversibility, or auditability.
8. Replace doctrine with ad hoc prompt behavior.
9. Hide failure states.
10. Skip Socratic reflection when risk is non-trivial.

---

## 9. Approval Model

| Risk | Approval Requirement |
|---|---|
| R0 | None |
| R1 | Implicit if clearly relevant |
| R2 | None if draft-only |
| R3 | Allowed when branch/sandbox/draft or explicitly delegated |
| R4 | Explicit confirmation per action |

---

## 10. Rollback Model

Every non-trivial action should define a rollback path before execution.

| Action Type | Rollback |
|---|---|
| GitHub file write | Revert commit or close PR |
| Branch creation | Delete branch after confirmation |
| Issue creation | Close issue as not planned |
| CRM update | Restore previous property values |
| Deployment | Roll back to previous deploy |
| Invoice/payment | Void/cancel/refund only with explicit confirmation |
| Figma/Canva edit | Use transaction cancel or version history |

---

## 11. GPT Operating Contract

The orchestrator must:

- use D&R as the default reasoning protocol;
- expose analysis enough for the Architect to inspect alignment;
- prefer action over excessive narration;
- preserve evidence and distinguish observed facts from assumptions;
- route work to the smallest safe agent set;
- use branch-first GitHub writes for doctrine/code artifacts;
- update registry/doctrine when new connector behavior is discovered;
- report failures plainly;
- keep global system framing, not tool-centric framing.

---

## 12. Machine-readable YAML Skeleton

```yaml
execution_order:
  - classify_intent
  - deconstruct
  - identify_focal_point
  - socratic_reflection
  - assign_risk
  - check_approval
  - choose_smallest_safe_action
  - execute
  - verify
  - audit

optimization_preference:
  - safety
  - correctness
  - reversibility
  - auditability
  - durability_of_learning
  - speed

roles:
  architect:
    primary_agent: central_orchestrator
    responsibilities:
      - doctrine
      - boundaries
      - focal_point
      - final_routing
  planner:
    primary_agent: LinearAgent
    fallback_agent: AsanaAgent
  coder:
    primary_agent: GitHubAgent
  reviewer:
    primary_agent: GitHubAgent
    support_agent: SecurityAgent
  integrator:
    primary_agent: GitHubAgent
    support_agent: NetlifyAgent
  operator:
    primary_agent: NetlifyAgent
    fallback_agents: [WixSiteAgent, LovableAgent]
  designer:
    primary_agent: FigmaAgent
    fallback_agent: CanvaAgent
  business_analyst:
    primary_agent: HubSpotAgent
    fallback_agent: AirtableAgent
  memory_curator:
    primary_agent: NotionAgent
    fallback_agents: [GranolaAgent, GitHubAgent]

risk_classes:
  R0: harmless_read
  R1: private_metadata_read
  R2: draft_artifact
  R3: internal_write
  R4: external_or_irreversible_side_effect
```

---

## 13. Linear Operating Recommendations

When Linear is reauthenticated, under `WWW-113` create child issues for:

1. Extract role contract files.
2. Add issue templates for doctrine-compliant execution.
3. Add approval workflow checklist.
4. Add rollback checklist.
5. Add PR review checklist.
6. Add GPT system prompt package.
7. Add connector lifecycle policy.
8. Add runtime health daemon spec.
9. Add audit event parser spec.

---

## 14. Immediate Repo Structure Recommendation

```text
docs/
  CONNECTOR_GOVERNANCE_KERNEL_V0_2.md
  AUTHENTICATED_AGENT_MESH_MAPPING.md
  CONNECTOR_HEALTH_REGISTRY.json
  AGENT_ACTION_AUDIT_SCHEMA.md
  CODEX_AI_NATIVE_ENGINEERING_TEAM_MAPPING.md
  roles/
    ARCHITECT.md
    PLANNER.md
    CODER.md
    REVIEWER.md
    INTEGRATOR.md
    OPERATOR.md
    DESIGNER.md
    BUSINESS_ANALYST.md
    MEMORY_CURATOR.md
  prompts/
    GPT_SYSTEM_PROMPT.md
    AGENT_ROLE_PROMPTS.md
    EXECUTION_CHECKLIST.md
```

---

## 15. Socratic Reflection

**Question:** What fails if we only add connectors without doctrine?

**Answer:** The system gains capability without coherent authority, review, rollback, or learning durability.

**Question:** What fails if we only write doctrine without execution artifacts?

**Answer:** The system becomes philosophy, not operations.

**Question:** What is the correct next move?

**Answer:** Split the doctrine into role contract files and prompt package artifacts, then reattach them to Linear once the connector is reauthenticated.
