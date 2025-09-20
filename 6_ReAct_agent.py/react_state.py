import operator
from typing import Annotated, TypedDict, Union

from langchain_core.agents import AgentAction, AgentFinish

class AgentState(TypedDict):
    input: str
    agent_outcome : Union[AgentFinish,AgentAction,None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]],operator.add]


##------------------- State --------------------------##
"""
input : the original user query or the task that agent need to solve 
        remains constant through the agent's execution 

agent_outcome: Union[AgentFinish, AgentAction, None]
               it determine which action will be executed and  Union[AgentFinish, AgentAction, None]
                means that it could be one of those 
            -- AgentAction would be like that :
            -- agent_outcome": AgentAction(
                    tool="search_tool",
                    tool_input="France population 2024",
                    log="Now I need France's population")
            -- AgentFinish would be like that :
            -- "agent_outcome": AgentFinish(
                    return_values={"output": "The weather in Paris is 22°C and sunny. France has a population of approximately 68 million people."},
                    log="I have all the information needed to answer the question"
    ),

"intermediate_steps": a list of tuples store the history of all tool executions 
                      Each tuple contains the AgentAction and the result of it 
                      "intermediate_steps": [
                             (AgentAction(tool="weather_tool", tool_input="Paris", log="..."), 
                             "Weather in Paris: 22°C, sunny"),
                             (AgentAction(tool="search_tool", tool_input="France population 2024", log="..."),
                             "France population: approximately 68 million")
    ]
"""

# {
#     "input": "What's the weather in Paris and what's the population of France?",
#     "agent_outcome": AgentAction(
#         tool="search_tool",
#         tool_input="France population 2024",
#         log="Now I need France's population"
#     ),
#     "intermediate_steps": [
#         (AgentAction(tool="weather_tool", tool_input="Paris", log="..."), 
#          "Weather in Paris: 22°C, sunny")
#     ]
# }