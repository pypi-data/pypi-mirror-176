"""Make docker management a nice experience
Contact:
--------
- https://github.com/coelias/ulises
"""
# Standard library imports
import sys

# Reader imports
from ulises import maincli

def banner():
    print("""
Ulises by carlos@delojo.me
Type `help` or `h` + <ENTER>  for help
Each sub CLI has its own help command

Use ALWAYS <TAB> to autocomplete! it's the point of this!
""")


def main() -> None:
    banner()
    maincli.MainCli().cmdloop()


if __name__ == "__main__":
    main()
