from chainlit.server import app
from fastapi import Request
from fastapi.responses import (
    HTMLResponse,
)
from langchain.prompts import ChatPromptTemplate
from chainlit.context import init_http_context
import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    template = """Your a brilliant bot who can comprehensively answer the users question from the given context Be polite and answer question breifly based on the context.
    Context: {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    runnable = prompt
    cl.user_session.set("runnable", runnable)
    print("Ready!")


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")

    msg = cl.Message(content="")

    await msg.update()
