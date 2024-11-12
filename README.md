# DocuZèbre 🦓🗎

**DocuZèbre** est une application permettant de construire des modèles de données Pydantic, intégrée avec la bibliothèque **Kor** pour l'extraction de données structurées. L'application offre une interface graphique (Streamlit) et une API (FastAPI) pour tester les modèles via des appels OCR.

## 1. Structure du projet

``` plaintext
.
├── deployments/            # Déploiement Kubernetes (fichiers YAML)
├── docuzebre/              # Package python partagé
│   ├── inference.py        # Inférence avec Kor
│   ├── model_generation.py # Génération des modèles de données Pydantic V2
├── api/                    # Code pour l'API FastAPI
│   ├── app.py              # Script principal
├── front/                  # Code et fichiers de l'interface Streamlit
│   ├── .streamlit/         # Configuration Streamlit
│   ├── main.py             # Script principal
│   ├── tab_*.py            # Les tab du frontend
├── tests/                  # Tests unitaires et d'intégration
└── .env                    # Fichier de configuration des variables d'environnement
```

## 2. Dépendances

### Environnement Local

1.  Installez **uv** de **Astral** : `make install`

2.  Créez un fichier `.env` à partir de `.env.sample` et définissez les variables d'environnement nécessaires.

3.  Lancez les services locaux (FastAPI et Streamlit) : `make run`

### Environnement Docker Compose (pas testé)

1.  Assurez-vous que **Docker** et **Docker Compose** sont installés.

2.  Utilisez le fichier `docker-compose.yml` pour lancer l'application :

    docker-compose up --build

## Environnement Kubernetes

1.  Déployez l'application sur Kubernetes en utilisant les manifests dans le dossier `deployments/` :

    kubectl apply -f deployments/

## 3. CI/CD

Les déploiements sont automatiquement gérés via CI/CD avec GitHub Actions pour les environnements **production** et **staging**. Les URL de production et de staging sont :

-   Production : https://docuzebre.c0.cloud-pi-native.com
-   Staging : https://docuzebre-staging.c0.cloud-pi-native.com

## 4. API FastAPI

L'API FastAPI est accessible à l'adresse suivante :

-   Swagger Documentation : https://fastapi-docuzebre.c0.cloud-pi-native.com/docs

## 5. Licence

Ce projet est sous licence **Copyleft**. Vous pouvez le redistribuer et le modifier selon les termes de la licence. Pour plus de détails, consultez le fichier **LICENSE**.

## 6. Alternatives à DocuZèbre

-   Parser Expert : https://parser.expert/
-   DocuPanda : https://docupanda.com