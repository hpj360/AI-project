---
name: douyin-reader
description: 读取抖音视频内容并提取文字版本。当用户提供抖音视频链接（douyin.com、v.douyin.com）并要求阅读、学习、总结、提取文字、获取字幕、转录内容时，必须使用此 skill。也适用于用户提到"抖音视频""抖音链接""这个视频""看看这个抖音"等场景。抖音视频有严格的反爬机制和加密签名，此 skill 提供多层降级策略确保可靠获取视频内容和文字转写。
---

# 抖音视频内容提取器

专门解决抖音视频的程序化内容提取问题。抖音对自动化访问极不友好——视频地址使用复杂加密算法且频繁更新，直接请求几乎必定失败。此 skill 提供三层降级策略，从视频下载+语音转写到页面信息提取，确保在各种情况下都能尽可能获取视频内容。

## 核心策略：三层降级

```
Layer 1: douyin_reader.py 脚本（yt-dlp 下载 + faster-whisper 转写）
    ↓ 失败
Layer 2: agent-browser 提取页面信息（标题、描述、评论等文字内容）
    ↓ 失败
Layer 3: WebSearch 搜索视频相关信息
```

## Layer 1: douyin_reader.py 脚本（首选）

这是内容最完整的方案。脚本使用 yt-dlp 下载视频、ffmpeg 提取音频、faster-whisper 进行语音转文字，输出结构化 JSON。

**执行命令：**

```bash
python3 /workspace/.trae/skills/douyin-reader/scripts/douyin_reader.py "<URL>" --json
```

**可选参数：**
- `--model tiny` — Whisper 模型大小（tiny/base/small/medium/large），默认 tiny（最快）
- `--language zh` — 音频语言，默认中文
- `--skip-transcribe` — 跳过语音转写，仅下载视频+获取元数据
- `--output-dir DIR` — 指定输出目录

**输出格式（JSON）：**
- `title` — 视频标题
- `description` — 视频描述
- `uploader` — 作者
- `duration` — 时长（秒）
- `view_count` / `like_count` / `comment_count` — 统计数据
- `tags` — 标签列表
- `transcription.full_text` — 完整转写文字
- `transcription.segments` — 带时间轴的分段转写

**判断成功/失败：**
- 成功：JSON 输出 `success: true`，包含 `title` 和 `transcription`
- 失败：`success: false`，包含 `error` 字段

**为什么这是首选：** 能获取最完整的内容——不仅包含视频中的语音文字，还包含标题、描述、统计数据等元数据。faster-whisper 使用 CPU int8 量化，内存占用小，适合服务器环境。

**已知限制：**
- yt-dlp 对抖音的兼容性不稳定，抖音频繁更新反爬机制可能导致下载失败
- 视频文件较大（通常 10-100MB），下载需要时间和带宽
- faster-whisper 的 tiny 模型对中文识别准确率约 85-90%，如需更高精度可使用 `--model base` 或 `--model small`

## Layer 2: agent-browser 提取页面信息（备用）

当 yt-dlp 下载失败时（反爬拦截、视频不可用等），使用 agent-browser 访问抖音网页版，提取页面中可见的文字内容。

**操作步骤：**

1. 使用 agent-browser 导航到视频页面
   - 短链接 `v.douyin.com/xxx` 需先解析为长链接 `douyin.com/video/xxx`
   - 可用 WebFetch 发送短链接请求获取 302 重定向后的真实 URL
2. 获取页面快照，提取以下信息：
   - 视频标题（`<h1>` 或页面 title）
   - 视频描述/文案
   - 作者名称
   - 点赞/评论/分享数
   - 评论区热门评论文字
3. 注意：此方案**无法获取视频本身的语音内容**，只能获取页面上的文字信息

**优势：** 不需要下载大文件，速度快，能获取评论等 yt-dlp 无法提取的信息。
**劣势：** 无法获取视频语音转写，信息完整性不如 Layer 1。

## Layer 3: WebSearch 搜索相关信息（最后手段）

当以上两层全部失败时，通过搜索引擎查找视频相关信息。

**操作步骤：**

