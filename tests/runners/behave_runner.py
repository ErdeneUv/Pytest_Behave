import os
from behave.__main__ import main
from pathlib import Path
from dotenv import find_dotenv

dotenv_path = find_dotenv(usecwd=True)
project_root = os.path.dirname(dotenv_path)
path = Path.joinpath(Path(project_root), "tests/features")

if __name__ == '__main__':
    tag_expression = ''

    main([
        path,
        tag_expression
    ])

