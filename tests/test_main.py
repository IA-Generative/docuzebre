from streamlit.testing.v1 import AppTest
from pathlib import Path
import json

from unittest.mock import patch, MagicMock
from model_generation import DynamicModel


front_dir = Path(__file__).resolve().parent.parent / "front"
# Test for model selection and updating selectbox functionality

app_test = AppTest.from_file(str(front_dir / "main.py"))


def test_model_selection_and_update():
    return


# Test for uploading and loading the session file
def test_upload_file():
    """Simulates uploading a file and checks if models are loaded correctly"""
    at = app_test.run()

    # Set the model
    at.session_state["models_dict"] = {dog_fixture.name: dog_fixture}
    at.sidebar.selectbox(key="model_selectbox").set_value("Chien").run()

    # Set select
    at.selectbox(key="tab_selectbox").set_value("Essai sur le modèle").run()
    # TDB


# Test for tab selection functionality
def test_tab_selection(dog_fixture):
    """Simulates selecting a tab and checks if the correct tab is displayed"""
    """Test the "Générer le prompt pour le modèle" functionality."""
    # TODO