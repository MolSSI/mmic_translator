from typing import Dict, Any, Optional, List
from mmelemental.models.proc import ProcInput, ProcOutput
from pydantic import Field, root_validator

__all__ = ["TransInput", "TransOutput"]


class TransInput(ProcInput):
    """An input model that serves as an intermediate input object used in converting toolkit data objects
    to MMSchema models."""

    tk_object: Any = Field(
        None, 
        description="Toolkit data object that stores atoms e.g. MDanalysis.Universe object."
    )
    tk_units: Optional[Dict[str, str]] = Field(
        None, description="Units for variables stored in tk_object."
    )
    schema_object: Any = Field(None, description="MMSchema data object or model.")


    @root_validator
    def _valid_fields(cls, values):
        if values["tk_object"] and values["schema_object"]:
            raise ValueError(
                "tk_object and schema_object cannot be simultaneously defined."
            )
        return values


class TransOutput(ProcOutput):
    """An output model that serves as an intermediate output object used in converting toolkit data objects
    to MMSchema models."""

    tk_object: Any = Field(
        None, 
        description="Toolkit data object that stores atoms e.g. MDanalysis.Universe object."
    )
    tk_units: Optional[Dict[str, str]] = Field(
        None, description="Units for variables stored in tk_object."
    )
    schema_object: Any = Field(None, description="MMSchema data object or model.")


