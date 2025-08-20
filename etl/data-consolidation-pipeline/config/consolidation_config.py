#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ CONFIGURATION CENTRALE - CONSOLIDATION MAXIMALE DES VARIABLES
===============================================================

Configuration complète pour le pipeline ETL ultra-intelligent
Basé sur les spécifications du real_estate_prompt.md
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ConsolidationGroup:
    """Configuration d'un groupe de consolidation"""
    name: str
    final_column: str
    source_columns: List[str]
    description: str
    priority: int  # 1 = critique, 2 = important, 3 = optionnel
    data_type: str
    validation_rules: List[str]
    unit_conversion: Optional[Dict[str, float]] = None
    outlier_thresholds: Optional[Dict[str, float]] = None

class ConsolidationConfig:
    """
    Configuration centralisée pour la consolidation maximale
    Respecte exactement les spécifications du real_estate_prompt.md
    """
    
    # === VERSION ET MISSION ===
    PIPELINE_VERSION = "7.0.0_ultra_intelligent"
    MISSION = "consolidation_maximale_variables_similaires"
    OBJECTIVE = "50_plus_to_20_25_columns"
    
    # === SEUILS DE PERFORMANCE ===
    TARGET_REDUCTION_PERCENTAGE = 65  # 50+ → 20-25 colonnes
    MIN_VALUES_RECOVERED_PERCENTAGE = 40  # +40% de données récupérées
    TARGET_PERFORMANCE_IMPROVEMENT = 5  # 5x plus rapide
    
    # === GROUPES DE CONSOLIDATION (25+ comme spécifié) ===
    CONSOLIDATION_GROUPS = [
        # === GROUPE 1: PRIX ===
        ConsolidationGroup(
            name="Prix",
            final_column="price_final",
            source_columns=[
                "price", "prix_evaluation", "prix", "valeur", "montant", "asking_price", 
                "list_price", "sale_price", "price_assessment"
            ],
            description="Prix de la propriété (toutes variantes)",
            priority=1,
            data_type="numeric",
            validation_rules=["positive", "reasonable_range", "no_outliers"],
            outlier_thresholds={"z_score": 3.0, "iqr_multiplier": 1.5}
        ),
        
        # === GROUPE 2: SURFACE ===
        ConsolidationGroup(
            name="Surface",
            final_column="surface_final",
            source_columns=[
                "surface", "living_area", "superficie", "area", "floor_area", 
                "sqft", "m2", "square_feet", "square_meters", "footage"
            ],
            description="Surface/superficie (toutes unités)",
            priority=1,
            data_type="numeric",
            validation_rules=["positive", "unit_conversion", "geometric_coherence"],
            unit_conversion={"sqft": 0.092903, "m2": 1.0, "square_feet": 0.092903}
        ),
        
        # === GROUPE 3: CHAMBRES ===
        ConsolidationGroup(
            name="Chambres",
            final_column="bedrooms_final",
            source_columns=[
                "bedrooms", "nb_bedroom", "nbr_chanbres", "rooms", "chambres",
                "bed", "br", "room", "number_bedrooms"
            ],
            description="Nombre de chambres",
            priority=1,
            data_type="numeric",
            validation_rules=["non_negative", "reasonable_range", "integer"]
        ),
        
        # === GROUPE 4: SALLES DE BAIN ===
        ConsolidationGroup(
            name="Salles de bain",
            final_column="bathrooms_final",
            source_columns=[
                "bathrooms", "nb_bathroom", "nbr_sal_bain", "salle_bain",
                "bath", "ba", "toilet", "wc", "number_bathrooms"
            ],
            description="Nombre de salles de bain",
            priority=1,
            data_type="numeric",
            validation_rules=["non_negative", "reasonable_range", "integer"]
        ),
        
        # === GROUPE 5: SALLES D'EAU ===
        ConsolidationGroup(
            name="Salles d'eau",
            final_column="water_rooms_final",
            source_columns=[
                "water_rooms", "nbr_sal_deau", "nb_water_room", "salle_eau",
                "water", "wc", "toilet"
            ],
            description="Nombre de salles d'eau",
            priority=2,
            data_type="numeric",
            validation_rules=["non_negative", "reasonable_range", "integer"]
        ),
        
        # === GROUPE 6: LATITUDE ===
        ConsolidationGroup(
            name="Latitude",
            final_column="latitude_final",
            source_columns=[
                "latitude", "lat", "lat_", "lat_property", "lat_coord"
            ],
            description="Latitude de la propriété",
            priority=1,
            data_type="numeric",
            validation_rules=["geographic_bounds", "precision_validation"]
        ),
        
        # === GROUPE 7: LONGITUDE ===
        ConsolidationGroup(
            name="Longitude",
            final_column="longitude_final",
            source_columns=[
                "longitude", "lng", "long", "lon", "lng_", "lng_property", "lng_coord"
            ],
            description="Longitude de la propriété",
            priority=1,
            data_type="numeric",
            validation_rules=["geographic_bounds", "precision_validation"]
        ),
        
        # === GROUPE 8: GÉOLOCALISATION ===
        ConsolidationGroup(
            name="Géolocalisation",
            final_column="geolocation_final",
            source_columns=[
                "location", "geolocation", "geo", "coordinates", "coord"
            ],
            description="Informations de géolocalisation",
            priority=2,
            data_type="mixed",
            validation_rules=["geographic_consistency", "format_validation"]
        ),
        
        # === GROUPE 9: ADRESSES ===
        ConsolidationGroup(
            name="Adresses",
            final_column="address_final",
            source_columns=[
                "address", "full_address", "adresse", "street", "rue", "addr",
                "complete_address"
            ],
            description="Adresse complète de la propriété",
            priority=1,
            data_type="categorical",
            validation_rules=["not_null", "format_validation", "geographic_consistency"]
        ),
        
        # === GROUPE 10: DATE CRÉATION ===
        ConsolidationGroup(
            name="Date création",
            final_column="date_created_final",
            source_columns=[
                "add_date", "created_at", "creation_date", "listing_date"
            ],
            description="Date de création/ajout de l'annonce",
            priority=2,
            data_type="datetime",
            validation_rules=["date_format", "chronological_consistency"]
        ),
        
        # === GROUPE 11: DATE MISE À JOUR ===
        ConsolidationGroup(
            name="Date mise à jour",
            final_column="date_updated_final",
            source_columns=[
                "updated_at", "update_at", "modified_at", "last_update"
            ],
            description="Date de dernière mise à jour",
            priority=2,
            data_type="datetime",
            validation_rules=["date_format", "chronological_consistency"]
        ),
        
        # === GROUPE 12: ANNÉE CONSTRUCTION ===
        ConsolidationGroup(
            name="Année construction",
            final_column="year_built_final",
            source_columns=[
                "construction_year", "year_built", "annee", "annee_construction",
                "built_year", "construction_date"
            ],
            description="Année de construction du bâtiment",
            priority=1,
            data_type="numeric",
            validation_rules=["year_range", "logical_consistency"]
        ),
        
        # === GROUPE 13: TAXES MUNICIPALES ===
        ConsolidationGroup(
            name="Taxes municipales",
            final_column="tax_municipal_final",
            source_columns=[
                "municipal_tax", "municipal_taxes", "taxe_municipale",
                "city_tax", "property_tax"
            ],
            description="Taxes municipales",
            priority=1,
            data_type="numeric",
            validation_rules=["non_negative", "reasonable_range", "no_outliers"]
        ),
        
        # === GROUPE 14: TAXES SCOLAIRES ===
        ConsolidationGroup(
            name="Taxes scolaires",
            final_column="tax_school_final",
            source_columns=[
                "school_tax", "school_taxes", "taxe_scolaire",
                "education_tax", "school_district_tax"
            ],
            description="Taxes scolaires",
            priority=1,
            data_type="numeric",
            validation_rules=["non_negative", "reasonable_range", "no_outliers"]
        ),
        
        # === GROUPE 15: REVENUS ===
        ConsolidationGroup(
            name="Revenus",
            final_column="revenue_final",
            source_columns=[
                "revenu", "plex-revenue", "plex-revenu", "plex_revenu",
                "potential_gross_revenue", "revenus_annuels_bruts", "income",
                "rental_income", "gross_revenue"
            ],
            description="Revenus locatifs et revenus potentiels",
            priority=1,
            data_type="numeric",
            validation_rules=["non_negative", "reasonable_range", "no_outliers"]
        ),
        
        # === GROUPE 16: IMAGES ===
        ConsolidationGroup(
            name="Images",
            final_column="images_final",
            source_columns=[
                "image", "img_src", "images", "photo", "photos", "picture"
            ],
            description="Images et photos de la propriété",
            priority=3,
            data_type="categorical",
            validation_rules=["url_validation", "format_validation"]
        ),
        
        # === GROUPE 17: ÉVALUATION TOTALE ===
        ConsolidationGroup(
            name="Évaluation totale",
            final_column="evaluation_total_final",
            source_columns=[
                "price_assessment", "evaluation_total", "municipal_evaluation_total",
                "assessed_value", "total_evaluation"
            ],
            description="Évaluation totale de la propriété",
            priority=1,
            data_type="numeric",
            validation_rules=["positive", "reasonable_range", "no_outliers"]
        ),
        
        # === GROUPE 18: ÉVALUATION BÂTIMENT ===
        ConsolidationGroup(
            name="Évaluation bâtiment",
            final_column="evaluation_building_final",
            source_columns=[
                "evaluation_batiment", "municipal_evaluation_building",
                "building_evaluation", "structure_value"
            ],
            description="Évaluation du bâtiment",
            priority=2,
            data_type="numeric",
            validation_rules=["positive", "reasonable_range", "no_outliers"]
        ),
        
        # === GROUPE 19: ÉVALUATION TERRAIN ===
        ConsolidationGroup(
            name="Évaluation terrain",
            final_column="evaluation_land_final",
            source_columns=[
                "evaluation_terrain", "municipal_evaluation_land",
                "land_evaluation", "land_value"
            ],
            description="Évaluation du terrain",
            priority=2,
            data_type="numeric",
            validation_rules=["positive", "reasonable_range", "no_outliers"]
        ),
        
        # === GROUPE 20: ANNÉE ÉVALUATION ===
        ConsolidationGroup(
            name="Année évaluation",
            final_column="evaluation_year_final",
            source_columns=[
                "evaluation_year", "municipal_evaluation_year",
                "assessment_year", "evaluation_date"
            ],
            description="Année de l'évaluation municipale",
            priority=2,
            data_type="numeric",
            validation_rules=["year_range", "logical_consistency"]
        ),
        
        # === GROUPE 21: PARKING TOTAL ===
        ConsolidationGroup(
            name="Parking total",
            final_column="parking_total_final",
            source_columns=[
                "parking", "nb_parking", "nb_garage", "parking_spaces",
                "garage_spaces", "car_spaces"
            ],
            description="Nombre total de places de stationnement",
            priority=2,
            data_type="numeric",
            validation_rules=["non_negative", "reasonable_range", "integer"]
        ),
        
        # === GROUPE 22: UNITÉS ===
        ConsolidationGroup(
            name="Unités",
            final_column="units_final",
            source_columns=[
                "unites", "residential_units", "commercial_units",
                "nb_unit", "units", "apartments"
            ],
            description="Nombre d'unités résidentielles/commerciales",
            priority=2,
            data_type="numeric",
            validation_rules=["positive", "reasonable_range", "integer"]
        ),
        
        # === GROUPE 23: DÉPENSES ===
        ConsolidationGroup(
            name="Dépenses",
            final_column="expenses_final",
            source_columns=[
                "depenses", "expense", "expenses", "costs", "operating_costs"
            ],
            description="Dépenses et coûts d'exploitation",
            priority=2,
            data_type="numeric",
            validation_rules=["non_negative", "reasonable_range", "no_outliers"]
        ),
        
        # === GROUPE 24: PÉRIODE REVENUS ===
        ConsolidationGroup(
            name="Période revenus",
            final_column="period_final",
            source_columns=[
                "revenu_period", "expense_period", "period", "frequency",
                "revenue_frequency", "expense_frequency"
            ],
            description="Période des revenus et dépenses",
            priority=3,
            data_type="categorical",
            validation_rules=["period_validation", "consistency_check"]
        ),
        
        # === GROUPE 25: STYLE BÂTIMENT ===
        ConsolidationGroup(
            name="Style bâtiment",
            final_column="building_style_final",
            source_columns=[
                "building_style", "style", "architecture", "architectural_style"
            ],
            description="Style architectural du bâtiment",
            priority=3,
            data_type="categorical",
            validation_rules=["style_validation", "consistency_check"]
        ),
        
        # === GROUPE 26: TAXES CONSOLIDÉES ===
        ConsolidationGroup(
            name="Taxes consolidées",
            final_column="taxes_other_final",
            source_columns=[
                "taxes", "other_taxes", "additional_taxes", "total_taxes"
            ],
            description="Autres taxes et taxes consolidées",
            priority=2,
            data_type="numeric",
            validation_rules=["non_negative", "reasonable_range", "no_outliers"]
        ),
        
        # === GROUPE 27: CODE POSTAL ===
        ConsolidationGroup(
            name="Code postal",
            final_column="postal_code_final",
            source_columns=[
                "postal_code", "zip_code", "code_postal", "zip"
            ],
            description="Code postal de la propriété",
            priority=2,
            data_type="categorical",
            validation_rules=["postal_code_format", "geographic_consistency"]
        ),
        
        # === GROUPE 28: TAILLE TERRAIN ===
        ConsolidationGroup(
            name="Taille terrain",
            final_column="lot_size_final",
            source_columns=[
                "lot_size", "taille_terrain", "land_size", "plot_size",
                "acreage", "land_area"
            ],
            description="Taille du terrain",
            priority=2,
            data_type="numeric",
            validation_rules=["positive", "reasonable_range", "geometric_coherence"]
        ),
        
        # === GROUPE 29: SOUS-SOL ===
        ConsolidationGroup(
            name="Sous-sol",
            final_column="basement_final",
            source_columns=[
                "basement", "sous_sol", "cave", "cellar"
            ],
            description="Présence et type de sous-sol",
            priority=3,
            data_type="categorical",
            validation_rules=["basement_validation", "consistency_check"]
        ),
        
        # === GROUPE 30: TYPE PROPRIÉTÉ ===
        ConsolidationGroup(
            name="Type propriété",
            final_column="property_type_final",
            source_columns=[
                "type", "property_type", "type_propriete", "category",
                "property_category", "building_type"
            ],
            description="Type de propriété",
            priority=1,
            data_type="categorical",
            validation_rules=["type_validation", "consistency_check"]
        )
    ]
    
    # === COLONNES À SUPPRIMER (MÉTADONNÉES ET UTILITAIRES) ===
    COLUMNS_TO_REMOVE = [
        # Métadonnées d'extraction
        "extraction_metadata", "metadata_extraction", "data_metadata",
        "source_metadata", "extraction_info", "metadata",
        
        # Versions et utilitaires
        "version", "version_donnees", "data_version", "schema_version",
        "extraction_version", "pipeline_version", "data_version",
        
        # Liens et URLs
        "link", "lien", "url", "website", "listing_url",
        "property_url", "detail_url", "href",
        
        # Entreprises et agences
        "company", "entreprise", "agency", "agence", "broker",
        "real_estate_company", "property_company", "listing_company",
        
        # Champs de test et temporaires
        "test_field", "temp_field", "dummy_field", "placeholder"
    ]
    
    # === RÈGLES DE VALIDATION AVANCÉES ===
    VALIDATION_RULES = {
        "geographic_bounds": {
            "latitude": {"min": 45.0, "max": 75.0},  # Québec approximatif
            "longitude": {"min": -80.0, "max": -50.0}
        },
        "reasonable_range": {
            "price": {"min": 50000, "max": 10000000},  # 50k à 10M
            "surface": {"min": 20, "max": 10000},      # 20 à 10k m²
            "bedrooms": {"min": 0, "max": 20},         # 0 à 20 chambres
            "bathrooms": {"min": 0, "max": 15},        # 0 à 15 salles de bain
            "year_built": {"min": 1800, "max": 2030}   # 1800 à 2030
        },
        "unit_conversion": {
            "sqft_to_m2": 0.092903,
            "m2_to_sqft": 10.7639,
            "acres_to_m2": 4046.86
        }
    }
    
    # === RÈGLES MÉTIER ===
    BUSINESS_RULES = {
        "price_range": (10000, 10000000),      # Prix en dollars
        "surface_range": (20, 10000),          # Surface en m²
        "bedrooms_range": (0, 20),             # Nombre de chambres
        "bathrooms_range": (0, 20),            # Nombre de salles de bain
        "year_range": (1900, 2025),            # Année de construction
        "quebec_coordinates": {                 # Limites Québec
            "lat_min": 45.0, "lat_max": 63.0,
            "lng_min": -80.0, "lng_max": -57.0
        }
    }
    
    # === SEUILS DE QUALITÉ ===
    QUALITY_THRESHOLDS = {
        "global_score": 80.0,        # Score global minimum
        "type_consistency": 85.0,    # Cohérence des types
        "value_validity": 90.0,      # Validité des valeurs
        "geographic_validation": 95.0, # Validation géographique
        "business_rules": 88.0       # Règles métier
    }
    
    # === OPTIMISATIONS ===
    OPTIMIZATIONS = {
        "memory_optimization": True,
        "type_optimization": True,
        "parallel_processing": True,
        "jit_compilation": False,
        "chunked_processing": True,
        "categorization": True,
        "advanced_algorithms": True
    }
    
    # === CONFIGURATION GÉOSPATIALE ===
    GEOGRAPHIC_BOUNDS = {
        "latitude": {"min": 45.0, "max": 47.5},  # Québec
        "longitude": {"min": -74.5, "max": -71.0}
    }
    
    # === CONFIGURATION PERFORMANCE ===
    PERFORMANCE_CONFIG = {
        "chunk_size": 10000,  # Taille des chunks pour gros datasets
        "parallel_workers": 4,  # Nombre de workers parallèles
        "memory_limit_gb": 8,  # Limite mémoire en GB
        "cache_enabled": True,  # Activation du cache
        "progress_bar": True  # Barre de progression
    }
    
    # === CONFIGURATION EXPORT ===
    EXPORT_CONFIG = {
        "formats": ["parquet", "csv", "geojson", "hdf5"],
        "compression": "snappy",  # Compression Parquet
        "encoding": "utf-8",
        "float_format": "%.6f",
        "index": False
    }
    
    @classmethod
    def get_groups_by_priority(cls, priority: int) -> List[ConsolidationGroup]:
        """Retourne les groupes par priorité"""
        return [group for group in cls.CONSOLIDATION_GROUPS if group.priority == priority]
    
    @classmethod
    def get_group_by_final_column(cls, final_column: str) -> Optional[ConsolidationGroup]:
        """Retourne un groupe par sa colonne finale"""
        for group in cls.CONSOLIDATION_GROUPS:
            if group.final_column == final_column:
                return group
        return None
    
    @classmethod
    def get_all_source_columns(cls) -> List[str]:
        """Retourne toutes les colonnes sources"""
        columns = []
        for group in cls.CONSOLIDATION_GROUPS:
            columns.extend(group.source_columns)
        return list(set(columns))  # Suppression des doublons
    
    @classmethod
    def get_final_columns(cls) -> List[str]:
        """Retourne toutes les colonnes finales"""
        return [group.final_column for group in cls.CONSOLIDATION_GROUPS]
    
    @classmethod
    def validate_configuration(cls) -> bool:
        """Valide la configuration"""
        try:
            # Vérification des groupes
            if len(cls.CONSOLIDATION_GROUPS) < 20:
                logger.error("Configuration invalide: moins de 20 groupes")
                return False
            
            # Vérification des colonnes finales uniques
            final_columns = cls.get_final_columns()
            if len(final_columns) != len(set(final_columns)):
                logger.error("Configuration invalide: colonnes finales dupliquées")
                return False
            
            # Vérification des priorités
            priorities = [group.priority for group in cls.CONSOLIDATION_GROUPS]
            if not all(1 <= p <= 3 for p in priorities):
                logger.error("Configuration invalide: priorités hors limites")
                return False
            
            logger.info("✅ Configuration validée avec succès")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur validation configuration: {e}")
            return False
    
    @classmethod
    def log_configuration(cls):
        """Log la configuration complète"""
        logger.info("⚙️ === CONFIGURATION CONSOLIDATION MAXIMALE ===")
        logger.info(f"Version: {cls.PIPELINE_VERSION}")
        logger.info(f"Mission: {cls.MISSION}")
        logger.info(f"Objectif: {cls.OBJECTIVE}")
        logger.info(f"Groupes de consolidation: {len(cls.CONSOLIDATION_GROUPS)}")
        logger.info(f"Colonnes finales: {len(cls.get_final_columns())}")
        logger.info(f"Réduction cible: {cls.TARGET_REDUCTION_PERCENTAGE}%")
        logger.info(f"Récupération cible: +{cls.MIN_VALUES_RECOVERED_PERCENTAGE}%")
        logger.info(f"Performance cible: {cls.TARGET_PERFORMANCE_IMPROVEMENT}x")
        logger.info("⚙️" + "="*60)
