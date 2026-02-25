"""
LangGraph 条件分支示例：智能客服分流
演示 add_conditional_edges 的用法
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

# 定义 State 结构
class GraphState(TypedDict):
    """工作流的状态"""
    user_question: str    # 用户问题
    question_type: str    # 问题类型（technical/account）
    response: str         # 最终回复

def analyze_question(state: GraphState) -> dict:
    question = state["user_question"]
    dicts = ["登录","注册","忘记密码","重置密码","修改密码"]
    for dict in dicts:
        if dict in question:
            return  {"question_type": "account"}
    return {"question_type": "technical"} 
def technical_support(state: GraphState) -> dict:
    """节点2：技术支持"""
    # 你的代码
    question = state["user_question"]
    response = "技术支持"+question
    return {"response": response}

def account_support(state: GraphState) -> dict:
    """节点3：账户支持"""
    # 你的代码
    question = state["user_question"]
    response = "账户支持"+question
    return {"response": response}

def route_question(state: GraphState) -> str:
    """判断函数：根据问题类型路由"""
    # 你的代码
    question_type = state["question_type"]
    if question_type == "technical":
        return "technical_support"
    else:
        return "account_support"

graph = StateGraph(GraphState)

graph.add_node("analyze_question", analyze_question)
graph.add_node("technical_support", technical_support)
graph.add_node("account_support", account_support)

graph.set_entry_point("analyze_question")  # 填入：入口节点名

graph.add_conditional_edges(
    "analyze_question",
    route_question,
    {
        "technical_support":"technical_support",
        "account_support":"account_support"
    }
)
graph.add_edge("technical_support", END)
graph.add_edge("account_support", END)

app = graph.compile()

# 测试
if __name__ == "__main__":
    # 测试1：技术问题
    print("=" * 50)
    print("测试1：技术问题")
    print("=" * 50)
    
    result = app.invoke({
        "user_question": "我的软件无法启动",
        "question_type": "",
        "response": ""
    })
    print(f"问题类型: {result['question_type']}")
    print(f"回复: {result['response']}\n")
    
    # 测试2：账户问题
    print("=" * 50)
    print("测试2：账户问题")
    print("=" * 50)
    
    result = app.invoke({
        "user_question": "我忘记密码了",
        "question_type": "",
        "response": ""
    })
    print(f"问题类型: {result['question_type']}")
    print(f"回复: {result['response']}\n")