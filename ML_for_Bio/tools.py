import asyncio
import os

import langchain
from dotenv import load_dotenv
from langchain.agents import AgentType, Tool, initialize_agent, load_tools
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.agents.react.base import DocstoreExplorer
from langchain.callbacks import HumanApprovalCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.docstore.base import Docstore
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.tools import ShellTool
from langchain.tools.playwright.utils import \
    create_sync_playwright_browser  # A synchronous browser is available, though it isn't compatible with jupyter.
from langchain.tools.playwright.utils import create_async_playwright_browser
from llama_hub.github_repo import GithubClient, GithubRepositoryReader

load_dotenv(override=True, dotenv_path='../.env')

os.environ["LANGCHAIN_TRACING"] = "true"  # If you want to trace the execution of the program, set to "true"
langchain.debug = True
VERBOSE = True


def get_tools(llm):
  # TOOLS
  async_browser = create_async_playwright_browser()
  browser_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
  # sync_browser = create_sync_playwright_browser()
  # browser_toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
  browser_tools = browser_toolkit.get_tools()

  human_tools = load_tools(["human"], llm=llm, input_func=get_human_input)

  # Agent to search docs and pull out helpful sections, code & examples
  get_docstore_agent()

  python = get_shell_tool()

  tools = browser_tools + human_tools
  return tools


def get_docstore_agent(docstore: Docstore | None = None):
  """This returns an agent. Usage of this agent: react.run(question)"""
  if docstore is None:
    doc_explorer = DocstoreExplorer(langchain.Wikipedia())
  else:
    doc_explorer = DocstoreExplorer(docstore)

  tools = [
      Tool(
          name="Search",
          func=doc_explorer.search,
          description="useful for when you need to ask with search",
      ),
      Tool(
          name="Lookup",
          func=doc_explorer.lookup,
          description="useful for when you need to ask with lookup",
      ),
  ]

  llm = ChatOpenAI(temperature=0, model="gpt-4-0613", max_retries=3, request_timeout=60 * 3)  # type: ignore
  react = initialize_agent(tools, llm, agent=AgentType.REACT_DOCSTORE, verbose=VERBOSE)
  return react


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


def get_shell_tool():
  '''Adding the default HumanApprovalCallbackHandler to the tool will make it so that a user has to manually approve every input to the tool before the command is actually executed.
  Human approval on certain tools only: https://python.langchain.com/docs/modules/agents/tools/human_approval#configuring-human-approval
  '''
  tool = ShellTool(callbacks=[HumanApprovalCallbackHandler(should_check=_should_check, approve=_approve)])
