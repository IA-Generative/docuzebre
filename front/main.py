import streamlit as st
from tab_model_generation import display_tab as display_tab1
from tab_example import display_tab as display_tab2
from tab_tryout import display_tab as display_tab3
from docuzebre.model_generation import DynamicModel
from utils import load_from_api
import json
import os


def display_tab4():
    return st.components.v1.iframe(f"https://user-astree-940072-0.c0.cloud-pi-native.com/absproxy/5000/docs", height=600, scrolling=True)


pages = [
    {
        "title": "Génération d'un modèle de données",
        "function": display_tab1,
        "icon": "🔧",
    },
    {
        "title": "Saisie d'example",
        "function": display_tab2,
        "icon": "📝",
    },
    {
        "title": "Tester l'extraction",
        "function": display_tab3,
        "icon": "🔍",
    },
    {
        "title": "Voir l'API",
        "function": display_tab4,
        "icon": "🌐",
    }
]

st.set_page_config(
    page_title="Docuzebre",
    page_icon="🦓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

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


st.sidebar.radio(
    label="Modeles Disponibles",
    options=(st.session_state["models_dict"] or []),
    key="model_selectbox",
    on_change=update_selectbox,
)


with st.sidebar.expander("Importer une session"):
    st.file_uploader(
        label="Charger depuis son ordinateur",
        on_change=lambda: upload_file(),
        key="session_uploader",
        type="json"
    )

    st.button(
        label="Charger depuis le serveur",
        on_click=lambda: load_from_api(st),
        key="session_api")


st.sidebar.download_button(
    label="Télécharger la session",
    data=json.dumps(
        [model.to_json() for model in st.session_state["models_dict"].values()]
    ),
    file_name="Sauvegarde_session.json",
)

# options[st.session_state["tab_selectbox"]]()

pg = st.navigation([
    st.Page(page["function"], title=page["title"], icon=page["icon"], url_path=f"/{page["title"].replace(' ', '-').lower()}" )
    for page in pages
])

pg.run()