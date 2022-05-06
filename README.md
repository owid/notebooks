# Our World In Data Jupyter Notebooks

This repository contains Jupyter notebooks created at Our World In Data.

The folder structure is sorted by author first, then by project. Jupyter notebooks in here are created for different purposes and thus to different standards of quality. The readme in every individual folder will tell you more.

See below how to install a local setup for running these notebooks.

To run and modify these notebooks from your browser, one of the easiest ways is using [Nextjournal.com](https://github.nextjournal.com/). Just open the This repository in nextjournal by [clicking this link](https://github.nextjournal.com/owid/notebooks/tree/main).


### Local setup for running these notebooks

We are not yet using poetry or pipenv yet to standardize our jupyter setups precicely. Below is the recommended setup for running the notebooks in this repository.

#### MacOS

* Install [VS Code](https://code.visualstudio.com/)

Whenever you are asked to paste something in the terminal from now on you can either do so in the terminal app or in a terminal window in VS Code.

You may have to restart your terminal session in between for newly installed packages to be found on your system

* Install [Homebrew](https://brew.sh/)
* In a terminal run `brew install pyenv xz`
* Configure some build details for python packages:
  * Run `ps -p $$` to figure out which shell is configured for your system and open your profile file:
  * If your shell is bash
    * Open or create the file `.bashrc` in your user directory. You can show hidden files (those starting with a dot) by pressing CMD + SHIFT + .
  * If your shell is zsh
    * Open or create the file `.zshrc` in your user directory. You can show hidden files (those starting with a dot) by pressing CMD + SHIFT + .
  * Put this into into your profile file `export PYTHON_CONFIGURE_OPTS="--enable-framework"`. (On some system not having this led to problems with installing some python libraries)
* Install python 3.10 with pyenv: `pyenv install 3.10.4`
* Make this the default python version so that typing `python` start this version: `pyenv global 3.10.4`
* Install common libraries: `pip install pandas matplotlib ipython jupyter jupyterlab ipywidgets altair parse`

#### Windows

* Install [VS Code](https://code.visualstudio.com/)
* Install the [Windows Terminal](https://www.microsoft.com/de-de/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)

Whenever you are asked to paste something in the terminal from now on you can either do so in the Windows Terminal or in a terminal window in VS Code.

You may have to restart your terminal session in between for newly installed packages to be found on your system.

* Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Use the Python 3.9 Windows 64-bit version unless you have a good reason to pick something else)
* Install common libraries: `conda install pandas matplotlib ipython jupyter jupyterlab ipywidgets altair` - pip install should work well for most libraries but for some with compiled dependencies like pandas, conda is the easier way to get them installed
* Install additional libraries not in conda `pip install parse`
