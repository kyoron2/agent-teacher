# 标准库，用于类型注解
from typing import TypedDict
from nodes.intent_node import intent_node
# 来自 langgraph 库，用于构建状态图
from langgraph.graph import StateGraph, END
from typing import Any
from nodes.chat_node import chat_node,direct_chat_node
from nodes.search_node import search_node


class GraphState(TypedDict):
    question:str
    answer:str
    retriever: Any
    documents:Any
    intent:str
def should_knowledge(state: GraphState) -> str:
    """判断是否继续循环"""
    # 你的代码
    intent = state["intent"]
    if intent == "knowledge":
        return "chat_node"
    if intent == "search":
        return "search_node"
    return "direct_chat_node"

    
graph = StateGraph(GraphState)
graph.add_node("chat_node",chat_node)
graph.add_node("intent_node",intent_node)
graph.add_node("search_node",search_node)
graph.add_node("direct_chat_node",direct_chat_node)
graph.set_entry_point("intent_node")

graph.add_conditional_edges(
    "intent_node",
    should_knowledge,  # 返回下一个节点的名字
    {
        "direct_chat_node": "direct_chat_node",
        "chat_node": "chat_node",
        "search_node":"search_node"
    }
)
app = graph.compile()
