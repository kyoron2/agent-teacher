"""
LangGraph Human-in-the-loop 示例：邮件助手
演示如何在工作流中加入人工审查环节
"""
from datetime import datetime
from typing import TypedDict
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# 定义 State
class GraphState(TypedDict):
    topic: str       # 邮件主题
    draft: str       # Agent 起草的草稿
    final: str       # 最终邮件

# 初始化 LLM（不需要工具，直接用 LLM 写邮件）
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
    temperature=0.7,  # 写邮件用稍高的创造力
)

def draft_email(state:GraphState)->dict:
    topic = state["topic"]
    response = llm.invoke([HumanMessage(content=f"请根据主题起草一封邮件：{topic}")])
    print(response.content)
    return {"draft":response.content}

def format_email(state:GraphState)->dict:
    draft = state["draft"]
    time = datetime.now().strftime("%Y%m%d")
    final = f"""发件人：[EMAIL_ADDRESS]
收件人：[EMAIL_ADDRESS]
日期：{time}
主题：{state['topic']}

{draft}
"""
    print(final)
    return {"final":final}

# 创建图
graph = StateGraph(GraphState)

# 添加节点
graph.add_node("draft_email", draft_email)  # 起草节点
graph.add_node("format_email", format_email)  # 格式化节点

# 设置入口和边
graph.set_entry_point("draft_email")
graph.add_edge("draft_email", "format_email")  # 起草 → 格式化
graph.add_edge("format_email", END)    # 格式化 → 结束

# 编译（关键：在起草节点后中断）
# MemorySaver：把每次执行的 State 保存在内存中，支持中断后继续
memory = MemorySaver()
app = graph.compile(
    checkpointer=memory,              # 启用检查点机制
    interrupt_after=["draft_email"]   # 在起草节点后中断
)
if __name__ == "__main__":
    print("=" * 50)
    print("邮件助手（带人工审查）")
    print("=" * 50)
    
    # 初始输入
    initial_state = {
        "topic": "本周项目进度汇报",
        "draft": "",
        "final": ""
    }
    
    # thread_id：本次会话的唯一标识，同一个 thread_id 才能继续上次的执行
    config = {"configurable": {"thread_id": "email_session_1"}}

    # 第一次执行（执行到中断点后暂停）
    print("\n🤖 Agent 正在起草邮件...\n")
    result = app.invoke(initial_state, config=config)
    
    # 显示草稿给用户
    print("\n" + "=" * 50)
    print("📝 草稿（请审查）：")
    print("=" * 50)
    print(result["draft"])
    
    # 用户决定是否修改
    print("\n" + "=" * 50)
    user_input = input("是否修改草稿？(直接回车跳过，或输入修改内容): ")
    
    if user_input.strip():
        # 用户修改草稿：更新 State 并重新保存
        app.update_state(config, {"draft": user_input})
        print("✅ 草稿已更新")
    else:
        print("✅ 使用原始草稿")
    
    # 第二次执行（传入 None 表示继续上次，不是重头开始）
    print("\n🔄 继续执行...\n")
    final_result = app.invoke(None, config=config)
    
    # 显示最终结果
    print("\n" + "=" * 50)
    print("📧 最终邮件：")
    print("=" * 50)
    print(final_result["final"])