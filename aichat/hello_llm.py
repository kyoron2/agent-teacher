from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# 1. 加载环境变量 (就像 Django 的 settings.py 加载)
load_dotenv()

# 2. 初始化客户端 (就像配置 Django 的 DATABASES)
# 我们使用的是 DeepSeek-V3 模型 (硅基流动提供的兼容接口)
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),  # 目标服务器：硅基流动
    api_key=os.getenv("OPENAI_API_KEY"),    # 你的密钥
    model="deepseek-ai/DeepSeek-V3",        # 指定调用的模型 ID
    temperature=0.7,                        # 创造力参数 (0.0 - 2.0)
)

# 3. 发送请求并获取响应 (就像 ORM 的 .get())
# invoke 会发起网络请求，等待完整响应返回
response = llm.invoke("你好，请用一句话介绍你自己。")

# 4. 打印结果
print("AI 回复内容：", response.content)
print("\n完整响应对象 (包含元数据)：")
print(response)
