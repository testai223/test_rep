#!/usr/bin/env python3
"""
A simple Hello World application template following Python best practices.

This module serves as a template for Python projects, demonstrating proper
structure, type hints, docstrings, and PEP8 compliance.
"""

# Standard library imports
import argparse
import logging
import random
import subprocess
import sys
from pathlib import Path
from typing import Optional, List

# Third-party imports
try:
    import requests
except ImportError:
    requests = None  # type: ignore

# GUI imports (optional)
try:
    import tkinter as tk
    from tkinter import messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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


# Configuration
FIGURES_FILE = Path(__file__).with_name("data") / "historical_figures.txt"
# Using a real API endpoint for demonstration (returns JSON with historical events)
REMOTE_FIGURES_URL = "https://api.api-ninjas.com/v1/historicalevents?text=born"

DEFAULT_HISTORICAL_FIGURES = [
    "Albert Einstein",
    "Marie Curie",
    "Leonardo da Vinci",
    "Isaac Newton",
    "Charles Darwin",
    "Galileo Galilei",
    "Nikola Tesla",
    "Ada Lovelace",
    "Alan Turing",
    "Rosalind Franklin",
    "Stephen Hawking",
    "Katherine Johnson",
    "Aristotle",
    "Cleopatra",
    "William Shakespeare",
    "Jane Austen",
    "Mahatma Gandhi",
    "Martin Luther King Jr.",
    "Nelson Mandela",
    "Eleanor Roosevelt",
]


def load_historical_figures() -> List[str]:
    """Load historical figures from file or remote source."""
    # Try loading from local file first
    if FIGURES_FILE.exists():
        try:
            with FIGURES_FILE.open("r", encoding="utf-8") as f:
                names = [line.strip() for line in f if line.strip()]
            # Filter out obviously fake combinations
            valid_names = [name for name in names if is_valid_historical_name(name)]
            if valid_names:
                logger.info(f"Loaded {len(valid_names)} historical figures from {FIGURES_FILE}")
                return valid_names[:50]  # Limit to 50 names for performance
        except OSError as exc:
            logger.warning(f"Failed to read {FIGURES_FILE}: {exc}")

    # Try fetching from remote source (disabled for now as the example URL is placeholder)
    if requests and False:  # Disabled until we have a real API endpoint
        try:
            response = requests.get(REMOTE_FIGURES_URL, timeout=5)
            response.raise_for_status()
            # This would need to be adapted based on actual API response format
            logger.info("Successfully fetched historical figures from remote source")
        except requests.exceptions.RequestException as exc:
            logger.warning(f"Unable to fetch remote historical figures: {exc}")

    logger.info("Using default historical figures list")
    return DEFAULT_HISTORICAL_FIGURES


def is_valid_historical_name(name: str) -> bool:
    """
    Check if a name is likely a valid historical figure.
    
    This is a simple heuristic to filter out obviously fake combinations.
    """
    # List of actual historical first names and last names
    valid_first_names = {
        "Albert", "Isaac", "Marie", "Leonardo", "Nikola", "Charles", "William",
        "George", "Thomas", "Benjamin", "Alexander", "Julius", "Napoleon",
        "Winston", "Franklin", "Theodore", "John", "Elizabeth", "Catherine",
        "Cleopatra", "Joan", "Rosa", "Harriet", "Ada", "Alan", "Stephen"
    }
    
    valid_last_names = {
        "Einstein", "Newton", "Curie", "da Vinci", "Tesla", "Darwin", "Shakespeare",
        "Washington", "Jefferson", "Franklin", "Hamilton", "Caesar", "Bonaparte",
        "Churchill", "Roosevelt", "Kennedy", "Luther", "Galilei", "Copernicus",
        "Pasteur", "Nightingale", "Parks", "Tubman", "Lovelace", "Turing", "Hawking"
    }
    
    parts = name.split()
    if len(parts) >= 2:
        # Check if it's a known valid combination or has valid components
        known_figures = {
            "Albert Einstein", "Isaac Newton", "Marie Curie", "Leonardo da Vinci",
            "Nikola Tesla", "Charles Darwin", "William Shakespeare", "George Washington",
            "Martin Luther King Jr.", "Rosa Parks", "Ada Lovelace", "Alan Turing"
        }
        if name in known_figures:
            return True
        
        # Otherwise check if first and last names make sense together
        first = parts[0]
        last = parts[-1]
        
        # Avoid nonsensical combinations like "Albert Newton" or "Isaac Einstein"
        nonsensical_combos = {
            ("Albert", "Newton"), ("Isaac", "Einstein"), ("Marie", "Tesla"),
            ("Nikola", "Darwin"), ("Leonardo", "Shakespeare")
        }
        
        if (first, last) in nonsensical_combos:
            return False
            
    return True  # Default to true for other cases


