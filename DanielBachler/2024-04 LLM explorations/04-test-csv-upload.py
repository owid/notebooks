# %%

from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from rich import print

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
# ❗ Repeat this step until the status is completed or failed
run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
run.status

# %%

messages = client.beta.threads.messages.list(thread_id=thread.id)

# %%
# Iterate over the messages (the output text)
for message in reversed(messages.data):
    print(message.content[0].text.value)

# %%

# Let's also inspect now the other steps and see what code was run
run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)
# %%
for step in reversed(run_steps.data):
    # check if the step detail is an instance of ToolCallsStepDetail
    if step.step_details.__class__.__name__ == "ToolCallsStepDetails":
        for tool_call in step.step_details.tool_calls:
            print("[lightblue]" + tool_call.code_interpreter.input)
            for output in tool_call.code_interpreter.outputs:
                print("[green]" + output.logs)

# %%

# Clean up resources
client.beta.threads.delete(thread.id)

client.beta.assistants.delete(assistant.id)

# %%

client.files.delete(file.id)

# %%
