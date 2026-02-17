# Stage 2: RAG 与向量数据库

## 学习目标
理解 Embedding、向量相似度、向量数据库，掌握 RAG 完整流程。

## 核心概念
- **Embedding（向量化）**: 把文本变成数字向量，让 AI 能计算"相似度"
- **向量数据库（ChromaDB）**: 存储向量，快速检索相似内容
- **RAG（检索增强生成）**: Retrieval-Augmented Generation，让 LLM 基于外部文档回答问题
- **文本分割（Text Splitter）**: 把长文档切成小块，避免超出上下文窗口

## 文件说明

### 1. `embedding_demo.py` - Embedding 实验
**作用**: 理解文本向量化和余弦相似度  
**核心知识点**:
- `OpenAIEmbeddings().embed_documents()`
- 余弦相似度计算（`cosine_similarity`）
- 语义相似 vs 字面相似

**运行**:
```bash
uv run python embedding_demo.py
```

---

### 2. `chroma_demo.py` - ChromaDB 操作
**作用**: 学习向量数据库的增删查改  
**核心知识点**:
- `Chroma.from_texts()` 创建集合
- `similarity_search()` 检索相似文档
- 持久化存储（`persist_directory`）

**运行**:
```bash
uv run python chroma_demo.py
```

---

### 3. `rag_demo.py` - RAG 完整流程
**作用**: 实现"基于文档问答"的核心逻辑  
**核心知识点**:
- `RetrievalQA.from_chain_type()`
- `chain_type="stuff"` 的含义
- RAG 三步：检索 → 拼接 Prompt → 生成答案

**运行**:
```bash
uv run python rag_demo.py
```

---

### 4. `ingest_data.py` - 数据导入脚本
**作用**: 把外部文档（PDF/TXT）导入向量数据库  
**核心知识点**:
- `PyPDFLoader` / `TextLoader` 加载文档
- `RecursiveCharacterTextSplitter` 智能分割文本
- `chunk_size` 和 `chunk_overlap` 的作用

**运行**:
```bash
uv run python ingest_data.py
```

---

### 5. `app_pdf.py` - Chainlit PDF 问答
**作用**: 把 RAG 做成 Web 应用，支持上传 PDF  
**核心知识点**:
- `@cl.on_chat_start` 中初始化 RAG 链
- `cl.AskFileMessage()` 文件上传
- 动态创建向量数据库（每次会话独立）

**运行**:
```bash
uv run chainlit run app_pdf.py
```
然后上传 PDF 文件提问

---

### 6. `test_data.txt` - 测试数据
简单的文本文件，用于测试 RAG 流程。

---

## 学习顺序
1. `embedding_demo.py` → 理解向量化
2. `chroma_demo.py` → 掌握向量数据库
3. `rag_demo.py` → 完整 RAG 流程
4. `ingest_data.py` → 处理真实文档
5. `app_pdf.py` → Web 应用实战

## 下一步
→ 进入 `stage3_agent_tool/`，学习如何让 AI 使用"工具"（搜索、API 调用等）
