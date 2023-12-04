# Change this to the name of the topic page
PAGE <- "Smoking"

# Install data.table package if not already installed
if (!require("data.table")) install.packages("data.table")
library(data.table)

url <- "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1Tylsvt9CQ5v5RsxXG0FuL_DdnMAdUWG7cSx6yY1aiVddg3w9YYQXdTCRxx62k7gg3VBYoMeShHHB/pub?gid=598437417&single=true&output=csv"
df <- fread(url, showProgress = F)
df <- df[post_status == "publish"]

topic_page <- df[post_title == PAGE]

cat("Blocks used in the", PAGE, "topic page:\n")
print(topic_page[, c("reusable_block_slug", "reusable_block_title")])

blocks_used <- topic_page$reusable_block_slug
other_posts <- df[reusable_block_slug %in% blocks_used & post_title != PAGE]

cat("\nThese blocks are also used in:\n")
print(other_posts[, c("reusable_block_title", "post_title", "post_slug")])
