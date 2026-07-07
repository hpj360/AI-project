# 护栏工具统一入口（在 /workspace 下运行：make <target>）
# 详细文档见 Hermes/AGENTS.md

SCRIPTS := Hermes/content-creation/scripts

.PHONY: help check start working exit save status validate

help: ## 显示所有命令
	@echo "Hermes 护栏工具命令清单："
	@echo ""
	@echo "  make check     - 关卡1：会话启动检查（建立基线）"
	@echo "  make working   - 关卡2：工作中阶段性检查"
	@echo "  make exit      - 关卡3：会话结束检查（必须通过）"
	@echo "  make save m=\"说明\" - 持久化保存（commit+push+验证）"
	@echo "  make status    - 查看 git 持久化状态"
	@echo "  make validate  - 知识库数据校验（防数据幻觉）"
	@echo ""
	@echo "典型工作流："
	@echo "  1. make check              # 会话开始"
	@echo "  2. <创建/修改文件>"
	@echo "  3. make save m=\"feat: xxx\" # 持久化"
	@echo "  4. make exit               # 会话结束前检查"

check start: ## 关卡1：会话启动检查
	@python3 $(SCRIPTS)/session_check.py start

working: ## 关卡2：工作中阶段性检查
	@python3 $(SCRIPTS)/session_check.py working

exit: ## 关卡3：会话结束检查（必须通过才能结束会话）
	@python3 $(SCRIPTS)/session_check.py exit

save: ## 持久化保存（commit+push+三重验证），用法：make save m="提交说明"
	@if [ -z "$(m)" ]; then echo "用法: make save m=\"提交说明\""; exit 1; fi
	@python3 $(SCRIPTS)/git_guard.py save "$(m)"

status: ## 查看 git 持久化状态
	@python3 $(SCRIPTS)/git_guard.py status

validate: ## 知识库数据校验
	@cd Hermes && PYTHONPATH=src python3 content-creation/scripts/validate_kb.py
