from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent, tool
# tavily search is a tool that allows the agent to search the web
from langchain_community.tools import TavilySearchResults
import datetime

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


"""
The react agent follows a specific reasoning and tool use framework:

1- think about the problem
2- decide which tool to use
3- use the tool and pass the input to the tool
4- look at the result     |
5- think about the result | => observe the output
6- decide the next step
7- repeat until the problem is solved
8- give the final answer
"""

search_tool = TavilySearchResults(search_depth="basic")

@tool 
def get_current_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Get the current time in specified format"""
    return datetime.datetime.now().strftime(format)

#zero shot means the agent will not be given any examples of how to use tools
# the agent has no prior knowledge of the tools it has access to
# the react agent use the reasoning and tool use framework
agent = initialize_agent(
    tools=[search_tool, get_current_time],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
)

agent.invoke("What are the latest AI tools for small business? What time is it now?")
