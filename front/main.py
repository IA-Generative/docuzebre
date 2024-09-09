import streamlit as st
from tab_model_generation import display_tab as display_tab1
from tab_example import display_tab as display_tab2
from tab_tryout import display_tab as display_tab3
from model_generation import DynamicModel
import json

options = {
    "Génération de modèles": display_tab1,
    "Saisie d'example": display_tab2,
    "Essai sur le modèle": display_tab3,
}

# st.markdown("""
#     <base href="/proxy/8501/">
#     """, unsafe_allow_html=True)

if not st.session_state.get("models_dict"):
    st.session_state["models_dict"] = {}


def update_selectbox():
    st.session_state["current_model"] = st.session_state["models_dict"][
        st.session_state["model_selectbox"]
    ]


def upload_file():
    if (f := st.session_state["session_uploader"]) is None:
        return
    loaded_file = json.loads(f.read())
    for model_str in loaded_file:
        model = DynamicModel.from_json(model_str)
        st.session_state["models_dict"][model.name] = model


st.sidebar.selectbox(
    label="Modeles Disponibles",
    options=(st.session_state["models_dict"] or []),
    key="model_selectbox",
    on_change=update_selectbox,
)

st.sidebar.download_button(
    label="Sauvegarder la session",
    data=json.dumps(
        [model.to_json() for model in st.session_state["models_dict"].values()]
    ),
    file_name="Sauvegarde_session.json",
)

st.sidebar.file_uploader(
    label="Uploader une session",
    on_change=lambda: upload_file(),
    key="session_uploader",
)

st.selectbox(
    label="Séléction d'onglet",
    options=options.keys(),
    key="tab_selectbox",
    label_visibility="hidden",
)

options[st.session_state["tab_selectbox"]]()
