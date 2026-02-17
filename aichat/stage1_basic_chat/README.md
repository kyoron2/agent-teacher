# Stage 1: 基础对话机器人

## 学习目标
掌握 LLM API 调用、Prompt Template、流式输出和 Chainlit Web 框架。

## 核心概念
- **Token 与上下文窗口**：LLM 如何"理解"文本
- **Prompt Template**：结构化提示词（system/human/ai 角色）
- **LCEL 管道**：LangChain Expression Language，用 `|` 连接组件
- **Chainlit**：事件驱动的 Web UI 框架，支持流式输出

## 文件说明

### 1. `hello_llm.py` - 第一次 LLM 调用
**作用**: 验证 LLM API 连接是否成功  
**核心知识点**: 
- 环境变量配置（`.env` 文件）
- `ChatOpenAI` 基本用法
- `invoke()` vs `stream()` 的区别

**运行**:
```bash
uv run python hello_llm.py
```

---

### 2. `prompt_template_demo.py` - Prompt Template 实战
**作用**: 学习用结构化方式管理提示词  
**核心知识点**:
- `ChatPromptTemplate.from_messages()`
- 消息角色：`("system", ...)`, `("human", ...)`
- 变量插值：`{language}`, `{text}`
- LCEL 管道：`prompt | llm | parser`

**运行**:
```bash
uv run python prompt_template_demo.py
```

---

### 3. `translator.py` - 翻译助手
**作用**: 第一个实用小工具  
**核心知识点**:
- 更复杂的 Prompt 设计
- 流式输出 `stream()`

**运行**:
```bash
uv run python translator.py
```

---

### 4. `app.py` + `chainlit.md` - Chainlit Web UI
**作用**: 把命令行聊天机器人变成 Web 应用  
**核心知识点**:
- `@cl.on_chat_start` 和 `@cl.on_message` 装饰器
- `cl.Message().send()` 流式传输
- `chainlit.md` 作为欢迎页

**运行**:
```bash
uv run chainlit run app.py
```
然后在浏览器打开 `http://localhost:8000`

---

## 学习顺序
1. `hello_llm.py` → 确认环境能跑通
2. `prompt_template_demo.py` → 理解结构化提示词
3. `translator.py` → 实战演练
4. `app.py` → 变成 Web 应用

## 下一步
→ 进入 `stage2_rag_vector/`，学习如何让 AI "记住"外部文档
