"""
Agent + Chainlit Web UI
"""

from datetime import datetime
from dotenv import load_dotenv
import os

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults
import chainlit as cl

load_dotenv()

# 工具定义（从 agent_demo.py 复制）
@tool
def get_current_time() -> str:
    """获取当前的日期和时间。
    当用户询问"现在几点"、"今天几号"、"当前时间"时使用此工具。
    """
    now = datetime.now()
    return now.strftime("%Y年%m月%d日 %H:%M:%S")

@tool
def calculate(expression: str) -> str:
    """执行数学计算。
    当用户需要进行数学运算时使用此工具。
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"

# 初始化
search_tool = TavilySearchResults(max_results=3, description="用于搜索互联网上的实时信息。")
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
    temperature=0,
)
tools = [get_current_time, calculate, search_tool]
agent = create_agent(llm, tools)

@cl.on_chat_start
async def start():
    await cl.Message(content="欢迎使用Agent！").send()

@cl.on_message
async def main(message:cl.Message):
    msg = cl.Message(content="正在思考...")
    await msg.send()

    result = agent.invoke({
        "messages": [HumanMessage(content=message.content)]
    })

    final_answer = result["messages"][-1].content
    msg.content = final_answer
    await msg.update()
