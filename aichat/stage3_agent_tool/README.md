# Stage 3: Agent 与 Tool Calling

## 学习目标
掌握 Tool Calling 机制，学会创建自定义工具和第三方工具集成，实现能自主决策的 Agent。

## 核心概念
- **Tool Calling（工具调用）**: LLM 如何识别需求并调用外部工具获取信息或执行操作
- **Function Calling**: OpenAI API 的底层机制，通过 JSON Schema 描述工具
- **Agent（智能体）**: 能够自主决策、使用工具、多步推理的 AI 系统
- **ReAct 模式**: Reasoning（推理）+ Acting（行动）的循环模式
- **LangChain 1.x**: 新版本的 Agent API，更简洁高效

## 文件说明

### 1. `tool_basic_demo.py` - 工具调用基础

**作用**: 演示手动模式的工具调用流程

**核心知识点**:
- `@tool` 装饰器：把 Python 函数变成 LLM 可调用的工具
- `bind_tools()`: 把工具绑定到 LLM
- 手动检查 `tool_calls` 并执行工具
- docstring 的重要性（LLM 靠它判断何时使用工具）

**包含的工具**:
- `get_current_time()`: 获取当前日期时间
- `calculate()`: 执行数学计算

**运行**:
```bash
uv run python tool_basic_demo.py
```

**学习重点**:
- 理解工具调用的完整流程（LLM 决策 → 工具执行 → 结果返回）
- 观察 LLM 如何根据 description 选择工具

---

### 2. `agent_demo.py` - Agent 自动化（命令行版本）

**作用**: 使用 LangChain 1.x 的 Agent API 实现自动化工具调用

**核心知识点**:
- `create_agent()`: LangChain 1.x 的新 API（替代旧版 `create_react_agent`）
- 消息格式：`{"messages": [HumanMessage(...)]}`
- 消息对象系统：HumanMessage, AIMessage, ToolMessage, SystemMessage
- Agent 的多步推理和自动循环

**包含的工具**:
- `get_current_time()`: 时间查询
- `calculate()`: 数学计算
- `TavilySearchResults`: 联网搜索（需要 Tavily API Key）

**运行**:
```bash
uv run python agent_demo.py
```

**学习重点**:
- LangChain 1.x vs 0.x 的 API 变化
- Agent 如何自动判断需要哪个工具
- 多步推理的实现（测试 3："现在几点？1小时后几点？"）
- 搜索工具的集成和使用

---

### 3. `app_agent.py` - Chainlit Web UI 版本

**作用**: 把 Agent 做成 Web 应用，用户可以在浏览器中对话

**核心知识点**:
- Chainlit 事件驱动模型：`@cl.on_chat_start`, `@cl.on_message`
- 异步编程：`async/await`
- 消息更新机制：先显示"正在思考..."，再更新为答案
- 从命令行到 Web 应用的升级

**运行**:
```bash
uv run chainlit run app_agent.py
```
然后在浏览器打开 `http://localhost:8000`

**学习重点**:
- Chainlit 的异步消息处理
- 用户体验优化（实时反馈）
- Agent 在 Web 环境中的集成

---

### 4. `test_tavily.py` - Tavily API 测试

**作用**: 验证 Tavily API Key 是否配置正确

**运行**:
```bash
uv run python test_tavily.py
```

**预期输出**:
```
✅ 找到 API Key: tvly-dev-c...
✅ 搜索成功！
结果数量: 2
```

---

## 环境配置

### 必需的 API Key

在 `.env` 文件中配置：

```env
# LLM 服务（硅基流动）
OPENAI_API_BASE=https://api.siliconflow.cn/v1
OPENAI_API_KEY=sk-xxxxx

# Tavily 搜索 API
TAVILY_API_KEY=tvly-xxxxx
```

### 获取 Tavily API Key

1. 访问 https://tavily.com/
2. 注册账号（免费，每月 1000 次搜索）
3. 在 Dashboard 复制 API Key
4. 添加到 `.env` 文件

---

## 学习顺序

1. **`tool_basic_demo.py`** → 理解工具调用的底层流程
2. **`agent_demo.py`** → 掌握 Agent 自动化
3. **`test_tavily.py`** → 配置搜索 API
4. **`agent_demo.py`（再次运行）** → 测试搜索功能
5. **`app_agent.py`** → 体验 Web UI

