from fastapi import FastAPI
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model
from langgraph.graph import START,END,StateGraph,MessagesState
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage,SystemMessage
from typing import Optional
import os

from dotenv import load_dotenv


load_dotenv()

FRONTEND_URL =os.getenv("FRONTEND_URL")


from uuid import uuid4

model = init_chat_model("gpt-4o-mini",model_provider = "openai")

class MyState(MessagesState):
    pass

def chatr(state):
    messages = state["messages"]
    response = model.invoke(messages)

    return {"messages":[response]}


builder = StateGraph(MyState)
builder.add_node("chatr",chatr)
builder.add_edge(START,"chatr")
builder.add_edge("chatr",END)

mem = MemorySaver()

my_chat_bot = builder.compile(checkpointer = mem)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],   # your Vite dev server
    allow_credentials=True,                    # ok if you ever use cookies; harmless otherwise
    allow_methods=["*"],                       # or ["POST"]
    allow_headers=["*"],                       # or ["Content-Type"]
)




class UpdateMessage(BaseModel):
    message:str
    id:Optional[str] = None










@app.post("/")
def talk(message:UpdateMessage):

    if(not message.id):
        id = str(uuid4())
    else:
        id = str(message.id)

    my_thread = {"configurable":{"thread_id":id}}
        
    response = my_chat_bot.invoke({"messages":[HumanMessage(message.message)]},my_thread)
    response_txt = response["messages"][-1].content
    print(message.message)
    print(response_txt)
    return {"response":response_txt,"id":id}






