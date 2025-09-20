from typing import TypedDict 
from langgraph.graph import END, StateGraph

class SimpleState(TypedDict):
    count: int

def increment(state: SimpleState) -> SimpleState:
    return {
        "count": state["count"] +1 
    }

def should_end(state: SimpleState) -> str:
    if(state["count"] < 5):
        return "continue"
    return "stop"

graph = StateGraph(SimpleState)
graph.add_node("increment", increment)
graph.set_entry_point("increment")
graph.add_conditional_edges("increment", should_end, {
    "continue": "increment",
    "stop": END
})

app = graph.compile()

state = {"count": 0}
final_state = app.invoke(state)
print(final_state)