---

## 核心技术要点

### 1. 工具定义的最佳实践

```python
@tool
def function_name(param: type) -> return_type:
    """工具的简短描述。
    
    详细说明何时使用此工具，包含关键词。
    
    Args:
        param: 参数说明
    """
    # 实现
    return result
```

**关键点**:
- 必须有类型标注（`param: str`）
- docstring 第一行是简短描述
- 详细说明中包含"何时使用"的关键词
- LLM 靠 docstring 判断是否调用此工具

---

### 2. LangChain 1.x vs 0.x 对比

| 特性 | 0.x（旧版）| 1.x（新版）|
|-----|-----------|-----------|
| 创建 Agent | `create_react_agent()` | `create_agent()` |
| 执行引擎 | 需要 `AgentExecutor` | Agent 自身可执行 |
| Prompt | 需要 `hub.pull()` | 内置默认 Prompt |
| 输入格式 | `{"input": "..."}` | `{"messages": [...]}` |
| 底层机制 | 文本解析（ReAct 格式）| 原生 Function Calling |

---

### 3. 消息对象系统

| 消息类型 | 作用 | 创建方式 |
|---------|------|---------|
| **HumanMessage** | 用户输入 | `HumanMessage(content="...")` |
| **AIMessage** | AI 回复或工具调用 | LLM 自动生成 |
| **ToolMessage** | 工具执行结果 | 系统自动创建 |
| **SystemMessage** | 系统指令 | `SystemMessage(content="...")` |

**关键概念**:
- `tool_call_id`: 关联工具调用请求和响应，支持并发调用
- 消息历史：`result["messages"]` 包含完整的对话记录

---

### 4. 工具的即插即用设计

**核心原理**: 所有工具都遵循统一接口

```python
class BaseTool:
    name: str           # 工具名称
    description: str    # 工具描述
    def invoke(input):  # 执行方法
        pass
```

**好处**:
- 自定义工具（`@tool`）和预制工具（`TavilySearchResults`）完全兼容
- Agent 不关心工具的实现，只看 `name` 和 `description`
- 添加新工具只需 `tools.append(new_tool)`

---

## 常见问题

### Q1: 为什么 Agent 选错工具？

**原因**: description 写得不清楚

**解决**:
- 在 description 中明确说明"何时使用"
- 包含关键词（如"实时信息"、"数学计算"）
- 避免模糊的描述（如"一个函数"）

---

### Q2: Tavily 搜索失败？

**检查清单**:
1. API Key 是否正确配置在 `.env` 文件
2. 是否安装了 `langchain-community`（`uv add langchain-community`）
3. 网络是否正常（Tavily 需要访问国外服务器）

---

### Q3: LangChain 版本问题？

**症状**: 导入错误（`cannot import name 'create_react_agent'`）

**原因**: LangChain 1.x 废弃了旧 API

**解决**:
- 使用 `create_agent` 代替 `create_react_agent`
- 不需要 `AgentExecutor`
- 参考 `agent_demo.py` 的写法

---

## 进阶扩展

### 添加更多工具

**示例：天气查询工具**

```python
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。
    
    当用户询问天气、温度、气象时使用。
    
    Args:
        city: 城市名称，如"北京"、"上海"
    """
    # 调用天气 API
    return f"{city}的天气是..."

# 添加到工具列表
tools.append(get_weather)
```

---

### 显示 Agent 的中间步骤

在 Chainlit 中显示 Agent 调用了哪些工具：

```python
@cl.on_message
async def main(message: cl.Message):
    result = agent.invoke(...)
    
    # 遍历消息历史，显示工具调用
    for msg in result["messages"]:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            await cl.Message(
                content=f"🔧 调用工具: {msg.tool_calls[0]['name']}"
            ).send()
```

---

## 下一步

完成 Stage 3 后，你可以：

- **Stage 4**: LangGraph（复杂 Agent 工作流、状态管理）
- **实战项目**: 结合 RAG + Agent，做一个"能搜索 + 能查文档"的智能助手
- **增强应用**: 添加更多工具、优化 UI、添加对话历史

---

## 参考资源

- [LangChain 官方文档 - Agents](https://python.langchain.com/docs/modules/agents/)
- [Tavily API 文档](https://docs.tavily.com/)
- [Chainlit 文档](https://docs.chainlit.io/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
