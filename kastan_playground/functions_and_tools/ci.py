import os

from codeinterpreterapi import CodeInterpreterSession, File
from dotenv import load_dotenv

# ret = load_dotenv(override=True, dotenv_path='../../.env')
load_dotenv(override=True, dotenv_path='.env')


async def main():
  # create a session
  session = CodeInterpreterSession(openai_api_key=os.getenv('OPENAI_API_KEY'))
  await session.astart()

  # generate a response based on user input
  response = await session.generate_response(
    "Plot the bitcoin chart of 2023 YTD"
  )

  # output the response (text + image)
  print("AI: ", response.content)
  for file in response.files:
    file.show_image()

  # terminate the session
  await session.astop()
  
async def dataset_analysis():
  # context manager for auto start/stop of the session
  async with CodeInterpreterSession(openai_api_key=os.getenv('OPENAI_API_KEY')) as session:
    # define the user request
    user_request = "Analyze this dataset and plot something interesting about it."
    files = [
      File.from_path("iris.csv"),
    ]

    # generate the response
    response = await session.generate_response(
        user_request, files=files
    )

    # output to the user
    print("AI: ", response.content)
    for file in response.files:
      file.show_image()


if __name__ == "__main__":
  import asyncio

  # run the async function
  asyncio.run(dataset_analysis())
