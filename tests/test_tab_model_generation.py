from pathlib import Path
from streamlit.testing.v1 import AppTest

# Set up the path to the "main.py" file in the "front" directory
front_dir = Path(__file__).resolve().parent.parent / "front"
app_test = AppTest.from_file(str(front_dir / "main.py"))


def test_generate_model_prompt(dog_fixture):
    """Test the "Générer le prompt pour le modèle" functionality."""
    # Initialize the app and set the necessary inputs
    at = app_test.run()

    # Set the model name input
    at.text_input(key="model_name").set_value(dog_fixture.name).run()

    # Simulate adding fields
    for i, field in enumerate(dog_fixture.fields):
        at.text_input(key=f"name_{i}").set_value(field.name).run()
        at.selectbox(key=f"type_{i}").set_value(field.field_type).run()
        at.text_input(key=f"description_{i}").set_value(
            field.description).run()
        if i != len(dog_fixture.fields):
            at.button(key="add_field").click().run()

    # Simulate clicking the "Générer le prompt pour le modèle" button
    at.button(key="save").click().run()

    at.button(key="generate_prompt").click().run()

    # Check the output for the generated prompt

    assert "Your goal is to extract structured information" in at.text[0].value
    assert dog_fixture.fields[0].description in at.text[0].value
