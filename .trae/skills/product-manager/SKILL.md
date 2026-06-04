---
name: "product-manager"
description: |
  Build products users love with discovery, prioritization, roadmapping, and cross-functional leadership. Use when: defining product strategy, prioritizing features, creating roadmaps, conducting user research, leading cross-functional teams, making data-driven decisions.
  Triggers: "产品战略"、"需求优先级"、"产品路线图"、"用户研究"、"PRD"、"产品决策"
---

# Product Manager

Build products users love with discovery, prioritization, roadmapping, and cross-functional leadership.

## 🔴 CHECKPOINT · Before Starting

Confirm with user: "你的产品管理任务是什么？选择一个：[1]产品战略 [2]需求优先级 [3]路线图规划 [4]用户研究 [5]PRD撰写 [6]跨团队协作"

---

## Workflow 1: 产品战略定义

**Use when**: 用户需要定义产品方向和愿景

### Phase 1: 输入收集

**Step 1.1 — 收集业务背景**
```
Ask user:
- 当前产品阶段：种子期/早期/成长期/成熟期
- 核心用户群体：谁是我们的目标用户？
- 业务目标：本季度/本年度核心目标是什么？
- 约束条件：资源、技术、时间限制是什么？
```

**Step 1.2 — 🔴 CHECKPOINT · 确认输入**
展示收集到的信息，问用户："这些信息准确吗？需要补充什么吗？"

### Phase 2: 战略分析

**Step 2.1 — 市场分析框架**
```
输出：
1. 市场规模与趋势
2. 竞争格局（直接/间接竞品）
3. 机会空间（未满足的需求）
4. 威胁与风险
```

**Step 2.2 — 用户价值主张**
```
输出格式：
"为 [目标用户]，我们的产品 [产品名称] 提供 [核心价值]，与 [竞品] 相比，我们的独特优势是 [差异化点]。"
```

### Phase 3: 战略输出

**Step 3.1 — 产品愿景声明**
```
格式："在 [时间范围] 内，成为 [市场定位]，为 [用户] 创造 [价值]。"
```

**Step 3.2 — 战略支柱（3-5条）**
```
每条格式："[支柱名称] — 具体说明如何支撑愿景"
```

**Step 3.3 — 🔴 CHECKPOINT · 确认战略**
展示战略文档给用户，询问是否需要调整。

---

## Workflow 2: 需求优先级排序

**Use when**: 用户需要对需求列表进行优先级排序

### Phase 1: 需求收集

**Step 1.1 — 获取需求列表**
```
Input: 用户提供的需求列表（每条包含：需求描述、预估工作量）
Output: 整理后的需求清单
```

**Step 1.2 — 🔴 CHECKPOINT · 确认需求完整性**
"这是你提供的需求清单，有遗漏或需要修改的吗？"

### Phase 2: RICE 评分

**Step 2.1 — 定义评分标准**
```
Reach: 受影响用户数（季度）
Impact: 影响程度（0.25/0.5/1）
Confidence: 确定性（%）
Effort: 工作量（人月）
```

**Step 2.2 — 计算 RICE 分数**
```
Score = (Reach × Impact × Confidence) / Effort
```

**失败分支**:
- 如果缺少数据 → 提示用户补充关键信息
- 如果分数异常 → 检查计算是否正确

### Phase 3: MoSCoW 分类

**Step 3.1 — 按分数分组**
```
Must-have: 最高优先级，不做就失败
Should-have: 重要但可延后
Could-have: 锦上添花
Won't-have: 本周期不考虑
```

**Step 3.2 — 输出优先级矩阵**
```
展示格式：需求名称 | RICE分数 | MoSCoW分类 | 理由
```

---

## Workflow 3: 产品路线图规划

**Use when**: 用户需要规划产品时间线

### Phase 1: 范围定义

**Step 1.1 — 确定规划周期**
```
Ask: "规划周期是？[季度/半年/一年]"
```

**Step 1.2 — 收集输入**
```
- 战略目标（来自Workflow 1）
- 已排序的需求列表（来自Workflow 2）
- 资源限制（团队人数、技术依赖）
```

### Phase 2: 时间线编排

**Step 2.1 — 排期原则**
```
1. 先排 Must-have 需求
2. 考虑技术依赖顺序
3. 平衡团队负载
4. 预留 20% 缓冲时间
```

**Step 2.2 — 绘制路线图**
```
输出格式：
Q1: [里程碑1] | [需求A, 需求B]
Q2: [里程碑2] | [需求C, 需求D]
...
```

**Step 2.3 — 🔴 CHECKPOINT · 确认排期**
"这是初步排期，有冲突需要调整吗？"

---

## Workflow 4: 用户研究

**Use when**: 用户需要了解用户需求

### Phase 1: 研究设计

**Step 1.1 — 定义研究问题**
```
Ask: "你想通过研究回答什么问题？"
输出：3-5个具体研究问题
```

**Step 1.2 — 选择研究方法**
```
Options:
- 用户访谈（深度洞察）
- 问卷调查（定量数据）
- 可用性测试（产品体验）
- 数据分析（行为洞察）
```

### Phase 2: 执行与分析

**Step 2.1 — 访谈指南模板**
```
1. 开场（5min）：介绍目的，建立信任
2. 探索性问题（10min）：了解用户现状
3. 深入问题（15min）：挖掘痛点和需求
4. 收尾（5min）：感谢，邀请后续沟通
```

**Step 2.2 — 数据分析**
```
输出：
- 关键发现（Top 5）
- 用户画像
- 需求优先级排序
- 行动建议
```

---

## Workflow 5: PRD 撰写

**Use when**: 用户需要撰写产品需求文档

### Phase 1: PRD 结构

**Step 1.1 — 标准章节**
```
1. 背景与目标
2. 成功标准
3. 用户故事
4. 功能需求
5. 非功能需求
6. 验收标准
7. 风险与依赖
8. 发布计划
```

**Step 1.2 — 🔴 CHECKPOINT · 确认范围**
"需要包含哪些章节？有特殊格式要求吗？"

### Phase 2: 内容填充

**Step 2.1 — 用户故事模板**
```
As a [角色], I want [目标] so that [价值].
```

**Step 2.2 — 验收标准模板**
```
Given [前置条件], When [操作], Then [预期结果].
```

---

## 反例清单（What NOT to do）

1. **不要凭空制定战略** — 必须基于真实数据和用户反馈
2. **不要跳过检查点** — 每个阶段结束前必须获得用户确认
3. **不要只给框架不给方法** — 提供具体操作步骤和模板
4. **不要忽视技术可行性** — 排期前必须咨询技术团队
5. **不要承诺无法验证的目标** — 所有目标必须可量化
6. **不要在真空里做决策** — 跨团队对齐是必要步骤

---

## 失败处理

| 场景 | 处理方式 |
|------|----------|
| 用户信息不足 | 明确指出需要补充的信息，暂停执行 |
| 数据冲突 | 展示冲突点，让用户做最终决定 |
| 资源不足 | 调整优先级或拆分需求 |
| 时间冲突 | 重新排期或协商延期 |

---

## 输出质量检查

每次输出前检查：
- [ ] 目标明确
- [ ] 步骤可执行
- [ ] 数据来源清晰
- [ ] 有明确的成功标准
- [ ] 包含风险评估
- [ ] 有下一步行动建议
