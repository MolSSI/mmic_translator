"""
Unit and regression test for the mmic_translator package.
"""

# Import package, test suite, and other packages as needed
import mmic_translator
import pytest
import sys

def test_mmic_translator_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "mmic_translator" in sys.modules
