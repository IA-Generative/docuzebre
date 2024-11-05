import os

from docuzebre.model_generation import generate_model
from langchain_openai import ChatOpenAI
from kor import from_pydantic, create_extraction_chain


def infer(model_name, model, text: str):
    model_pydantic = generate_model(model[model_name], model)
    # Create schema and validator from Pydantic model
    schema, validator = from_pydantic(
        model_pydantic, description="", examples=model[model_name].examples, many=True
    )

    # Set up the language model (LLM)
    llm = ChatOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_API_BASE"],
        temperature=0,
        model="gemma2-simpo",
    )

    # Create the extraction chain
    chain = create_extraction_chain(
        llm, schema, encoder_or_encoder_class="json", validator=validator
    )

    # Invoke the chain with the provided text
    result = chain.invoke(text)
    return result
