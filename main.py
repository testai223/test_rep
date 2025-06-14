#!/usr/bin/env python3
"""
A simple Hello World application template following Python best practices.

This module serves as a template for Python projects, demonstrating proper
structure, type hints, docstrings, and PEP8 compliance.
"""

import argparse
import random
import subprocess
import sys
from pathlib import Path
from typing import Optional, List

import tkinter as tk
from tkinter import messagebox


def greet(name: Optional[str] = None) -> str:
    """
    Generate a greeting message.

    Args:
        name: The name to greet. If None, greets the world.

    Returns:
        A greeting message string.

    Examples:
        >>> greet()
        'Hello, World!'
        >>> greet("Alice")
        'Hello, Alice!'
    """
    if name is None:
        return "Hello, World!"
    return f"Hello, {name}!"


FIGURES_FILE = Path(__file__).with_name("data") / "historical_figures.txt"
REMOTE_FIGURES_URL = "https://example.com/historical_figures.txt"

DEFAULT_HISTORICAL_FIGURES = [
    "Albert Einstein",
    "Cleopatra",
    "Leonardo da Vinci",
    "Mahatma Gandhi",
    "Marie Curie",
]

IEEE9BUS_FILE = Path(__file__).with_name("data") / "ieee9bus.json"


def load_ieee9bus() -> dict:
    """Load the IEEE 9 bus grid example from disk."""
    import json

    with IEEE9BUS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_historical_figures() -> List[str]:
    """Load historical figures from file or remote source."""
    if FIGURES_FILE.exists():
        try:
            with FIGURES_FILE.open("r", encoding="utf-8") as f:
                names = [line.strip() for line in f if line.strip()]
            if names:
                return names
        except OSError as exc:
            print(f"Failed to read {FIGURES_FILE}: {exc}")

    try:
        import requests

        response = requests.get(REMOTE_FIGURES_URL, timeout=5)
        if response.ok:
            names = [line.strip() for line in response.text.splitlines() if line.strip()]
            if names:
                return names
    except Exception as exc:  # pragma: no cover - network may fail
        print(f"Unable to fetch remote historical figures: {exc}")

    return DEFAULT_HISTORICAL_FIGURES


HISTORICAL_FIGURES = load_historical_figures()


def greet_random_historical_figure() -> str:
    """Return a greeting for a random historical figure."""
    return greet(random.choice(HISTORICAL_FIGURES))


def git_commit_and_push(commit_message: str) -> bool:
    """
    Commit all changes and push to GitHub.

    Args:
        commit_message: The commit message to use.

    Returns:
        True if successful, False otherwise.
    """
    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)

        # Commit with the provided message. When there are no changes to commit,
        # Git exits with status 1 and prints "nothing to commit". That should not
        # be treated as a hard failure, so we handle that case manually.
        commit = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True,
        )
        commit_output = (commit.stdout or "") + (commit.stderr or "")
        if commit.returncode != 0 and "nothing to commit" not in commit_output.lower():
            raise subprocess.CalledProcessError(
                commit.returncode,
                commit.args,
                output=commit.stdout,
                stderr=commit.stderr,
            )

        # Push to origin
        subprocess.run(["git", "push"], check=True, capture_output=True, text=True)

        print(f"Successfully committed and pushed with message: '{commit_message}'")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False


def run_gui() -> None:
    """Run the application in GUI mode."""

    def on_greet() -> None:
        message = greet(name_var.get() or None)
        output_var.set(message)

    def on_commit() -> None:
        msg = commit_var.get()
        if not msg:
            messagebox.showerror("Error", "Commit message cannot be empty")
            return
        success = git_commit_and_push(msg)
        if success:
            messagebox.showinfo("Success", "Changes committed and pushed")
        else:
            messagebox.showerror("Error", "Git operation failed")

    def on_load_ieee9bus() -> None:
        try:
            grid = load_ieee9bus()
        except OSError as exc:
            messagebox.showerror("Error", f"Failed to read example: {exc}")
            return
        buses = len(grid.get("buses", []))
        branches = len(grid.get("branches", []))
        loads = len(grid.get("loads", []))
        generators = len(grid.get("generators", []))
        messagebox.showinfo(
            "IEEE 9 Bus Loaded",
            f"Loaded grid with {buses} buses, {branches} branches, "
            f"{loads} loads and {generators} generators",
        )

    root = tk.Tk()
    root.title("Hello World GUI")

    name_var = tk.StringVar()
    commit_var = tk.StringVar()
    output_var = tk.StringVar()

    tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(root, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

    tk.Button(root, text="Greet", command=on_greet).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Commit message:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(root, textvariable=commit_var).grid(row=1, column=1, padx=5, pady=5)

    tk.Button(root, text="Commit", command=on_commit).grid(row=1, column=2, padx=5, pady=5)

    tk.Button(root, text="Load IEEE 9 Bus", command=on_load_ieee9bus).grid(
        row=2, column=0, columnspan=3, padx=5, pady=5
    )

    tk.Label(root, textvariable=output_var).grid(row=3, column=0, columnspan=3, padx=5, pady=10)

    root.mainloop()


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Hello World application with Git integration"
    )
    parser.add_argument(
        "--commit",
        type=str,
        help="Commit message for git commit and push",
        metavar="MESSAGE"
    )
    parser.add_argument(
        "--name",
        type=str,
        help="Name to greet",
        default=None
    )
    parser.add_argument(
        "--random-historical",
        action="store_true",
        help="Greet a random historical figure"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Run the application in GUI mode"
    )
    
    return parser.parse_args()


def main() -> None:
    """
    Main entry point of the application.
    
    This function orchestrates the program execution and handles
    any necessary setup or cleanup.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    if args.gui:
        run_gui()
        return

    # If commit message is provided, perform git operations
    if args.commit:
        success = git_commit_and_push(args.commit)
        if not success:
            sys.exit(1)
        return

    if args.random_historical:
        print(greet_random_historical_figure())
    else:
        # Otherwise, run the greeting functionality
        print(greet(args.name))


if __name__ == "__main__":
    main()
