# Hello World Python Template with Git Integration

A simple Python project template that follows best practices and PEP8 guidelines, now with Git integration features.

## Features

- ✅ Type hints for better code clarity
- ✅ Comprehensive docstrings
- ✅ PEP8 compliant code style
- ✅ Proper project structure
- ✅ Main entry point pattern
- ✅ Ready for testing and linting
- ✅ **Git commit and push functionality**
- ✅ **Command-line argument parsing**
- ✅ **GUI mode with `--gui` option**
- ✅ **Includes a database of 1000 historical personalities**
- ✅ **Fetches a list from the internet if the local database is missing**

### GUI Usage

Launch the graphical interface with:

```bash
python main.py --gui
```

## Project Structure

### Historical Figures Database

The `data/historical_figures.txt` file contains 1000 names used when
invoking `--random-historical`. Feel free to expand or replace this list
as desired. If the file is missing, the application attempts to download a
list from `https://example.com/historical_figures.txt` before falling back
to a small built-in set.

