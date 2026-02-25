"""
LangGraph 基础示例：简单的问候流程
演示 State、Node、Edge 的基本用法
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

# 定义 State 结构
class GraphState(TypedDict):
    """工作流的状态"""
    user_input: str      # 用户输入
    language: str        # 检测到的语言
    greeting: str        # 生成的问候语
    
# ============================================
# 节点函数
# ============================================

def detect_language(state: GraphState) -> dict:
    """节点1：检测用户输入的语言"""
    user_input = state["user_input"]
    
    # 简单判断：包含中文字符就是中文
    if any('\u4e00' <= char <= '\u9fff' for char in user_input):
        language = "中文"
    else:
        language = "English"
    
    print(f"[节点1] 检测到语言: {language}")
    
    # 返回要更新的字段
    return {"language": language}


def generate_greeting(state: GraphState) -> dict:
    """节点2：根据语言生成问候语"""
    language = state["language"]
    user_input = state["user_input"]
    
    if language == "中文":
        greeting = f"你好！你刚才说的是：{user_input}"
    else:
        greeting = f"Hello! You said: {user_input}"
    
    print(f"[节点2] 生成问候语: {greeting}")
    
    return {"greeting": greeting}
# ============================================
# 构建图
# ============================================

# 1. 创建图
graph = StateGraph(GraphState)

# 2. 添加节点
graph.add_node("detect_language", detect_language)
graph.add_node("generate_greeting", generate_greeting)

# 3. 定义流程（添加边）
graph.set_entry_point("detect_language")  # 入口节点
graph.add_edge("detect_language", "generate_greeting")  # 节点1 → 节点2
graph.add_edge("generate_greeting", END)  # 节点2 → 结束

# 4. 编译
app = graph.compile()

# ============================================
# 测试
# ============================================

if __name__ == "__main__":
    # 测试1：中文输入
    print("=" * 50)
    print("测试1：中文输入")
    print("=" * 50)
    
    initial_state = {
        "user_input": "你好，世界！",
        "language": "",
        "greeting": ""
    }
    
    result = app.invoke(initial_state)
    print(f"\n最终结果: {result['greeting']}\n")
    
    # 测试2：英文输入
    print("=" * 50)
    print("测试2：英文输入")
    print("=" * 50)
    
    initial_state = {
        "user_input": "Hello, world!",
        "language": "",
        "greeting": ""
    }
    
    result = app.invoke(initial_state)
    print(f"\n最终结果: {result['greeting']}\n")