from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
LIB_ROOT = Path(__file__).parent.resolve()
PARENT_DIR = lambda p: Path(p).parent.resolve()
