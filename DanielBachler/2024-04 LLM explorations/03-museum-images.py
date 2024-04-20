# %%
import base64
from dataclasses import dataclass
from io import BytesIO
from typing import cast
import requests
import os
from pathlib import Path
from PIL import Image
from rich import print
import multiprocessing
from PIL.ExifTags import TAGS
from dotenv import load_dotenv

# We're not using it here in the example but if you want to
# use HEIC/HEIF images from modern iphones you need this
from pillow_heif import register_heif_opener
register_heif_opener()


load_dotenv()


# %%
# OpenAI API Key
api_key = os.getenv('OPENAI_API_KEY')

# %%
# Directory for images
images_directory = Path(r"files")

# %%
@dataclass
class ImageInformation:
    # location: str
    date: str | None
    image_data: str

# %%
# Function to prepare the image
def prepare_image(image_path: Path):
    # resize the image to a maximum of 2048px on the longest side using the pillow library
    # The OpenAI API will do this server side if you don't do it here things go faster
    # if you constrain the image to 2048px
    image = Image.open(image_path)
    image.thumbnail((2048, 2048))

    # Metadata is not passed to the models by OpenAI - so if we want to extract information
    # like when the image was taken we have to do it client side, e.g. with the pillow library
    try:
        exif = image.getexif()
        date_time = cast(str, exif.get(306)) # datetime - used in iphones
        date_taken = cast(str, exif.get(36867)) # datetime_taken - used in android phones
        date_to_use = date_time if date_time else date_taken
    except:
        date_to_use = None
    with BytesIO() as output:
        image.save(output, format="JPEG")
        return ImageInformation(date=date_to_use, image_data=base64.b64encode(output.getvalue()).decode('utf-8'))


# %%
def infer_image_content(image_info: ImageInformation):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    prompt = """You are given an image that was taken in a museum. The image shows either an artwork or a description plaque.

    Reply with a snippet of JSON.

    If the image shows an artwork, the JSON should look like this:

    ```json
    {
        "type": "artwork"
    }
    ```

    If the image shows a description plaque, extract the text from the plaque and fill in all applicable fields in the following JSON snippet:

    ```json
    {
        "type": "plaque",
        "artist": "Artist's name",
        "title": "Title of the artwork",
        "date": "Year the artwork was created",
        "description": "Description of the artwork",
        "artist_lifespan": "Artist's lifespan",
        "medium": "Medium used to create the artwork"
    }
    ```"""

    payload = {
    "model": "gpt-4-turbo",
    "response_format": { "type": "json_object" },
    "messages": [
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_info.image_data}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

# %%

def process_image(image_path):
    print(f"Processing {image_path}")
    image_info = prepare_image(image_path)
    inferred_info = infer_image_content(image_info)
    # write the information into a json file with the same name as the image
    with open(image_path.with_suffix(".json"), "w") as f:
        f.write(inferred_info)


# %%
# Get the images from the directory

heics = list(images_directory.glob("*.heic"))
jpgs = list(images_directory.glob("*.jpg"))
both = heics + jpgs

# %%

if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        pool.map(process_image, both)

# %%
