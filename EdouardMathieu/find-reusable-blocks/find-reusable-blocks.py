import pandas as pd

# Change this to the name of the topic page
PAGE = "Smoking"

# URL to fetch data from
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1Tylsvt9CQ5v5RsxXG0FuL_DdnMAdUWG7cSx6yY1aiVddg3w9YYQXdTCRxx62k7gg3VBYoMeShHHB/pub?gid=598437417&single=true&output=csv"

# Load data into a DataFrame
df = pd.read_csv(url)

# Filter rows where post_status is 'publish'
df = df[df["post_status"] == "publish"]

# Get the rows for the specified topic page
topic_page = df[df["post_title"] == PAGE]

print("Blocks used in the", PAGE, "topic page:\n")
print(topic_page[["reusable_block_slug", "reusable_block_title"]])

blocks_used = topic_page["reusable_block_slug"].tolist()
other_posts = df[
    df["reusable_block_slug"].isin(blocks_used) & (df["post_title"] != PAGE)
]

print("\nThese blocks are also used in:\n")
print(other_posts[["reusable_block_title", "post_title", "post_slug"]])
