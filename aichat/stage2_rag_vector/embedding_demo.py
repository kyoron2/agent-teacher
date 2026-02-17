import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import numpy as np

load_dotenv()

# 1. 初始化 Embedding 模型
embeddings = OpenAIEmbeddings(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="BAAI/bge-m3", 
    check_embedding_ctx_length=False
)

# 2. 定义两句意思相近的话，和一句无关的话
text1 = "不管是白猫还是黑猫，捉到老鼠就是好猫。"
text2 = "只要能解决问题，用什么方法都行。"
text3 = "今天天气真不错，适合出去野餐。"

print("正在计算向量... (这可能需要几秒钟)")

# 3. 将文本转换为向量
vec1 = embeddings.embed_query(text1)
vec2 = embeddings.embed_query(text2)
vec3 = embeddings.embed_query(text3)

print(f"向量维度: {len(vec1)}")
print(f"向量前5位: {vec1[:5]}...")

# 4. 计算余弦相似度函数
def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 5. 比较相似度
similarity_1_2 = cosine_similarity(vec1, vec2)
similarity_1_3 = cosine_similarity(vec1, vec3)

print(f"\n--- 相似度结果 (越接近 1 越相似) ---")
print(f"句子1 vs 句子2 (语义相似): {similarity_1_2:.4f}")
print(f"句子1 vs 句子3 (语义无关): {similarity_1_3:.4f}")