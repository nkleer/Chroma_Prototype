"""Play Chroma in a terminal:  python3 play.py   (needs Python 3 and numpy)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from console import Console  # noqa: E402


def main():
    c = Console()
    print(c.start_text())
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if line.strip().lower() in ("q", "quit", "exit"):
            return
        text, busy = c.handle(line)
        if text:
            print(text, flush=True)
        while busy:
            text, busy = c.handle("")
            if text:
                print(text, flush=True)


if __name__ == "__main__":
    main()
