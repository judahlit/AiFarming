# AI Farming Python App (Deprecated)

## Description

This python app contains modules relevant for applying machine learning on farm
data and predicting the meat quality of cows based on data acquired from blood
samples.

## How to contribute to the project

### Pull the project from Gitlab

(Include git section here when the project is located in projects.fhict.nl)

### Install python

If you're on Windows, the easiest way to install python is to search for it in
the Microsoft Store. If you use a different OS, or if installing on the store
doesn't work, search for a different way to install it.

### Install pipx and poetry

This project uses modules (dependencies) from third parties, which need to be
installed for the modules in this project to run. Poetry is a dependency manager
for python, and this project uses poetry to install dependencies. Below are the
necessary steps to install it.

To install poetry, we need to install pipx first. Poetry needs to be installed
in an isolated environment (see the [poetry
docs](https://python-poetry.org/docs/)), and pipx is a tool that can install
applications in that way. If you're on **Windows**, the easiest way to install pipx
is with scoop. If you are using something else, please view the [pipx
docs](https://pipx.pypa.io/stable/).

Copy paste the following lines in a terminal, such as Windows Powershell, Command
Prompt, or a terminal in Visual Studio Code.

#### Install scoop

```sh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

#### Install pipx

```sh
scoop install pipx
pipx ensurepath
```

#### Install poetry

```sh
pipx install poetry
```

### Load the project environment and install the dependencies

Make sure your terminal is set to the path of the project on your machine.
The easiest way to do this, is to open the project in VSCode, and opening a
terminal from there. Then, run the commands below.

#### Load the poetry virtual environment

**Note:** make sure you are in this virtual environment every time before
contributing and running scripts.

```sh
poetry shell
```

#### Install the dependencies

```sh
poetry install
```

When contributing and opening a script in VSCode, you might get warnings saying
that some dependencies could not be located. To remove these warnings, do this:

1. Press **Ctrl + Shift + P**.
2. Choose *Python: Select interpreter*.
3. Select the virtual environment that poetry created.

Now you can contribute. Have fun !!!!!!!!!
