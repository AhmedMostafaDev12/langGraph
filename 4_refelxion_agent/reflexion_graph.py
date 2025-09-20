from typing import List 

from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import revisor_chain, generation_chain
from tool_execution import execute_tools

graph = MessageGraph()
MAX_ITERATIONS = 2

graph.add_node("generate", generation_chain)
graph.add_node("execute_tools", execute_tools)
graph.add_node("revise", revisor_chain)

graph.add_edge("generate", "execute_tools")
graph.add_edge("execute_tools", "revise")

def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    if count_tool_visits >= MAX_ITERATIONS:
        return END
    return "execute_tools" 

graph.add_conditional_edges("revise", event_loop)
graph.set_entry_point("generate")

app = graph.compile()

print(app.get_graph().draw_mermaid())

response = app.invoke( "Write about how small business can leverage AI to grow")
for msg in response:
    if hasattr(msg, "content"):
        print(msg.content)

