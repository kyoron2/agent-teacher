"""
LangGraph 循环示例：数字累加器
演示如何实现循环流程
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

# 定义 State 结构
class GraphState(TypedDict):
    """工作流的状态"""
    count: int           # 计数器
    max_count: int       # 最大循环次数
    result: str          # 最终结果

def increment(state: GraphState) -> dict:
    """累加节点：count += 1"""
    # 你的代码
    count = state["count"] + 1
    return {"count": count}

def should_continue(state: GraphState) -> str:
    """判断是否继续循环"""
    # 你的代码
    count = state["count"]
    max_count = state["max_count"]
    if count < max_count:
        return "continue"
    return "end"

graph = StateGraph(GraphState)

graph.add_node("increment",increment)
graph.set_entry_point("increment")
graph.add_conditional_edges(
    "increment",
    should_continue,
    {
        "continue":"increment",
        "end":END
    }
)
app = graph.compile()
# 测试
if __name__ == "__main__":
    print("=" * 50)
    print("测试：循环累加（最多3次）")
    print("=" * 50)
    
    result = app.invoke({
        "count": 0,
        "max_count": 3,
        "result": ""
    })
    
    print(f"\n最终结果: count = {result['count']}")
    print(f"循环了 {result['count']} 次")