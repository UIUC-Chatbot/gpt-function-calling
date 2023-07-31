'''
## USAGE

In Notebooks, since they have their own eventloop:
  import nest_asyncio
  nest_asyncio.apply()

On the command line

'''

import asyncio
import os
import threading
from typing import List, Sequence

import langchain
from agents import get_docstore_agent
from dotenv import load_dotenv
from langchain.agents import AgentType, Tool, initialize_agent, load_tools
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.agents.react.base import DocstoreExplorer
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.docstore.base import Docstore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools.base import BaseTool
from langchain.tools.playwright.utils import \
    create_sync_playwright_browser  # A synchronous browser is available, though it isn't compatible with jupyter.
from langchain.tools.playwright.utils import create_async_playwright_browser
from langchain.vectorstores import Qdrant
from llama_hub.github_repo import GithubClient, GithubRepositoryReader
from qdrant_client import QdrantClient
from tools import get_shell_tool, get_tools

load_dotenv(override=True, dotenv_path='.env')

os.environ["LANGCHAIN_TRACING"] = "true"  # If you want to trace the execution of the program, set to "true"
langchain.debug = True
VERBOSE = True

from langchain_experimental.autonomous_agents.autogpt.agent import AutoGPT
from langchain_experimental.autonomous_agents.baby_agi import BabyAGI
from langchain_experimental.plan_and_execute.agent_executor import \
    PlanAndExecute
from langchain_experimental.plan_and_execute.executors.agent_executor import \
    load_agent_executor
from langchain_experimental.plan_and_execute.planners.chat_planner import \
    load_chat_planner


class OuterLoopPlanner:

  def __init__(self):
    print("Before qdrant")
    self.qdrant_client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))

    print("Before creating vectorstore")
    self.langchain_docs_vectorstore = Qdrant(
        client=self.qdrant_client,
        collection_name=os.getenv('QDRANT_LANGCHAIN_DOCS'),  # type: ignore
        embeddings=OpenAIEmbeddings())  # type: ignore

    print("Before creating vectorstore")
    self.langchain_docs_vectorstore = Qdrant(
        client=self.qdrant_client,
        collection_name=os.getenv('QDRANT_LANGCHAIN_DOCS'),  # type: ignore
        embeddings=OpenAIEmbeddings())  # type: ignore

    print("after __init__")
    # todo: try babyagi
    # BabyAGI()

  def autogpt_babyagi(self, llm: BaseChatModel, tools: List[BaseTool], prompt: str, memory=None):

    # langchain_retriever = RetrievalQA.from_chain_type(llm=ChatOpenAI(model='gpt-4-0613'), chain_type="stuff", retriever=self.langchain_docs_vectorstore.as_retriever())

    autogpt = AutoGPT.from_llm_and_tools(
        ai_name='coding assistant',
        ai_role='ML engineer',
        tools=tools,
        llm=llm,
        human_in_the_loop=True,
        memory=self.langchain_docs_vectorstore.as_retriever(),
    )
    goals: List[str] = [prompt]
    autogpt.run(goals=goals)


def experimental_main(llm: BaseLanguageModel, tools: Sequence[BaseTool], memory, prompt: str):
  input = {'input': prompt}
  planner = load_chat_planner(llm)
  executor = load_agent_executor(
      llm=llm,
      tools=list(tools),
      verbose=True,
      include_task_in_prompt=False,
  )

  agent = PlanAndExecute(
      planner=planner,
      executor=executor,
  )
  response = agent.run(input=input)
  print(f"👇FINAL ANSWER 👇\n{response}")
  # handle_parsing_errors=True,  # or pass a function that accepts the error and returns a string
  # max_iterations=30,
  # max_execution_time=None,
  # early_stopping_method='generate',
  # memory=memory,
  # trim_intermediate_steps=3, # TODO: Investigate this undocumented feature
  # agent_kwargs={
  #     "memory_prompts": [chat_history],
  #     "input_variables": ["input", "agent_scratchpad", "chat_history"]
  # })


def main(llm: BaseLanguageModel, tools: Sequence[BaseTool], memory, prompt: str):
  agent_chain = initialize_agent(
      tools=tools,
      llm=llm,
      agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
      verbose=VERBOSE,
      handle_parsing_errors=True,  # or pass a function that accepts the error and returns a string
      max_iterations=30,
      max_execution_time=None,
      early_stopping_method='generate',
      memory=memory,
      trim_intermediate_steps=3,  # TODO: Investigate this undocumented feature
      agent_kwargs={
          "memory_prompts": [chat_history],
          "input_variables": ["input", "agent_scratchpad", "chat_history"]
      })

  # response = await agent_chain.arun(input="Ask the user what they're interested in learning about on Langchain, then Browse to blog.langchain.dev and summarize the text especially whatever is relevant to the user, please.")
  response = agent_chain.run(input=prompt)
  print(f"👇FINAL ANSWER 👇\n{response}")


# if __name__ == "__main__":
#   # LLM
#   llm = ChatOpenAI(temperature=0, model="gpt-4-0613", max_retries=20, request_timeout=60 * 3)  # type: ignore

#   # TOOLS
#   tools = get_tools(llm, sync=True)

# async def main_async(llm, tools, memory, prompt):
#   async_browser = await create_async_playwright_browser()
#   browser_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
#   tools += browser_toolkit.get_tools()
#   await main(llm=llm, tools=tools, memory=memory, prompt=prompt)

# def main_sync(llm, memory, prompt):
#   tools = get_tools(llm)
#   t = threading.Thread(target=run_in_new_thread, args=(main, llm, tools, memory, prompt))
#   t.start()
#   t.join()

# agents.agent.LLMSingleActionAgent
# 1. collect relevant code documentation
# 2. collect relevant code files from github
# 3. Propose a change to the code and commit it into a new branch on github

# Input: I ask it to write some code in a specific library (Langchain). It writes it.
# 1. Find docs
# 2. Write code
#   a. just return code or Decide if it's reasonable to execute & debug OR

if __name__ == "__main__":
  # LLM
  llm = ChatOpenAI(temperature=0, model="gpt-4-0613", max_retries=3, request_timeout=60 * 3)  # type: ignore

  # TOOLS
  tools = get_tools(llm, sync=True)

  # MEMORY
  chat_history = MessagesPlaceholder(variable_name="chat_history")
  memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

  # can't do keyboard input
  # prompt = "Browse to https://lumetta.web.engr.illinois.edu/120-binary/120-binary.html and complete the first challenge using the keyboard to enter information, please."

  # prompt = "Please find the Python docs for LangChain, then write a function that takes a list of strings and returns a list of the lengths of those strings."
  # prompt = "Please find the Python docs for LangChain to help you write an example of a Retrieval QA chain, or anything like that which can answer questions against a corpus of documents. Return just a single example in Python, please."
  # ✅ worked with both Langchain PlanExecuteAgents. But NOT AutoGPT because it struggled with the internet.
  prompt = "Write an example of making parallel requests to an API with expentional backoff, or anything like that. Return just a single example in Python, please."
  prompt = "Write an example of making parallel requests to an API with expentional backoff, or anything like that. Return just a single example in Python, please."

  # main(llm=llm, tools=tools, memory=memory, prompt=prompt)
  # experimental_main(llm=llm, tools=tools, memory=memory, prompt=prompt)
  # vectorstore

  o = OuterLoopPlanner()
  o.autogpt_babyagi(llm=llm, tools=tools, prompt=prompt)
