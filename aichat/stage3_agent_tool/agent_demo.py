# 基础库
from datetime import datetime
from dotenv import load_dotenv
import os

from langchain_community.tools.tavily_search import TavilySearchResults  # 新增这一行
# LangChain 核心
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# Agent 相关
# Agent 相关（LangChain 1.x 新 API）
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

# 加载环境变量
load_dotenv()

@tool
def get_current_time() -> str:
    """获取当前的日期和时间。
    
    当用户询问"现在几点"、"今天几号"、"当前时间"时使用此工具。
    """
    # 为什么要有这个工具？因为 LLM 的训练数据是过去的，不知道"现在"是什么时候
    now = datetime.now()
    return now.strftime("%Y年%m月%d日 %H:%M:%S")

@tool
def calculate(expression: str) -> str:
    """执行数学计算。
    
    当用户需要进行数学运算时使用此工具，比如"计算 123 * 456"。
    
    Args:
        expression: 数学表达式，例如 "123 * 456" 或 "(100 + 50) / 2"
    """
    # 为什么要有这个工具？因为 LLM 经常算错数学题，尤其是大数字
    # 注意：eval() 在生产环境有安全风险，这里仅用于演示
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"


llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),  # 目标服务器：硅基流动
    api_key=os.getenv("OPENAI_API_KEY"),    # 你的密钥
    model="deepseek-ai/DeepSeek-V3",        # 指定调用的模型 ID
    temperature=0,                        # 创造力参数 (0.0 - 2.0)
)
search_tool = TavilySearchResults(
    max_results=3,  # 最多返回 3 条搜索结果
    description="用于搜索互联网上的实时信息。当用户询问最新新闻、实时数据、或你不知道的信息时使用。"
)
tools = [get_current_time, calculate, search_tool]

agent = create_agent(llm, tools)



def test_agent(question: str):
    """测试 Agent（LangChain 1.x）"""
    print(f"\n{'='*50}")
    print(f"💬 用户问题: {question}")
    print('='*50)
    
    # 调用 Agent（新格式：messages）
    result = agent.invoke({
        "messages": [HumanMessage(content=question)] 
    })
    
    # 打印完整的消息历史（看到 Agent 的思考过程）
    print(f"\n📝 对话历史（共 {len(result['messages'])} 条消息）:")
    for i, msg in enumerate(result["messages"], 1):
        role = msg.__class__.__name__  # 消息类型（HumanMessage, AIMessage, ToolMessage）
        print(f"{i}. [{role}] {msg.content}")  # 只显示前 100 字符
    
    # 提取最终答案（最后一条消息）
    final_answer = result["messages"][-1].content
    
    print(f"\n✅ 最终答案:")
    print(final_answer)

if __name__ == "__main__":
    # 测试 1：简单问题
    test_agent("现在几点了？")
    
    # 测试 2：需要计算
    test_agent("帮我计算 999 * 888")
    
    # 测试 3：复杂问题（可能需要多步）
    test_agent("现在是几点？1小时后是几点？")
    # 测试 4：需要搜索的问题
    test_agent("2026年春节是几月几号？")
    # 测试 5：需要搜索的问题
    test_agent("最新的 Python 版本是什么？")
