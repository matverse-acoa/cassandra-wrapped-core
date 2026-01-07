"""MatVerse package root."""

from __future__ import annotations

from typing import Dict, List

__all__ = ["get_system_info"]


def get_system_info() -> Dict[str, object]:
    """Return basic system metadata."""
    return {
        "version": "1.0.0",
        "author": "MatVerse Team",
        "modules": _available_modules(),
    }


def _available_modules() -> List[str]:
    return [
        "core",
        "api",
        "packager",
        "blockchain",
        "ipfs",
    ]
