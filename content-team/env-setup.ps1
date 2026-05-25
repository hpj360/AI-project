$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ProjectRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ContentTeam 环境配置脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Check-EnvVar {
    param([string]$Name, [string]$Desc, [bool]$Required = $true)
    $val = [Environment]::GetEnvironmentVariable($Name, "User")
    if ($val) {
        Write-Host "  [OK] $Desc ($Name) 已设置" -ForegroundColor Green
        return $true
    } else {
        $tag = if ($Required) { "必须" } else { "可选" }
        Write-Host "  [--] $Desc ($Name) 未设置 [$tag]" -ForegroundColor Yellow
        return $false
    }
}

Write-Host "--- 1. 检查运行时依赖 ---" -ForegroundColor White
Write-Host ""

$nodeOk = $false
if (Test-Command "node") {
    $nodeVer = & node --version 2>$null
    if ($nodeVer -match "v(\d+)\.") {
        $major = [int]$Matches[1]
        if ($major -ge 22) {
            Write-Host "  [OK] Node.js $nodeVer (>= 22.16.0)" -ForegroundColor Green
            $nodeOk = $true
        } else {
            Write-Host "  [!!] Node.js $nodeVer 版本过低，需要 >= 22.16.0" -ForegroundColor Red
        }
    }
} else {
    Write-Host "  [!!] Node.js 未安装，请前往 https://nodejs.org 安装 v22+" -ForegroundColor Red
}

if (Test-Command "npm") {
    $npmVer = & npm --version 2>$null
    Write-Host "  [OK] npm $npmVer" -ForegroundColor Green
} else {
    Write-Host "  [!!] npm 未安装" -ForegroundColor Red
}

if (Test-Command "pnpm") {
    $pnpmVer = & pnpm --version 2>$null
    Write-Host "  [OK] pnpm $pnpmVer" -ForegroundColor Green
} else {
    Write-Host "  [--] pnpm 未安装 (OpenClaw 源码构建需要)" -ForegroundColor Yellow
}

if (Test-Command "python") {
    $pyVer = & python --version 2>$null
    Write-Host "  [OK] Python $pyVer" -ForegroundColor Green
} else {
    Write-Host "  [--] Python 未安装 (Skillhub CLI 需要)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "--- 2. 检查 Skill 工具依赖 ---" -ForegroundColor White
Write-Host ""

if (Test-Command "jq") {
    Write-Host "  [OK] jq 已安装 (Trello skill 依赖)" -ForegroundColor Green
} else {
    Write-Host "  [--] jq 未安装 (Trello skill 依赖)" -ForegroundColor Yellow
    Write-Host "      安装: winget install jqlang.jq 或 choco install jq" -ForegroundColor DarkGray
}

if (Test-Command "gh") {
    Write-Host "  [OK] GitHub CLI 已安装 (github skill 依赖)" -ForegroundColor Green
} else {
    Write-Host "  [--] GitHub CLI 未安装 (github skill 依赖)" -ForegroundColor Yellow
    Write-Host "      安装: winget install GitHub.cli" -ForegroundColor DarkGray
}

if (Test-Command "blogwatcher") {
    Write-Host "  [OK] blogwatcher 已安装 (调研 skill)" -ForegroundColor Green
} else {
    Write-Host "  [--] blogwatcher 未安装 (调研 skill, 可选)" -ForegroundColor Yellow
    Write-Host "      安装: go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest" -ForegroundColor DarkGray
}

if (Test-Command "summarize") {
    Write-Host "  [OK] summarize 已安装 (摘要 skill)" -ForegroundColor Green
} else {
    Write-Host "  [--] summarize 未安装 (摘要 skill, 可选)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "--- 3. 检查环境变量 ---" -ForegroundColor White
Write-Host ""

Check-EnvVar "FEISHU_BOT_TOKEN" "飞书 Bot Token" $true
Check-EnvVar "NOTION_API_KEY" "Notion API Key" $true
Check-EnvVar "TRELLO_API_KEY" "Trello API Key" $true
Check-EnvVar "TRELLO_TOKEN" "Trello Token" $true
Check-EnvVar "OPENAI_API_KEY" "OpenAI API Key (designer/图片生成)" $false
Check-EnvVar "ANTHROPIC_API_KEY" "Anthropic API Key (主模型)" $false

Write-Host ""
Write-Host "--- 4. 检查 npm 依赖 ---" -ForegroundColor White
Write-Host ""

if (Test-Path "$Root\node_modules\openclaw") {
    Write-Host "  [OK] openclaw npm 包已安装" -ForegroundColor Green
} else {
    Write-Host "  [!!] openclaw npm 包未安装" -ForegroundColor Red
    Write-Host "      运行: cd $Root && npm install" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "--- 5. 检查 ContentTeam 配置 ---" -ForegroundColor White
Write-Host ""

$configPath = "$ProjectRoot\content-team-config.json"
if (Test-Path $configPath) {
    try {
        $null = Get-Content $configPath -Raw | ConvertFrom-Json
        Write-Host "  [OK] content-team-config.json 格式正确" -ForegroundColor Green
    } catch {
        Write-Host "  [!!] content-team-config.json JSON 格式错误: $_" -ForegroundColor Red
    }
} else {
    Write-Host "  [!!] content-team-config.json 不存在" -ForegroundColor Red
}

$agentCount = (Get-ChildItem "$ProjectRoot\agents" -Directory).Count
if ($agentCount -eq 8) {
    Write-Host "  [OK] 8 个 Agent 目录完整" -ForegroundColor Green
} else {
    Write-Host "  [!!] Agent 目录数量: $agentCount (应为 8)" -ForegroundColor Red
}

$soulCount = (Get-ChildItem "$ProjectRoot\agents" -Recurse -Filter "SOUL.md").Count
if ($soulCount -eq 8) {
    Write-Host "  [OK] 8 个 SOUL.md 文件完整" -ForegroundColor Green
} else {
    Write-Host "  [!!] SOUL.md 文件数量: $soulCount (应为 8)" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  检查完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步操作:" -ForegroundColor White
Write-Host "  1. 安装缺失的运行时依赖 (Node.js 22+, npm, pnpm)" -ForegroundColor White
Write-Host "  2. 设置环境变量 (FEISHU_BOT_TOKEN, NOTION_API_KEY 等)" -ForegroundColor White
Write-Host "  3. 安装 npm 依赖: cd $Root && npm install" -ForegroundColor White
Write-Host "  4. 启动团队: npx openclaw start --config $ProjectRoot\content-team-config.json" -ForegroundColor White
Write-Host ""
