import asyncio
import os
from typing import List

import langchain
from dotenv import load_dotenv
from langchain import SerpAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent, load_tools
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.agents.react.base import DocstoreExplorer
from langchain.callbacks import HumanApprovalCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.base import Docstore
from langchain.llms import OpenAI, OpenAIChat
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.retrievers import ArxivRetriever
from langchain.tools import (ArxivQueryRun, PubmedQueryRun, ShellTool,
                             VectorStoreQATool, VectorStoreQAWithSourcesTool,
                             WikipediaQueryRun, WolframAlphaQueryRun)
from langchain.tools.base import BaseTool
from langchain.tools.playwright.utils import \
    create_sync_playwright_browser  # A synchronous browser is available, though it isn't compatible with jupyter.
from langchain.tools.playwright.utils import create_async_playwright_browser
from langchain.tools.python.tool import PythonREPLTool
from langchain.utilities.github import GitHubAPIWrapper
from langchain.vectorstores import Qdrant
from llama_hub.github_repo import GithubClient, GithubRepositoryReader
from qdrant_client import QdrantClient

load_dotenv(override=True, dotenv_path='../.env')

os.environ["LANGCHAIN_TRACING"] = "true"  # If you want to trace the execution of the program, set to "true"
langchain.debug = True
VERBOSE = True

### MAIN ###
# def get_tools(llm, sync=False):
#   '''Main function to assemble tools for ML for Bio project.'''
#   # TOOLS
#   browser_toolkit = None
#   if sync:
#     sync_browser = create_sync_playwright_browser()
#     browser_toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
#   else:
#     async_browser = create_async_playwright_browser()
#     browser_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
#   browser_tools = browser_toolkit.get_tools()

#   human_tools = load_tools(["human"], llm=llm, input_func=get_human_input)

#   shell = get_shell_tool()


#   tools: list[BaseTool] = browser_tools + human_tools + [shell]
#   return tools
def get_tools(llm, sync=True):
  '''Main function to assemble tools for ML for Bio project.'''
  # WEB BROWSER
  browser_toolkit = None
  if sync:
    sync_browser = create_sync_playwright_browser()
    browser_toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
  else:
    # TODO async is work in progress... not functional yet.
    async_browser = create_async_playwright_browser()
    browser_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
  browser_tools = browser_toolkit.get_tools()

  # HUMAN
  human_tools = load_tools(["human"], llm=llm, input_func=get_human_input)
  # SHELL
  shell = get_shell_tool()
  # GOOGLE SEARCH
  search = load_tools(["serpapi"])

  # GITHUB
  github = GitHubAPIWrapper()  # type: ignore
  toolkit = GitHubToolkit.from_github_api_wrapper(github)
  github_tools: list[BaseTool] = toolkit.get_tools()

  #TODO: VectorStoreQATool, VectorStoreQAWithSourcesTool, WikipediaQueryRun, WolframAlphaQueryRun, PubmedQueryRun, ArxivQueryRun

  # ARXIV SEARCH
  arxiv_qa_llm = OpenAIChat(model_name="gpt-4", temperature=0) # type: ignore
  arxiv_tool = ArxivQueryRun(llm=arxiv_qa_llm)

  # TODO: Agent to search docs and pull out helpful sections, code & examples
  # Tool to search Langchain Docs. Can make this more sophisticated with time..

  # TODO BUG: This is not a collection, is a filter for `course_name`
  # TODO: Make a custom tool for this purpose?? Already have implementation... Use a list of available package names to request documentation for. Super cool!
  # qdrant_client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))
  # langchain_docs_vectorstore = Qdrant(
  #     client=qdrant_client,
  #     collection_name=os.getenv('QDRANT_LANGCHAIN_DOCS'),  # type: ignore
  #     embeddings=OpenAIEmbeddings())  # type: ignore
  # # docs_agent = get_docstore_agent()
  # langchain_qa_llm = OpenAIChat(model_name="gpt-4", temperature=0)  # type: ignore
  # langchain_docs_tool = VectorStoreQATool(vectorstore=langchain_docs_vectorstore, llm=langchain_qa_llm, description="Search Langchain Docs", name="langchain_docs_tool")

  tools: list[BaseTool] = human_tools + browser_tools + github_tools + search + [shell, PythonREPLTool(), arxiv_tool, ] # langchain_docs_tool
  return tools


################# TOOLS ##################
def get_shell_tool():
  '''Adding the default HumanApprovalCallbackHandler to the tool will make it so that a user has to manually approve every input to the tool before the command is actually executed.
  Human approval on certain tools only: https://python.langchain.com/docs/modules/agents/tools/human_approval#configuring-human-approval
  '''
  return ShellTool(callbacks=[HumanApprovalCallbackHandler(should_check=_should_check, approve=_approve)])


############# HELPERS ################
def _should_check(serialized_obj: dict) -> bool:
  # Only require approval on ShellTool.
  return serialized_obj.get("name") == "terminal"


def _approve(_input: str) -> bool:
  if _input == "echo 'Hello World'":
    return True
  msg = ("Do you approve of the following input? "
         "Anything except 'Y'/'Yes' (case-insensitive) will be treated as a no.")
  msg += "\n\n" + _input + "\n"
  resp = input(msg)
  return resp.lower() in ("yes", "y")


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
