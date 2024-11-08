from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from pathlib import Path
from docuzebre.model_generation import DynamicModel
from docuzebre.inference import infer
import json, os

app = FastAPI(root_path=f"/{os.getenv("ROOT_PATH", "")}")

# Directory to store models as JSON files using pathlib
MODEL_DIR = Path("models")


# Ensure model directory exists
@app.on_event("startup")
async def load_models_on_startup():
    MODEL_DIR.mkdir(exist_ok=True)
    app.state.models = {}
    for model_file in MODEL_DIR.glob("*.json"):
        model_name = model_file.stem  # Extract file name without extension
        print(f"import model {model_name}")
        with model_file.open("r") as f:
            model_data = json.load(f)
            app.state.models[model_name] = DynamicModel.from_json(model_data)


class DocumentInput(BaseModel):
    text: str


@app.get("/models")
async def get_models():
    return {"models": list(app.state.models.keys())}


@app.get("/models/{model_name}")
async def get_model(model_name: str):
    if model_name in app.state.models:
        return app.state.models[model_name].dict()
    raise HTTPException(status_code=404, detail="Model not found")


@app.post("/models/{model_name}")
async def save_model(model_name: str, model: dict, response: Response):
    # Print the incoming model for debugging
    print(f'model : {model}')
    
    # Generate Pydantic model and parse the incoming data
    model = DynamicModel.from_json(model)

    # Check if the model already exists
    model_file_path = MODEL_DIR / f"{model_name}.json"
    model_exists = model_file_path.exists()

    # Save parsed model to memory
    app.state.models[model_name] = model

    # Try to persist the model data to its own JSON file
    try:
        with model_file_path.open("w") as f:
            json.dump(model._to_json(), f, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save model: {str(e)}")

    # Set the appropriate status code
    if model_exists:
        response.status_code = status.HTTP_200_OK  # Model modified
        return {"message": "Model modified successfully", "model": model.dict()}
    else:
        response.status_code = status.HTTP_201_CREATED  # Model added
        return {"message": "Model added successfully", "model": model.dict()}


@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    if model_name in app.state.models:
        del app.state.models[model_name]
        model_file_path = MODEL_DIR / f"{model_name}.json"
        if model_file_path.exists():
            try:
                model_file_path.unlink()  # Remove the file
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete model: {str(e)}")
        return {"message": f"Model '{model_name}' deleted successfully"}
    raise HTTPException(status_code=404, detail="Model not found")


# New route to post a document and return a dict
@app.post("/extract/{model_name}")
async def extract_data(model_name: str, text: str):
    try:
        result = infer(model_name, app.state.models, text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during extraction: {str(e)}")
    # Return the extracted dictionary
    return result
