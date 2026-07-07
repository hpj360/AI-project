#!/usr/bin/env python3
"""会话流程层护栏（三道关卡）。

关卡1 会话启动 (start)   : 建立基线，识别是否全新沙箱，防止在空环境上假装"工作还在"
关卡2 工作中   (working) : 每完成一个阶段后调用，确认本地状态
关卡3 会话结束 (exit)    : 强制持久化检查，未 push 则拒绝退出

使用：
    python3 session_check.py start     # 会话启动时
    python3 session_check.py working   # 工作中阶段性
    python3 session_check.py exit      # 会话结束前
"""
from __future__ import annotations

import subprocess
import sys
import os
from pathlib import Path

# 脚本路径 /workspace/Hermes/content-creation/scripts/session_check.py
# 需回到 4 层 parent 才到 git root /workspace
REPO_DIR = Path(__file__).resolve().parent.parent.parent.parent  # /workspace
STATE_FILE = REPO_DIR / ".session_state"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"


def run(cmd: str, check: bool = False, timeout: int = 30) -> tuple[int, str]:
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=REPO_DIR, capture_output=True,
            text=True, timeout=timeout
        )
        return r.returncode, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return 1, "TIMEOUT"


def banner(title: str, color: str = CYAN):
    print(f"\n{color}{BOLD}{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}{RESET}\n")


def remote_reachable() -> bool:
    code, _ = run("git ls-remote --heads origin", timeout=15)
    return code == 0


def get_local_head() -> str:
    _, h = run("git rev-parse HEAD")
    return h[:12] if h else "无"


def get_remote_head() -> str:
    if not remote_reachable():
        return "不可达"
    _, out = run("git ls-remote origin main", timeout=15)
    return out.split()[0][:12] if out else "空仓库"


def get_unpushed_commits() -> list[str]:
    _, out = run("git log origin/main..HEAD --oneline", check=False)
    return [l for l in out.split("\n") if l.strip()]


def get_uncommitted_files() -> list[str]:
    _, out = run("git status --porcelain")
    return [l for l in out.split("\n") if l.strip()]


def is_fresh_sandbox() -> bool:
    """检测是否全新沙箱（无 .session_state 文件）。"""
    return not STATE_FILE.exists()


# ============================================================
# 关卡 1：会话启动检查
# ============================================================

def gate_start():
    """会话启动时建立基线，防止在空环境上假装"工作还在"。"""
    banner("关卡 1/3 · 会话启动检查", CYAN)

    issues = []
    warnings = []

    # 1.1 检查是否全新沙箱
    if is_fresh_sandbox():
        warnings.append("检测到全新沙箱（无 .session_state），之前会话的临时文件可能已销毁")
    else:
        # 读取上次会话状态
        prev_state = STATE_FILE.read_text(encoding="utf-8").strip()
        print(f"  {GREEN}✓{RESET} 上次会话状态: {prev_state[:60]}")

    # 1.2 检查本地 git 是否存在
    if not (REPO_DIR / ".git").exists():
        issues.append("本地无 .git 目录，需要 clone 远程仓库")
        print(f"  {RED}✗{RESET} 本地无 git 仓库")
        return finish(issues, warnings)

    # 1.3 检查本地 HEAD
    local_head = get_local_head()
    print(f"  {GREEN}✓{RESET} 本地 HEAD: {local_head}")

    # 1.4 检查远程可达性与一致性
    print(f"\n  {CYAN}远程仓库连通性...{RESET}")
    if not remote_reachable():
        issues.append("远程仓库不可达，无法验证持久化状态")
        print(f"  {RED}✗{RESET} 远程不可达")
    else:
        remote_head = get_remote_head()
        print(f"  {GREEN}✓{RESET} 远程 HEAD: {remote_head}")
        if local_head == remote_head:
            print(f"  {GREEN}✓{RESET} 本地与远程一致")
        elif remote_head == "空仓库":
            warnings.append("远程仓库为空，本会话是首次持久化")
        else:
            # 检查是否有未 push 的 commit
            unpushed = get_unpushed_commits()
            if unpushed:
                warnings.append(f"本地有 {len(unpushed)} 个未 push 的 commit，沙箱销毁后将丢失")
                for c in unpushed[:3]:
                    print(f"    {YELLOW}⚠{RESET} {c}")

    # 1.5 检查未提交变更
    uncommitted = get_uncommitted_files()
    if uncommitted:
        warnings.append(f"有 {len(uncommitted)} 个未提交文件")
        print(f"\n  {YELLOW}⚠{RESET} 未提交文件: {len(uncommitted)} 个")
    else:
        print(f"  {GREEN}✓{RESET} 工作区干净")

    # 1.6 显示最近 3 个 commit
    _, log = run("git log --oneline -3")
    print(f"\n  {CYAN}最近 commit:{RESET}")
    for line in log.split("\n"):
        print(f"    {line}")

    return finish(issues, warnings)


# ============================================================
# 关卡 2：工作中阶段性检查
# ============================================================

