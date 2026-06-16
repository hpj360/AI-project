# Skill 质量评估框架

基于 Anthropic《Demystifying evals for AI agents》和 OpenAI《Eval skills》方法论，结合项目实际，建立三层评分体系。

## 评估体系架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Skill 质量评估框架                         │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: 确定性评分 (20%)                                  │
│    ├── 结构合规性 (10分) — 脚本自动检查                      │
│    ├── 执行效率 (5分) — 脚本自动检查                         │
│    └── 稳定性指标 (5分) — 脚本自动检查                       │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: 模型评分 (60%)                                    │
│    ├── 内容质量 (20分) — LLM 按 Rubric 评分                  │
│    ├── 工作流清晰度 (15分) — LLM 按 Rubric 评分              │
│    ├── 失败处理覆盖 (15分) — LLM 按 Rubric 评分              │
│    └── 反例与黑名单 (10分) — LLM 按 Rubric 评分              │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: 人工审核 (20%)                                    │
│    ├── 复杂场景覆盖 (10分) — 人工检查清单                    │
│    ├── 可维护性 (5分) — 人工检查清单                         │
│    └── 用户体验 (5分) — 人工检查清单                         │
└─────────────────────────────────────────────────────────────┘
```

## 评分标准

### 总分 100 分，等级划分

| 等级 | 分数 | 说明 | 行动 |
|------|------|------|------|
| A+ | 90-100 | 优秀 | 可作为标杆，推广最佳实践 |
| A | 80-89 | 良好 | 质量合格，小优化即可 |
| B | 70-79 | 合格 | 需要针对性改进 |
| C | 60-69 | 需改进 | 存在明显缺陷，需重构 |
| D | 40-59 | 较差 | 严重影响使用，必须重写 |
| F | 0-39 | 不合格 | 无法使用，建议删除 |

### 关键指标

- **pass@1**：单次评估达标的概率（峰值能力）
- **pass^3**：连续 3 次评估都达标的概率（稳定性）
- **达标阈值**：T = 70 分（B 等级）

## 评估工具

### 1. 单 Skill 评估

```bash
python3 evals/scripts/skill_evaluator.py <skill-path> [--json]
```

输出：总分、三维度得分、问题列表、改进建议、人工审核清单。

### 2. 批量评估

```bash
python3 evals/scripts/batch_eval.py [--skills-dir DIR] [--output DIR]
```

输出：全量排名、等级分布、Top/Bottom 列表、JSON + Markdown 报告。

### 3. 基线对比

```bash
# 保存当前评估为基线
python3 evals/scripts/skill_evaluator.py <skill-path> --json > evals/baseline/<skill-name>.json

# 后续对比
python3 evals/scripts/skill_evaluator.py <skill-path> --baseline evals/baseline/<skill-name>.json
```

## 基线管理

### 基线建立流程

1. **初始评估**：对新 skill 执行完整评估
2. **人工确认**：检查人工审核清单，确认复杂场景覆盖
3. **记录基线**：将评估结果保存到 `evals/baseline/<skill-name>.json`
4. **版本关联**：基线随代码仓库版本化管理

### 基线更新时机

| 场景 | 操作 |
|------|------|
| Skill 逻辑变更 | 重新评估，对比基线，确认改进 |
| 模型升级 | 重新评估，更新基线 |
| 新增用例 | 补充基线覆盖 |
| 发现 Bad Case | 新增用例，记录基线 |

### 基线数据内容

```json
{
  "skill": "wechat-reader",
  "version": "1.0.0",
  "baseline_at": "2026-06-16T12:00:00",
  "evaluator_version": "1.0",
  "total_score": 83.4,
  "scores": {
    "deterministic": 18.5,
    "model": 50.0,
    "human": 14.9
  },
  "issues": [],
  "recommendations": []
}
```

## 回归测试流程

### 触发时机

- **PR 合入前**：对修改的 skill 执行快速评估
- **定期巡检**：每周全量评估，生成趋势报告
- **模型升级后**：全量评估，对比基线

### 执行模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| 快速评估 | 单 skill 评估，1 轮 | 日常开发调试 |
| 全量回归 | 所有 skill 评估，3 轮 | 版本验收、模型升级 |
| 定向评估 | 指定 skill 列表 | PR 合入前验证 |

### 稳定性判定

```
单次 Trial:  trial_score = 评估得分
d达标判定:   trial_pass = (trial_score >= 70)
Skill 总分:  skill_score = avg(所有 trial_score)  若全部 trial_pass
              skill_score = 0                      若任一 trial 不达标
```

**"0 容忍"策略**：对于关键 skill（如 wechat-reader、douyin-reader），任一 trial 不达标即判定不通过。

## 用例集设计

### 用例分类

| 分类 | 说明 | 示例 |
|------|------|------|
| 正常用例 | 标准输入，预期成功 | 提供有效微信文章链接 |
| 边界用例 | 极端输入，测试鲁棒性 | 提供已删除的文章链接 |
| 错误用例 | 错误输入，测试失败处理 | 提供非微信链接 |
| 复杂用例 | 多步骤/多资源，测试完整性 | 批量处理多个链接 |

### 用例定义格式

```yaml
skill: wechat-reader
test_cases:
  - id: TC001
    name: 正常微信文章读取
    input: "https://mp.weixin.qq.com/s/xxxxx"
    expected:
      - success: true
      - title: not empty
      - content_markdown: length > 500
    
  - id: TC002
    name: 验证码拦截处理
    input: "https://mp.weixin.qq.com/s/xxxxx"
    pre_condition: "文章触发验证码"
    expected:
      - fallback_triggered: true
      - error_message: contains "验证码"
```

## 评估报告解读

### 报告结构

```
evals/reports/
├── skill_evaluation_report_YYYYMMDD_HHMMSS.json   # 原始数据
├── skill_evaluation_report_YYYYMMDD_HHMMSS.md     # 可视化报告
└── baseline/
    ├── wechat-reader.json
    ├── douyin-reader.json
    └── ...
```

### 报告内容

- **汇总指标**：总 skill 数、平均分、等级分布
- **排名列表**：按分数排序，含三维度得分
- **重点改进**：分数 < 60 的 skill 及具体建议
- **趋势对比**：与历史基线对比（如有）

## 持续改进

### 评估器迭代

1. **收集反馈**：记录评估结果与实际使用体验的偏差
2. **调整权重**：根据反馈调整三维度权重
3. **新增检查项**：补充新的质量维度
4. **版本管理**：评估器版本与 skill 版本独立管理

### 质量门禁

| 场景 | 门禁标准 |
|------|---------|
| 新 skill 合入 | 总分 >= 70，无 F 等级 |
| 现有 skill 更新 | 不降低基线分数 |
| 关键 skill 发布 | 总分 >= 80，pass^3 达标 |
