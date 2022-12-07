import importlib
from .base import BasePlugin


def get_plugin(name):
    """Get a plugin by name."""
    return importlib.import_module(f"phoenix_framework.server.plugins.{name}.plugin").Plugin()
