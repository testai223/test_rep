#!/usr/bin/env python3
"""
A simple Hello World application template following Python best practices.

This module serves as a template for Python projects, demonstrating proper
structure, type hints, docstrings, and PEP8 compliance.
"""

import argparse
import subprocess
import sys
from typing import Optional

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

    tk.Label(root, textvariable=output_var).grid(row=2, column=0, columnspan=3, padx=5, pady=10)

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
    else:
        # Otherwise, run the greeting functionality
        print(greet(args.name))


if __name__ == "__main__":
    main()
