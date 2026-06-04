---
name: "product-manager-skills"
description: |
  PM skill for diagnosing SaaS metrics, critiquing PRDs, planning roadmaps, running discovery, coaching PM career transitions. Use when: analyzing product metrics, writing or reviewing PRDs, planning roadmaps, conducting user research.
  Triggers: "分析产品指标"、"审查PRD"、"规划路线图"、"用户研究"、"产品经理职业发展"
---

# Product Manager Skills

A structured PM toolkit for diagnosing SaaS metrics, critiquing PRDs, planning roadmaps, running discovery, and coaching career transitions.

## 🔴 CHECKPOINT · Before Starting Any PM Task

Confirm with user: "你现在的PM任务是什么？分析指标 / 写PRD / 规划路线图 / 用户研究 / 职业发展？" This routes to the correct workflow.

## PM Workflows

### Workflow A: SaaS Metrics Diagnosis

**Use when**: user wants to analyze product business performance

**Step A1 — Gather metrics**
Input: which metrics to analyze (from user's scope at checkpoint)
```
Ask user for:
- MRR, ARR, churn rate, NDR (if available)
- CAC, LTV, Payback Period
- DAU/MAU, feature adoption
```
**If user has no data → STOP. Do not fabricate numbers. Tell user what data is needed.**

**Step A2 — Apply diagnostic frameworks**

For each metric the user provides:
```
Metric: [X]
Healthy benchmark: [Y]
User's value: [Z]
Gap: [Analysis]
Root cause hypothesis: [1-2 sentences]
Recommended action: [specific next step]
```

**Step A3 — Prioritize with RICE**
```
Score = (Reach × Impact × Confidence) / Effort

RICE components (define for each proposed initiative):
- Reach: # users affected per quarter
- Impact: 0.25 (minimal) / 0.5 (moderate) / 1 (massive)
- Confidence: % certainty on estimates
- Effort: person-months required
```

**Step A4 — 🔴 CHECKPOINT · Present findings**
Show: diagnostic summary + top 3 priority actions
"If this analysis is directionally correct, I'll draft a deeper investigation plan. Continue?"

---

### Workflow B: PRD Critique

**Use when**: user shares a PRD or wants to review a product requirement doc

**Step B1 — Receive PRD content**
Input: user's PRD text/link
Output: raw content for analysis

**Step B2 — Systematic critique**

For each section of the PRD:
```
Section: [Name]
Completeness: ✓ Complete / ⚠️ Missing / ✗ Absent
Issues found: [Specific problems — one per line]
Severity: 🔴 Critical / 🟡 Warning / 🟢 Minor
```

**Required PRD sections — flag as missing if absent:**
1. **Goal** — What success looks like
2. **Non-goals** — What is explicitly out of scope
3. **User stories** — At least one concrete scenario
4. **Success metrics** — Measurable KPIs with targets
5. **Edge cases** — Known failure modes
6. **Dependencies** — What other teams/systems are required
7. **Rollout plan** — How this gets to users

**Step B3 — Score the PRD**

| Dimension | Score | Criteria |
|-----------|-------|----------|
| Clarity | 1-5 | Is every requirement unambiguous? |
| Completeness | 1-5 | Are all 7 sections present? |
| Feasibility | 1-5 | Are tech constraints identified? |
| Testability | 1-5 | Can each requirement be verified? |
| Alignment | 1-5 | Does it tie to business goals? |

**Step B4 — 🔴 CHECKPOINT · Present critique**
"If the critical issues are addressed, I can write an improved version. Which issues should we prioritize?"

---

### Workflow C: Roadmap Planning

**Use when**: user wants to plan a product roadmap

**Step C1 — Scope definition**
```
Input: planning horizon (Q1-Q4 / 6 months / 1 year)
Output: confirmed scope + user confirmation
```
**🔴 CHECKPOINT · Confirm scope before planning anything**

**Step C2 — Gather inputs**
```
From user, gather:
- Strategic goal (1 sentence): what are we optimizing for this period?
- Constraints (time/resources/tech): what limits us?
- Current initiatives in flight: what's already committed?
- Known opportunities: top 3 opportunities already identified
```

**Step C3 — Apply MoSCoW + RICE**

For each proposed initiative:
```
Initiative: [Name]
→ MoSCoW: Must / Should / Could / Won't
→ RICE score: [calculated]
→ Strategic alignment: High / Medium / Low
→ Dependencies: [list]
→ Risk: [description + mitigation]
```

**Step C4 — Sequence into timeline**

```
Quarter 1:
- [Initiative A] — MoSCoW: Must, RICE: X, Strategic: High
  Fallback if blocked: [alternative]
- [Initiative B] ...

Quarter 2: ...
```

**Step C5 — 🔴 CHECKPOINT · Present roadmap**
"Here's a draft roadmap. Adjust timeline/priorities?"

---

### Workflow D: Product Discovery

**Use when**: user wants to understand a user problem or validate a solution

**Step D1 — Problem framing**
```
Ask user: "What problem are we trying to solve? For whom? In what context?"
Output: confirmed problem statement
```

**Step D2 — Research design**
```
Research type:
- Customer interviews (3-5 sessions, 30min each)
- Survey (if >20 data points needed)
- Data analysis (if behavioral data available)
- Competitive analysis (if market context needed)

Research questions (3-5 max):
1. [Specific, answerable question]
2. ...
```

**Step D3 — Interview guide structure (if interviews selected)**
```
Opening (5min): Rapport, purpose
Questions:
1. "Tell me about the last time you [did X related to problem]"
2. "What makes that difficult?"
3. "How do you currently solve this?"
4. "What would an ideal solution look like?"
5. "What would have to be true for you to switch?"
Closing: "Is there anything I should have asked but didn't?"
```

**Step D4 — 🔴 CHECKPOINT · Confirm research plan**
"Before we start recruiting participants — does this research design answer your core question?"

---

## Key SaaS Metrics Reference

### Growth (diagnose with Workflow A)
| Metric | Healthy Benchmark |
|--------|-----------------|
| MRR Growth | >10% MoM for early-stage |
| NDR | >110% indicates expansion > churn |
| CAC Payback | <12 months; <6 months ideal |
| LTV:CAC | >3:1 |

### Retention (diagnose with Workflow A)
| Metric | Healthy Benchmark |
|--------|-----------------|
| Gross Churn | <5% MoM for SMB |
| Logo Retention | >90% quarterly |
| DAU/MAU | >20% indicates strong engagement |

## Key Frameworks Reference

| Framework | When to Use |
|-----------|-------------|
| RICE | Prioritizing features/initiatives |
| MoSCoW | Scope negotiation |
| JTBD | Understanding user motivation |
| Double Diamond | Discovery + definition process |
| OKR | Quarterly goal setting |

## Anti-Patterns (What NOT to do)

- Do NOT give advice without asking what data is available first — numbers matter
- Do NOT prioritize without knowing strategic constraints — RICE without context is math theater
- Do NOT write a PRD without confirming scope — "full-featured PRD" without boundaries is not helpful
- Do NOT recommend roadmap items without user sign-off — PM owns the roadmap, you facilitate
- Do NOT present unvalidated user needs as facts — always label assumptions explicitly
- Do NOT use framework names without explaining what they mean in plain language
