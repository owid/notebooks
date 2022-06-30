# %%


from IPython.display import Markdown as md

# %%
variableName = "This header is stored as a Variable"

# %%
print("This is a print out from code")

# %% [markdown]
# This is markdown:
# * So is this
# * And this
#
# # And this.

# %%
# You can also use variables in markdown inline using the Markdown library, like this:
md("## {}".format(variableName))




# %%
