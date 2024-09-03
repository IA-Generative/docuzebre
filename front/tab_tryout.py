import os
from model_generation import generate_model
import streamlit as st
from kor import from_pydantic, create_extraction_chain
from langchain_openai import ChatOpenAI


def parse_txt(text, model):

    model_pydantic = generate_model(model, st.session_state["models_dict"])
    schema, validator = from_pydantic(
        model_pydantic, description="", examples=model.examples, many=True
    )
    llm = ChatOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_API_BASE"],
        temperature=0,
        model="qwen2",
    )

    chain = create_extraction_chain(
        llm, schema, encoder_or_encoder_class="json", validator=validator
    )

    st.session_state["model_output"] = chain.invoke(text)


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
        st.text_area(label="Veuillez entrer le texte à parser", key="user_input")
        st.button(
            "Parser le texte",
            on_click=lambda: parse_txt(
                st.session_state["user_input"],
                st.session_state["models_dict"][st.session_state["model_selectbox"]],
            ),
        )

    with col_llm:
        st.write(st.session_state["model_output"])
