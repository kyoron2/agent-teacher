from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate  # 新组件：Prompt 模版

# 1. 加载配置 & 初始化 (这部分不变)
load_dotenv()
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
    temperature=0.7,
)

# 2. 定义 Prompt 模版 (就像 Django 的 template)
# 我们定义两个角色的模版：
# - system: AI 的人设，这里是一个通用翻译助手
# - user: 用户的具体输入，{text} 和 {target_language} 是要填的空
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的翻译助手。请将用户的输入翻译成 {target_language}。"),
    ("human", "{text}"),
])

# 3. 组合成链 (LCEL 语法)
# 管道符 `|` 的意思是：把 prompt 的输出，传给 llm
# 这就像 shell 里的 `cat file.txt | grep "error"`
chain = prompt | llm

# 4. 执行链 (invoke)
# 这里必须传入字典，因为模版里有两个空 {target_language} 和 {text}
response = chain.invoke({
    "target_language": "英语",
    "text": "今天天气真不错，我想去公园散步。"
})

print("AI 回复：", response.content)
