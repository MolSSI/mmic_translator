from typing import Dict, Any, Optional
from cmselemental.models.procedures import ProcInput, ProcOutput
from cmselemental.models.base import ProtoModel
from pydantic import Field, root_validator

schema_input_default = "mmel_input_default"
schema_output_default = "mmel_output_default"
__all__ = ["TransInput", "TransOutput", "schema_input_default", "schema_output_default"]


class Trans(ProtoModel):
    data_object: Any = Field(
        None,
        description="Toolkit-specific data object that stores atoms e.g. MDanalysis.Universe object.",
    )
    data_units: Optional[Dict[str, str]] = Field(
        None, description="Units for variables stored in data_object."
    )
    schema_object: Any = Field(None, description="MMSchema data object or model.")

    @root_validator
    def _valid_trans_fields(cls, values):
        if values["data_object"] and values["schema_object"]:
            raise ValueError(
                "data_object and schema_object cannot be simultaneously defined."
            )
        return values


class TransInput(ProcInput, Trans):
    """An input model that serves as an intermediate input object used in converting toolkit data objects
    to MMSchema models."""

    schema_name: str = (
        Field(
            schema_input_default,
            description=f"The specification to which this model conforms. Explicitly fixed as {schema_input_default}.",
        ),
    )
    schema_version: int = Field(
        1,
        description="The version number of ``schema_name`` to which this model conforms.",
    )


class TransOutput(ProcOutput, Trans):
    """An output model that serves as an intermediate output object used in converting toolkit data objects
    to MMSchema models."""

    schema_name: str = (
        Field(
            schema_output_default,
            description=f"The specification to which this model conforms. Explicitly fixed as {schema_output_default}.",
        ),
    )
    schema_version: int = Field(
        1,
        description="The version number of ``schema_name`` to which this model conforms.",
    )
    proc_input: TransInput = Field(
        None, description="Translation procedure input model."
    )
