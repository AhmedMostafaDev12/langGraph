from dotenv import load_dotenv  

from agent_reason_runnable import react_agent_runnable, tools
from react_state import AgentState

load_dotenv()

def reason_node(state: AgentState):
    agent_outcome = react_agent_runnable.invoke(state)
    return {"agent_outcome":agent_outcome}

# agent_executor
def act_node(state:AgentState):
    agent_action = state["agent_outcome"]

    """-- agent_outcome": AgentAction(
                    tool="search_tool",
                    tool_input="France population 2024",
                    log="Now I need France's population") """
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input

    tool_function = None
    #tools = [get_current_time, search_tool]
    # find the matching tool function 
    for tool in tools :
        if  tool.name == tool_name :
            tool_function = tool 
            break

    #Execute the tool with the input 
    if tool_function :
        if isinstance(tool_input, dict):
            output = tool_function.invoke(**tool_function)
        else :
            output = tool_function.invoke(tool_input)
    
    else :
        output = f"Tool {tool_name} not found"

    return {"intermediate_steps": [(agent_action, str(output))]}


    



