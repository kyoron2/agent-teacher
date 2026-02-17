# 短期记忆

## 当前阶段
Stage 1：基础对话机器人（已完成）
Stage 2：RAG 与向量数据库（已完成）
Stage 3：Agent 与 Tool Calling（准备开始）

## 当前步骤
**文件夹整理完成** - 按学习阶段重组项目结构：
- `stage1_basic_chat/` - 基础对话（hello_llm.py, app.py 等）
- `stage2_rag_vector/` - RAG 实战（embedding_demo.py, app_pdf.py 等）
- `stage3_agent_tool/` - Agent 待学习
- `tools/` - 工具演示（clientlin.py）
- `shared/` - 共享资源（chroma_db, .files）

下一步：开始 Stage 3 全局概览（Tool Calling 原理）。

## 已完成概念
- ✅ Token 与上下文窗口
- ✅ Prompt Template（消息角色：system/human/ai）
- ✅ LLM API 调用与流式输出（invoke vs stream）
- ✅ 基础环境配置与 API 连接测试 (`hello_llm.py`)
- ✅ 结构化提示词实操 (`prompt_template_demo.py`)
- ✅ LCEL 管道符与 StrOutputParser
- ✅ Chainlit Web 框架（事件驱动、流式传输、Session、Element展示）
- ✅ Embedding 向量化与余弦相似度 (`embedding_demo.py`)
- ✅ ChromaDB 向量数据库的基本操作 (`chroma_demo.py`)
- ✅ RAG 完整流程：检索+生成 (`rag_demo.py`)
- ✅ Document Loader (TextLoader/PyPDFLoader) 与 Text Splitter (Recursive)
- ✅ Chainlit 文件上传与动态 RAG 链 (`app_pdf.py`)
 

## 学生疑惑/偏好
- 学生不熟悉任何 LLM 相关库，完全从零开始
- 选择了混合路径（先概念后实操）
- 使用硅基流动，已有 Key

## 最近的错误及解决方案
（暂无）

## 关键发现/注意事项
- 硅基流动兼容 OpenAI API 格式，base_url 需要配置为硅基流动的地址
- 项目结构已重组：按 Stage 分文件夹，每个文件夹有 README.md 索引
- 共享资源（chroma_db, .files）统一放在 `shared/` 避免重复
