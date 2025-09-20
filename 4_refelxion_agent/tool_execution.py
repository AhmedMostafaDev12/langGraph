import json 
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()
tavily_tool = TavilySearch(max_results=5)

# create the Tavely search tool 
def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    last_ai_message: AIMessage = state[-1]  

   # Extract tool calls from the AI message
    if not hasattr(last_ai_message, 'tool_calls') or not last_ai_message.tool_calls:
      return []
   
   # process the AnswerQuestion tool calls to extract the search queries
    tool_messages = []
    for tool_call in last_ai_message.tool_calls:
        if tool_call['name'] in ['AnswerQuestion', 'ReviseAnswer']:
            call_id = tool_call['id']
            search_queries = tool_call['args'].get('search_queries', [])[:2]  # Limit to 2 queries

            query_results = {}
            for query in search_queries:
                # Execute the Tavily search tool for each query
                search_results = tavily_tool.invoke(query)
                query_results[query] = search_results

            tool_messages.append(
                ToolMessage(
                    content=json.dumps(query_results),
                    tool_call_id=call_id
                )
            )
   
    return tool_messages


# Example test state for debugging
# This state simulates a conversation where the AI has made a tool call to "
test_state = [
    HumanMessage(
        content="Write about how small business can leverage AI to grow"
    ),
    AIMessage(
        content="", 
        tool_calls=[
            {
                "name": "AnswerQuestion",
                "args": {
                    'answer': '', 
                    'search_queries': [
                            'AI tools for small business', 
                            'AI in small business marketing', 
                            'AI automation for small business'
                    ], 
                    'reflection': {
                        'missing': '', 
                        'superfluous': ''
                    }
                },
                "id": "call_KpYHichFFEmLitHFvFhKy1Ra",
            }
        ],
    )
]

#Execute the tools
# results = execute_tools(test_state)

# print("Raw results:", results)
# if results:
#     parsed_content = json.loads(results[0].content)
#     print("Parsed content:", parsed_content)