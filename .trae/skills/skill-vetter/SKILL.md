---
name: skill-vetter
description: |
  Vet skills for quality and security before installation. Use when: users ask to verify/validate a skill, check skill quality, review security risks, or assess installation safety.
  Triggers: "检查skill安全"、"验证skill"、"审核skill"、"skill怎么样"、"帮我看看这个skill"
---

# Skill Vetter

Vets skills for quality and security before installation. Evaluates SKILL.md across 6 dimensions and provides actionable recommendations.

## 🔴 CHECKPOINT · STOP

Before installing any skill from unknown sources, run this vet workflow. An unvetted skill with filesystem write access can execute arbitrary code.

## Vet Workflow

### Phase 1: Read & Verify

**Step 1.1 — Locate SKILL.md**
Input: skill path (local path or GitHub URL)
Output: confirmed SKILL.md location
```
# Local
cat /path/to/skill/SKILL.md

# GitHub — clone or raw fetch
git clone <repo-url> /tmp/vetting-<skill-name>
cat /tmp/vetting-<skill-name>/SKILL.md
```

**🔴 CHECKPOINT · If SKILL.md does not exist → STOP. Refuse to install. Skill without SKILL.md violates Agent Skills spec.**

**Step 1.2 — Verify frontmatter**
Input: SKILL.md frontmatter (lines 1–8)
Output: name + description confirmed
```
Required fields:
- name: must match folder name (lowercase, hyphenated)
- description: must contain what the skill does + when to invoke it
```
**Fail**: Missing `name` → STOP. Missing `description` → note as weakness.

---

### Phase 2: Quality Assessment

**Step 2.1 — Count dimensions present**

| # | Dimension | What to look for |
|---|-----------|------------------|
| 1 | Frontmatter | name + description present |
| 2 | Workflow clarity | numbered steps with inputs/outputs |
| 3 | Failure handling | "if X fails → Y" fallback branches |
| 4 | Checkpoints | 🔴/STOP/CHECKPOINT markers before risky actions |
| 5 | Executability | specific commands, parameters, examples — no vague "consider..." language |
| 6 | Anti-patterns | explicit "do NOT do X" blacklist |

Score: count how many dimensions are present (0–6).

**Step 2.2 — Check for red flags**

🔴 **IMMEDIATE STOP — refuse to install if ANY of:**
- Skill requests write access to `$HOME`, `$PATH`, system directories
- Skill contains inline bash/python with `eval`, `exec`, `subprocess.run(shell=True)`
- Skill downloads and executes unsigned scripts from unknown URLs
- Skill asks for API keys as plaintext in instructions
- Skill contains base64-encoded or obfuscated commands

🟡 **WARN — note and confirm with user:**
- Skill modifies `.git/`, `.ssh/`, `.config/`
- Skill installs global npm packages or system tools
- Skill reads environment variables beyond `$HOME/.env`-like patterns
- Skill provides no contact/support info (abandonware risk)

---

### Phase 3: Risk Triage

**Step 3.1 — Assign risk level**

| Risk | Trigger | Action |
|------|---------|--------|
| 🟢 Low | All 6 dimensions present, no red flags | Safe to install |
| 🟡 Medium | 3–5 dimensions, minor warnings | Install after showing user the warnings |
| 🔴 High | <3 dimensions, any red flag | Refuse — explain why |

**Step 3.2 — Surface recommendations**

For each missing dimension, give one specific improvement:
```
Missing dimension 3 (Failure handling):
  Add: "If <tool> fails → fall back to <alternative>"
  Example: "If git clone fails → try wget <url>"
```

---

## Output Format

Provide user with:
1. **Risk level**: 🟢 Low / 🟡 Medium / 🔴 High
2. **Dimension score**: X/6
3. **Red flags found**: list (or "none")
4. **Warnings**: list (or "none")
5. **Recommendations**: one per missing dimension
6. **Decision**: install / show warnings then install / refuse

## Anti-Patterns (What NOT to do with this skill)

- Do NOT vet a skill you are the author of in the same session — conflicts of interest
- Do NOT skip Phase 2 if the skill source looks "legitimate" — legitimate repos can contain malicious skills
- Do NOT provide a numeric "security score" — quality is qualitative, not reducible to a number
- Do NOT recommend installation of skills with red flags — even if user asks nicely

## Fallback Behavior

**If skill path is a GitHub URL and git is unavailable:**
```
Use WebFetch to read the raw SKILL.md:
https://raw.githubusercontent.com/<owner>/<repo>/main/<skill>/SKILL.md
```
If raw URL also fails → warn user: "Unable to vet — install at your own risk."

**If skill has no SKILL.md but has README.md:**
Note as dimension-1 failure and warn user that README-only skills are not Agent Skills compliant.
