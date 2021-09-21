import importlib
import inspect
import abc
from typing import Optional, Any, Dict
from pydantic import Field, validator
from mmelemental.models.base import ProtoModel

__all__ = ["ToolkitModel"]


class ToolkitModel(ProtoModel, abc.ABC):
    """An abstract base class that acts as a wrapper for toolkit data objects."""

    data: Any = Field(
        ..., description="Toolkit-specific data object."
    )  # validator added in subclasses
    data_units: Optional[Dict] = Field(
        None, description="Units for the stored physical properties in data."
    )

    @classmethod
    @abc.abstractmethod
    def engine(cls):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def dtype(cls):
        """Returns the fundamental data object type."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_file(cls, filename: str = None, dtype: str = None, **kwargs):
        """Constructs a data object from file(s)."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_schema(cls, data: Any, version: Optional[str] = None, **kwargs):
        """Constructs data object from MMSchema."""
        raise NotImplementedError

    @abc.abstractmethod
    def to_file(self, filename: str, dtype: str = None, **kwargs):
        """Writes the data object to a file.
        Parameters
        ----------
        filename : str
            The filename to write to
        dtype : Optional[str], optional
            File format
        **kwargs
            Additional kwargs to pass to the constructors.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_schema(self, version: Optional[str] = None, **kwargs):
        """Converts the data object to MMSchema compliant object.
        Parameters
        ----------
        version: str, optional
            Schema specification version to comply with e.g. 1.0.1.
        **kwargs
            Additional kwargs to pass to the constructor.
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractclassmethod
    def isvalid(cls, data):
        raise NotImplementedError

    @validator("data", allow_reuse=True)
    def valid_data(cls, data):
        return cls.isvalid(data)

    @property
    def toolkit(self) -> str:
        """Returns the path module that defines the data type object."""
        return type(self.data).__module__

    @property
    def translator(self) -> str:
        name, _ = self.__module__.split(".", 1)
        return name

    @property
    def path(self) -> str:
        return self.__module__ + "." + self.__name__

    @property
    def components(self):
        comp_mod = importlib.import_module(self.translator + ".components")
        return inspect.getmembers(comp_mod, inspect.isclass)

    @property
    def models(self):
        mod = importlib.import_module(self.translator + ".models")
        return inspect.getmembers(mod, inspect.isclass)
