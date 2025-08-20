#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎼 PACKAGE CORE - Pipeline ETL Modulaire
=========================================

Modules principaux du pipeline de consolidation modulaire
"""

from .pipeline_manager import PipelineManager
from .data_processor import DataProcessor
from .export_manager import ExportManager
from .report_generator import ReportGenerator
from .config_manager import ConfigManager

__all__ = [
    "PipelineManager",
    "DataProcessor", 
    "ExportManager",
    "ReportGenerator",
    "ConfigManager"
]

__version__ = "7.0.0"
__author__ = "Pipeline ETL Modulaire Team"
__description__ = "Modules principaux du pipeline ETL modulaire unifié"
