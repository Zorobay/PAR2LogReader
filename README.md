# PAR2LogReader

## Setup

1. Install Python 3.13 (3.14 not supported yet).
2. Install Poetry dependency manager: https://python-poetry.org/docs/#installation
3. From the repository root, run `poetry install`
   1. This creates a new poetry environment and installs all required dependencies

## Running

### Development
For development, just run the project from `main.py` in your IDE.

### "Just" running
The project can also be run from the terminal using `poetry run python .\main.py`

A simple trick is to create a little PowerShell script, like `par2logreader.ps1` and place it in a folder that is on the `PATH`.
The script can be implemented like:

```ps1
Push-Location "dir\to\PAR2LogReader"
poetry run python main.py
Pop-Location
```
Change `dir\to` to where you've cloned the repo. The log reader can then be launched from any terminal by running the command `par2logreader`.

## Building executable

⚠️ Highly experimental!

To build a single file executable, run `.\build.bat`. This creates an executable file in the `/dist` folder and copies assets.

## Configuration

The application is configured from `config/main.json`.

The following can be configured:

| Key                   | Type   | Description                                                                                                                    |
|-----------------------|--------|--------------------------------------------------------------------------------------------------------------------------------|
| log_read_batch_size   | int    | The maximum number of lines that are read from a log file before updating the interface table.                                 |
| log_read_frequency_ms | int    | The number of milliseconds to wait before attempting to read a live log again. All new data will be processesed on each read.  |
| highlights            | object | This key controls the syntax highlighting of the stack trace and json views. See more info below.                              |

### Highlights

The `highlights` is a json object, with two possible keys; `stack_trace` and `json` like below:

```json
"highlights": {
   "stack_trace": {...},
   "json": {...}
}
```

#### Stacktrace

This configures the syntax highlighting in the stack trace view that is shown when an error is highlighted in the log table.

Each key in this JSON object will be used as a regular expression, that when matched, will be colored according to the value.
The value is a list with four values `[200, 0, 255, 255]` which represents Red, Green, Blue and Opacity.

Example:

```json
"stack_trace": {
   "line\\s\\d+": [200, 0, 255, 255],
   "DPA.PAR2[\\.\\w]*": [0, 150, 0, 255]
},
```

#### Json

This configures the syntax highlighting in the "Raw text" view of a log line (as all log messages are JSON formatted).

Configuration works same as for **Stacktrace**.