from docuzebre.inference import infer
import streamlit as st
from utils import request_ocr


def parse_txt(text, model_name):
    result = infer(model_name, st.session_state["models_dict"], text)
    st.session_state["model_output"] = result 

def display_tab():
    if st.session_state.get("model_output") is None:
        st.session_state["model_output"] = ""

    st.title("Essai du modèle")
    st.write("Vous pouvez dans cet onglet tester le modèle selectionné contre un texte")

    if st.session_state["model_selectbox"] is None:
        st.error("Veuillez séléctionner un modèle dans le menu déroulant à gauche")
        # Early return
        return None

    col_user, col_llm = st.columns(2)

    with col_user:
     
        # Initial user input handling
        if 'user_input' not in st.session_state:
            st.session_state.user_input = ""  # Initialize the key in session_state

        # File upload and OCR request handling
        file = st.file_uploader("Téléverser votre document", type=["pdf", "jpeg", "jpg", "png"])
        if file:
            text_ocr = request_ocr(st, file)
            st.session_state.user_input = text_ocr  # Update session state with OCR result

        # Text area to display or enter text to parse
        st.text_area(label="Veuillez entrer le texte à parser", key="user_input", height=600)

        st.button(
            "Parser le texte",
            on_click=lambda: parse_txt(
                st.session_state["user_input"],
                st.session_state["model_selectbox"]
            ),
            key="parse"
        )

    with col_llm:
        st.write(st.session_state["model_output"])