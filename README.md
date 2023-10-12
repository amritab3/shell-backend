# shell-backend

## Project Setup

- Clone the repo using

    ```sh
        git clone git@github.com:amritab3/shell-backend.git
    ```

- Go into the project folder using

    ```sh
        cd shell-backend
    ```

- Install `pyenv` following the instructions from [here](https://github.com/pyenv/pyenv).
- Run

    ```sh
        pyenv install
    ```

    `pyenv` will automatically pick up the correct python version from `.python-version` file.
- Create a virtual environment by running

    ```sh
        python -m venv venv
    ```

- Activate the newly created virtual environment by running

    ```sh
        source venv/bin/activate
    ```

- Install `pip-tools` using

    ```sh
        pip install pip-tools
    ```

    It is used to manage dependencies.
- Install the dependencies using

    ```sh
        pip-sync dev-requirements.txt requirements.txt
    ```

## Installing a new dependency

If you need to install a new dependency, add that into `requirements.in` file and run

```sh
    pip-compile requirements.in
```

It will update the `requirements.txt` file adding new dependencies. After that install the dependencies using

```sh
    pip-sync requirements.txt
```

It will be the same for installing new dev dependencies as well.
