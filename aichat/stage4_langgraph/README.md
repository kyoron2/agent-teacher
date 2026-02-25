# Stage 4: LangGraph - 复杂 Agent 工作流

## 学习目标
掌握 LangGraph 的核心概念，学会构建包含条件分支、循环、Agent 集成和人工介入的复杂工作流。

## 核心概念

- **StateGraph（状态图）**：定义整个工作流的结构
- **State（状态）**：在节点之间传递的数据容器（TypedDict）
- **Node（节点）**：执行具体操作的函数，接收 State，返回更新
- **Edge（边）**：连接节点，定义流程走向
  - **普通边**：固定的下一步（`add_edge`）
  - **条件边**：根据条件决定下一步（`add_conditional_edges`）
- **MemorySaver**：检查点机制，保存执行状态，支持中断后恢复
- **Annotated**：给 State 字段附加合并策略（如 `operator.add` 累积追加）

## 文件说明

### 1. `graph_basic.py` - StateGraph 基础

**作用**：演示 State、Node、Edge 的基本用法

**核心知识点**：
- `TypedDict` 定义 State 结构
- 节点函数：接收 State，返回要更新的字段
- **State 自动合并**：节点返回的 dict 自动合并到 State 中（不是替换）
- `set_entry_point`、`add_edge`、`END`、`compile`

**实现的流程**：
```
用户输入 → [检测语言] → [生成问候] → END
```

**运行**：
```bash
uv run graph_basic.py
```

---

### 2. `graph_conditional.py` - 条件分支

**作用**：演示根据条件走不同路径

**核心知识点**：
- `add_conditional_edges(节点, 判断函数, 路径映射)`
- 判断函数：接收 State，返回路径名（字符串）
- 路径映射：字典定义路径名对应的节点

**实现的流程**：
```
用户问题 → [分析类型] → 判断
                        /      \
                   技术问题   账户问题
                    ↓          ↓
               [技术支持]  [账户支持]
                    ↓          ↓
                   END        END
```

**运行**：
```bash
uv run graph_conditional.py
```

---

### 3. `graph_loop.py` - 循环流程

**作用**：演示如何实现循环（条件边指向自己）

**核心知识点**：
- 循环 = 条件边的目标节点是自己
- 循环和分支用的是**同一个方法**（`add_conditional_edges`），区别在于目标节点
- 必须有退出条件，否则死循环

**实现的流程**：
```
[累加节点] ←──── 继续
    ↓               ↑
  判断 ─────────────┘
    ↓
  结束 → END
```

**运行**：
```bash
uv run graph_loop.py
```

---

### 4. `graph_agent.py` - Agent 集成

**作用**：把 Stage 3 的 Agent 作为节点嵌入到 LangGraph

**核心知识点**：
- Agent 在 LangGraph 中就是一个普通的节点函数
- Agent 的输入来自 State，输出写回 State
- Agent 的内部流程（工具调用、多步推理）对 LangGraph 是透明的

**实现的流程**：
```
用户问题 → [Agent 节点] → [格式化节点] → END
```

**运行**：
```bash
uv run graph_agent.py
```

---

### 5. `graph_hitl.py` - Human-in-the-loop

**作用**：在工作流中加入人工审查环节

**核心知识点**：
- `interrupt_after`：在指定节点执行后暂停
- `interrupt_before`：在指定节点执行前暂停
- `MemorySaver`：保存执行状态（类比游戏存档）
- `thread_id`：区分不同会话的唯一标识
- `update_state`：在中断时修改保存的 State
- `invoke(None, config)`：继续上次的执行

**实现的流程**：
```
[LLM 起草邮件] → ⏸️ 中断（用户审查）→ [格式化] → END
```

**运行**：
```bash
uv run graph_hitl.py
```

---

### 6. `graph_research.py` - 研究助手（综合实战）

**作用**：综合运用所有概念，实现一个完整的研究助手

**核心知识点**：
- `Annotated[str, operator.add]`：累积追加（搜索结果不会被替换）
- Tavily 搜索 + LLM 评估 + 条件分支 + 循环 + 人工审查
- `operator.add` 是 Python 的 `+` 运算符的函数版本
- 框架通过 `__metadata__` 读取 Annotated 附加信息并当作函数调用

**实现的流程**：
```
[搜索] ←──── 信息不足
  ↓               ↑
[评估] ───────────┘
  ↓
信息充足
  ↓
[生成报告] → ⏸️ 中断 → [格式化] → END
```

**运行**：
```bash
uv run graph_research.py
```

---

## 学习顺序

1. **`graph_basic.py`** → 理解 State、Node、Edge
2. **`graph_conditional.py`** → 掌握条件分支
3. **`graph_loop.py`** → 理解循环机制
4. **`graph_agent.py`** → 学会集成 Agent
5. **`graph_hitl.py`** → 掌握人工介入
6. **`graph_research.py`** → 综合实战

---

## 核心技术要点

### 1. State 的自动合并

```python
# 节点只需要返回要更新的字段
def my_node(state: GraphState) -> dict:
    return {"field_a": "新值"}  # 只更新 field_a，其他字段不变
```

### 2. 条件边 = 分支 + 循环

```python
# 分支：指向不同节点
{"路径A": "节点A", "路径B": "节点B"}

# 循环：指向自己
{"continue": "当前节点", "end": END}
```

### 3. Annotated 累积 State

```python
# 普通字段：替换
name: str  # 每次更新会替换旧值

# Annotated 字段：累积
results: Annotated[str, operator.add]  # 每次更新会追加到旧值后面
```

### 4. Human-in-the-loop 三件套

```python
memory = MemorySaver()                          # 1. 存档功能
app = graph.compile(checkpointer=memory,        # 2. 绑定存档
                    interrupt_after=["节点名"])   # 3. 设置中断点

config = {"configurable": {"thread_id": "会话ID"}}
result = app.invoke(initial_state, config)       # 第一次：执行到中断点
final = app.invoke(None, config)                 # 第二次：继续执行
```

---

## 常见问题

### Q1: 为什么第二次 invoke 要传 None？

`None` 表示"不是新的输入，继续上次的执行"。LangGraph 会从 MemorySaver 中恢复之前的 State。

### Q2: 为什么需要 thread_id？

MemorySaver 可以保存多个会话的状态。`thread_id` 是区分不同会话的唯一标识，类似 Django 的 session_id。

### Q3: 循环和分支有什么区别？

没有区别！都用 `add_conditional_edges`。区别在于字典中的目标节点：
- 指向其他节点 = 分支
- 指向自己 = 循环

### Q4: Annotated 的附加信息框架怎么读取？

框架用 `get_type_hints(include_extras=True)` 读取，然后从 `__metadata__` 属性取出函数直接调用。

---

## 下一步

完成 Stage 4 后，你可以：

- **Stage 5**：API 服务化、链路追踪、评估（部署 + 监控 + 测试）
- **实战项目**：结合 RAG + Agent + LangGraph，做一个完整的智能应用

---

## 参考资源

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [LangGraph 教程](https://langchain-ai.github.io/langgraph/tutorials/)
- [Python typing.Annotated 文档](https://docs.python.org/3/library/typing.html#typing.Annotated)
