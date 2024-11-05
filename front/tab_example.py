import functools
import streamlit as st
from docuzebre.model_generation import DynamicModel
from utils import request_ocr, save_model


def register_example():
    model = st.session_state["models_dict"][st.session_state["model_selectbox"]]
    example = (
        st.session_state["example_text"],
        [model.example_to_json(st.session_state["models_dict"])],
    )
    model.add_example(example)
    save_model(model, st, display="Exemple")


def update_field_example(field, key):
    field.example = st.session_state[f"example_input_{key}"]


def display_tab():

    st.title("Gestion des examples")

    st.info("Ajouter des examples améliore les résultats d'extraction", icon="ℹ️")

    option = st.selectbox(
        label="Choissisez une option", options=["Nouvel exemple", "Liste des exemples"]
    )

    if option == "Nouvel exemple":
        new_example()

    elif option == "Liste des exemples":
        model: DynamicModel = st.session_state["models_dict"][
            st.session_state["model_selectbox"]
        ]
        for idx, example in enumerate(model.examples):
            st.divider()
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write("Texte de l'exemple")
                st.write(example[0])
                st.write("Json de l'exemple")
                st.write(example[1])
            with col2:
                st.button(
                    "Supprimer l'exemple",
                    on_click=functools.partial(model.delete_example, idx=idx),
                    key=f"delete_example_{idx}",
                )


def display_model(model: DynamicModel, key=0):
    for field in model.fields:
        if field.is_base_type():
            st.text_input(
                label=f"Valeur pour le champ {field.name}",
                placeholder=field.example,
                key=f"example_input_{key}",
                on_change=functools.partial(update_field_example, field=field, key=key),
                value=field.example,
            )
            key += 1
        else:
            with st.expander(label=f"Valeurs pour le champ {field.name}"):
                field_model = st.session_state["models_dict"][field.field_type]
                key = display_model(field_model, key + 1)

    return key


def new_example():

    st.write("Saisie d'exemples")

    if st.session_state.get("model_selectbox") is None:
        st.error("Veuillez sélectionner un modèle dans le menu déroulant à gauche")
        # Early return
        return None

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            label="Type du document", options=["texte plein", "ocr"], key="file_type"
        )

        if st.session_state["file_type"] == "texte plein":
            text = st.text_area(label="Entrez le texte d'exemple")

        elif st.session_state["file_type"] == "ocr":
            file = st.file_uploader("Téléverser votre document", type=["pdf", "jpeg", "jpg", "png"])
            text = request_ocr(st, file)
            text = st.text_area(label="Entrez le texte d'exemple", value=text)

        st.session_state["example_text"] = text

    with col2:
        current_model: DynamicModel = st.session_state["models_dict"][
            st.session_state["model_selectbox"]
        ]

        display_model(current_model)
        st.button(
            label="Enregistrer l'exemple",
            on_click=register_example,
        )
