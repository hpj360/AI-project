"""Hermes 知识库框架 v1.0

提供：
- KnowledgeBase: 核心引擎（加载/lint/检索/统计）
- BM25 全文检索
- RRF 融合
- 规则重排（向量降级时使用）
- 知识图谱关系
"""
from .kb import KnowledgeBase, Entry, LintReport

__all__ = ["KnowledgeBase", "Entry", "LintReport"]
__version__ = "1.0.0"
