# %%

from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# %%

filePath = Path(r"files/life-expectancy.csv")

# Upload a file with an "assistants" purpose
file = client.files.create(
  file=open(filePath, "rb"),
  purpose='assistants'
)


# %%
# Create an assistant using the file ID
assistant = client.beta.assistants.create(
  instructions="",
  model="gpt-4-turbo",
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  }
)

# %%
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "You are the Our World In Data QA bot. When asked a question about data, write and run code to answer the question. The available file will be relevant for the question.",
    },
    {
      "role": "user",
      "content": "Which country had the highest life expectancy in 1970?",
      "attachments": [
        {
          "file_id": file.id,
          "tools": [{"type": "code_interpreter"}]
        }
      ]
    }
  ]
)

# %%

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)

# %%
# Repeat this step until the status is completed or failed
run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
run.status

# %%

messages = client.beta.threads.messages.list(thread_id=thread.id)

# %%

messages.data[0].content

# %%

client.beta.threads.delete(thread.id)

client.beta.assistants.delete(assistant.id)

# %%

client.files.delete(file.id)

# %%
