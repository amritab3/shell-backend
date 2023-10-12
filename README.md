# shell-backend

## Project Setup

- Clone the repo using ```git clone git@github.com:amritab3/shell-backend.git```.
- Install `pyenv` following the instructions from [here](https://github.com/pyenv/pyenv).
- Run ```pyenv install```. `pyenv` will automatically pick up the correct python version from `.python-version` file.
- Create a virtual environment by running ```python -m venv venv```.
- Install `pip-tools` using ```pip install pip-tools```. It is used to manage dependencies.
- Install the dependencies using ```pip-sync requirements.txt```.

## Installing a new dependency

If you need to install a new dependency, add that into `requirements.in` file and run ```pip-compile requirements.in```. After that install the dependencies using ```pip-sync requirements.txt```.
