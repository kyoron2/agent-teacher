from cmath import polar
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# 1. 初始化 LLM
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
)

# 2. 创建提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{language}翻译官。"),
    ("human", "请翻译这段话：{text}")
])

# 3. 实例化输出解析器
parser = StrOutputParser()

# 4. 构建 LCEL 链
chain = prompt | llm | parser

# 5. 执行链
result = chain.invoke({
    "language": "德语",
    "text": "生活就像一盒巧克力，你永远不知道下一块是什么味道。"
})

# 6. 打印结果
print(f"--- 翻译结果 ---")
print(result)