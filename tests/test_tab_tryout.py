

from pathlib import Path
from streamlit.testing.v1 import AppTest

from dotenv import load_dotenv

load_dotenv()

# Set up the path to the "main.py" file in the "front" directory
front_dir = Path(__file__).resolve().parent.parent / "front"
app_test = AppTest.from_file(str(front_dir / "main.py"))


def test_new_example(dog_fixture, tryout_fixture):
    """Test the "Générer le prompt pour le modèle" functionality."""
    # Initialize the app and set the necessary inputs
    at = app_test.run()

    # Set the model
    at.session_state["models_dict"] = {dog_fixture.name: dog_fixture}

    # Set select
    at.selectbox(key="tab_selectbox").set_value("Essai sur le modèle").run()
    at.sidebar.selectbox(key="model_selectbox").set_value("Chien").run()


    # Simulate adding example
    at.text_area(key="user_input").set_value(tryout_fixture[1]).run()   
    at.button(key="parse").click().run()

    # Check the output for the generated prompt
    import pdb; pdb.set_trace()

    assert "" in at.session_state["model_output"]["raw"]