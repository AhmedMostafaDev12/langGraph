from pydantic import BaseModel, Field
from typing import List, Any

class Reflection(BaseModel):
    missing: str = Field(description = "Critique of what is missing.")
    superfluous: str = Field(description = "Critique of what is superfluous.")

class AnswerQuestion(BaseModel):
    """Answer the question"""
    answer : str = Field(description = "~250 word detailed answer to the question.")
    search_queries : List[str] = Field(description = "1-3 queries for researching improvements to address the critique of your current answer.")
    reflections: Reflection = Field(description = "your reflections of the initial answer.")

class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question"""
    References : List[str] = Field(description = "List of references used to improve your answer.")