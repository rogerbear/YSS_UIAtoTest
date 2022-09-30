import os
from pathlib import Path

def get_project_root() -> Path:
    """Returns project root folder."""
    return os.path.abspath(Path(__file__).parent.parent)