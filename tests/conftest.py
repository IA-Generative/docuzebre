from pydantic import BaseModel, Field
import pytest
from model_generation import DynamicModel, DynamicField

model_str = "{\"name\": \"Chien\", \"examples\": [], \"fields\": [{\"name\": \"nom\", \"field_type\": \"str\", \"description\": \"Nom du chien\", \"optional\": false, \"many\": false, \"example\": \"\"}, {\"name\": \"age\", \"field_type\": \"int\", \"description\": \"Age du chien\", \"optional\": false, \"many\": false, \"example\": \"\"}, {\"name\": \"maitre\", \"field_type\": \"str\", \"description\": \"Nom du maitre\", \"optional\": false, \"many\": true, \"example\": \"\"}]}"


# Define the Dog model
Chien = DynamicModel(
    name='Chien',
    fields=[
        DynamicField(name='nom', field_type='str', description='Nom du chien',
                     optional=False, many=False, example=''),
        DynamicField(name='age', field_type='int', description='Age du chien',
                     optional=False, many=False, example=''),
        DynamicField(name='race', field_type='str', description='Race du chien',
                     optional=True, many=False, example=''),
        DynamicField(name='maitre', field_type='str',
                     description='Nom du maitre', optional=True, many=True, example='')
    ],
    examples=[])

dingo = ("Dingo est un labrador age de 4 ans et appartient a Mickey.",
         {"nom": "Dingo", "age": "4", "maitre": ["Mickey"]})

pluto = ("""Pluto est un caniche  qui semble avoir 10 ans e Mickey revendique sa propriété. 
    Cependant, d'après son acte de naissance, il est née en 2021 et sa maitresse est Minnie. 
    L'acte de naissance prévaut sur toutes les autres informations.""",
         {"nom": "Pluto", "race": "caniche", "age": "1", "maitre": ["Minnie"]})
# Create a pytest fixture that returns a Dog instance


@pytest.fixture
def dog_fixture():
    return Chien


@pytest.fixture
def example_fixture():
    return [dingo]

@pytest.fixture
def tryout_fixture():
    yield [
        "L'age de Mickey est au moins de 5 ans, et un dogue allemand.",
        "Le chien  retrouvé doit etre un dogue, sur le médaillon on lit Pluto et doit avoir au moins 5ans. Il a été rendu à son maitre Dingo."
        ]
