import sys
import os

# 确保可以导入skills_upgrade模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from skills_store_cli import main

if __name__ == "__main__":
    # 运行skillhub的帮助命令
    sys.argv = ["skillhub", "--help"]
    main()
