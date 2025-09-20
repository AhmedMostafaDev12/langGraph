# Import required modules from LangChain and Python stdlib
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
from langchain_ollama import ChatOllama   
from langchain_groq import ChatGroq  
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.messages import HumanMessage
from schema import AnswerQuestion, ReviseAnswer  # Your custom Pydantic schemas
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file

# ---------------- PARSERS ----------------
# Define a parser that converts LLM JSON outputs into a Python object (AnswerQuestion)
pydantic_parser = PydanticOutputParser(pydantic_object=AnswerQuestion)


# ---------------- PROMPT TEMPLATE ----------------
# A flexible prompt with placeholders. This acts as the "system instruction" for the LLM.

# -------------placeholder for dynamic user/assistant messages to be injected later -------#
# -------------partial ----------- #
 # 1. parially fill the needed variable and not need it with all the variables
 # 2. set this variable permenently
actor_prompt_template = ChatPromptTemplate.from_messages(
    [ 
        (
            "system",  # System role prompt
            """You are expert AI researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. After the reflection, **list 1-3 search queries separately** for researching improvements. Do not include them inside the reflection.
""",
        ),
        # Placeholder for dynamic user/assistant messages to be injected later
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Answer the user's question above using the required format.",
        ),
    ]
).partial(
    # Automatically fill the {time} placeholder with the current datetime
    time = lambda: datetime.datetime.now().isoformat(),
)


# ---------------- FIRST RESPONSE CHAIN ----------------
# Create a specialized prompt for generating the first answer (~250 words)
first_response_prompt_template = actor_prompt_template.partial(
    first_instruction="Answer the question in ~250 words.",
)

# Define which local LLM to use (via Ollama)
llm = ChatGoogleGenerativeAI(model= "gemini-2.5-flash")  # Example using Groq model

# Build a chain:
#   prompt → LLM with AnswerQuestion tool schema → parse result into AnswerQuestion object
generation_chain = (
    first_response_prompt_template 
    | llm.bind_tools(tools=[AnswerQuestion], tool_choice="auto") 
)


# ---------------- REVISOR CHAIN ----------------
# Parser for revised answers (produces ReviseAnswer objects)
validator = PydanticOutputParser(pydantic_object=ReviseAnswer)

# Instructions for revising an answer
revise_instruction = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""

# Build a chain for revising answers:
#   prompt → LLM with ReviseAnswer tool schema → parse result into ReviseAnswer object
revisor_chain = (
    actor_prompt_template.partial(first_instruction=revise_instruction)
    | llm.bind_tools(tools=[ReviseAnswer], tool_choice="auto")
)
