"""
Very simple tool to create a new project directory with a .gitignore and empty README.
"""

from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser(description='Create a new python project.')
parser.add_argument('name', help='name of the project')
parser.add_argument('path', nargs='?', help='project path')

command_line = parser.parse_args()

PROJECT_NAME = command_line.name
PROJECT_PATH = Path(command_line.path or PROJECT_NAME)

if PROJECT_PATH.exists():
    raise FileExistsError(PROJECT_PATH.absolute())

PROJECT_PATH.mkdir()
(PROJECT_PATH / '.gitignore').write_text(r'__pycache__/')
(PROJECT_PATH / 'README.md').touch()
(PROJECT_PATH / PROJECT_NAME).mkdir()
(PROJECT_PATH / PROJECT_NAME / '__init__.py').touch()
