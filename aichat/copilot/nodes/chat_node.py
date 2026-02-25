from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage 
from dotenv import load_dotenv
import os
load_dotenv()
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
    temperature=0.7,  # 写邮件用稍高的创造力
)

def chat_node(state: dict) -> dict:
    question = state["question"]
    retriever = state["retriever"]
    document= retriever.invoke(question)
    context ="\n\n".join([doc.page_content for doc in document])  
    template = f"""你是一个由公司内部文档驱动的 AI 助手。
    请仅根据以下提供的【参考资料】回答问题。如果资料中没有提到相关信息，请直接回答“资料中未提及”。

    【参考资料】：
    {context}

    问题：{question}
    """
    result = llm.invoke([HumanMessage(content=template)])
    return {"answer":result.content,"documents":document }
def direct_chat_node(state: dict) -> dict:
    question = state["question"]
    result = llm.invoke([HumanMessage(content=question)])
    return {"answer":result.content, "documents": []}