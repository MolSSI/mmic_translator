from typing import Dict, Any, Optional, List
from mmelemental.models.proc import ProcInput, ProcOutput
from mmelemental.models.base import ProtoModel
from pydantic import Field, root_validator

__all__ = ["TransInput", "TransOutput"]


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

    ...


class TransOutput(ProcOutput, Trans):
    """An output model that serves as an intermediate output object used in converting toolkit data objects
    to MMSchema models."""

    trans_input: TransInput
