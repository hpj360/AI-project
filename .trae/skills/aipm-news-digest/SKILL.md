---
name: "aipm-news-digest"
description: |
  AI Product Manager daily intelligence digest. Use when: preparing morning briefings, analyzing AI/ML trends, monitoring competitor launches, tracking funding news.
  Triggers: "AI资讯"、"今日AI新闻"、"产品经理日报"、"AI行业动态"、"AI趋势分析"
---

# AIPM News Digest

AI Product Manager daily intelligence digest. Fetches and synthesizes news from curated RSS/API sources into structured briefings.

## 🔴 CHECKPOINT · Before Publishing

Confirm the briefing scope with user: "要覆盖哪些分类？需要包含竞品动态/论文/融资/产品发布中的哪些？"

## Core Workflow

### Phase 1: Source Selection

**Step 1.1 — Identify relevant sources**

Input: user's briefing scope
Output: ordered list of RSS/API endpoints to query

| Category | Source | Endpoint Pattern |
|----------|--------|-----------------|
| AI/ML Labs | OpenAI Blog | https://openai.com/blog/rss.xml |
| AI/ML Labs | DeepMind Blog | https://deepmind.com/blog/feed/basic/ |
| AI/ML Labs | Google AI Blog | https://blog.google/technology/ai/rss/ |
| AI/ML Labs | Meta AI | https://ai.meta.com/blog/rss/ |
| AI/ML Labs | Microsoft Research | https://www.microsoft.com/en-us/research/feed/ |
| Research | arXiv cs.AI | https://export.arxiv.org/rss/cs.AI |
| Research | arXiv cs.LG | https://export.arxiv.org/rss/cs.LG |
| Tech Media | TechCrunch | https://techcrunch.com/feed/ |
| Tech Media | The Verge | https://www.theverge.com/rss/index.xml |
| Developer | Hacker News | https://hnrss.org/frontpage |
| Developer | GitHub Trending | https://api.github.com/search/repositories?q=stars:>1000+pushed:>DATE |
| PM | Product Hunt | https://feed.producthunt.com/posts.rss |
| PM | Lenny's Newsletter | https://www.lennysnewsletter.com/rss |
| Funding | Crunchbase News | https://techcrunch.com/feed/ (filter funding keywords) |

**If source URL is unreachable → fallback to cached version or skip with note:**
```
"⚠️ [Source Name] unreachable — skipping. Last known: [last title from memory]"
```

**Step 1.2 — Fetch content**
```
# RSS via curl
curl -fsSL --max-time 30 "<rss-url>" | grep -o '<title>[^<]*</title>\|<link>[^<]*</link>' | head -40

# If curl fails → try wget
wget -qO- --timeout=30 "<rss-url>" 2>/dev/null | grep -o '<title>[^<]*</title>' | head -20

# If network fails → output: "[Source]: Unable to fetch — no recent data"
```

---

### Phase 2: Filtering & Prioritization

**Step 2.1 — Apply user scope filter**

Input: fetched items, user's scope (from Phase 1 checkpoint)
Output: filtered item list

**Filter by priority:**
1. **P0 — Must include**: AI breakthrough announcements, major product launches, funding >$50M, regulatory news
2. **P1 — Include if recent**: competitor feature releases, significant research papers, industry analyst reports
3. **P2 — Include if space**: minor tool releases, community updates, opinion pieces

**Step 2.2 — Deduplicate across sources**
```
If same story appears in multiple sources → keep the most authoritative source (research paper > official blog > tech media > social)
```

---

### Phase 3: Briefing Generation

**Step 3.1 — Write structured digest**

Output format — adapt sections to user's scope from Phase 1:

```markdown
## [DATE] AI Product Manager Daily Digest

### 🔥 Top Stories (P0)
- **[Headline] — [Source]**
  Why it matters: [1-2 sentences on product strategy implication]
  Action: [specific recommendation — feature to explore / risk to monitor]

### 🤖 AI/ML Developments
- **[Model/Research Name]** — [Source]
  What's new: [1-sentence summary]
  Impact: [how this affects product roadmap]
  Relevance: High / Medium / Low

### 📦 Product Launches
- **[Company] [Product/Feature]** — [Source]
  Competitive angle: [how this changes the landscape]
  Response options: [monitor / fast-follow / differentiate]

### 💰 Funding & M&A
- **[Company] raises $[Amount] [Round]** — [Source]
  Significance: [market signal interpretation]
  Watch for: [competitive threat or opportunity]

### 📄 Key Papers
- **[Paper Title]** — [arXiv/Meta/Google]
  TL;DR: [2-3 sentence summary]
  Product potential: [specific feature idea or technology application]

### 📊 Weekly Trend Indicator
[1-paragraph synthesis of patterns across sources this week]
```

**Step 3.2 — Add PM-specific annotations**
For each story, add:
- `Product angle`: what this means for a PM building AI-powered products
- `Confidence`: how reliable this signal is (official source / rumor / early)
- `Time horizon`: immediate (<1 week) / short-term (1-4 weeks) / long-term (>1 month)

---

### Phase 4: Review & Deliver

**🔴 CHECKPOINT · Before sending**
Present draft to user and ask:
"这份简报覆盖了 [N] 条内容。要调整范围/深度/格式吗？"

**If user approves → finalize and deliver**
**If user requests changes → go back to Phase 1.1 with adjusted scope**

---

## Fallback Behavior

**If ALL sources fail (network offline):**
```
⚠️ Unable to fetch live data.

Fallback options:
1. Search cached memory for recent AI news
2. Use web search: "site:openai.com OR site:deepmind.com this week"
3. Ask user to provide specific topics to research manually

Output: "AI Digest unavailable — [reason]. Recommend checking manually at:
• https://openai.com/blog
• https://news.ycombinator.com
• https://techcrunch.com/category/artificial-intelligence/"
```

**If RSS feed is broken (returns HTML instead of XML):**
→ Skip that source, note in output: "⚠️ [Source] feed unavailable"

**If arXiv returns rate-limited:**
→ Reduce to top 5 papers only, add note: "⚠️ arXiv rate-limited — showing top 5 papers"

---

## Anti-Patterns (What NOT to do)

- Do NOT include every fetched item — filter aggressively to P0/P1 only. User's time is valuable.
- Do NOT present rumors as confirmed news — label unverified claims clearly.
- Do NOT skip the Phase 4 checkpoint — always let user review before finalizing.
- Do NOT omit the "why it matters for PMs" angle — generic news summaries are useless to PMs.
- Do NOT include fundraising rounds under $10M — noise, not signal.
- Do NOT guess at product implications — if unsure, say "implication unclear — monitor."

## Use Case Routing

| User says | Route to |
|-----------|----------|
| "今日AI资讯" | Full digest (all categories) |
| "看一下最近AI论文" | Filter: research papers only |
| "竞品动态" | Filter: Product Launches + Tech Media |
| "融资新闻" | Filter: Funding & M&A only |
| "我只需要最重要的三条" | P0 stories only, Phase 3 output |

## Output Quality Gates

Before delivering, verify:
- [ ] At least 1 P0 story included (or clear note if none found)
- [ ] Every story has "Product angle" annotation
- [ ] Source attribution present for every item
- [ ] No story is duplicated across sections
- [ ] Confidence level labeled on each item
