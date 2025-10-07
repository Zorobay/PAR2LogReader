# PAR2LogReader

## Setup

1. Install Poetry dependency manager: https://python-poetry.org/docs/#installation
2. From the repository root, run `poetry install`
   1. This creates a new poetry environment and installs all required dependencies

## Running

For development, it is recommended to use `PyCharm` to run the project from the `main.py` file.

The project can also be run from the terminal using `poetry run python .\main.py`

### The simplest way

The easiest way, however, is to just create a little PowerShell script, like 'par2logreader.ps1' and place it in a folder that is on the `PATH`.
The script can be implemented like:

```ps1
Push-Location "<dir>\PAR2LogReader"
poetry run python main.py
```
Change `<dir>` to where you've cloned the repo. The log reader can then be launched from any terminal by running the command `par2logreader`.

## Building executable

To build a single file executable, run `.\build.bat`. This creates an executable file in the `/dist` folder and copies assets.

## Configuration

...