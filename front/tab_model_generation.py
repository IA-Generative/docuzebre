import functools
from model_generation import generate_model, DynamicModel, base_defined_type
from copy import deepcopy
from kor import from_pydantic, create_extraction_chain
from langchain_openai import ChatOpenAI
import streamlit as st


def generate_key(current_model, current_field, attr):
    return f"{current_model.name}_{current_field.name}_{attr}"


def update_field(field, key):
    # Hack pour éviter de clicker deux fois sur un attribut
    attr = key.split("_")[-1]
    setattr(field, attr, st.session_state[key])


def display_tab():
    st.title("Création de modèles pydantic")

    if not st.session_state.get("models_dict"):
        st.session_state["models_dict"] = {}
    if not st.session_state.get("current_model"):
        st.session_state["current_model"] = DynamicModel.default()

    current_model: DynamicModel = st.session_state["current_model"]

    current_model.name = st.text_input(label="Nom du modèle", value=current_model.name, key="model_name")
    available_type = list(base_defined_type.keys()) + [
        model
        for model in st.session_state["models_dict"]
        if model != current_model.name
    ]

    for idx, field in enumerate(current_model.fields):
        st.divider()
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            field.name = st.text_input(
                label="Nom du champ", value=field.name, key=f"name_{idx}"
            )
            field.field_type = st.selectbox(
                label="Type du champ",
                options=available_type,
                key=f"type_{idx}",
                index=available_type.index(field.field_type),
            )
            field.description = st.text_input(
                label="Description du champ",
                value=field.description,
                key=f"description_{idx}",
            )
        with col2:
            st.checkbox(
                label="Plusieurs entités possibles",
                value=field.many,
                key=generate_key(current_model, field, "many"),
                on_change=functools.partial(
                    update_field,
                    field=field,
                    key=generate_key(current_model, field, "many"),
                ),
            )
            st.checkbox(
                label="Facultatif",
                value=field.optional,
                key=generate_key(current_model, field, "optional"),
                on_change=functools.partial(
                    update_field,
                    field=field,
                    key=generate_key(current_model, field, "optional"),
                ),
            )
            col2.button(
                "🗑️",
                help="Bouton pour supprimer le champ",
                key=f"suppres_{idx}",
                on_click=functools.partial(current_model.suppress_field, idx=idx),
            )

    st.button("Ajouter un champ", key="add_field", on_click=lambda: current_model.add_field())

    st.divider()

    if st.button("Enregistrer ou mettre à jour le modèle", key="save"):
        tmp_list = [field.name for field in current_model.fields]
        cond = len(set(tmp_list)) == len(tmp_list)
        if not cond:
            st.error("Veuillez choisir des noms de champ différent")
        else:
            st.session_state["models_dict"][current_model.name] = deepcopy(
                current_model
            )
            st.rerun()

    st.divider()

    if st.button("Générer le prompt pour le modèle", key="generate_prompt"):
        if current_model.name not in st.session_state["models_dict"]:
            st.error("Fonctionnalité disponible pour les modèles enregistrés")
        else:

            result = generate_model(
                st.session_state["current_model"], st.session_state["models_dict"]
            )
            schema, validator = from_pydantic(result)
            chain = create_extraction_chain(
                ChatOpenAI(api_key="gserghrtjeyhstgezt"),
                schema,
                encoder_or_encoder_class="json",
            )
            st.text(
                chain.get_prompts()[0].format_prompt(text="[user_input]").to_string()
            )
