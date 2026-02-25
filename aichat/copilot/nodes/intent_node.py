from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage 
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
    temperature=0,  # 保持 0，我们需要稳定的分类输出
)

def intent_node(state: dict) -> dict:
    question = state["question"]
    # 升级后的 3 分类 Prompt
    template = f"""你是一个智能请求路由器。请根据用户的输入，判断并只输出以下3个词中的1个：
    - "knowledge"：如果用户在讨论特定文档、文章、PDF的内容，或者要求总结某份资料。
    - "search"：如果用户询问实时信息（如天气、新闻、比赛结果），或者需要查询互联网百科知识。
    - "chat"：如果用户只是打招呼、闲聊、表达情绪，或询问无需外部来源的事实。

    注意：只能输出一个单词，不能包含任何其他内容或标点。

    用户输入：{question}
    """
    
    result = llm.invoke([HumanMessage(content=template)])
    intent = result.content.strip().lower()
    
    # 简单的容错处理
    if "knowledge" in intent:
        intent = "knowledge"
    elif "search" in intent:
        intent = "search"
    else:
        intent = "chat"
    
    print(f"👉 [Intent Node] 判断意图为: {intent}")  # 打印出来方便排错
    return {"intent": intent}
