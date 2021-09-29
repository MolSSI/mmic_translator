from mmic.components.blueprints import StrategyComponent
from cmselemental.util.decorators import classproperty
from ..mmic_translator import reg_trans
from ..models import InputTrans, OutputTrans
from typing import Dict, Any, List, Union, Set, Optional
import importlib

__all__ = ["TransComponent"]


class TransComponent(StrategyComponent):
    """An abstract template component that provides methods for converting between MMSchema and other MM codes."""

    @classproperty
    def input(cls):
        return InputTrans

    @classproperty
    def output(cls):
        return OutputTrans

    @classproperty
    def version(cls) -> str:
        """Finds program, extracts version, returns normalized version string.

        Returns
        -------
        str
            Return a valid, safe python version string.
        """
        ...

    @classproperty
    def tactic_comps(cls) -> Set[str]:
        """Returns the supported tactic components e.g. set(['mmic_mda',...]).

        Returns
        -------
        Set[str]

        """
        return set(reg_trans)

    @staticmethod
    def installed_comps(trans: Optional[Set[str]] = set(reg_trans)) -> Set[str]:
        """Returns module spec if it exists.

        Parameters
        ----------
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        List[str]
            Translator names that are installed.

        """
        return set([spec for spec in trans if importlib.util.find_spec(spec)])

    @staticmethod
    def installed_comps_model(
        model: str, trans: Optional[Set[str]] = set(reg_trans)
    ) -> Set[str]:
        """Returns module spec if it exists and supports a specific model.

        Parameters
        ----------
        model: str
            Model name e.g. Molecule, ForceField, ...
        trans: Optional[Tuple[str]], optional
            Supported Molecule translator names to check.

        Returns
        -------
        List[str]
            Molecule Translator names that are installed.

        """
        ins_comps = TransComponent.installed_comps(trans)
        return set(
            [
                tname
                for tname in ins_comps
                if importlib.import_module(tname)._classes_map.get(model)
            ]
        )

    @staticmethod
    def get_dtype(tname: str, trans: Optional[Dict[str, str]] = reg_trans):
        if tname not in trans:
            raise KeyError(
                f"{tname} not found in the following available translators: {trans}."
            )
        return trans[tname]

    # Trans-specific methods
    @staticmethod
    def find_trans(dtype: str, trans: Optional[Dict[str, str]] = reg_trans) -> str:
        """Returns mmic_translator name (if any) corresponding to a specific data type.
        If no appropriate toolkit is available on the system, this method raises an error.

        Parameters
        ----------
        dtype: str
            Data type e.g. MDAnalysis, parmed, etc.
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        str
            Translator name e.g. mmic_parmed

        """
        for trans, tk in trans.items():
            if dtype == tk:
                return trans

        raise ValueError(f"Could not find appropriate toolkit for {dtype} object.")

    ################################################################
    ###################### Molecule extension maps #################

    @staticmethod
    def find_molread_ext_maps(
        trans: Optional[Set[str]] = set(reg_trans),
    ) -> Dict[str, Dict]:
        """Finds a Dict of molecule translators and the file formats they support reading.

        Parameters
        ----------
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        Dict
            Dictionary of mmic_translators and molecule files they can read.

        """
        trans_mod = (
            importlib.import_module(mod)
            for mod in TransComponent.installed_comps(trans)
        )
        return {
            mod.__name__: mod.molread_ext_maps
            for mod in trans_mod
            if hasattr(mod, "molread_ext_maps")
        }

    @staticmethod
    def find_molread_tk(
        dtype: str, trans: Optional[Set[str]] = set(reg_trans)
    ) -> Union[str, None]:
        """Finds an appropriate translator for reading a specific molecule object.

        Parameters
        ----------
        dtype: str
            Data type object e.g. gro, pdb, etc.
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        str or None
            Translator name e.g. mmic_mda

        """
        extension_maps = TransComponent.find_molread_ext_maps(trans)
        for toolkit in extension_maps:
            if extension_maps[toolkit].get(dtype):
                if importlib.util.find_spec(toolkit):
                    return toolkit
        return None

    @staticmethod
    def find_molwrite_ext_maps(
        trans: Optional[Set[str]] = set(reg_trans),
    ) -> Dict[str, Dict]:
        """Returns a Dict of molecule translators and the file formats they can write.

        Parameters
        ----------
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        Dict[str, Dict]
            A dictionary of molecule translators: dictionary file formats they can write.

        """
        trans_mod = (
            importlib.import_module(mod)
            for mod in TransComponent.installed_comps(trans)
        )
        return {
            mod.__name__: mod.molwrite_ext_maps
            for mod in trans_mod
            if hasattr(mod, "molwrite_ext_maps")
        }

    @staticmethod
    def find_molwrite_tk(
        dtype: str, trans: Optional[Set[str]] = set(reg_trans)
    ) -> Union[str, None]:
        """Finds an appropriate translator for writing a specific molecule object.

        Parameters
        ----------
        dtype: str
            Data type object e.g. gro, pdb, etc.
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        str or None
            Translator name e.g. mmic_mda

        """
        extension_maps = TransComponent.find_molwrite_ext_maps(trans)
        for toolkit in extension_maps:
            if extension_maps[toolkit].get(dtype):
                if importlib.util.find_spec(toolkit):
                    return toolkit
        return None

    ################################################################
    #################### ForceField extension maps #################

    @staticmethod
    def find_ffread_ext_maps(
        trans: Optional[Set[str]] = set(reg_trans),
    ) -> Dict[str, Dict]:
        """Finds a Dict of forcefield translators and the file formats they support reading.

        Parameters
        ----------
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        Dict[str, Dict]
            Dictionary of mmic_translators: dictionary of forcefield file formats they can read.

        """
        trans_mod = (
            importlib.import_module(mod)
            for mod in TransComponent.installed_comps(trans)
        )
        return {
            mod.__name__: mod.ffread_ext_maps
            for mod in trans_mod
            if hasattr(mod, "ffread_ext_maps")
        }

    @staticmethod
    def find_ffread_tk(
        dtype: str, trans: Optional[Set[str]] = set(reg_trans)
    ) -> Union[str, None]:
        """Finds an appropriate translator for reading a specific forcefield object.

        Parameters
        ----------
        dtype: str
            Data type object e.g. gro, pdb, etc.
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        str or None
            Translator name e.g. mmic_mda

        """
        extension_maps = TransComponent.find_ffread_ext_maps(trans)
        for toolkit in extension_maps:
            if extension_maps[toolkit].get(dtype):
                if importlib.util.find_spec(toolkit):
                    return toolkit
        return None

    @staticmethod
    def find_ffwrite_ext_maps(
        trans: Optional[Set[str]] = set(reg_trans),
    ) -> Dict[str, Dict]:
        """
        Finds a Dict of forcefield translators and the file formats they can write.

        Parameters
        ----------
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        Dict[str, Dict]
            A dictionary of forcefield translators: dictionary of forcefield file formats they can write.

        """
        trans_mod = (
            importlib.import_module(mod)
            for mod in TransComponent.installed_comps(trans)
        )
        return {
            mod.__name__: mod.ffwrite_ext_maps
            for mod in trans_mod
            if hasattr(mod, "ffwrite_ext_maps")
        }

    @staticmethod
    def find_ffwrite_tk(
        dtype: str, trans: Optional[Set[str]] = set(reg_trans)
    ) -> Union[str, None]:
        """Finds an appropriate translator for writing a specific forcefield object.

        Parameters
        ----------
        dtype: str
            Data type object e.g. gro, pdb, etc.
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        str or None
            Translator name e.g. mmic_mda

        """
        extension_maps = TransComponent.find_ffwrite_ext_maps(trans)
        for toolkit in extension_maps:
            if extension_maps[toolkit].get(dtype):
                if importlib.util.find_spec(toolkit):
                    return toolkit
        return None

    ################################################################
    #################### Trajectory extension maps #################

    @staticmethod
    def find_trajread_ext_maps(
        trans: Optional[Set[str]] = set(reg_trans),
    ) -> Dict[str, Dict]:
        """Finds a Dict of trajectory translators and the file formats they support reading.

        Parameters
        ----------
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        Dict[str, Dict]
            Dictionary of mmic_translators: dictionary of trajectory file formats they can read.

        """
        trans_mod = (
            importlib.import_module(mod)
            for mod in TransComponent.installed_comps(trans)
        )
        return {
            mod.__name__: mod.trajread_ext_maps
            for mod in trans_mod
            if hasattr(mod, "trajread_ext_maps")
        }

    @staticmethod
    def find_trajread_tk(
        dtype: str, trans: Optional[Set[str]] = set(reg_trans)
    ) -> Union[str, None]:
        """Finds an appropriate translator for reading a specific trajectory object.

        Parameters
        ----------
        dtype: str
            Data type object e.g. gro, dcd, etc.
        trans: Tuple[str], optional
            Supported translator names to check.

        Returns
        -------
        str or None
            Translator name e.g. mmic_mda

        """
        extension_maps = TransComponent.find_trajread_ext_maps(trans)
        for toolkit in extension_maps:
            if extension_maps[toolkit].get(dtype):
                if importlib.util.find_spec(toolkit):
                    return toolkit
        return None

    @staticmethod
    def find_trajwrite_ext_maps(
        trans: Optional[Set[str]] = set(reg_trans),
    ) -> Dict[str, Dict]:
        """
        Finds a dict of trajectory translators and the file formats they can write.

        Parameters
        ----------
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        Dict[str, Dict]
            A dictionary of trajectory translators: dictionary oftrajectory file formats they can write.

        """
        trans_mod = (
            importlib.import_module(mod)
            for mod in TransComponent.installed_comps(trans)
        )
        return {
            mod.__name__: mod.ffwrite_ext_maps
            for mod in trans_mod
            if hasattr(mod, "trajwrite_ext_maps")
        }

    @staticmethod
    def find_trajwrite_tk(
        dtype: str, trans: Optional[Set[str]] = set(reg_trans)
    ) -> Union[str, None]:
        """Finds an appropriate translator for writing a specific trajectory object.

        Parameters
        ----------
        dtype: str
            Data type object e.g. trr, dcd, tng, etc.
        trans: Optional[Tuple[str]], optional
            Supported translator names to check.

        Returns
        -------
        str or None
            Translator name e.g. mmic_mda

        """
        extension_maps = TransComponent.find_trajwrite_ext_maps(trans)
        for toolkit in extension_maps:
            if extension_maps[toolkit].get(dtype):
                if importlib.util.find_spec(toolkit):
                    return toolkit
        return None
