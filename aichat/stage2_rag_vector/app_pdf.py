import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableConfig
import chainlit as cl

load_dotenv()

# 1. 初始化模型
embeddings = OpenAIEmbeddings(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="BAAI/bge-m3",
    check_embedding_ctx_length=False,
    chunk_size=50
)

llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model="deepseek-ai/DeepSeek-V3",
    streaming=True
)

@cl.on_chat_start
async def on_chat_start():
    # 2. 请求用户上传 PDF
    files = None
    while files == None:
        files = await cl.AskFileMessage(
            content="请上传一个 PDF 文件",
            accept=["application/pdf"],
            max_size_mb=10,
            timeout=180,
        ).send()
    
    file = files[0]
    msg = cl.Message(content=f"正在处理 `{file.name}`...")
    await msg.send()

    # 3. 加载并切分 PDF
    loader = PyPDFLoader(file.path)
    pages = loader.load()
    
    # 这里的 chunk_size 可以根据需要调整
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = splitter.split_documents(pages)

    # 4. 存入临时向量数据库
    doc_search = await cl.make_async(Chroma.from_documents)(
        documents=splits,
        embedding=embeddings
    )
    
    # 5. 把 retriever 存入 Session，而不是存整个 chain
    retriever = doc_search.as_retriever()
    cl.user_session.set("retriever", retriever)

    msg.content = f"✅ `{file.name}` 处理完成！共切分为 {len(splits)} 个文本块。现在你可以问我关于它的问题了。"
    await msg.update()

@cl.on_message
async def main(message: cl.Message):
    # 1. 从 Session 获取检索器
    retriever = cl.user_session.get("retriever")
    
    # 2. 手动执行检索
    docs = await cl.make_async(retriever.invoke)(message.content)
    
    # 3. 将检索到的文档转换为 Chainlit 的 Text 元素
    elements = [
        cl.Text(name=f"参考来源 {i+1}", content=doc.page_content, display="inline")
        for i, doc in enumerate(docs)
    ]
    
    # 4. 拼接上下文供 LLM 使用
    context_str = "\n\n".join([doc.page_content for doc in docs])
    
    # 5. 构造 Prompt 并生成
    template = """你是一个专业的文档助手。
    请根据以下【参考资料】回答用户的问题。
    
    【参考资料】：
    {context}
    
    问题：{question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    chain = prompt | llm | StrOutputParser()
    
    msg = cl.Message(content="", elements=elements)
    
    async for chunk in chain.astream({
        "context": context_str,
        "question": message.content
    }):
        await msg.stream_token(chunk)
    
    await msg.send()