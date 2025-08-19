"""
🧹 Package de nettoyage immobilier
===================================

Package principal pour le nettoyage et l'analyse des données immobilières
"""

__version__ = "1.0.0"
__author__ = "Équipe de nettoyage immobilier"
__description__ = "Système de nettoyage expert pour données immobilières québécoises"

from .core.cleaner import RealEstateDataCleaner
from .core.simple_cleaner import SimpleRealEstateCleaner

__all__ = [
    'RealEstateDataCleaner',
    'SimpleRealEstateCleaner'
]
