from docuzebre.model_generation import DynamicModel

import requests
import time
import os


def request_ocr(st, file) -> str:
    if file is None:
        return "Aucun fichier téléchargé"

    try:
        # Première étape : téléversement du fichier et demande OCR
        with st.spinner('Téléversement du fichier et traitement OCR...'):
            files = {"file": (file.name, file.getvalue(), "multipart/form-data")}
            res = requests.post(url=f'{os.environ["OCR_URL"]}/?max_height=1200&grayscale=true&return_image=false',
                                files=files)
            
            # Vérification des erreurs côté API
            if res.status_code != 200:
                raise Exception(f"Erreur lors de l'appel API : {res.status_code}")
            
            res_json = res.json()
            print(res_json.get('results'))

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API : {str(e)}")
        return None
    except Exception as e:
        st.error(f"Une erreur est survenue lors du traitement OCR : {str(e)}")
        return None

    # Si tout va bien jusqu'à présent, on fait la deuxième requête
    try:
        if "results" in res_json:
            with st.spinner('Lecture des résultats OCR...'):
                response = requests.post(url=f'{os.environ["OCR_URL"]}/read/',
                                        json=res_json['results'])
                
                # Vérification des erreurs lors de la deuxième requête
                if response.status_code != 200:
                    raise Exception(
                        f"Erreur lors de la lecture des résultats : {response.status_code}")
                
                return response.json()
        else:
            return "Aucune donnée lue"

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API pour la lecture des résultats : {str(e)}")
        return None
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la lecture des résultats : {str(e)}")
        return None


def load_from_api(st):
    # Load all model names
    try:
        print(f'{os.environ["API_URL"]}/models')
        response = requests.get(f'{os.environ["API_URL"]}/models')
        # response.raise_for_status()  # Raise an error if the response is unsuccessful
        model_names = response.json().get("models", [])
        
        # Iterate over each model name and fetch the corresponding model details
        for model_name in model_names:
            try:
                model_response = requests.get(f'{os.environ["API_URL"]}/models/{model_name}')
                model_response.raise_for_status()
                
                # Parse the model JSON and add it to session state
                model = DynamicModel.from_json(model_response.json())
                st.session_state["models_dict"][model_name] = model
                st.toast(f"Model '{model_name}' loaded successfully.")
            
            except requests.exceptions.RequestException as e:
                st.toast(f"Failed to load model '{model_name}': {str(e)}")
            except Exception as e:
                st.toast(f"An error occurred while processing model '{model_name}': {str(e)}")

    except requests.exceptions.RequestException as e:
        st.toast(f"Failed to retrieve model list: {str(e)}")
    except Exception as e:
        st.toast(f"An error occurred while loading models at{os.environ['API_URL']}/models': {str(e)}")


def save_model(current_model, st, display="Modèle"):
    try:
        # Première étape : téléversement du fichier et demande OCR
        with st.spinner('Sauvegarde en base...'):
            time.sleep(1)  # Simulate some processing time            
            response = requests.post(
                url=f'{os.environ["API_URL"]}/models/{current_model.name}',
                json=current_model._to_json()
            )

        # Check the response status code
        if response.status_code == 201:
            st.success(f"{display} ajouté avec succès!")
        elif response.status_code == 200:
            st.success(f"{display} modifié avec succès!")
        else:
            st.error(f"Erreur lors de la sauvegarde : {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API : {str(e)}")
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la sauvegarde en base : {str(e)}")