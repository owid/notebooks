# %%

from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()

# %%

team_file_path = Path("files/owid-team.txt")
team = team_file_path.read_text()

# %%

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  # response_format={"type": "json_object"},
  messages=[
    {"role": "user", "content": team + "\n---\n\nPlease extract from the above text the following information for each team member as json with the following properties: author name, joined in, role.."}
  ]
)


# %%

print(completion.choices[0].message.content)
