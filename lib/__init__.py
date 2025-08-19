"""
Package d'analyse immobilière
Système modulaire pour l'analyse et la sélection de variables
"""

# Imports des composants principaux
from .property_analysis import (
    PropertyAnalyzer,
    PropertyDataProcessor,
    PropertyClassifier,
    FeatureSelector,
    DataValidator
)

from .interfaces import (
    IDataProcessor,
    IPropertyClassifier,
    IFeatureSelector
)

from .property_type_normalizer import PropertyTypeNormalizer
from .mongodb_loader import MongoDBLoader

# Version du package
__version__ = "2.0.0"

# Description
__description__ = "Système d'analyse immobilière modulaire avec sélection de variables"

# Auteur
__author__ = "Assistant IA"

# Classes exposées
__all__ = [
    'PropertyAnalyzer',
    'PropertyDataProcessor',
    'PropertyClassifier', 
    'FeatureSelector',
    'DataValidator',
    'IDataProcessor',
    'IPropertyClassifier',
    'IFeatureSelector',
    'PropertyTypeNormalizer',
    'MongoDBLoader'
] 