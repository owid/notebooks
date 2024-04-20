# %%

from pathlib import Path
from typing import List
from dotenv import load_dotenv
import instructor
from pydantic import BaseModel
from openai import OpenAI


load_dotenv()

# %%

team_file_path = Path("files/owid-team.txt")
team = team_file_path.read_text()

# %%
class TeamMember(BaseModel):
    author_name: str
    joined_in: str
    role: str

# %%

# Patch the OpenAI client
client = instructor.from_openai(OpenAI())

# %%

team_members = client.chat.completions.create(
  model="gpt-3.5-turbo",
  response_model=List[TeamMember],
  messages=[
    {"role": "user", "content": team + "\n---\n\nPlease extract from the above text the following information for each team member as json with the following properties: author name, joined in, role.."}
  ]
)


# %%

for member in team_members:
    print(member)

# %%
