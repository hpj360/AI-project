$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ProjectRoot
$ConfigPath = "$ProjectRoot\content-team-config.json"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动 ContentTeam 内容智能体团队" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $ConfigPath)) {
    Write-Host "[错误] 配置文件不存在: $ConfigPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Command "node")) {
    Write-Host "[错误] Node.js 未安装，请先运行 env-setup.ps1 检查环境" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "$Root\node_modules\openclaw")) {
    Write-Host "[提示] 正在安装 npm 依赖..." -ForegroundColor Yellow
    Push-Location $Root
    npm install
    Pop-Location
}

$envFile = "$ProjectRoot\.env"
if (Test-Path $envFile) {
    Write-Host "[提示] 加载 .env 文件..." -ForegroundColor Yellow
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
            $key = $Matches[1].Trim()
            $val = $Matches[2].Trim()
            Set-Item -Path "env:$key" -Value $val
        }
    }
}

Write-Host "[启动] ContentTeam (端口 18791)" -ForegroundColor Green
Write-Host "[配置] $ConfigPath" -ForegroundColor White
Write-Host ""

Push-Location $Root
npx openclaw start --config $ConfigPath
Pop-Location
