from pathlib import Path
from streamlit.testing.v1 import AppTest

# Set up the path to the "main.py" file in the "front" directory
front_dir = Path(__file__).resolve().parent.parent / "front"
app_test = AppTest.from_file(str(front_dir / "main.py"))