1. 从 URL 或上下文中提取视频标题关键词、作者名
2. 使用 WebSearch 搜索：`"<视频标题>" <作者名> 抖音`
3. 查找是否有文字版转载、截图、或他人整理的文字内容

**注意：** 搜索结果可能不准确，需标注信息来源。

## 完整工作流

收到抖音视频阅读需求时，按以下流程执行：

### Step 1: 识别输入

判断用户提供的链接是否为抖音视频：
- 域名包含 `douyin.com` 或 `v.douyin.com` 或 `iesdouyin.com`
- 或用户明确提到"抖音视频""抖音链接"

从用户输入中提取纯 URL（可能夹杂"复制此链接"等文字）。

### Step 2: 执行 Layer 1

```bash
python3 /workspace/.trae/skills/douyin-reader/scripts/douyin_reader.py "<URL>" --json
```

如果成功获取到标题和转写文字，跳到 Step 5。

如果下载失败但元数据获取成功，保留元数据，继续尝试 Layer 2 补充页面信息。

### Step 3: 执行 Layer 2

如果 Layer 1 失败：
1. 解析短链接获取真实 URL
2. 使用 agent-browser 访问视频页面
3. 提取标题、描述、评论等文字内容
4. 与 Layer 1 已获取的元数据合并

### Step 4: 执行 Layer 3

如果 Layer 1 和 Layer 2 都失败，WebSearch 搜索相关信息。

### Step 5: 输出结果

向用户呈现视频内容，包含：
- **标题**
- **作者**
- **时长**
- **统计数据**（播放/点赞/评论）
- **视频描述/文案**
- **语音转写文字**（如成功获取）
- **热门评论**（如通过 Layer 2 获取）

如果用户要求"学习""总结""提取知识点"，在输出内容后进一步：
- 提炼核心观点（3-5 个要点）
- 识别视频结构（开头钩子 → 主体内容 → 结尾行动号召）
- 标注可行动的信息

## 内容沉淀指导

当用户要求"内容沉淀"时，将提取的内容整理为结构化文档：

```
# [视频标题]

## 基本信息
- 作者：xxx
- 链接：xxx
- 时长：xx秒
- 播放量：xx | 点赞：xx | 评论：xx

## 核心内容
[语音转写文字或页面描述的精华提炼]

## 关键要点
1. [要点1]
2. [要点2]
3. [要点3]

## 可行动信息
- [具体可执行的建议或步骤]

## 来源标注
- 内容来源：[Layer 1 视频转写 / Layer 2 页面信息 / Layer 3 搜索结果]
- 获取时间：[日期]
```

## 失败处理

如果三层全部失败：

1. 明确告知用户："抖音视频内容获取失败，可能是反爬限制或视频不可用"
2. 提供替代方案：
   - "请在抖音 APP 中打开视频，手动复制文案内容给我"
   - "如果视频有文字版描述，请直接粘贴"
3. 不要静默返回空内容或伪造结果

## 常见问题

**Q: 为什么不用 whisper 而用 faster-whisper？**
A: openai-whisper 依赖 PyTorch（~2GB），在磁盘空间有限的环境中无法安装。faster-whisper 基于 CTranslate2，CPU int8 量化下内存占用仅 ~1GB，安装包更小，转写速度更快。

**Q: 转写准确率如何？**
A: tiny 模型中文准确率约 85-90%，base 模型约 90-95%。如果对准确率有要求，使用 `--model base`。注意抖音视频常有背景音乐、口音、方言等因素影响准确率。

**Q: 短链接怎么处理？**
A: 脚本会自动解析 `v.douyin.com/xxx` 格式的短链接。如果用户粘贴的是分享文本（含"复制此链接"等），脚本会自动提取 URL 部分。

**Q: 视频太大下载不了怎么办？**
A: 脚本限制最大 500MB。如果视频超过此限制，会自动降级到 Layer 2（提取页面信息）。大多数抖音视频在 10-100MB 之间，不会触发此限制。

**Q: 如何只获取元数据不做语音转写？**
A: 使用 `--skip-transcribe` 参数，仅下载视频并提取标题、描述、统计等信息，跳过耗时的语音转写步骤。
