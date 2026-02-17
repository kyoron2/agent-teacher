import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

load_dotenv()

# 1. 初始化 Embedding 模型 (和之前一样)
embeddings = OpenAIEmbeddings(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="BAAI/bge-m3",
    check_embedding_ctx_length=False
)

# 2. 模拟一些私有文档数据
# Document 对象包含 page_content (内容) 和 metadata (元数据，如来源、页码)
docs = [
    Document(
        page_content="公司报销政策：打车费需要在晚上 9 点以后才能报销。",
        metadata={"source": "财务手册", "page": 1}
    ),
    Document(
        page_content="公司报销政策：餐饮费单人单次上限为 200 元。",
        metadata={"source": "财务手册", "page": 2}
    ),
    Document(
        page_content="年假政策：入职满一年可享受 10 天带薪年假。",
        metadata={"source": "员工手册", "page": 5}
    ),
]

print("正在初始化向量数据库并存入数据...")

# 3. 创建 Chroma 数据库实例并存入数据
# persist_directory: 指定数据存在本地哪里
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="company_rules", # 相当于 SQL 里的表名
    persist_directory="./chroma_db"  # 数据会存在当前目录下的 chroma_db 文件夹
)

print(f"成功存入 {len(docs)} 条文档。")

# 4. 模拟检索
query = "我要报销昨晚回家的打车费，有什么规定？"
print(f"\n--- 正在检索：{query} ---")

# k=1 表示只找最相似的那 1 条
results = vector_store.similarity_search(query, k=1)

for doc in results:
    print(f"\n找到相关文档 (来源: {doc.metadata['source']}):")
    print(f"内容: {doc.page_content}")