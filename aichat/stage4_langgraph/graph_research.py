"""
LangGraph 实战案例：研究助手
综合运用：Agent节点 + 条件分支 + 循环 + Human-in-the-loop
"""

from typing import TypedDict, Annotated
from datetime import datetime
from dotenv import load_dotenv
import operator
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# 初始化
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
    temperature=0,
)

search_tool = TavilySearchResults(max_results=3)

class GraphState(TypedDict):
    # 你来定义 6 个字段
    question:str
    search_result:Annotated[str, operator.add]
    search_count:int
    is_sufficient:bool
    report:str
    final_output:str

def search_node(state:GraphState)->dict:
    question = state["question"]
    count = state["search_count"]
    results = search_tool.invoke({"query": question})
    formatted = f"\n--- 第{count+1}次搜索 ---\n"
    for r in results:
        formatted += r["content"] + "\n"
    return {"search_result": formatted, "search_count": count + 1}

def evaluate_node(state:GraphState)->dict:
    question = state["question"]
    search_result = state["search_result"]
    prompt = f"""
    你是一个研究助手。

    用户的问题是：{question}

    收集到的信息：
    {search_result}

    请根据以上信息，返回当前的收集信息是否充足对于回答用户的问题，你只能
    回答“YES” 或者 “NO”来表明是否充足，不可以返回任何其他东西
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    answer = response.content.strip().upper()
    is_sufficient = "YES" in answer
    return {"is_sufficient":is_sufficient}

def generate_report(state:GraphState)->dict:
    question = state["question"]
    search_result = state["search_result"]
    prompt = f"""
    你是一个研究助手。

    用户的问题是：{question}

    收集到的信息：
    {search_result}

    请根据以上信息，写一份简洁的研究报告（300字以内）。
    要求：有标题、有要点、有总结。
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"report":response.content}
def format_output(state:GraphState)->dict:
    report = state["report"]
    search_count = state["search_count"]
    question = state["question"]
    final_output = f"报告：{report}，搜索次数：{search_count}，问题：{question}"
    return {"final_output":final_output}

def should_continue(state: GraphState) -> str:
    """判断是否继续循环"""
    # 你的代码
    is_sufficient = state["is_sufficient"]
    search_count = state["search_count"]

    if search_count < 3 and not is_sufficient :
        return "search_more"
    return "sufficient"
    
graph = StateGraph(GraphState)

# 添加 4 个节点
graph.add_node("search_node", search_node)
graph.add_node("evaluate_node", evaluate_node)
graph.add_node("generate_report", generate_report)
graph.add_node("format_output", format_output)

# 入口
graph.set_entry_point("search_node")

# 边：search → evaluate（固定）
graph.add_edge("search_node", "evaluate_node")

# 条件边：evaluate → 判断 → search_more 或 sufficient
graph.add_conditional_edges(
    "evaluate_node",
    should_continue,
    {
        "search_more": "search_node",
        "sufficient": "generate_report"
    }
)

# 边：generate_report → format_output → END
graph.add_edge("generate_report", "format_output")
graph.add_edge("format_output", END)

# 编译（带中断和检查点）
memory = MemorySaver()
app = graph.compile(
    checkpointer=memory,
    interrupt_after=["generate_report"] # 在哪个节点后中断？
)

if __name__ == "__main__":
    print("=" * 50)
    print("研究助手")
    print("=" * 50)

    config = {"configurable": {"thread_id": "research_1"}}

    initial_state = {
        "question": "请对比分析2026年春节档票房前三名电影的口碑、票房走势和营销策略的差异",
        "search_result": "",
        "search_count": 0,
        "is_sufficient": False,
        "report": "",
        "final_output": ""
    }

    # 第一阶段：搜索 + 评估 + 生成报告（自动循环）
    print("\n🔍 开始研究...\n")
    result = app.invoke(initial_state, config=config)

    # 中断：显示报告给用户审查
    print("\n" + "=" * 50)
    print("📝 研究报告草稿：")
    print("=" * 50)
    print(result["report"])

    print("\n" + "=" * 50)
    user_input = input("修改报告？(回车跳过): ")

    if user_input.strip():
        app.update_state(config, {"report": user_input})
        print("✅ 报告已更新")
    else:
        print("✅ 使用原始报告")

    # 继续执行 format_output
    print("\n🔄 生成最终输出...\n")
    final = app.invoke(None, config=config)

    print("\n" + "=" * 50)
    print("📋 最终输出：")
    print("=" * 50)
    print(final["final_output"])