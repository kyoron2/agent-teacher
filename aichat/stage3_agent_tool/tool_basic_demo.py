"""
Tool Calling 基础示例
演示如何定义工具并让 LLM 调用
"""

from datetime import datetime
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()

# ============================================
# 第 1 部分：定义工具
# ============================================

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


# ============================================
# 第 2 部分：绑定工具到 LLM
# ============================================

# 初始化 LLM
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),  # 目标服务器：硅基流动
    api_key=os.getenv("OPENAI_API_KEY"),    # 你的密钥
    model="deepseek-ai/DeepSeek-V3",        # 指定调用的模型 ID
    temperature=0.7,                        # 创造力参数 (0.0 - 2.0)
)

# 把工具绑定到 LLM（关键步骤！）
tools = [get_current_time, calculate]  # 工具列表
llm_with_tools = llm.bind_tools(tools)  # bind_tools() 自动生成 JSON Schema

print("✅ 工具已定义并绑定到 LLM")
print(f"可用工具: {[tool.name for tool in tools]}")
print()


# ============================================
# 第 3 部分：测试工具调用
# ============================================

def test_tool_calling(user_question: str):
    """测试工具调用的完整流程"""
    print(f"💬 用户问题: {user_question}")
    print("-" * 50)
    
    # Step 1: 调用 LLM（附带工具）
    response = llm_with_tools.invoke(user_question)
    
    # Step 2: 检查 LLM 是否想调用工具
    if response.tool_calls:
        print("🔧 LLM 决定调用工具:")
        
        # 遍历所有工具调用请求（可能同时调用多个工具）
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            print(f"  - 工具名: {tool_name}")
            print(f"  - 参数: {tool_args}")
            
            # Step 3: 执行对应的工具
            # 创建一个工具名到函数的映射
            tool_map = {
                "get_current_time": get_current_time,
                "calculate": calculate
            }
            
            if tool_name in tool_map:
                # 调用真实的 Python 函数
                tool_function = tool_map[tool_name]
                tool_result = tool_function.invoke(tool_args)  # .invoke() 是 LangChain 工具的标准调用方式
                print(f"  - 结果: {tool_result}")
                
                # Step 4: 把工具结果返回给 LLM（需要构造特殊的消息）
                # 这里为了演示简化，我们直接展示结果
                # 在 Agent 中，这一步是自动的
                print(f"\n✅ 最终答案: (需要再次调用 LLM，这里暂不实现)")
                print(f"   工具已返回结果，Agent 会自动完成后续步骤")
            else:
                print(f"  ⚠️ 未知工具: {tool_name}")
    else:
        # LLM 不需要工具，直接回答
        print("💡 LLM 直接回答（不需要工具）:")
        print(f"   {response.content}")
    
    print()


# ============================================
# 测试用例
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("Tool Calling 基础示例")
    print("=" * 50)
    print()
    
    # 测试 1：需要工具的问题（时间查询）
    test_tool_calling("现在几点了？")
    
    # 测试 2：需要工具的问题（计算）
    test_tool_calling("帮我计算 12345 * 67890")
    
    # 测试 3：不需要工具的问题
    test_tool_calling("你好，请介绍一下自己")
