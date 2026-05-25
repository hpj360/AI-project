<#
.SYNOPSIS
    AI project sync tool
.DESCRIPTION
    Sync local Trae IDE project with GitHub remote.
    Handles main repo + nested pm-team repo.
.EXAMPLE
    .\sync.ps1 pull      # Pull latest from remote
    .\sync.ps1 push      # Push local changes to remote
    .\sync.ps1 status    # Check sync status
#>

param(
    [Parameter(Position=0)]
    [ValidateSet("pull", "push", "status", "")]
    [string]$Action = ""
)

$ScriptDir = $PSScriptRoot
if (-not $ScriptDir) { $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition }
$ProjectRoot = $ScriptDir
while ($ProjectRoot -and -not (Test-Path (Join-Path $ProjectRoot ".git"))) {
    $Parent = Split-Path -Parent $ProjectRoot
    if ($Parent -eq $ProjectRoot) { break }
    $ProjectRoot = $Parent
}
if (-not (Test-Path (Join-Path $ProjectRoot ".git"))) {
    Write-Host "Error: Cannot find Git repository root from $ScriptDir" -ForegroundColor Red
    exit 1
}
$PmTeamDir = Join-Path $ProjectRoot "pm-team"

$SensitivePatterns = @(
    ".env"
    "*.key"
    "*.pem"
    "*.p12"
    "*.pfx"
    "credentials/"
    ".secrets.*"
)

function Write-Header {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  AI project sync tool" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Repo: $ProjectRoot" -ForegroundColor Gray
    Write-Host ""
}

function Show-Menu {
    Write-Host "Select action:" -ForegroundColor Yellow
    Write-Host "  1. Pull from remote"
    Write-Host "  2. Push to remote"
    Write-Host "  3. Check status"
    Write-Host "  4. Exit"
    Write-Host ""
    $choice = Read-Host "Enter option (1/2/3/4)"
    switch ($choice) {
        "1" { Do-Pull }
        "2" { Do-Push }
        "3" { Do-Status }
        "4" { exit }
        default { Write-Host "Invalid option" -ForegroundColor Red; Show-Menu }
    }
}

function Do-Pull {
    Write-Host ""

    Write-Host "[1/2] Pulling main repo..." -ForegroundColor Green
    Push-Location $ProjectRoot
    try {
        git pull origin main
        if ($LASTEXITCODE -ne 0) { Write-Host "Pull main repo failed" -ForegroundColor Red; return }
        Write-Host "Main repo: OK" -ForegroundColor Green
    }
    finally { Pop-Location }

    Write-Host ""
    Write-Host "[2/2] Pulling pm-team repo..." -ForegroundColor Green
    if (Test-Path $PmTeamDir) {
        Push-Location $PmTeamDir
        try {
            git pull origin master
            if ($LASTEXITCODE -ne 0) { Write-Host "Pull pm-team failed" -ForegroundColor Red; return }
            Write-Host "pm-team repo: OK" -ForegroundColor Green
        }
        finally { Pop-Location }
    } else {
        Write-Host "pm-team directory not found, skipped." -ForegroundColor Gray
    }

    Write-Host ""
    Write-Host "Done! Pull completed." -ForegroundColor Green
}

function Invoke-SafeGitAdd {
    param([string]$RepoPath)

    Push-Location $RepoPath
    try {
        $allChanges = git status --porcelain
        if (-not $allChanges) { return $false }

        $safeFiles = @()
        $blockedFiles = @()
        foreach ($line in $allChanges) {
            $filePath = $line.Substring(3)
            $isSensitive = $false
            foreach ($pattern in $SensitivePatterns) {
                if ($filePath -like $pattern) {
                    $isSensitive = $true
                    break
                }
            }
            if ($isSensitive) {
                $blockedFiles += $filePath
            } else {
                $safeFiles += $filePath
            }
        }

        if ($blockedFiles) {
            Write-Host "  Blocked sensitive files:" -ForegroundColor Red
            foreach ($f in $blockedFiles) { Write-Host "    [SKIP] $f" -ForegroundColor Red }
        }

        if ($safeFiles) {
            foreach ($f in $safeFiles) {
                git add $f
            }
            return $true
        }
        return $false
    }
    finally { Pop-Location }
}

function Do-Push {
    Write-Host ""

    if (Test-Path $PmTeamDir) {
        Write-Host "[1/2] Checking pm-team changes..." -ForegroundColor Green
        Push-Location $PmTeamDir
        try {
            $subChanges = git status --porcelain
            if ($subChanges) {
                Write-Host "pm-team changes found, committing..." -ForegroundColor Yellow
                $hasSafeFiles = Invoke-SafeGitAdd $PmTeamDir
                if ($hasSafeFiles) {
                    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                    $shortHash = (git log -1 --format="%h" 2>$null) ?? "unknown"
                    git commit -m "sync: auto commit $timestamp (base: $shortHash)"
                    git push origin master
                    if ($LASTEXITCODE -ne 0) { Write-Host "Push pm-team failed" -ForegroundColor Red; return }
                    Write-Host "pm-team pushed." -ForegroundColor Green
                } else {
                    Write-Host "Only sensitive files changed, skipping commit." -ForegroundColor Yellow
                }
            } else {
                Write-Host "No pm-team changes, skipped." -ForegroundColor Gray
            }
        }
        finally { Pop-Location }
    } else {
        Write-Host "[1/2] pm-team directory not found, skipped." -ForegroundColor Gray
    }

    Write-Host ""
    Write-Host "[2/2] Checking main repo changes..." -ForegroundColor Green
    Push-Location $ProjectRoot
    try {
        $mainChanges = git status --porcelain
        if ($mainChanges) {
            Write-Host "Main repo changes found, committing..." -ForegroundColor Yellow
            $hasSafeFiles = Invoke-SafeGitAdd $ProjectRoot
            if ($hasSafeFiles) {
                $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                $shortHash = (git log -1 --format="%h" 2>$null) ?? "unknown"
                git commit -m "sync: auto commit $timestamp (base: $shortHash)"
                git push origin main
                if ($LASTEXITCODE -ne 0) { Write-Host "Push main repo failed" -ForegroundColor Red; return }
                Write-Host "Main repo pushed." -ForegroundColor Green
            } else {
                Write-Host "Only sensitive files changed, skipping commit." -ForegroundColor Yellow
            }
        } else {
            Write-Host "No main repo changes, nothing to push." -ForegroundColor Gray
        }
    }
    finally { Pop-Location }

    Write-Host ""
    Write-Host "Done! Push completed." -ForegroundColor Green
}

function Do-Status {
    Write-Host ""

    Write-Host "=== Main Repo Status ===" -ForegroundColor Yellow
    Push-Location $ProjectRoot
    try {
        git status -sb
        Write-Host ""
        Write-Host "=== Recent Commits ===" -ForegroundColor Yellow
        git log --oneline -5
    }
    finally { Pop-Location }
    Write-Host ""

    if (Test-Path $PmTeamDir) {
        Write-Host "=== pm-team Repo Status ===" -ForegroundColor Yellow
        Push-Location $PmTeamDir
        try {
            git status -sb
            Write-Host ""
            Write-Host "=== pm-team Recent Commits ===" -ForegroundColor Yellow
            git log --oneline -3
        }
        finally { Pop-Location }
        Write-Host ""
    } else {
        Write-Host "=== pm-team directory not found ===" -ForegroundColor Gray
        Write-Host ""
    }
}

Write-Header
switch ($Action) {
    "pull"   { Do-Pull }
    "push"   { Do-Push }
    "status" { Do-Status }
    ""       { Show-Menu }
}
