import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import logging
import imp
import os
import json
import sys
import datetime
from IPython import get_ipython

ipython = get_ipython()
ipython.magic("load_ext rich")
ipython.magic("load_ext autoreload")
ipython.magic("autoreload 2")
ipython.magic("matplotlib inline")
ipython.magic("config InlineBackend.figure_format = 'svg'")

# nice / large graphs
sns.set_context("notebook")

# this is for vs code
if "VSCODE_CWD" in os.environ:
    plt.rcParams["figure.figsize"] = (6, 3)
# this is for jupyterlab
else:
    plt.rcParams["figure.figsize"] = (8, 4)

# Make NumPy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)

# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"
# InteractiveShell.ast_node_interactivity = "last_expr"

try:
    import cufflinks as cf

    cf.go_offline()
except:
    pass

try:
    import plotly.express as px
except:
    pass


def set_logging_level(level):
    imp.reload(logging)
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        level=getattr(logging, level),
        datefmt="%I:%M:%S",
    )
