from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import tool , create_react_agent
import datetime
from langchain_tavily import TavilySearch
from langchain import hub 
from dotenv import load_dotenv

load_dotenv()

search_tool = TavilySearch(search_depth="basic")

@tool 
def get_current_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Get the current time in specified format"""
    return datetime.datetime.now().strftime(format)

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

"""
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [get_current_time, tavily_search]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
"""

react_prompt =  hub.pull("hwchase17/react")
tools = [get_current_time, search_tool]

react_agent_runnable = create_react_agent(tools=tools, llm=llm, prompt=react_prompt)