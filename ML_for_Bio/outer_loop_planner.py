'''

## USAGE

In Notebooks, since they have their own eventloop:
  import nest_asyncio
  nest_asyncio.apply()
'''


import asyncio
import os

import langchain
from dotenv import load_dotenv
from langchain.agents import AgentType, Tool, initialize_agent, load_tools
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.agents.react.base import DocstoreExplorer
from langchain.chat_models import ChatOpenAI
from langchain.docstore.base import Docstore
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.tools.playwright.utils import \
    create_sync_playwright_browser  # A synchronous browser is available, though it isn't compatible with jupyter.
from langchain.tools.playwright.utils import create_async_playwright_browser
from llama_hub.github_repo import GithubClient, GithubRepositoryReader

from ML_for_Bio.tools import get_docstore_agent, get_shell_tool

load_dotenv(override=True, dotenv_path='../.env')

os.environ["LANGCHAIN_TRACING"] = "true" # If you want to trace the execution of the program, set to "true"
langchain.debug = True
VERBOSE = True

def get_human_input() -> str:
  """Placeholder for Slack input from user."""
  print("Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.")
  contents = []
  while True:
    try:
      line = input()
    except EOFError:
      break
    if line == "q":
      break
    contents.append(line)
  return "\n".join(contents)


async def main(llm=None, tools=None, memory=None):
  
  agent_chain = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=VERBOSE,
    handle_parsing_errors=True, # or pass a function that accepts the error and returns a string
    memory=memory, 
    agent_kwargs = {
      "memory_prompts": [chat_history],
      "input_variables": ["input", "agent_scratchpad", "chat_history"]
    }
  )
  
  # response = await agent_chain.arun(input="Ask the user what they're interested in learning about on Langchain, then Browse to blog.langchain.dev and summarize the text especially whatever is relevant to the user, please.")
  response = await agent_chain.arun(input="Browse to https://lumetta.web.engr.illinois.edu/120-binary/120-binary.html and complete the first challenge using the keyboard to enter information, please.")
  print(response)

# agents.agent.LLMSingleActionAgent
# 1. collect relevant code documentation
# 2. collect relevant code files from github
# 3. Propose a change to the code and commit it into a new branch on github

if __name__ == "__main__":
  # LLM 
  llm = ChatOpenAI(temperature=0, model="gpt-4-0613", max_retries=3, request_timeout=60 * 3) # type: ignore

  # TOOLS
  tools = get_tools(llm)
  
  # MEMORY 
  chat_history = MessagesPlaceholder(variable_name="chat_history")
  memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
  
  
  asyncio.run(main(llm=llm, tools=tools, memory=memory))
