import pkgutil
import importlib
import sys

from .base import Base

def _import_submodules(package_name: str) -> None:
    pkg = sys.modules[package_name]
    
    for _, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
        if name.endswith(".base"):
            continue
        importlib.import_module(name)
        if ispkg:
            _import_submodules(name)


_import_submodules(__name__)

__all__ = ["Base"]