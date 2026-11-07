"""Vendored text normaliser (upstream commit fe5e6ec).

The modules in this directory are byte-identical copies of the source (see maya3/text/README.md); only this
__init__.py was added so they import as a package.  Use mithi_tts.text_norm.normalise_text rather than this package directly.
"""
from .normalize import NormalizationError, normalize, resolve_language  # noqa: F401
