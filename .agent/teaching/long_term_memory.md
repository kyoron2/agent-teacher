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
| Stage 3 | Memory、Tool/Function Calling、Agent | 记忆 + 工具 | ⬜ 准备开始 |
| Stage 4 | 图论、状态管理、Human-in-the-loop | LangGraph 重构 | ⬜ |
| Stage 5 | API 服务化、链路追踪、评估 | 部署 + 监控 + 测试 | ⬜ |

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

**关键文件**：
- `stage3_agent_tool/tool_basic_demo.py` - 手动工具调用演示
- `stage3_agent_tool/agent_demo.py` - Agent 自动化（命令行版本）
- `stage3_agent_tool/app_agent.py` - Chainlit Web UI 版本

## 关键决策记录
- 2026-02-15: 学习路径选择 → 混合路径（每 Stage 先学概念再动手）
- 2026-02-15: LLM 服务选择 → 硅基流动（SiliconFlow），学生已有 API Key
- 2026-02-17: 项目结构重组 → 按 Stage 分文件夹（stage1/2/3），便于回顾和管理
