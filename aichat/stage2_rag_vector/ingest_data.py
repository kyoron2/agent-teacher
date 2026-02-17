import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# 1. 初始化 Embedding
embeddings = OpenAIEmbeddings(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="BAAI/bge-m3",
    check_embedding_ctx_length=False
)

# 2. 加载文档
# 我们直接加载项目根目录下的 README.md (假设你有的话，没有的话我们创建一个)
file_path = "test_data.txt" 

# 为了演示，我们先写入一个长一点的测试文件
with open(file_path, "w", encoding="utf-8") as f:
    f.write("""
# 员工福利手册

## 1. 带薪休假
所有入职满一年的员工，每年享有 10 天带薪年假。
入职满三年者，增加至 15 天。
病假每月有 1 天全薪额度，超过部分按 80% 发放。

## 2. 远程办公
公司实行混合办公制。
每周三和周五为固定远程办公日。
其他时间如需远程，需提前向直属 Leader 申请。

## 3. 补充医疗保险
公司为所有正式员工购买高端医疗保险。
门诊报销比例为 90%，年度上限 20000 元。
子女可享受半价参保优惠。
    """)

print(f"正在加载文件: {file_path}...")
loader = TextLoader(file_path, encoding="utf-8")
docs = loader.load()
print(f"原始文档长度: {len(docs[0].page_content)} 字符")

# 3. 文本分割 (Splitting)
print("正在切分文档...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,    # 每块约 100 字符
    chunk_overlap=20,  # 重叠 20 字符，防止语义中断
    separators=["\n\n", "\n", " ", ""] # 优先按双换行切，再按单换行切
)
splits = text_splitter.split_documents(docs)

print(f"切分完成，共生成 {len(splits)} 个文档块。")
for i, split in enumerate(splits[:3]):
    print(f"\n--- 块 {i+1} ---")
    print(split.page_content)

# 4. 存入 ChromaDB
print("\n正在存入向量数据库...")
vector_store = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    collection_name="employee_handbook", # 新集合名
    persist_directory="./chroma_db"
)
print("入库完成！")