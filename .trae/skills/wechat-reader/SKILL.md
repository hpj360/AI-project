---
name: wechat-reader
description: 读取微信公众号文章全文内容。当用户提供微信文章链接（mp.weixin.qq.com）并要求阅读、学习、总结、提取、抓取、获取内容时，必须使用此 skill。也适用于用户提到"微信文章""公众号文章""这篇微信""看看这篇文章"等场景。微信文章有严格反爬机制，直接 WebFetch 几乎必定失败，此 skill 提供多层降级策略确保可靠获取。
---

# 微信公众号文章阅读器

专门解决微信公众号文章的程序化阅读问题。微信文章对自动化访问极不友好——直接请求会触发验证码、返回空白页或登录墙。此 skill 提供四层降级策略，确保在各种情况下都能尽可能获取文章内容。

## 核心策略：四层降级

按优先级依次尝试，任何一层成功即停止：

```
Layer 1: wechat_reader.py 脚本（UA 伪装 + 重试）
    ↓ 失败
Layer 2: WebSearch 搜索镜像内容
    ↓ 失败
Layer 3: WebFetch 直接尝试
    ↓ 失败
Layer 4: agent-browser 模拟真实浏览器
```

## Layer 1: wechat_reader.py 脚本（首选）

这是成功率最高的方案。脚本使用 6 个移动端/桌面端 User-Agent 轮换，最多重试 5 次，自带验证码检测和 HTML-to-Markdown 转换。

**执行命令：**

```bash
python3 /workspace/.trae/skills/wechat-reader/scripts/wechat_reader.py "<URL>" --json
```

**输出格式（JSON）：**
- `title` — 文章标题
- `author` — 作者/公众号名称
- `publish_time` — 发布时间
- `url` — 原文链接
- `content_markdown` — 正文 Markdown 格式

**判断成功/失败：**
- 成功：JSON 输出包含 `title` 和非空的 `content_markdown`
- 失败：脚本输出 `全部5次尝试失败` 或 `无法解析文章内容`

**为什么这是首选：** 微信的反爬本质上是检查 User-Agent 中是否包含微信标识。此脚本通过随机轮换移动端 UA 模拟正常用户访问，绕过率最高，且零成本、速度快。

## Layer 2: WebSearch 搜索镜像（备用）

当脚本被验证码拦截时，微信文章经常被其他平台（CSDN、今日头条、知乎、阿里云开发者社区等）转载。

**操作步骤：**

1. 从 URL 中提取文章的特征信息（标题关键词、公众号名称）
2. 使用 WebSearch 搜索：`"<文章标题关键词>" site:csdn.net OR site:toutiao.com OR site:zhihu.com OR site:mp.weixin.qq.com`
3. 如果找到镜像，用 WebFetch 获取镜像页面全文

**搜索技巧：**
- 提取 URL 中的短 hash（如 `PUbGqheJhFMmb6hGj1ZtOw`）作为精确搜索词
- 搜索时加上公众号名称或作者名提高匹配精度
- 优先搜索 CSDN、今日头条等平台，这些平台经常完整转载微信文章

## Layer 3: WebFetch 直接尝试

虽然 WebFetch 对微信文章成功率低，但作为轻量尝试值得一试（可能有不同的网络出口）。

```bash
WebFetch(url="微信文章URL")
```

**判断标准：** 如果返回内容超过 500 字且不包含"环境异常""验证码"等关键词，视为成功。

## Layer 4: agent-browser 模拟浏览器（最后手段）

当以上三层全部失败时，使用 agent-browser 模拟真实浏览器环境。

**操作步骤：**

1. 使用 agent-browser 导航到微信文章 URL
2. 检查页面是否触发验证码
3. 如果触发验证码，通知用户需要手动完成验证
4. 验证通过后，获取页面快照提取正文

**注意：** agent-browser 消耗资源较大（内存 ~200MB/实例），仅在必要时使用。

## 完整工作流

收到微信文章阅读需求时，按以下流程执行：

### Step 1: 识别输入

判断用户提供的链接是否为微信文章：
- 域名包含 `mp.weixin.qq.com`
- 或用户明确提到"微信文章""公众号文章"

### Step 2: 执行 Layer 1

```bash
python3 /workspace/.trae/skills/wechat-reader/scripts/wechat_reader.py "<URL>" --json
```

如果成功获取到标题和正文，跳到 Step 5。

### Step 3: 执行 Layer 2

如果 Layer 1 失败（验证码拦截），立即启动 WebSearch 搜索镜像：

1. 从原始 URL 或上下文中提取文章标题关键词
2. 搜索转载内容
3. 用 WebFetch 获取镜像全文

如果找到镜像，跳到 Step 5。

### Step 4: 执行 Layer 3 + Layer 4

依次尝试 WebFetch 和 agent-browser。

### Step 5: 输出结果

向用户呈现文章内容，包含：
- **标题**
- **作者/公众号**
- **发布时间**
- **正文内容**（Markdown 格式，保留结构）

如果用户要求"学习""总结""提取知识点"，在输出正文后进一步：
- 提炼核心观点（3-5 个要点）
- 识别文章结构（开头方式、论证框架、结尾方式）
- 标注可行动的信息

## 失败处理

如果四层全部失败：

1. 明确告知用户："微信文章触发了反爬验证，无法自动获取内容"
2. 提供替代方案：
   - "请在微信中打开文章，复制全文后粘贴给我"
   - "文章可能被其他平台转载，我已搜索但未找到镜像"
3. 不要静默返回空内容或伪造结果

## 常见问题

**Q: 为什么不直接用 WebFetch？**
A: 微信文章的反爬机制会检测请求来源。WebFetch 使用非微信 UA，几乎必定触发验证码拦截，返回空白页或验证码页面。

**Q: 为什么不直接用浏览器？**
A: agent-browser 资源消耗大（~200MB 内存/实例），启动慢。UA 伪装方案零成本、速度快，应优先使用。

**Q: 多篇文章怎么处理？**
A: 每篇文章独立执行四层降级。文章之间加入 2-3 秒延迟，避免触发频率限制。

**Q: 如何提高成功率？**
A: 微信对单 IP 连续访问 5-8 篇文章会触发风控。批量处理时，每篇文章之间保持 3-5 秒间隔。如果持续被拦截，暂停 30 秒后重试。
