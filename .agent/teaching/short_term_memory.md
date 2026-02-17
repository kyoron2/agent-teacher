# 短期记忆

## 当前阶段
Stage 1：基础对话机器人（已完成）
Stage 2：RAG 与向量数据库（已完成）
Stage 3：Agent 与 Tool Calling（准备开始）

## 当前步骤
**Stage 3: Agent 与 Tool Calling** - ✅ 已完成

已完成：
- ✅ Step 0：全局概览（背景、ReAct 模式、LangChain 1.x 变化）
- ✅ Step 1：工具定义和手动调用（`tool_basic_demo.py`）
  - 学习 `@tool` 装饰器
  - 学习 `bind_tools()` 手动模式
  - 创建 `get_current_time` 和 `calculate` 工具
- ✅ Step 2：Agent 自动化（`agent_demo.py`）
  - 理解 LangChain 1.x 新 API（`create_agent`）
  - 掌握消息格式（`{"messages": [...]}`）
  - 实现多步推理（Agent 自动循环调用工具）
  - 理解消息对象（HumanMessage, AIMessage, ToolMessage, SystemMessage）
- ✅ Step 3：集成联网搜索工具（`agent_demo.py` + Tavily）
  - 注册 Tavily API，获取 API Key
  - 使用 `TavilySearchResults` 预制工具
  - 理解工具的即插即用设计
  - Agent 自动判断何时需要搜索
- ✅ Step 4：Chainlit Web UI 集成（`app_agent.py`）
  - 理解 Chainlit 事件驱动模型（`@cl.on_chat_start`, `@cl.on_message`）
  - 掌握异步编程（`async/await`）
  - 实现消息更新机制（先显示"思考中"，再更新为答案）
  - 完成从命令行到 Web 应用的升级

Stage 3 核心成果：
- 创建了 3 个可用的工具（时间、计算、搜索）
- 实现了能自主决策的 Agent
- 完成了 Web UI 应用（浏览器中对话）

下一步选择：
- Stage 4：LangGraph（复杂 Agent 工作流）
- 或：增强当前应用（添加更多工具、显示中间步骤）
- 或：实战项目（结合 RAG + Agent）

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

