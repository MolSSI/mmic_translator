from typing import Dict, Any, Optional
from cmselemental.models.procedures import InputProc, OutputProc
from cmselemental.models.base import ProtoModel
from pydantic import Field, root_validator

__all__ = ["InputTrans", "OutputTrans"]


class InputTrans(InputProc):
    """An input model that serves as an intermediate input object used in converting toolkit data objects
    to MMSchema models."""

    data_object: Any = Field(
        None,
        description="Toolkit-specific data object that stores atoms e.g. MDanalysis.Universe object.",
    )
    data_units: Optional[Dict[str, str]] = Field(
        None, description="Units for variables stored in data_object."
    )
    schema_object: Any = Field(None, description="MMSchema data object or model.")

    schema_name: str = Field(
        ...,
        description=f"The specification to which this model conforms.",
    )
    schema_version: int = Field(
        ...,
        description="The version number of ``schema_name`` to which this model conforms.",
    )

    @root_validator
    def _valid_trans_fields(cls, values):
        if values["data_object"] and values["schema_object"]:
            raise ValueError(
                "data_object and schema_object cannot be simultaneously defined."
            )
        return values


class OutputTrans(OutputProc):
    """An output model that serves as an intermediate output object used in converting toolkit data objects
    to MMSchema models."""

    data_object: Any = Field(
        None,
        description="Toolkit-specific data object that stores atoms e.g. MDanalysis.Universe object.",
    )
    data_units: Optional[Dict[str, str]] = Field(
        None, description="Units for variables stored in data_object."
    )
    schema_object: Any = Field(None, description="MMSchema data object or model.")

    schema_name: str = Field(
        ...,
        description=f"The specification to which this model conforms.",
    )
    schema_version: int = Field(
        ...,
        description="The version number of ``schema_name`` to which this model conforms.",
    )
    proc_input: InputTrans = Field(
        None, description="Translation procedure input model."
    )

    @root_validator
    def _valid_trans_fields(cls, values):
        if values["data_object"] and values["schema_object"]:
            raise ValueError(
                "data_object and schema_object cannot be simultaneously defined."
            )
        return values
