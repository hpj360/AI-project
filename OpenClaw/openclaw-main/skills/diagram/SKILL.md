---
name: diagram
description: "使用 Mermaid 或 PlantUML 语法生成图表。适用场景：(1) 绘制架构图，(2) 绘制时序图/流程图/类图，(3) 可视化业务流程，(4) 生成数据库 ER 图。通过 npx @mermaid-js/mermaid-cli 渲染 Mermaid，或输出 PlantUML 源码供外部渲染。"
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["npx"] } } }
---

# 图表技能

使用 Mermaid 或 PlantUML 语法生成技术图表。

## 适用场景

✅ **使用此技能的场景：**

- 绘制系统架构图
- 创建 API 交互时序图
- 可视化业务流程
- 生成数据库 ER 图
- 生成 OOP 设计类图
- 创建项目甘特图

## 不适用场景

❌ **不使用此技能的场景：**

- 简单文字说明即可表达时
- 图表用于演示文稿（请使用专业设计工具）
- 需要像素级精确设计时（请使用 Figma/Sketch）

## Mermaid 语法

### 流程图

```mermaid
flowchart TD
    A[开始] --> B{判断}
    B -->|是| C[操作1]
    B -->|否| D[操作2]
    C --> E[结束]
    D --> E
```

### 时序图

```mermaid
sequenceDiagram
    participant 客户端
    participant API
    participant 数据库
    客户端->>API: POST /users
    API->>数据库: INSERT user
    数据库-->>API: user_id
    API-->>客户端: 201 Created
```

### 类图

```mermaid
classDiagram
    class 用户 {
        +String 姓名
        +String 邮箱
        +登录()
    }
    class 订单 {
        +Date 创建时间
        +Float 总额
        +结账()
    }
    用户 "1" --> "*" 订单 : 下单
```

### ER 图

```mermaid
erDiagram
    USER ||--o{ ORDER : 下单
    USER {
        int id PK
        string 姓名
        string 邮箱
    }
    ORDER ||--|{ ORDER_ITEM : 包含
    ORDER {
        int id PK
        date 创建时间
        float 总额
    }
    ORDER_ITEM {
        int id PK
        int 数量
        float 单价
    }
```

### 甘特图

```mermaid
gantt
    title 项目时间线
    dateFormat  YYYY-MM-DD
    section 规划
    需求分析   :a1, 2026-01-01, 14d
    方案设计   :a2, after a1, 7d
    section 开发
    前端开发   :b1, after a2, 21d
    后端开发   :b2, after a2, 21d
    section 测试
    质量保障   :c1, after b1, 14d
```

## 渲染方式

### Mermaid CLI

```bash
# 渲染为 PNG
npx @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.png

# 渲染为 SVG
npx @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg

# 使用暗色主题
npx @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.png -t dark
```

### PlantUML

```bash
# 生成 PlantUML 源码（需要 PlantUML 服务器或本地 jar）
# 保存为 .puml 文件，通过 plantuml.com/plantuml 渲染
java -jar plantuml.jar diagram.puml
```

## 输出规范

- Mermaid 文件保存为 `.mmd`，存放于 `shared/diagrams/`
- PlantUML 文件保存为 `.puml`，存放于 `shared/diagrams/`
- 使用描述性文件名：`user-auth-flow.mmd`、`db-schema.puml`
- 图表中必须包含标题

## 最佳实践

- 每张图表聚焦一个概念
- 保持方向一致（流程图用 TD，时间线用 LR）
- 节点数控制在 15-20 个以内，确保可读性
- 所有连线/关系必须添加标签
- 使用子图（subgraph）对相关组件分组
