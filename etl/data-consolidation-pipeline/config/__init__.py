#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ PACKAGE CONFIGURATION - Pipeline ETL Ultra-Intelligent
==========================================================

Configuration centralisée pour la consolidation maximale des variables
"""

from .consolidation_config import ConsolidationConfig, ConsolidationGroup

__all__ = [
    "ConsolidationConfig",
    "ConsolidationGroup"
]

__version__ = "7.0.0"
__author__ = "Pipeline ETL Ultra-Intelligent Team"
__description__ = "Configuration centralisée pour la consolidation maximale des variables immobilières"
