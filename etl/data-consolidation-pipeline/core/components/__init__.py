#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 COMPOSANTS DU PIPELINE - Module d'initialisation
===================================================

Export de tous les composants spécialisés du pipeline ETL
"""

# === COMPOSANTS PRINCIPAUX ===
from .data_extractor import DataExtractor
from .data_consolidator import DataConsolidator
from .data_cleaner import DataCleaner
from .data_enricher import DataEnricher
from .data_validator import DataValidator
from .pipeline_orchestrator import PipelineOrchestrator

# === ORCHESTRATEUR PRINCIPAL ===
# Import supprimé pour éviter l'import circulaire
# MainPipelineOrchestrator est disponible directement depuis core.main_pipeline_orchestrator

# === VERSION ET MÉTADONNÉES ===
__version__ = "7.0.0"
__author__ = "Pipeline Ultra-Intelligent Team"
__description__ = "Composants modulaires pour le pipeline de consolidation de données"

# === LISTE DES COMPOSANTS DISPONIBLES ===
__all__ = [
    'DataExtractor',
    'DataConsolidator', 
    'DataCleaner',
    'DataEnricher',
    'DataValidator',
    'PipelineOrchestrator'
]

# === DOCUMENTATION DES COMPOSANTS ===
COMPONENTS_DOC = {
    'DataExtractor': {
        'description': 'Extraction de données depuis différentes sources',
        'responsability': 'Extraction MongoDB, CSV, JSON, datasets de test',
        'key_methods': ['extract_data', 'validate_extracted_data']
    },
    'DataConsolidator': {
        'description': 'Consolidation intelligente des variables similaires',
        'responsability': 'Regroupement et fusion des colonnes selon la configuration',
        'key_methods': ['consolidate_variables', 'calculate_column_quality']
    },
    'DataCleaner': {
        'description': 'Nettoyage et validation des données',
        'responsability': 'Gestion des valeurs manquantes, outliers, normalisation',
        'key_methods': ['clean_data', 'validate_data_quality']
    },
    'DataEnricher': {
        'description': 'Enrichissement avec métriques dérivées',
        'responsability': 'Calculs financiers, géographiques, scores d\'opportunité',
        'key_methods': ['enrich_data', 'get_enriched_columns']
    },
    'DataValidator': {
        'description': 'Validation complète de la qualité des données',
        'responsability': 'Validation métier, cohérence, génération de rapports',
        'key_methods': ['validate_data', 'generate_validation_report']
    },
    'PipelineOrchestrator': {
        'description': 'Orchestration principale du pipeline ETL',
        'responsability': 'Coordination de tous les composants et phases',
        'key_methods': ['run_complete_pipeline', 'get_pipeline_stats']
    },
    # MainPipelineOrchestrator supprimé pour éviter l'import circulaire
}

def get_component_info(component_name: str = None) -> dict:
    """
    Retourne les informations sur les composants
    
    Args:
        component_name: Nom du composant (optionnel)
        
    Returns:
        Dict avec les informations des composants
    """
    if component_name:
        return COMPONENTS_DOC.get(component_name, {})
    return COMPONENTS_DOC

def list_available_components() -> list:
    """
    Liste tous les composants disponibles
    
    Returns:
        Liste des noms des composants
    """
    return list(COMPONENTS_DOC.keys())

def get_component_responsibilities() -> dict:
    """
    Retourne les responsabilités de chaque composant
    
    Returns:
        Dict composant -> responsabilité
    """
    return {name: info['responsability'] for name, info in COMPONENTS_DOC.items()}
