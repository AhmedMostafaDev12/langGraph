from typing import TypedDict, List, Annotated
from langgraph.graph import END, StateGraph
import operator 

#Annotated is used to specify how to combine the values when merging states
# Here, we use operator.add to sum the 'sum' field and operator.concat to concatenate lists in the 'history' field.
class ComplexState(TypedDict):
    count :int
    sum : Annotated[int,operator.add]
    history : Annotated[List[int],operator.concat]

def increment(state: ComplexState) -> ComplexState:
    new_count = state["count"] +1

    return {
        "count": new_count,
        "sum":  new_count,
        "history":  [new_count]
    }

def should_end(state: ComplexState) -> str:
    if(state["count"] < 5):
        return "continue"
    return "stop"

graph = StateGraph(ComplexState)
graph.add_node("increment", increment)
graph.set_entry_point("increment")

graph.add_conditional_edges("increment", should_end, {
    "continue": "increment",
    "stop": END
})

app = graph.compile()
state = {"count": 0, "sum": 0, "history": []}
final_state = app.invoke(state)
print(final_state)