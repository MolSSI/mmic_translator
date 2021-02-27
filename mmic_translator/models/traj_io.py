from typing import Dict, Any, Optional, List
from mmelemental.models.base import ProtoModel
from mmelemental.models.collect import Trajectory
from pydantic import Field, validator
import parmed

__all__ = ["TrajInToSchema", "TrajInFromSchema", "TrajOutToSchema", "TrajOutFromSchema"]


class TrajInToSchema(ProtoModel):
    """ An input model that serves as an intermediate input object used in converting toolkit data objects
    to MMSchema models. """

    tk_object: Any = Field(..., description="Toolkit data object that stores atoms.")
    tk_units: Optional[Dict[str, str]] = Field(
        None, description="Units for variables stored in tk_object."
    )
    tk_version: str = Field(
        None, description="Supported toolkit version. e.g. >= 3.4.0."
    )
    schema_version: Optional[str] = Field(
        None, description="Supported MMSchema version. e.g. <= 0.1.1."
    )
    kwargs: Optional[Dict[str, Any]] = Field(
        None, description="Additional keyword arguments to pass to the constructors."
    )


class TrajInFromSchema(ProtoModel):
    """ An input model that serves as an intermediate input object used in converting MMSchema models
    to toolkit data objects. """

    schema_object: Trajectory = Field(..., description="MMSchema data object or model.")
    schema_version: Optional[str] = Field(
        None, description="Supported MMSchema version. e.g. <= 0.1.1."
    )
    tk_version: str = Field(
        None, description="Supported toolkit version. e.g. >= 3.4.0."
    )
    kwargs: Optional[Dict[str, Any]] = Field(
        None, description="Additional keyword arguments to pass to the constructors."
    )


class TrajOutToSchema(ProtoModel):
    """ An output model that serves as an intermediate output object used in converting toolkit data objects
    to MMSchema models. """

    schema_object: Trajectory = Field(..., description="MMSchema data object or model.")
    schema_version: Optional[str] = Field(
        None, description="Supported MMSchema version. e.g. <= 0.1.1."
    )
    warning: Optional[List[str]] = Field(
        None, description="Warning messages generated from the conversion."
    )


class TrajOutFromSchema(ProtoModel):
    """ An output model that serves as an intermediate output object used in converting MMSchema models
    to toolkit data objects. """

    tk_object: Any = Field(..., description="Toolkit data object that stores atoms.")
    tk_units: Optional[Dict[str, str]] = Field(
        None, description="Units for variables stored in tk_object."
    )
    tk_version: Optional[str] = Field(
        None, description="Supported toolkit version. e.g. >= 3.4.0."
    )
    warning: Optional[List[str]] = Field(
        None, description="Warning messages generated from the conversion."
    )
