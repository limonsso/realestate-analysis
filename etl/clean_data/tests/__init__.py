#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 MODULE TESTS - VALIDATION ET INTÉGRATION
============================================

Module de tests pour valider l'implémentation de la stratégie de consolidation avancée
et l'harmonisation avec la configuration personnalisée.

Tests disponibles:
- test_consolidation_strategy.py : Test de la stratégie de consolidation
- test_custom_config_integration.py : Test d'intégration de la config personnalisée
- test_new_features.py : Test des nouvelles fonctionnalités
"""

__version__ = '1.0.0'
__author__ = 'Pipeline Ultra-Intelligent'

# Import des tests pour faciliter l'accès
try:
    from .test_consolidation_strategy import test_consolidation_strategy
    from .test_custom_config_integration import test_custom_config_integration
    from .test_new_features import test_new_features
except ImportError:
    # Les tests peuvent ne pas être disponibles dans tous les environnements
    pass

__all__ = [
    'test_consolidation_strategy',
    'test_custom_config_integration', 
    'test_new_features'
]
