from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage 
from dotenv import load_dotenv
import os
from langchain_community.tools.tavily_search import TavilySearchResults  # 新增这一行
from langchain.agents import create_agent

load_dotenv()
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
    temperature=0.7,  # 写邮件用稍高的创造力
)

search_tool = TavilySearchResults(
    max_results=3,  # 最多返回 3 条搜索结果
    description="用于搜索互联网上的实时信息。当用户询问最新新闻、实时数据、或你不知道的信息时使用。"
)
tools = [search_tool]
def search_node(state:dict) ->dict:
    question = state["question"]
    agent = create_agent(llm, tools)
    result = agent.invoke({
        "messages": [HumanMessage(content=question)] 
    })
    final_answer = result["messages"][-1].content
    return {"answer":final_answer,"documents":[] }
