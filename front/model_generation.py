from typing import Optional
from pydantic import create_model, Field, BaseModel
import json

base_defined_type = {"int": int, "str": str, "float": float, "bool": bool}


class DynamicField(BaseModel):
    """
    Classe pour répresenter un champ d'un modèle pydantic
    """

    name: str
    field_type: str
    description: str
    optional: bool
    many: bool
    example: str = ""

    @classmethod
    def default(cls) -> "DynamicField":
        return cls(
            name="Nom du champ",
            field_type="str",
            description="Description par défaut du champ",
            optional=False,
            many=False,
        )

    def is_base_type(self) -> bool:
        """Return true if the field_type is one of the base type, false otherwise"""
        if self.field_type in base_defined_type:
            return True
        else:
            return False

    def _to_json(self) -> dict[str, str]:
        return {attr: getattr(self, attr) for attr in self.__fields__.keys()}

    @classmethod
    def _from_json(cls, dict_field: dict[str, str]) -> "DynamicField":
        return cls(**dict_field)


class DynamicModel(BaseModel):
    """Classe pour répresenter un modèle pydantic"""

    name: str
    fields: list[DynamicField]
    examples: list[tuple[str, list[dict]]]

    @classmethod
    def default(cls) -> "DynamicModel":
        default_field = DynamicField.default()
        return cls(name="Nom du modèle", fields=[default_field], examples=[])

    def add_field(self) -> None:
        self.fields.append(DynamicField.default())

    def suppress_field(self, idx) -> None:
        self.fields.pop(idx)

    def _example_to_dict(self, model_dict: dict[str, "DynamicModel"]) -> dict[str, str]:
        example_dict = {}
        for field in self.fields:
            if field.is_base_type():
                example_dict[field.name] = field.example
            else:
                example_dict[field.name] = model_dict[
                    field.field_type
                ]._example_to_dict(model_dict)

        return example_dict

    def example_to_json(self, model_dict: dict[str, "DynamicModel"]) -> dict:
        example_dict = self._example_to_dict(model_dict)
        return example_dict

    def _to_json(self) -> dict[str, str]:
        res = {
            attr: getattr(self, attr)
            for attr in self.__fields__.keys()
            if attr != "fields"
        }
        res["fields"] = [field._to_json() for field in self.fields]
        return res

    def to_json(self) -> str:
        return json.dumps(self._to_json())

    @classmethod
    def from_json(cls, json_model: str):
        model = json.loads(json_model)
        fields = [DynamicField._from_json(field_str) for field_str in model["fields"]]
        return cls(name=model["name"], fields=fields, examples=model["examples"])

    def add_example(self, example):
        self.examples.append(example)

    def delete_example(self, idx):
        self.examples.pop(idx)


def is_leaf(model: DynamicModel, defined_type: dict[str, type]) -> bool:
    """Check if the model defined by model_dict is a leaf,
    ie is defined only from defined elements"""
    for field in model.fields:
        if field.field_type not in defined_type:
            return False
    return True


def generate_field_args(
    field: DynamicField, defined_type: dict[str, type]
) -> tuple[type, Field]:
    """Generate the class of the field, assuming that it's type has already been defined"""
    field_type = defined_type[field.field_type]
    if field.many:
        field_type = list[field_type]

    if field.optional:
        return (Optional[field_type], Field("", description=field.description))
    else:
        return (field_type, Field(..., description=field.description))


def generate_model_rec(
    current_model: DynamicModel,
    defined_type: dict[str, type],
    models_dict: dict[str, DynamicModel],
):
    # Two case: every field has his type already defined -> define current_model and end recursion
    # at least one field has not been defined -> defined every field not already defined through
    # recursion and define current_model
    if is_leaf(current_model, defined_type):
        kwargs = {
            field.name: generate_field_args(field, defined_type)
            for field in current_model.fields
        }
        defined_type[current_model.name] = create_model(current_model.name, **kwargs)
    else:
        for field in current_model.fields:
            if field.field_type not in defined_type:
                generate_model_rec(
                    models_dict[field.field_type], defined_type, models_dict
                )
        # Caling with recursion will end up on the is leaf branch which will create the model
        # normally, but it ends up in infinite recursion, and I don't understand why...
        kwargs = {
            field.name: generate_field_args(field, defined_type)
            for field in current_model.fields
        }
        defined_type[current_model.name] = create_model(current_model.name, **kwargs)


def generate_model(
    current_model: DynamicModel, models_dict: dict[str, DynamicModel], debug=True
) -> type:
    """Generate the pydantic model from the DynamicModel current_model
    In case of nested models, it needs the other models structures to build the final models
    """
    defined_type = base_defined_type.copy()
    generate_model_rec(current_model, defined_type, models_dict)
    if debug:
        from pydantic import BaseModel

        for model in defined_type.values():
            if issubclass(model, BaseModel):
                print(model.model_json_schema())
    return defined_type[current_model.name]
