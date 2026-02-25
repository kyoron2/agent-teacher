# 长期记忆

## 当前学习主题
LLM 应用开发（通过 "Personal Knowledge Copilot" 项目驱动学习）

## 技术背景摘要
学生熟悉 Python/Django/DRF 生态，不熟悉 LLM 相关库。
采用混合学习路径：每个 Stage 先学概念，再动手写代码。

## 工具选型结果

| 工具 | 选择 | 原因 |
|---|---|---|
| LLM 服务 | 硅基流动（SiliconFlow） | 国内可直接访问，兼容 OpenAI API 格式，学生已有 Key |
| 编排框架 | LangChain + LangGraph | 待确认 |
| 向量数据库 | ChromaDB | 待确认 |
| Web UI | Chainlit | 待确认 |
| 调试 | LangSmith | 待确认 |

## 学习路线图

| 阶段 | 概念学习 | 项目实操 | 状态 |
|---|---|---|---|
| Stage 1 | Token、Prompt Template、LLM API、流式输出 | 基础聊天机器人 + Web UI | ✅ 已完成 |
| Stage 2 | Embedding、向量数据库、RAG、文本分割 | 文档问答功能 | ✅ 已完成 |
| Stage 3 | Memory、Tool/Function Calling、Agent | 记忆 + 工具 | ✅ 已完成 |
| Stage 4 | 图论、状态管理、Human-in-the-loop | LangGraph 重构 | ✅ 已完成 |
| 实战项目 | 综合运用知识点设计系统架构 | 个人知识库助手 | ⏳ 进行中 |

### Stage 2: RAG 与 向量数据库 (已完成)
- [x] Embedding 概念与实战
- [x] ChromaDB 向量数据库操作
- [x] Document Loader 与 Text Splitter (PDF 处理)
- [x] Chainlit 集成：文件上传与动态 RAG

### Stage 3: Agent 与 Tool Calling (已完成)
- [x] Tool Calling 核心原理（OpenAI Function Calling 底层机制）
- [x] 自定义 Tool（`@tool` 装饰器、docstring 的重要性）
- [x] LangChain 1.x 新 API（`create_agent`、消息格式变化）
- [x] 消息对象系统（HumanMessage, AIMessage, ToolMessage, SystemMessage）
- [x] Agent 自动化（多步推理、自动循环）
- [x] 第三方工具集成（Tavily 搜索 API）
- [x] Chainlit Web UI（事件驱动、异步编程、消息更新）

### Stage 4: LangGraph - 复杂 Agent 工作流 (已完成)
- [x] LangGraph 背景和核心原理
- [x] StateGraph 基础（State、Node、Edge）
- [x] 条件分支（`add_conditional_edges`）
- [x] 循环流程（条件边指向自己）
- [x] 集成 LangChain Agent（Agent 作为节点）
- [x] Human-in-the-loop（MemorySaver、interrupt、thread_id）
- [x] 实战案例（研究助手：搜索+评估+循环+报告+审查）

**关键文件**：
- `stage4_langgraph/graph_basic.py` - StateGraph 基础示例
- `stage4_langgraph/graph_conditional.py` - 条件分支示例
- `stage4_langgraph/graph_loop.py` - 循环流程示例
- `stage4_langgraph/graph_agent.py` - Agent 集成示例
- `stage4_langgraph/graph_hitl.py` - Human-in-the-loop 示例
- `stage4_langgraph/graph_research.py` - 研究助手（综合实战）

### 实战项目: 个人知识库助手 (进行中)
- [x] Step 1：项目搭建与基础单节点图 (`copilot/`)
- [x] Step 2：知识库模块（PDF 上传 + RAG）
- [x] Step 3：LangGraph 路由（意图分类：knowledge/chat）
- [ ] Step 4：搜索模块（Tavily 网络搜索集成）
- [ ] Step 5：边界体验优化（中间状态、来源回溯）

## 重要讨论
- 2026-02-21: 讨论了意图分类的局限性（AI 无法单靠问题判断该用搜索还是 RAG）

## 关键决策记录
- 2026-02-15: 学习路径选择 → 混合路径（每 Stage 先学概念再动手）
- 2026-02-15: LLM 服务选择 → 硅基流动（SiliconFlow），学生已有 API Key
- 2026-02-17: 项目结构重组 → 按 Stage 分文件夹（stage1/2/3），便于回顾和管理
