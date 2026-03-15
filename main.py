from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

tavily = TavilyClient()


@tool
def search(query: str) -> str:
    """
    Tools that searches over internet
    Args:
        query: The query to search for
    Returns:
        The search results
    """
    print(f"Searching for: {query}")
    return tavily.search(query=query)

class Source(BaseModel):
    """A source used to answer the question"""
    url: str = Field(description="The URL of the webpage used as a source")

class AgentResponse(BaseModel):
    """Final response of the agent"""
    answer: str = Field(description="The final answer to the user")
    sources: List[Source] = Field(
        description="List of URLs used to generate the answer"
    )
    
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.9)
tools = [search]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)
def main():
    
    print("Hello from langchain-course!")
    result= agent.invoke({"messages":HumanMessage(content="Find 3 DevOps engineer job postings in India requiring Docker and Kubernetes. Use the search tool and return the job details with their URLs and sources in the specified format.")})
    print(result)
    


if __name__ == "__main__":
    main()
