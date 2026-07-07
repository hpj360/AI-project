#!/usr/bin/env python3
"""Git 持久化护栏（根治沙箱环境丢失问题）。

根因：TRAE 远程沙箱是临时环境，会话结束后文件系统销毁。
      只有 push 到远程仓库的内容才能跨会话保留。
      之前会话的工作因未真实 push 而全部丢失。

根治：每次落盘必须 commit + push + 三重验证。

使用：
    cd /workspace
    python3 Hermes/content-creation/scripts/git_guard.py status   # 查看状态
    python3 Hermes/content-creation/scripts/git_guard.py save "提交说明"  # 保存+推送+验证
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent.parent  # /workspace


def run(cmd: str, check: bool = True, timeout: int = 60) -> tuple[int, str]:
    """运行 shell 命令，返回 (返回码, 输出)。"""
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=REPO_DIR, capture_output=True,
            text=True, timeout=timeout
        )
        out = (r.stdout + r.stderr).strip()
        if check and r.returncode != 0:
            print(f"  ✗ 命令失败: {cmd}", file=sys.stderr)
            print(f"    输出: {out[:500]}", file=sys.stderr)
        return r.returncode, out
    except subprocess.TimeoutExpired:
        print(f"  ✗ 超时: {cmd}", file=sys.stderr)
        return 1, "TIMEOUT"


def check_remote_reachable() -> bool:
    """检查远程仓库是否可达。"""
    code, _ = run("git ls-remote --heads origin", check=False, timeout=15)
    return code == 0


def status():
    """查看 git 持久化状态。"""
    print("=" * 60)
    print("Git 持久化状态检查")
    print("=" * 60)

    # 本地 HEAD
    code, local_head = run("git rev-parse HEAD")
    print(f"\n[1] 本地 HEAD: {local_head[:12]}")

    # 本地 log
    code, log = run("git log --oneline -5")
    print(f"\n[2] 本地最近 commit:")
    for line in log.split("\n"):
        print(f"    {line}")

    # 远程状态
    print(f"\n[3] 远程仓库连通性:")
    if check_remote_reachable():
        print(f"    ✓ 远程可达")
        code, remote_head = run("git ls-remote origin main", check=False)
        remote_head = remote_head.split()[0] if remote_head else "无"
        print(f"    远程 main HEAD: {remote_head[:12]}")
        if local_head.startswith(remote_head[:8]):
            print(f"    ✓ 本地与远程一致（已持久化）")
        else:
            print(f"    ✗ 本地领先远程（未 push，会话结束后将丢失！）")
    else:
        print(f"    ✗ 远程不可达（网络问题）")
        print(f"    ⚠ 警告：无法 push，本会话工作将随沙箱销毁丢失！")

    # 未提交变更
    code, status_out = run("git status --porcelain")
    lines = [l for l in status_out.split("\n") if l.strip()]
    print(f"\n[4] 未提交变更: {len(lines)} 个文件")
    for l in lines[:10]:
        print(f"    {l}")
    if len(lines) > 10:
        print(f"    ... 还有 {len(lines)-10} 个")

    # 未 push 的 commit
    code, unpushed = run("git log origin/main..HEAD --oneline", check=False)
    unpushed_lines = [l for l in unpushed.split("\n") if l.strip()]
    print(f"\n[5] 未 push 的 commit: {len(unpushed_lines)} 个")
    for l in unpushed_lines:
        print(f"    {l}")
    if unpushed_lines:
        print(f"\n  ⚠ 警告：以上 {len(unpushed_lines)} 个 commit 未 push，沙箱销毁后将丢失！")
    elif not lines:
        print(f"\n  ✓ 所有工作已持久化到远程")


def save(message: str):
    """commit + push + 三重验证。"""
    print("=" * 60)
    print(f"Git 持久化保存：{message}")
    print("=" * 60)

    # 0. 检查远程可达
    if not check_remote_reachable():
        print("\n✗ 远程仓库不可达，无法持久化！")
        print("  请检查网络或远程仓库配置。")
        return 1

    # 1. 配置 user（防止 commit 失败）
    run('git config user.email "ai-agent@hermes.local"', check=False)
    run('git config user.name "Hermes AI Agent"', check=False)

    # 2. add 所有变更
    print("\n[1/5] 暂存变更...")
    code, out = run("git add -A")
    if code != 0:
        return 1
    code, status = run("git status --porcelain")
    staged = [l for l in status.split("\n") if l.strip()]
    print(f"  ✓ 暂存 {len(staged)} 个文件")

    # 3. commit
    print("\n[2/5] 创建 commit...")
    code, _ = run(f'git commit -m "{message}"', check=False)
    if code != 0:
        code, out = run("git status --porcelain")
        if not out.strip():
            print("  ℹ 无变更需要 commit")
        else:
            print("  ✗ commit 失败")
            return 1
    else:
        code, head = run("git rev-parse HEAD")
        print(f"  ✓ commit: {head[:12]}")

    # 4. push（带重试）
    print("\n[3/5] 推送到远程...")
    success = False
    for attempt in range(3):
        code, out = run("git push origin main", check=False, timeout=30)
        if code == 0:
            success = True
            print(f"  ✓ push 成功（第 {attempt+1} 次尝试）")
            break
        else:
            print(f"  ⚠ 第 {attempt+1} 次失败: {out[:200]}")
            time.sleep(2)
    if not success:
        print("  ✗ push 3 次均失败！本会话工作未持久化！")
        return 1

    # 5. 三重验证
    print("\n[4/5] 三重验证...")
    # 验证1: 本地 HEAD
    code, local_head = run("git rev-parse HEAD")
    print(f"  [验证1] 本地 HEAD: {local_head[:12]}")

    # 验证2: 远程 HEAD
    code, remote_head = run("git ls-remote origin main", check=False)
    remote_head = remote_head.split()[0] if remote_head else ""
    print(f"  [验证2] 远程 HEAD: {remote_head[:12]}")

    # 验证3: git log
    code, log = run("git log --oneline -3")
    print(f"  [验证3] git log:")
    for line in log.split("\n"):
        print(f"    {line}")

    if local_head.startswith(remote_head[:8]):
        print("\n[5/5] ✓✓✓ 持久化成功！本地与远程一致，跨会话安全。")
        return 0
    else:
        print("\n[5/5] ✗ 验证失败：本地与远程不一致！")
        return 1


def main():
    if len(sys.argv) < 2:
        print("用法: git_guard.py [status|save '提交说明']")
        return 1
    cmd = sys.argv[1]
    if cmd == "status":
        status()
        return 0
    elif cmd == "save":
        if len(sys.argv) < 3:
            print("用法: git_guard.py save '提交说明'")
            return 1
        return save(sys.argv[2])
    else:
        print(f"未知命令: {cmd}")
        print("用法: git_guard.py [status|save '提交说明']")
        return 1


if __name__ == "__main__":
    sys.exit(main())