# Load historical figures at module level
HISTORICAL_FIGURES = load_historical_figures()


def greet_random_historical_figure() -> str:
    """Return a greeting for a random historical figure."""
    if not HISTORICAL_FIGURES:
        return greet("a mysterious historical figure")
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
        result = subprocess.run(
            ["git", "add", "."], 
            check=True, 
            capture_output=True, 
            text=True
        )
        logger.debug(f"Git add output: {result.stdout}")

        # Commit with the provided message
        commit = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True,
        )
        
        # Check if there were no changes to commit
        if commit.returncode != 0:
            if "nothing to commit" in commit.stdout or "nothing to commit" in commit.stderr:
                logger.info("No changes to commit")
                return True
            else:
                logger.error(f"Git commit failed: {commit.stderr}")
                return False

        # Push to origin
        push = subprocess.run(
            ["git", "push"], 
            check=True, 
            capture_output=True, 
            text=True
        )
        logger.debug(f"Git push output: {push.stdout}")

        logger.info(f"Successfully committed and pushed with message: '{commit_message}'")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Git operation failed: {e}")
        if e.stderr:
            logger.error(f"Error details: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("Git command not found. Please ensure Git is installed.")
        return False


def run_gui() -> None:
    """Run the application in GUI mode."""
    if not TKINTER_AVAILABLE:
        logger.error("Tkinter is not available. Please install tkinter to use GUI mode.")
        sys.exit(1)
    
    def on_greet() -> None:
        """Handle greet button click."""
        message = greet(name_var.get() or None)
        output_var.set(message)
        logger.info(f"GUI greeting: {message}")

    def on_greet_random() -> None:
        """Handle random historical figure greeting."""
        message = greet_random_historical_figure()
        output_var.set(message)
        logger.info(f"GUI random greeting: {message}")

    def on_commit() -> None:
        """Handle commit button click."""
        msg = commit_var.get()
        if not msg:
            messagebox.showerror("Error", "Commit message cannot be empty")
            return
        
        success = git_commit_and_push(msg)
        if success:
            messagebox.showinfo("Success", "Changes committed and pushed")
            commit_var.set("")  # Clear the commit message field
        else:
            messagebox.showerror("Error", "Git operation failed. Check the console for details.")

    # Create main window
    root = tk.Tk()
    root.title("Hello World GUI")
    root.geometry("400x250")
    
    # Variables
    name_var = tk.StringVar()
    commit_var = tk.StringVar()
    output_var = tk.StringVar(value="Welcome! Enter a name or click a button.")

    # Name input section
    tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(root, textvariable=name_var, width=25).grid(row=0, column=1, columnspan=2, padx=5, pady=5)

    # Buttons
    tk.Button(root, text="Greet", command=on_greet, width=15).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(root, text="Random Historical", command=on_greet_random, width=15).grid(row=1, column=1, padx=5, pady=5)

    # Git section
    tk.Label(root, text="Git Commit:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(root, textvariable=commit_var, width=25).grid(row=2, column=1, columnspan=2, padx=5, pady=5)
    tk.Button(root, text="Commit & Push", command=on_commit, width=15).grid(row=3, column=1, padx=5, pady=5)

    # Output section
    output_label = tk.Label(root, textvariable=output_var, wraplength=350, font=("Arial", 10))
    output_label.grid(row=4, column=0, columnspan=3, padx=10, pady=20)

    # Start the GUI event loop
    root.mainloop()


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Hello World application with Git integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     # Print 'Hello, World!'
  %(prog)s --name Alice        # Print 'Hello, Alice!'
  %(prog)s --random-historical # Greet a random historical figure
  %(prog)s --gui               # Launch GUI mode
  %(prog)s --commit "Initial commit"  # Commit and push changes
        """
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
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    return parser.parse_args()


def main() -> None:
    """
    Main entry point of the application.
    
    This function orchestrates the program execution based on command-line arguments.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    # Configure logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # GUI mode
    if args.gui:
        logger.info("Starting GUI mode")
        run_gui()
        return

    # Git commit mode
    if args.commit:
        logger.info(f"Performing git commit with message: {args.commit}")
        success = git_commit_and_push(args.commit)
        if not success:
            sys.exit(1)
        return

    # Greeting mode
    if args.random_historical:
        message = greet_random_historical_figure()
    else:
        message = greet(args.name)
    
    print(message)
    logger.info(f"Generated greeting: {message}")


if __name__ == "__main__":
    main()