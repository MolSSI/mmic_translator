from typing import Dict, Any, Optional, List
from mmelemental.models.base import ProtoModel
from pydantic import Field, root_validator

__all__ = ["TransInput", "TransOutput"]


class TransInput(ProtoModel):
    """An input model that serves as an intermediate input object used in converting toolkit data objects
    to MMSchema models."""

    tk_object: Any = Field(None, description="Toolkit data object that stores atoms.")
    tk_units: Optional[Dict[str, str]] = Field(
        None, description="Units for variables stored in tk_object."
    )
    tk_version: Optional[str] = Field(
        None, description="Supported toolkit version. e.g. >= 3.4.0."
    )
    schema_object: Any = Field(None, description="MMSchema data object or model.")
    schema_version: Optional[str] = Field(
        None, description="Supported schema version. e.g. >= 1.2.0."
    )  # we need this? yah, but non-MMSchemas
    kwargs: Optional[Dict[str, Any]] = Field(
        None, description="Additional keyword arguments to pass to the constructors."
    )

    @root_validator
    def _valid_fields(cls, values):
        if values["tk_object"] and values["schema_object"]:
            raise ValueError(
                "tk_object and schema_object cannot be simultaneously defined."
            )
        return values


class TransOutput(TransInput):
    """An output model that serves as an intermediate output object used in converting toolkit data objects
    to MMSchema models."""

    warning: Optional[List[str]] = Field(
        None, description="Warning messages generated from the conversion."
    )