def gate_working():
    """工作中阶段性检查，确认本地状态。"""
    banner("关卡 2/3 · 工作中状态检查", CYAN)

    uncommitted = get_uncommitted_files()
    unpushed = get_unpushed_commits()

    print(f"  未提交文件: {len(uncommitted)} 个")
    print(f"  未 push commit: {len(unpushed)} 个")

    if uncommitted:
        print(f"\n  {YELLOW}未提交（前 5 个）:{RESET}")
        for f in uncommitted[:5]:
            print(f"    {f}")
    if unpushed:
        print(f"\n  {YELLOW}未 push（前 3 个）:{RESET}")
        for c in unpushed[:3]:
            print(f"    {c}")

    if not uncommitted and not unpushed:
        print(f"\n  {GREEN}✓ 全部已持久化{RESET}")
        return 0
    else:
        print(f"\n  {YELLOW}⚠ 有未持久化内容，记得调用 git_guard.py save{RESET}")
        return 0


# ============================================================
# 关卡 3：会话结束检查
# ============================================================

def gate_exit():
    """会话结束前强制检查，未 push 则拒绝退出。"""
    banner("关卡 3/3 · 会话结束检查（防丢失）", YELLOW)

    issues = []

    # 3.1 未提交文件
    uncommitted = get_uncommitted_files()
    if uncommitted:
        issues.append(f"有 {len(uncommitted)} 个未提交文件")
        print(f"  {RED}✗{RESET} 未提交文件: {len(uncommitted)} 个")
        for f in uncommitted[:5]:
            print(f"      {f}")
        if len(uncommitted) > 5:
            print(f"      ... 还有 {len(uncommitted)-5} 个")

    # 3.2 未 push 的 commit
    unpushed = get_unpushed_commits()
    if unpushed:
        issues.append(f"有 {len(unpushed)} 个未 push 的 commit，沙箱销毁后将丢失")
        print(f"\n  {RED}✗{RESET} 未 push commit: {len(unpushed)} 个")
        for c in unpushed[:5]:
            print(f"      {c}")
        if len(unpushed) > 5:
            print(f"      ... 还有 {len(unpushed)-5} 个")

    # 3.3 远程一致性验证
    if remote_reachable():
        local_head = get_local_head()
        remote_head = get_remote_head()
        if local_head != remote_head:
            issues.append(f"本地 HEAD({local_head}) ≠ 远程 HEAD({remote_head})")
            print(f"\n  {RED}✗{RESET} 本地与远程不一致")
            print(f"      本地: {local_head}")
            print(f"      远程: {remote_head}")
        else:
            print(f"\n  {GREEN}✓{RESET} 本地与远程一致")

    # 3.4 判定
    if issues:
        print(f"\n{RED}{BOLD}✗ 会话结束检查未通过！{RESET}")
        print(f"{RED}以下内容将随沙箱销毁丢失：{RESET}")
        for i in issues:
            print(f"  - {i}")
        print(f"\n{YELLOW}修复方法：{RESET}")
        print(f"  python3 Hermes/content-creation/scripts/git_guard.py save \"提交说明\"")
        print(f"  python3 Hermes/content-creation/scripts/session_check.py exit")
        print(f"\n{RED}禁止在未通过 exit 检查的情况下结束会话！{RESET}")
        # 写入状态文件记录未通过
        STATE_FILE.write_text(f"EXIT_FAILED: {len(issues)} issues", encoding="utf-8")
        return 1
    else:
        print(f"\n{GREEN}{BOLD}✓✓✓ 会话结束检查通过！{RESET}")
        print(f"{GREEN}所有工作已持久化到远程仓库，沙箱销毁后可安全恢复。{RESET}")
        STATE_FILE.write_text(f"PASSED: local=remote={get_local_head()}", encoding="utf-8")
        return 0


def finish(issues: list, warnings: list) -> int:
    """关卡 1/2 通用收尾。"""
    if issues:
        print(f"\n{RED}✗ 检查未通过：{len(issues)} 个问题{RESET}")
        for i in issues:
            print(f"  - {i}")
        return 1
    elif warnings:
        print(f"\n{YELLOW}⚠ 检查通过，但有 {len(warnings)} 个警告：{RESET}")
        for w in warnings:
            print(f"  - {w}")
        return 0
    else:
        print(f"\n{GREEN}✓ 检查通过{RESET}")
        return 0


def main():
    if len(sys.argv) < 2:
        print("用法: session_check.py [start|working|exit]")
        print()
        print("关卡说明：")
        print("  start   - 会话启动时建立基线（防止在空环境上假装工作还在）")
        print("  working - 工作中阶段性检查")
        print("  exit    - 会话结束前强制检查（未 push 则拒绝退出）")
        return 1

    cmd = sys.argv[1]
    if cmd == "start":
        return gate_start()
    elif cmd == "working":
        return gate_working()
    elif cmd == "exit":
        return gate_exit()
    else:
        print(f"未知命令: {cmd}")
        print("用法: session_check.py [start|working|exit]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
