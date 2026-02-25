# 短期记忆

## 当前阶段
Stage 1：基础对话机器人（已完成）
Stage 2：RAG 与向量数据库（已完成）
Stage 3：Agent 与 Tool Calling（已完成）
Stage 4：LangGraph（已完成）
实战项目：个人知识库助手（进行中）

## 当前步骤
**实战项目：个人知识库助手（Knowledge Copilot）** - 进行中

功能：上传 PDF 建立知识库，提问时自动路由（RAG/直接回答）

步骤：
- ✅ Step 1：项目搭建 + 基础对话
- ✅ Step 2：知识库模块（PDF 上传 + RAG）
- ✅ Step 3：LangGraph 路由（意图分类）
- ✅ Step 4：搜索模块（采用 3 分类方案：知识库/搜索/闲聊）
- ⏳ 中间步骤：整理当前进度并提交 Git
- ⏳ Step 5：增加多轮对话记忆（History Memory）

下一步：先整理当前文件，更新 `.gitignore`，并引导学生提交代码到 Git 仓库。完成之后，再继续学习如何使用 LangGraph 的 MemorySaver。

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
- ✅ Tool Calling 与 Function Calling（LLM 如何调用工具）
- ✅ `@tool` 装饰器与工具定义
- ✅ LangChain 1.x Agent API（`create_agent`）
- ✅ 消息对象系统（HumanMessage, AIMessage, ToolMessage）
- ✅ Agent 多步推理与自动循环
- ✅ 第三方 API 集成（Tavily 搜索）
- ✅ Chainlit 异步编程（`async/await`、消息更新）
- ✅ StateGraph 基础（State、Node、Edge）
- ✅ 条件边（`add_conditional_edges`）
- ✅ 循环流程（条件边指向自己）
- ✅ Agent 作为 LangGraph 节点
- ✅ 人工介入（MemorySaver、interrupt、thread_id）
- ✅ `Annotated[str, operator.add]` 累积 State
- ✅ 控制反转 (IoC) 与声明式编程（Chainlit 和 LangGraph 的底层运行逻辑）

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
- LangChain 1.x 重大变化：`create_react_agent` → `create_agent`，不再需要 `AgentExecutor`
- 工具的 description 非常重要，决定 Agent 何时使用该工具
- `tool_call_id` 用于关联工具调用请求和响应，支持并发调用多个工具
- Chainlit 的消息更新机制提升用户体验（先显示"思考中"，再更新为答案）
- LangGraph 中断恢复需要 MemorySaver + thread_id，普通 invoke 会重新从头执行
- `Annotated` 的 `__metadata__` 属性让框架能读取附加信息并当作函数调用
- 使用框架（Chainlit/LangGraph）是声明式编程，编写组件并由框架自身的内部循环/服务器在收到事件时调用（控制反转）
