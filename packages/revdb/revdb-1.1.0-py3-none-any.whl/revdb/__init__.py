"""a light layer for revtel mongodb"""

__version__ = "1.1.0"

from revdb.db import (
    Model,
    StrictModel,
    collection_factory,
    connect,
    make_model_class,
    offline_database,
)

__all__ = [
    "make_model_class",
    "connect",
    "Model",
    "StrictModel",
    "collection_factory",
    "offline_database",
]
