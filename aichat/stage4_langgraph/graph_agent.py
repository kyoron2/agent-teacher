"""
LangGraph + Agent 集成示例
演示如何把 LangChain Agent 作为节点嵌入到 LangGraph
"""

from typing import TypedDict
from datetime import datetime
from dotenv import load_dotenv
import os

# LangChain 核心
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

# LangGraph
from langgraph.graph import StateGraph, END

# 加载环境变量
load_dotenv()

# ============================================
# 工具定义（从 Stage 3 复制）
# ============================================

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

# 初始化 LLM 和 Agent
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
    temperature=0,
)

tools = [get_current_time, calculate]
agent = create_agent(llm, tools)

# ============================================
# 定义 State
# ============================================

class GraphState(TypedDict):
    """工作流的状态"""
    # 你的代码：定义 3 个字段
    user_question:str
    agent_response:str
    formatted_output:str

def agent_node(state: GraphState) -> dict:
    """节点1：调用 Agent"""
    user_question = state["user_question"]
    result = agent.invoke({
        "messages": [HumanMessage(content=user_question)]
    })
    print(f"Agent 回答: {result['messages'][-1].content}")
    return {"agent_response": result["messages"][-1].content}

def format_output(state: GraphState) -> dict:
    """节点2：格式化输出"""
    # 你的代码
    agent_response = state["agent_response"]
    formatted_output = f"""用户问题: {state['user_question']}
Agent 回答: {agent_response}
"""
    print(f"\n{'='*50}")
    print(f"格式化输出:")
    print(formatted_output)
    print(f"{'='*50}")
    return {"formatted_output": formatted_output}

# ============================================
# 构建图
# ============================================

# 创建图
graph = StateGraph(GraphState)

# 添加节点
graph.add_node("agent_node", agent_node)  # Agent 节点
graph.add_node("format_output", format_output)  # 格式化节点

# 设置入口
graph.set_entry_point("agent_node")

# 添加边（线性流程）
graph.add_edge("agent_node", "format_output")  # Agent → 格式化
graph.add_edge("format_output", END)    # 格式化 → 结束

# 编译
app = graph.compile()
# ============================================
# 测试
# ============================================

if __name__ == "__main__":
    # 测试1：时间查询
    print("=" * 50)
    print("测试1：时间查询")
    print("=" * 50)
    
    result = app.invoke({
        "user_question": "现在几点了？",
        "agent_response": "",
        "formatted_output": ""
    })
    
    print(f"\n{result['formatted_output']}\n")
    
    # 测试2：计算任务
    print("=" * 50)
    print("测试2：计算任务")
    print("=" * 50)
    
    result = app.invoke({
        "user_question": "帮我计算 999 * 888",
        "agent_response": "",
        "formatted_output": ""
    })
    
    print(f"\n{result['formatted_output']}\n")