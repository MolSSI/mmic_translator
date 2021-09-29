"""
mmic_translator.py
Generic MMSchema translator

Handles the primary functions
"""


__all__ = ["reg_trans"]

reg_trans = {
    "mmic_mda": "mdanalysis",
    "mmic_parmed": "parmed",
    "mmic_qcschema": "qcschema",
    # "mmic_rdkit": "rdkit",
    # "mmic_gmx": "gmx",
}
reg_vers = {}
