from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
#-------------- to be solve later -------------------------# 
# from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


load_dotenv()

sqlite_conn = sqlite3.connect("checkpoint.sqlite", check_same_thread = False)
# memory = SqliteSaver(sqlite_conn)
memory = None

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class BasicChatState(TypedDict): 
    messages: Annotated[list, add_messages]

def chatbot(state: BasicChatState): 
    return {
       "messages": [llm.invoke(state["messages"])]
    }

graph = StateGraph(BasicChatState)

graph.add_node("chatbot", chatbot)

graph.add_edge("chatbot", END)

graph.set_entry_point("chatbot")

app = graph.compile(checkpointer=memory)

config = {"configurable": {
    "thread_id": 1
}}

while True: 
    user_input = input("User: ")
    if(user_input in ["exit", "end"]):
        break
    else: 
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        }, config=config)

        print("AI: " + result["messages"][-1].content)