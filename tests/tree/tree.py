"""
Docstring for tests.tree
"""

from pathlib import Path
from cnlib.cntree import CNTree  # type: ignore

if __name__ == "__main__":
    dir2 = Path(__file__).parent
    t = CNTree(dir2)
    t.main()

    with open("tests/tree/tree.txt", "w", encoding="UTF-8") as a_file:
        a_file.write(t.text)

    with open("tests/tree/tree.html", "w", encoding="UTF-8") as a_file:
        a_file.write(t.html)
