import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import chainlit as cl

# 加载环境变量（无实际LLM调用可忽略）
load_dotenv()

# 初始化LLM（可选，不影响按钮功能）
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_API_BASE", ""),
    api_key=os.getenv("OPENAI_API_KEY", "sk-xxx"),  # 占位符即可
    model="gpt-3.5-turbo",
    streaming=True
)
prompt = ChatPromptTemplate.from_messages([("human", "{question}")])
chain = prompt | llm | StrOutputParser()

# 初始化会话
@cl.on_chat_start
async def on_chat_start():
    welcome_msg = cl.Message(content="🎉 欢迎使用 Chainlit 常用方法演示！")
    await welcome_msg.send()
    cl.user_session.set("messages", [welcome_msg])

# 处理用户消息
@cl.on_message
async def main(message: cl.Message):
    user_query = message.content
    messages = cl.user_session.get("messages", [])
    messages.append(message)
    cl.user_session.set("messages", messages)

    # 1. 基础消息发送
    basic_msg = cl.Message(content=f"你发送的消息是：{user_query}")
    await basic_msg.send()
    messages.append(basic_msg)
    cl.user_session.set("messages", messages)

    # 2. 流式输出
    stream_msg = cl.Message(content="")
    await stream_msg.send()
    messages.append(stream_msg)
    cl.user_session.set("messages", messages)

    for i in range(5):
        await stream_msg.stream_token(f"流式输出第{i+1}个字符...")
        await asyncio.sleep(0.3)

    # 3. 更新消息
    await asyncio.sleep(1)
    stream_msg.content = "✅ 流式输出完成！这是更新后的消息内容"
    await stream_msg.update()

    # 4. 操作按钮（核心修复：payload 改为字典类型）
    action_msg = cl.Message(
        content="请选择一个操作：",
        actions=[
            cl.Action(
                name="delete_prev",
                value="delete",
                label="删除上一条消息",
                # 关键修改：payload 必须是字典（可自定义键值对）
                payload={"action_type": "delete", "target": "last_msg"}
            ),
            cl.Action(
                name="show_image",
                value="image",
                label="显示示例图片",
                payload={"action_type": "show_img", "img_type": "network"}
            )
        ]
    )
    await action_msg.send()
    messages.append(action_msg)
    cl.user_session.set("messages", messages)

# 处理删除按钮回调
@cl.action_callback("delete_prev")
async def on_delete_prev(action: cl.Action):
    messages = cl.user_session.get("messages", [])
    if len(messages) > 1:
        last_msg = messages.pop()
        await last_msg.remove()
        cl.user_session.set("messages", messages)
        tip_msg = cl.Message(content="🗑️ 已删除上一条消息！")
        await tip_msg.send()
        messages.append(tip_msg)
        cl.user_session.set("messages", messages)
    else:
        await cl.Message(content="⚠️ 没有更多消息可以删除了！").send()

# 处理显示图片按钮回调
@cl.action_callback("show_image")
async def on_show_image(action: cl.Action):
    img_msg = cl.Message(content="📸 这是示例图片（网络图片）：")
    await img_msg.send()
    messages = cl.user_session.get("messages", [])
    messages.append(img_msg)
    cl.user_session.set("messages", messages)

    # 发送网络图片
    img_element = cl.Image(
        name="network_img",
        url="https://picsum.photos/200/200",
        display="inline"
    )
    await img_element.send(for_id=img_msg.id)

# 运行入口
if __name__ == "__main__":
    import sys
    os.system(f"chainlit run {sys.argv[0]} --port 8000")