#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# Copyright 2022 Valiot. | All Rights Reserved

""" Define the components for filter jobs."""

__author__ = ["alejandro.pasos@valiot.io"]
__all__ = [
    "MovingAverage",
    "ExponentialMovingAverage",
    "Stats"

]

from factoryos_lib.filters._stats import Stats
