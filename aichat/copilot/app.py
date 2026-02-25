import chainlit as cl
from graph import app
from utils.document import process_pdf_and_get_retriever
@cl.on_chat_start
async def on_chat_start():
    # 请求用户上传文件，这里限定了只接受以 .pdf 结尾的文件，只让传 1 个，限制大小在 50MB
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content="请上传一个PDF文件开始建立个人知识库（大小不超过50MB）：",
            accept=["application/pdf"],
            max_size_mb=50,
            timeout=180,
        ).send()
    file = files[0]
    msg = cl.Message(content=f"正在处理文件 `{file.name}`，请稍候...")
    await msg.send()
    retriever = process_pdf_and_get_retriever(file.path)
    cl.user_session.set("retriever",retriever)
    msg.content = f"文件 `{file.name}` 处理完成！现在你可以提问了。"
    await msg.update()


@cl.on_message
async def main(message: cl.Message):
    retriever = cl.user_session.get("retriever")
    result = app.invoke({
    "question": message.content, 
    "answer": "",
    "intent": "",  # 添加
    "retriever": retriever,
    "documents": []  # 添加
    })
    answer = result["answer"]
    documents = result["documents"]
    elements = [
        cl.Text(name=f"资料片段 {i+1}", content=doc.page_content, display="side")
        for i, doc in enumerate(documents)
    ]
    source_refs = "  ".join([f"`{el.name}`" for el in elements])
    print(f">>> 检索到 {len(documents)} 条资料")
    final_content = f"{answer}\n\n📎 资料来源：{source_refs}"
    await cl.Message(content=final_content, elements=elements).send()
