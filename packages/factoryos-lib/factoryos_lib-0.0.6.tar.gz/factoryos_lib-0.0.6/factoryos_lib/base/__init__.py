# Copyright 2022 Valiot. | All Rights Reserved

"""Base classes for defining structure of workers."""

__author__ = ["alejandro.pasos@valiot.io"]
__all__ = [
    "Component",
    "Model",
    "Teacher",
    "Trainer",
    "setup_gql",
    "execute_jobs"
]

from factoryos_lib.base._model import Model
