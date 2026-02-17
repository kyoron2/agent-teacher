import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# 1. 初始化 Embedding 和 LLM
embeddings = OpenAIEmbeddings(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="BAAI/bge-m3",
    check_embedding_ctx_length=False
)

llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
)

# 2. 加载已存在的向量数据库
# 注意：我们直接加载刚才创建的 "company_rules" 集合
vector_store = Chroma(
    collection_name="employee_handbook",  
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# 将数据库转换为检索器 (Retriever)
# search_kwargs={"k": 1} 表示每次只找 1 条最相关的
retriever = vector_store.as_retriever(search_kwargs={"k": 1})

# 3. 定义 RAG 提示词模板
template = """你是一个由公司内部文档驱动的 AI 助手。
请仅根据以下提供的【参考资料】回答问题。如果资料中没有提到相关信息，请直接回答“资料中未提及”。

【参考资料】：
{context}

问题：{question}
"""
prompt = ChatPromptTemplate.from_template(template)

# 4. 构建 LCEL 链
# RunnablePassthrough() 允许我们将用户的输入直接传给 question
# retriever | format_docs 是一个简化的写法，实际开发中我们通常会自定义一个函数来格式化文档
def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])
print(format_docs(retriever.invoke("我要报销昨晚回家的打车费，有什么规定？")))
chain = (
    {
        "context": retriever | format_docs, # 1. 拿问题去检索，把结果拼成字符串赋值给 context
        "question": RunnablePassthrough()   # 2. 把问题原样赋值给 question
    }
    | prompt  # 3. 填充提示词
    | llm     # 4. 发给模型
    | StrOutputParser() # 5. 提取结果
)

# 5. 测试
question = "我想知道入职满三年的年假有多少天？"  
print(f"--- 提问：{question} ---")
print("AI 正在检索文档并生成回答...")

result = chain.invoke(question) 
print(f"\n回答：\n{result}")