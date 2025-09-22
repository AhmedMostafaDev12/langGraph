from typing import TypedDict, Annotated
from langgraph.graph import add_messages, END, StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv()

#------------ MemorySaver ---------------#
"""
this is keep a memory in the chatbot so it have a sense of memory and 
context aware 
this memory is maintained only for the single run of the code 
if the code stoped and run again  the bot will have no aware of the 
previous conversion 
this memory is locally in the machine memory  
"""
memory = MemorySaver()

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

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

#--------------- Thread_id----------------# 
"""
is a simply unique identifier for each specific conversation or workflow execution 
think it like :
- unique session ID for each user 
- A conversation ID that groups related messages together 
"""
app = graph.compile(checkpointer=memory)
config = {"configurable":{
    "thread_id":1
}}

while True:
    user_input = input("user: ")
    if(user_input in ["exit", "end"]):
        break
    else: 
        result = app.invoke({
            "messages" :[HumanMessage(content=user_input)]
        },config=config)

        print("AI: "+result["messages"][-1].content)