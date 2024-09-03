import functools
import streamlit as st
from model_generation import DynamicModel
import pymupdf


def parse_pdf(file) -> str:
    page_start, page_end = st.session_state["page_slider"]
    with pymupdf.open(None, file.read(), "pdf") as doc:
        text = ""
        for page in doc[page_start:page_end]:
            text += page.get_text()
    st.session_state["example_text"] = text


def display_page_range(file) -> int:
    if file is None:
        return
    with pymupdf.open(None, file.read(), "pdf") as doc:
        max_page = len(doc)
    file.seek(0)
    if max_page > 1:
        st.slider(
            label="Pages à traiter",
            min_value=1,
            max_value=max_page,
            value=(1, max_page),
            step=1,
            key="page_slider",
        )


def register_example():
    model = st.session_state["models_dict"][st.session_state["model_selectbox"]]
    example = (
        st.session_state["example_text"],
        [model.example_to_json(st.session_state["models_dict"])],
    )
    model.add_example(example)


def update_field_example(field, key):
    field.example = st.session_state[f"example_input_{key}"]


def display_tab():
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
                st.write(example[0][0])
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
            label="Type du document", options=["texte plein", "pdf"], key="file_type"
        )
        if st.session_state["file_type"] == "pdf":
            file = st.file_uploader("Téléverser votre pdf")
            display_page_range(file)
            parse_pdf(file)
            st.write(st.session_state["example_text"])

        elif st.session_state["file_type"] == "texte plein":
            text = st.text_area(label="Entrez le texte d'exemple")
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
