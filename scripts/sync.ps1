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

$ProjectRoot = "d:\AI" + [char]0x9879 + [char]0x76EE
$PmTeamDir = Join-Path $ProjectRoot "pm-team"

function Write-Header {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  AI project sync tool" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
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

    # Pull main repo
    Write-Host "[1/2] Pulling main repo..." -ForegroundColor Green
    Set-Location $ProjectRoot
    git pull origin main
    if ($LASTEXITCODE -ne 0) { Write-Host "Pull main repo failed" -ForegroundColor Red; return }
    Write-Host "Main repo: OK" -ForegroundColor Green

    # Pull pm-team
    Write-Host ""
    Write-Host "[2/2] Pulling pm-team repo..." -ForegroundColor Green
    Set-Location $PmTeamDir
    git pull origin master
    if ($LASTEXITCODE -ne 0) { Write-Host "Pull pm-team failed" -ForegroundColor Red; return }
    Write-Host "pm-team repo: OK" -ForegroundColor Green

    Write-Host ""
    Write-Host "Done! Pull completed." -ForegroundColor Green
}

function Do-Push {
    Write-Host ""

    # Check & push pm-team first
    Write-Host "[1/2] Checking pm-team changes..." -ForegroundColor Green
    Set-Location $PmTeamDir
    $subChanges = git status --porcelain
    if ($subChanges) {
        Write-Host "pm-team changes found, committing..." -ForegroundColor Yellow
        git add -A
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "sync: auto commit $timestamp"
        git push origin master
        if ($LASTEXITCODE -ne 0) { Write-Host "Push pm-team failed" -ForegroundColor Red; return }
        Write-Host "pm-team pushed." -ForegroundColor Green
    } else {
        Write-Host "No pm-team changes, skipped." -ForegroundColor Gray
    }

    # Check & push main repo
    Write-Host ""
    Write-Host "[2/2] Checking main repo changes..." -ForegroundColor Green
    Set-Location $ProjectRoot
    $mainChanges = git status --porcelain
    if ($mainChanges) {
        Write-Host "Main repo changes found, committing..." -ForegroundColor Yellow
        git add -A
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "sync: auto commit $timestamp"
        git push origin main
        if ($LASTEXITCODE -ne 0) { Write-Host "Push main repo failed" -ForegroundColor Red; return }
        Write-Host "Main repo pushed." -ForegroundColor Green
    } else {
        Write-Host "No main repo changes, nothing to push." -ForegroundColor Gray
    }

    Write-Host ""
    Write-Host "Done! Push completed." -ForegroundColor Green
}

function Do-Status {
    Write-Host ""

    Write-Host "=== Main Repo Status ===" -ForegroundColor Yellow
    Set-Location $ProjectRoot
    git status -sb
    Write-Host ""
    Write-Host "=== Recent Commits ===" -ForegroundColor Yellow
    git log --oneline -5
    Write-Host ""

    Write-Host "=== pm-team Repo Status ===" -ForegroundColor Yellow
    Set-Location $PmTeamDir
    git status -sb
    Write-Host ""
    Write-Host "=== pm-team Recent Commits ===" -ForegroundColor Yellow
    git log --oneline -3
    Write-Host ""
}

Write-Header
switch ($Action) {
    "pull"   { Do-Pull }
    "push"   { Do-Push }
    "status" { Do-Status }
    ""       { Show-Menu }
}
