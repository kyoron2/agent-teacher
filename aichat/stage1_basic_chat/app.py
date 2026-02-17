import os
from time import sleep
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import chainlit as cl  # 引入 Web 框架

load_dotenv()

# 1. 初始化我们要用的 Chain (这部分逻辑和之前一样)
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
    streaming=True  # 开启流式输出，让体验更丝滑
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个全能的 AI 助手。"),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

# 2. 定义 Web 交互逻辑
@cl.on_message
async def main(message: cl.Message):
    # 创建一个空的消息对象，准备接收流式输出
    msg = cl.Message(content="")
    print(message.content)
    print(message)
    await cl.Message("Hello World!").send()
    for i in range(60):
        sleep(0.1)
        await msg.stream_token("逐字内容")

    # # 使用 chain.astream 异步流式获取结果
    # async for chunk in chain.astream({"question": message.content}):
    #     await msg.stream_token(chunk)
    # 最后发送完整消息
    await msg.send()    
