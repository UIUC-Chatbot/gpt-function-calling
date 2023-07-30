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
from langchain.tools.base import BaseTool
from langchain.tools.playwright.utils import \
    create_sync_playwright_browser  # A synchronous browser is available, though it isn't compatible with jupyter.
from langchain.tools.playwright.utils import create_async_playwright_browser
from llama_hub.github_repo import GithubClient, GithubRepositoryReader

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
async def get_tools_async(llm, sync=False):
  '''Main function to assemble tools for ML for Bio project.'''
  async_browser = create_async_playwright_browser()
  browser_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
  browser_tools = browser_toolkit.get_tools()
  human_tools = load_tools(["human"], llm=llm, input_func=get_human_input)
  shell = get_shell_tool()
  tools: list[BaseTool] = human_tools + browser_tools + [shell]
  return tools


def get_tools(llm, sync=False):
  loop = asyncio.new_event_loop()
  tools = loop.run_until_complete(get_tools_async(llm, sync))
  loop.close()
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

  # Agent to search docs and pull out helpful sections, code & examples
  docs_agent = get_docstore_agent()
