#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 NETTOYEUR ULTRA-INTELLIGENT - ORCHESTRATEUR PRINCIPAL
========================================================

Module principal d'orchestration du pipeline ETL ultra-intelligent
Basé sur les spécifications du real_estate_prompt.md
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
from pathlib import Path
import warnings
import time
from datetime import datetime
import json
import os

# Imports des modules spécialisés
from config.consolidation_config import ConsolidationConfig
from intelligence.similarity_detector import SimilarityDetector
from validation.quality_validator import QualityValidator
from export.advanced_exporter import AdvancedExporter
from performance.performance_optimizer import PerformanceOptimizer
from utils.db import read_mongodb_to_dataframe, get_mongodb_stats
from utils.property_type_normalizer import PropertyTypeNormalizer

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class UltraIntelligentCleaner:
    """
    Nettoyeur ultra-intelligent pour le pipeline ETL immobilier
    Orchestre toutes les phases: Extraction, Transformation, Enrichment, Validation, Loading
    """
    
    def __init__(self, config: ConsolidationConfig = None):
        """
        Initialise le nettoyeur ultra-intelligent
        
        Args:
            config: Configuration de consolidation
        """
        self.config = config or ConsolidationConfig()
        self.pipeline_history = []
        self.consolidation_results = {}
        self.quality_metrics = {}
        
        # === INITIALISATION DES MODULES ===
        logger.info("🧠 === INITIALISATION ULTRA-INTELLIGENT CLEANER ===")
        
        # Validation de la configuration
        if not self.config.validate_configuration():
            raise ValueError("❌ Configuration de consolidation invalide")
        
        # Initialisation des composants
        self.similarity_detector = SimilarityDetector()
        self.quality_validator = QualityValidator()
        self.advanced_exporter = AdvancedExporter()
        self.performance_optimizer = PerformanceOptimizer()
        self.property_normalizer = PropertyTypeNormalizer()
        
        logger.info("✅ Tous les modules initialisés avec succès")
        self.config.log_configuration()
    
    def run_complete_pipeline(self, input_source: str = "mongodb", 
                             input_config: Dict = None, 
                             output_config: Dict = None) -> Dict[str, Any]:
        """
        Exécute le pipeline ETL complet
        
        Args:
            input_source: Source des données ("mongodb", "csv", "json", etc.)
            input_config: Configuration d'entrée
            output_config: Configuration de sortie
            
        Returns:
            Dict avec les résultats du pipeline
        """
        pipeline_start = datetime.now()
        logger.info("🚀 === DÉMARRAGE PIPELINE ETL COMPLET ===")
        
        try:
            # === PHASE 1: EXTRACTION ===
            logger.info("📥 === PHASE 1: EXTRACTION ===")
            df = self._extract_data(input_source, input_config)
            
            if df is None or df.empty:
                raise ValueError("❌ Aucune donnée extraite")
            
            logger.info(f"✅ Extraction réussie: {df.shape[0]} lignes × {df.shape[1]} colonnes")
            
            # === PHASE 2: TRANSFORMATION ===
            logger.info("🔄 === PHASE 2: TRANSFORMATION ===")
            df_transformed = self._transform_data(df)
            
            # === PHASE 3: ENRICHMENT ===
            logger.info("🚀 === PHASE 3: ENRICHMENT ===")
            df_enriched = self._enrich_data(df_transformed)
            
            # === PHASE 3.1: CLUSTERING SPATIAL ===
            logger.info("🌍 === PHASE 3.1: CLUSTERING SPATIAL DBSCAN ===")
            spatial_results = self.similarity_detector.spatial_clustering(df_enriched)
            if spatial_results.get("success"):
                df_enriched = spatial_results["df_with_clusters"]
                logger.info(f"✅ Clustering spatial réussi: {spatial_results['n_clusters']} zones créées")
            else:
                logger.warning(f"⚠️ Clustering spatial échoué: {spatial_results.get('error', 'Erreur inconnue')}")
            
            # === PHASE 3.2: CATÉGORISATION AUTOMATIQUE ===
            logger.info("🏷️ === PHASE 3.2: CATÉGORISATION AUTOMATIQUE ===")
            df_categorized = self.categorize_investment_opportunities(df_enriched)
            
            # === PHASE 4: VALIDATION ===
            logger.info("✅ === PHASE 4: VALIDATION ===")
            validation_results = self._validate_data(df_categorized)
            
            # === PHASE 5: LOAD ===
            logger.info("💾 === PHASE 5: LOAD ===")
            export_results = self._load_data(df_categorized, output_config)
            
            # === RÉSULTATS FINAUX ===
            pipeline_end = datetime.now()
            pipeline_duration = (pipeline_end - pipeline_start).total_seconds()
            
            results = {
                "success": True,
                "pipeline_duration": pipeline_duration,
                "input_shape": df.shape,
                "output_shape": df_categorized.shape,
                "reduction_percentage": ((df.shape[1] - df_categorized.shape[1]) / df.shape[1]) * 100,
                "spatial_clustering": spatial_results,
                "categorization_stats": self._extract_categorization_stats(df_categorized),
                "validation_results": validation_results,
                "export_results": export_results,
                "final_dataframe": df_categorized
            }
            
            logger.info(f"🎉 === PIPELINE ETL TERMINÉ EN {pipeline_duration:.2f}s ===")
            logger.info(f"📊 Réduction: {df.shape[1]} → {df_categorized.shape[1]} colonnes ({results['reduction_percentage']:.1f}%)")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Erreur pipeline: {e}")
            
            # Enregistrement de l'erreur
            error_results = {
                "pipeline_timestamp": pipeline_start.isoformat(),
                "pipeline_duration_seconds": (datetime.now() - pipeline_start).total_seconds(),
                "input_source": input_source,
                "status": "ERROR",
                "error": str(e)
            }
            
            self.pipeline_history.append(error_results)
            
            raise
    
    def _extract_data(self, input_source: str, input_config: Dict = None) -> pd.DataFrame:
        """Phase d'extraction des données"""
        logger.info(f"📥 Extraction depuis: {input_source}")
        
        if input_source.lower() == "mongodb":
            return self._extract_from_mongodb(input_config)
        elif input_source.lower() == "csv":
            return self._extract_from_csv(input_config)
        elif input_source.lower() == "json":
            return self._extract_from_json(input_config)
        else:
            raise ValueError(f"❌ Source non supportée: {input_source}")
    
    def _extract_from_mongodb(self, input_config: Dict = None) -> pd.DataFrame:
        """Extraction depuis MongoDB"""
        try:
            # Configuration par défaut
            default_config = {
                "database": "real_estate_db",
                "collection": "properties",
                "limit": None,
                "query": {}
            }
            
            if input_config:
                default_config.update(input_config)
            
            logger.info(f"🗄️ Connexion MongoDB: {default_config['database']}.{default_config['collection']}")
            
            # Test de connexion
            stats = get_mongodb_stats(default_config["database"], default_config["collection"])
            logger.info(f"📊 Statistiques MongoDB: {stats}")
            
            # Extraction des données
            df = read_mongodb_to_dataframe(
                database=default_config["database"],
                collection=default_config["collection"],
                query=default_config["query"],
                limit=default_config["limit"]
            )
            
            if df is None or df.empty:
                logger.warning("⚠️ Aucune donnée extraite de MongoDB - création d'un dataset de test")
                df = self._create_test_dataset()
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur extraction MongoDB: {e}")
            logger.info("🔄 Création d'un dataset de test...")
            return self._create_test_dataset()
    
    def _extract_from_csv(self, input_config: Dict = None) -> pd.DataFrame:
        """Extraction depuis un fichier CSV"""
        try:
            file_path = input_config.get("file_path", "data/real_estate_data.csv")
            logger.info(f"📁 Lecture CSV: {file_path}")
            
            df = pd.read_csv(file_path)
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur lecture CSV: {e}")
            raise
    
    def _extract_from_json(self, input_config: Dict = None) -> pd.DataFrame:
        """Extraction depuis un fichier JSON"""
        try:
            file_path = input_config.get("file_path", "data/real_estate_data.json")
            logger.info(f"📁 Lecture JSON: {file_path}")
            
            df = pd.read_json(file_path)
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur lecture JSON: {e}")
            raise
    
    def _create_test_dataset(self) -> pd.DataFrame:
        """Crée un dataset de test synthétique"""
        logger.info("🧪 Création d'un dataset de test synthétique")
        
        np.random.seed(42)
        n_samples = 1000
        
        # Génération de données synthétiques
        data = {
            "price": np.random.uniform(100000, 2000000, n_samples),
            "prix": np.random.uniform(100000, 2000000, n_samples),
            "surface": np.random.uniform(50, 500, n_samples),
            "superficie": np.random.uniform(50, 500, n_samples),
            "bedrooms": np.random.randint(1, 6, n_samples),
            "chambres": np.random.randint(1, 6, n_samples),
            "bathrooms": np.random.randint(1, 4, n_samples),
            "salle_bain": np.random.randint(1, 4, n_samples),
            "latitude": np.random.uniform(45.0, 47.5, n_samples),
            "longitude": np.random.uniform(-74.5, -71.0, n_samples),
            "property_type": np.random.choice(["Maison", "Appartement", "Condo"], n_samples),
            "type_propriete": np.random.choice(["House", "Apartment", "Condo"], n_samples),
            "year_built": np.random.randint(1950, 2024, n_samples),
            "annee_construction": np.random.randint(1950, 2024, n_samples),
            "tax_municipal": np.random.uniform(1000, 10000, n_samples),
            "taxe_municipale": np.random.uniform(1000, 10000, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Ajout de valeurs manquantes pour tester la consolidation
        for col in df.columns:
            if np.random.random() < 0.1:  # 10% de valeurs manquantes
                mask = np.random.choice([True, False], size=len(df), p=[0.1, 0.9])
                df.loc[mask, col] = np.nan
        
        logger.info(f"✅ Dataset de test créé: {df.shape[0]} lignes × {df.shape[1]} colonnes")
        return df

    def _transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Phase de transformation des données"""
        logger.info("🔄 === TRANSFORMATION DES DONNÉES ===")
        
        # === OPTIMISATION DES PERFORMANCES ===
        logger.info("🚀 Optimisation des performances...")
        df = self.performance_optimizer.optimize_dataframe(df, "medium")
        
        # === DÉTECTION INTELLIGENTE DES SIMILARITÉS ===
        logger.info("🧠 Détection intelligente des similarités...")
        similarity_groups = self.similarity_detector.detect_similar_columns(df)
        
        # === CONSOLIDATION MAXIMALE ===
        logger.info("🔗 Consolidation maximale des variables...")
        df_consolidated = self._consolidate_variables(df)
        
        # === NETTOYAGE DES DONNÉES ===
        logger.info("🧹 Nettoyage des données...")
        df_cleaned = self._clean_data(df_consolidated)
        
        # === NORMALISATION DES TYPES DE PROPRIÉTÉ ===
        logger.info("🏠 Normalisation des types de propriété...")
        df_normalized = self._normalize_property_types(df_cleaned)
        
        logger.info(f"✅ Transformation terminée: {df.shape[1]} → {df_normalized.shape[1]} colonnes")
        return df_normalized
    
    def _consolidate_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Consolidation maximale des variables selon la stratégie avancée
        Respecte exactement les 30 groupes de consolidation du real_estate_prompt.md
        """
        logger.info("🔗 === CONSOLIDATION MAXIMALE DES VARIABLES ===")
        logger.info(f"📊 Colonnes initiales: {df.shape[1]}")
        
        df_consolidated = df.copy()
        consolidation_results = {}
        
        # === TRI DES GROUPES PAR PRIORITÉ ===
        priority_groups = sorted(
            self.config.CONSOLIDATION_GROUPS,
            key=lambda x: x.priority
        )
        
        logger.info(f"🎯 {len(priority_groups)} groupes de consolidation à traiter")
        
        for group in priority_groups:
            logger.info(f"🔄 Consolidation du groupe: {group.name} → {group.final_column}")
            
            # === VÉRIFICATION DES COLONNES SOURCES DISPONIBLES ===
            available_columns = [col for col in group.source_columns if col in df_consolidated.columns]
            
            if not available_columns:
                logger.warning(f"⚠️ Aucune colonne source disponible pour {group.name}")
                continue
            
            logger.info(f"📋 Colonnes sources trouvées: {available_columns}")
            
            # === CONSOLIDATION INTELLIGENTE ===
            try:
                consolidated_column = self._consolidate_group(
                    df_consolidated, 
                    available_columns, 
                    group
                )
                
                if consolidated_column is not None:
                    # Ajout de la colonne consolidée
                    df_consolidated[group.final_column] = consolidated_column
                    
                    # Suppression des colonnes sources (après validation)
                    if self._validate_consolidated_column(consolidated_column, group):
                        for col in available_columns:
                            if col in df_consolidated.columns:
                                df_consolidated = df_consolidated.drop(columns=[col])
                        
                        # Statistiques de consolidation
                        non_null_count = consolidated_column.notna().sum()
                        total_count = len(consolidated_column)
                        completeness = (non_null_count / total_count) * 100
                        
                        consolidation_results[group.name] = {
                            "final_column": group.final_column,
                            "source_columns": available_columns,
                            "completeness": completeness,
                            "non_null_values": non_null_count,
                            "total_values": total_count,
                            "status": "success"
                        }
                        
                        logger.info(f"✅ {group.name} consolidé: {completeness:.1f}% de complétude")
                    else:
                        logger.warning(f"⚠️ Validation échouée pour {group.name}")
                        consolidation_results[group.name] = {
                            "status": "validation_failed",
                            "error": "Validation de la colonne consolidée échouée"
                        }
                else:
                    logger.warning(f"⚠️ Consolidation échouée pour {group.name}")
                    consolidation_results[group.name] = {
                        "status": "consolidation_failed",
                        "error": "Impossible de créer la colonne consolidée"
                    }
                    
            except Exception as e:
                logger.error(f"❌ Erreur lors de la consolidation de {group.name}: {e}")
                consolidation_results[group.name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # === RÉSULTATS FINAUX ===
        final_columns = df_consolidated.shape[1]
        reduction_percentage = ((df.shape[1] - final_columns) / df.shape[1]) * 100
        
        # === SUPPRESSION DES COLONNES MÉTADONNÉES ===
        logger.info("🗑️ Suppression des colonnes métadonnées et utilitaires...")
        columns_to_remove = [col for col in self.config.COLUMNS_TO_REMOVE if col in df_consolidated.columns]
        
        if columns_to_remove:
            df_consolidated = df_consolidated.drop(columns=columns_to_remove)
            logger.info(f"🗑️ {len(columns_to_remove)} colonnes métadonnées supprimées")
        
        # === FILTRAGE FINAL SELON SPÉCIFICATIONS ===
        logger.info("📋 Filtrage final selon real_estate_prompt.md...")
        try:
            from config.final_columns_config import FINAL_COLUMNS_LIST
            
            # Garder seulement les colonnes qui existent et sont dans la liste finale
            available_final_columns = [col for col in FINAL_COLUMNS_LIST if col in df_consolidated.columns]
            
            # Ajouter les colonnes essentielles qui pourraient avoir des noms différents
            essential_columns = ['_id', 'price', 'city', 'type', 'latitude', 'longitude']
            for col in essential_columns:
                if col in df_consolidated.columns and col not in available_final_columns:
                    available_final_columns.append(col)
            
            # Filtrer le DataFrame pour ne garder que ces colonnes
            df_consolidated = df_consolidated[available_final_columns]
            
            logger.info(f"📋 {len(available_final_columns)} colonnes finales conservées selon le prompt")
            
        except ImportError:
            logger.warning("⚠️ Configuration final_columns_config non trouvée, conservation de toutes les colonnes")
        
        # === CALCUL FINAL DES MÉTRIQUES ===
        final_columns_after_cleanup = df_consolidated.shape[1]
        total_reduction_percentage = ((df.shape[1] - final_columns_after_cleanup) / df.shape[1]) * 100
        
        logger.info(f"🎉 === CONSOLIDATION TERMINÉE ===")
        logger.info(f"📊 Colonnes initiales: {df.shape[1]}")
        logger.info(f"📊 Colonnes après consolidation: {final_columns}")
        logger.info(f"📊 Colonnes finales: {final_columns_after_cleanup}")
        logger.info(f"📉 Réduction totale: {total_reduction_percentage:.1f}%")
        
        # Vérification de l'objectif de réduction
        if total_reduction_percentage >= 65:
            logger.info(f"🎯 Objectif de réduction atteint: {total_reduction_percentage:.1f}% >= 65%")
        else:
            logger.warning(f"⚠️ Objectif de réduction non atteint: {total_reduction_percentage:.1f}% < 65%")
        
        # Sauvegarde des résultats
        self.consolidation_results = consolidation_results
        
        return df_consolidated
    
    def _consolidate_group(self, df: pd.DataFrame, source_columns: List[str], group: 'ConsolidationGroup') -> Optional[pd.Series]:
        """
        Consolide un groupe de colonnes sources en une colonne finale
        
        Args:
            df: DataFrame source
            source_columns: Liste des colonnes sources à consolider
            group: Configuration du groupe de consolidation
            
        Returns:
            Série consolidée ou None si échec
        """
        try:
            logger.info(f"🔄 Consolidation du groupe {group.name} avec {len(source_columns)} colonnes sources")
            
            # === SÉLECTION DES COLONNES SOURCES ===
            available_data = df[source_columns].copy()
            
            # === STRATÉGIE DE CONSOLIDATION PAR TYPE DE DONNÉES ===
            if group.data_type == "numeric":
                return self._consolidate_numeric_group(available_data, group)
            elif group.data_type == "categorical":
                return self._consolidate_categorical_group(available_data, group)
            elif group.data_type == "datetime":
                return self._consolidate_datetime_group(available_data, group)
            elif group.data_type == "mixed":
                return self._consolidate_mixed_group(available_data, group)
            else:
                logger.warning(f"⚠️ Type de données non supporté: {group.data_type}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erreur consolidation groupe {group.name}: {e}")
            return None
    
    def _consolidate_numeric_group(self, data: pd.DataFrame, group: 'ConsolidationGroup') -> pd.Series:
        """Consolide un groupe de colonnes numériques"""
        # Conversion en numérique et gestion des erreurs
        numeric_data = data.apply(pd.to_numeric, errors='coerce')
        
        # Fusion intelligente avec fillna en cascade
        consolidated = numeric_data.iloc[:, 0].copy()
        
        for col in numeric_data.columns[1:]:
            consolidated = consolidated.fillna(numeric_data[col])
        
        # Validation des règles métier
        if "positive" in group.validation_rules:
            consolidated = consolidated.where(consolidated > 0, np.nan)
        
        if "non_negative" in group.validation_rules:
            consolidated = consolidated.where(consolidated >= 0, np.nan)
        
        if "integer" in group.validation_rules:
            consolidated = consolidated.round(0)
        
        return consolidated
    
    def _consolidate_categorical_group(self, data: pd.DataFrame, group: 'ConsolidationGroup') -> pd.Series:
        """Consolide un groupe de colonnes catégorielles"""
        # Fusion avec priorité à la première colonne non-vide
        consolidated = data.iloc[:, 0].copy()
        
        for col in data.columns[1:]:
            mask = consolidated.isna() | (consolidated == '')
            consolidated[mask] = data[col][mask]
        
        return consolidated
    
    def _consolidate_datetime_group(self, data: pd.DataFrame, group: 'ConsolidationGroup') -> pd.Series:
        """Consolide un groupe de colonnes de dates"""
        # Conversion en datetime et fusion
        datetime_data = data.apply(pd.to_datetime, errors='coerce')
        
        consolidated = datetime_data.iloc[:, 0].copy()
        
        for col in datetime_data.columns[1:]:
            consolidated = consolidated.fillna(datetime_data[col])
        
        return consolidated
    
    def _consolidate_mixed_group(self, data: pd.DataFrame, group: 'ConsolidationGroup') -> pd.Series:
        """Consolide un groupe de colonnes de types mixtes"""
        # Stratégie de fusion intelligente pour types mixtes
        consolidated = data.iloc[:, 0].copy()
        
        for col in data.columns[1:]:
            mask = consolidated.isna() | (consolidated == '') | (consolidated == 'nan')
            consolidated[mask] = data[col][mask]
        
        return consolidated
    
    def _validate_consolidated_column(self, consolidated_column: pd.Series, group: 'ConsolidationGroup') -> bool:
        """
        Valide la colonne consolidée pour s'assurer qu'elle est cohérente
        et qu'elle ne contient pas trop de valeurs manquantes.
        """
        if consolidated_column.empty:
            logger.warning(f"⚠️ Colonne consolidée vide pour {group.name}")
            return False

        # Vérifier la complétude
        completeness = consolidated_column.notna().sum() / len(consolidated_column)
        if completeness < 0.9: # Exemple: 90% de complétude requis
            logger.warning(f"⚠️ Complétude insuffisante pour {group.name}: {completeness * 100:.1f}%")
            return False

        # Vérifier la diversité
        unique_ratio = consolidated_column.nunique() / len(consolidated_column)
        if unique_ratio < 0.5: # Exemple: 50% de diversité requis
            logger.warning(f"⚠️ Diversité insuffisante pour {group.name}: {unique_ratio * 100:.1f}%")
            return False

        # Vérifier les valeurs aberrantes
        if consolidated_column.dtype in ['int64', 'float64']:
            q1 = consolidated_column.quantile(0.25)
            q3 = consolidated_column.quantile(0.75)
            iqr = q3 - q1
            if iqr > 0:
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outliers = ((consolidated_column < lower_bound) | (consolidated_column > upper_bound)).sum()
                if outliers / len(consolidated_column) > 0.1: # Exemple: 10% d'outliers
                    logger.warning(f"⚠️ Taux d'outliers élevé pour {group.name}: {outliers / len(consolidated_column) * 100:.1f}%")
                    return False

        return True

    def _calculate_column_quality(self, series: pd.Series) -> float:
        """Calcule un score de qualité pour une colonne"""
        if series.empty:
            return 0.0
        
        # === COMPLÉTUDE ===
        completeness = 1 - (series.isnull().sum() / len(series))
        
        # === COHÉRENCE ===
        if series.dtype in ['int64', 'float64']:
            # Pour les colonnes numériques, cohérence basée sur les outliers
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            
            if iqr > 0:
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outliers = ((series < lower_bound) | (series > upper_bound)).sum()
                coherence = 1 - (outliers / len(series))
            else:
                coherence = 1.0
        else:
            # Pour les colonnes catégorielles, cohérence basée sur la diversité
            unique_ratio = series.nunique() / len(series)
            coherence = 1 - unique_ratio if unique_ratio < 0.9 else 0.1
        
        # === SCORE COMPOSITE ===
        quality_score = (completeness * 0.7) + (coherence * 0.3)
        
        return quality_score
    
    def _apply_validation_rules(self, series: pd.Series, group: 'ConsolidationGroup') -> pd.Series:
        """Applique les règles de validation à une série"""
        validated_series = series.copy()
        
        for rule_name in group.validation_rules:
            if rule_name in self.config.VALIDATION_RULES:
                rule_func = self.config.VALIDATION_RULES[rule_name]
                
                try:
                    # Application de la règle
                    if rule_name == "positive":
                        validated_series = validated_series[validated_series > 0]
                    elif rule_name == "non_negative":
                        validated_series = validated_series[validated_series >= 0]
                    elif rule_name == "reasonable_range":
                        validated_series = validated_series[
                            (validated_series > 0) & (validated_series < 1000000)
                        ]
                    elif rule_name == "geographic_bounds":
                        if "latitude" in group.name.lower():
                            validated_series = validated_series[
                                (validated_series >= 45.0) & (validated_series <= 47.5)
                            ]
                        elif "longitude" in group.name.lower():
                            validated_series = validated_series[
                                (validated_series >= -74.5) & (validated_series <= -71.0)
                            ]
                    elif rule_name == "year_range":
                        validated_series = validated_series[
                            (validated_series >= 1800) & (validated_series <= 2024)
                        ]
                    elif rule_name == "integer":
                        validated_series = validated_series[validated_series == validated_series.astype(int)]
                
                except Exception as e:
                    logger.debug(f"⚠️ Règle {rule_name} non applicable: {e}")
                    continue
        
        return validated_series
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données consolidées"""
        logger.info("🧹 === NETTOYAGE DES DONNÉES ===")
        
        df_cleaned = df.copy()
        
        # === SUPPRESSION DES LIGNES VIDE ===
        initial_rows = len(df_cleaned)
        df_cleaned = df_cleaned.dropna(how='all')
        rows_removed = initial_rows - len(df_cleaned)
        
        if rows_removed > 0:
            logger.info(f"🗑️ {rows_removed} lignes vides supprimées")
        
        # === NETTOYAGE DES VALEURS TEXTUELLES ===
        text_columns = df_cleaned.select_dtypes(include=['object']).columns
        for col in text_columns:
            if col in df_cleaned.columns:
                # Suppression des espaces en début/fin
                df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
                
                # Remplacement des chaînes vides par NaN
                df_cleaned[col] = df_cleaned[col].replace(['', 'nan', 'None'], np.nan)
        
        # === DÉTECTION ET TRAITEMENT DES OUTLIERS ===
        numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in df_cleaned.columns:
                df_cleaned[col] = self._handle_outliers(df_cleaned[col])
        
        logger.info(f"✅ Nettoyage terminé: {len(df_cleaned)} lignes conservées")
        return df_cleaned
    
    def _handle_outliers(self, series: pd.Series) -> pd.Series:
        """Gère les outliers d'une série numérique"""
        if series.empty or series.isnull().all():
            return series
        
        # Méthode IQR pour détecter les outliers
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        
        if iqr > 0:
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            # Remplacement des outliers par les bornes
            series_cleaned = series.copy()
            series_cleaned[series < lower_bound] = lower_bound
            series_cleaned[series > upper_bound] = upper_bound
            
            outliers_count = ((series < lower_bound) | (series > upper_bound)).sum()
            if outliers_count > 0:
                logger.debug(f"🔍 {outliers_count} outliers traités dans {series.name}")
            
            return series_cleaned
        
        return series
    
    def _normalize_property_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalise les types de propriété"""
        logger.info("🏠 === NORMALISATION DES TYPES DE PROPRIÉTÉ ===")
        
        df_normalized = df.copy()
        
        # Recherche des colonnes de type de propriété
        property_type_columns = []
        for col in df_normalized.columns:
            if any(term in col.lower() for term in ['type', 'category', 'property_type']):
                property_type_columns.append(col)
        
        if not property_type_columns:
            logger.info("ℹ️ Aucune colonne de type de propriété trouvée")
            return df_normalized
        
        # Normalisation de chaque colonne
        for col in property_type_columns:
            if col in df_normalized.columns:
                logger.info(f"🔄 Normalisation de la colonne: {col}")
                
                try:
                    normalized_values = self.property_normalizer.normalize_property_types(
                        df_normalized[col]
                    )
                    
                    if normalized_values is not None:
                        df_normalized[col] = normalized_values
                        logger.info(f"✅ Colonne {col} normalisée")
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erreur normalisation {col}: {e}")
        
        return df_normalized
    
    def _enrich_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Phase d'enrichissement des données"""
        logger.info("✨ === ENRICHISSEMENT DES DONNÉES ===")
        
        df_enriched = df.copy()
        
        # === CALCUL DES MÉTRIQUES DÉRIVÉES ===
        logger.info("📊 Calcul des métriques dérivées...")
        df_enriched = self._calculate_derived_metrics(df_enriched)
        
        # === GÉOLOCALISATION ET VALIDATION ===
        logger.info("🌍 Validation et enrichissement géographique...")
        df_enriched = self._enrich_geographic_data(df_enriched)
        
        # === CALCULS FINANCIERS ===
        logger.info("💰 Calculs financiers...")
        df_enriched = self._calculate_financial_metrics(df_enriched)
        
        # === OPTIMISATION FINALE ===
        logger.info("🚀 Optimisation finale des performances...")
        df_enriched = self.performance_optimizer.optimize_dataframe(df_enriched, "aggressive")
        
        logger.info(f"✅ Enrichissement terminé: {df.shape[1]} → {df_enriched.shape[1]} colonnes")
        return df_enriched
    
    def _calculate_derived_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcule les métriques dérivées"""
        df_enriched = df.copy()
        
        # === PRIX AU M² ===
        price_columns = [col for col in df.columns if any(term in col.lower() for term in ['price', 'prix'])]
        surface_columns = [col for col in df.columns if any(term in col.lower() for term in ['surface', 'superficie', 'area'])]
        
        if price_columns and surface_columns:
            price_col = price_columns[0]
            surface_col = surface_columns[0]
            
            if price_col in df_enriched.columns and surface_col in df_enriched.columns:
                try:
                    df_enriched['price_per_sqm'] = (
                        df_enriched[price_col] / df_enriched[surface_col]
                    ).round(2)
                    logger.info("✅ Prix au m² calculé")
                except Exception as e:
                    logger.debug(f"⚠️ Erreur calcul prix au m²: {e}")
        
        # === ÂGE DE LA PROPRIÉTÉ ===
        year_columns = [col for col in df.columns if any(term in col.lower() for term in ['year', 'annee', 'construction'])]
        
        if year_columns:
            year_col = year_columns[0]
            if year_col in df_enriched.columns:
                try:
                    current_year = datetime.now().year
                    df_enriched['property_age'] = current_year - df_enriched[year_col]
                    df_enriched['property_age'] = df_enriched['property_age'].clip(lower=0)
                    logger.info("✅ Âge de la propriété calculé")
                except Exception as e:
                    logger.debug(f"⚠️ Erreur calcul âge: {e}")
        
        # === RATIO TAXES/PRIX ===
        tax_columns = [col for col in df.columns if any(term in col.lower() for term in ['tax', 'taxe'])]
        
        if tax_columns and price_columns:
            tax_col = tax_columns[0]
            price_col = price_columns[0]
            
            if tax_col in df_enriched.columns and price_col in df_enriched.columns:
                try:
                    df_enriched['tax_price_ratio'] = (
                        df_enriched[tax_col] / df_enriched[price_col]
                    ).round(4)
                    logger.info("✅ Ratio taxes/prix calculé")
                except Exception as e:
                    logger.debug(f"⚠️ Erreur calcul ratio taxes: {e}")
        
        return df_enriched
    
    def _enrich_geographic_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrichit les données géographiques"""
        df_enriched = df.copy()
        
        # === VALIDATION DES COORDONNÉES ===
        lat_columns = [col for col in df.columns if any(term in col.lower() for term in ['lat', 'latitude'])]
        lng_columns = [col for col in df.columns if any(term in col.lower() for term in ['lng', 'long', 'longitude'])]
        
        if lat_columns and lng_columns:
            lat_col = lat_columns[0]
            lng_col = lng_columns[0]
            
            if lat_col in df_enriched.columns and lng_col in df_enriched.columns:
                # Validation des coordonnées
                valid_coords = (
                    (df_enriched[lat_col] >= 45.0) & (df_enriched[lat_col] <= 47.5) &
                    (df_enriched[lng_col] >= -74.5) & (df_enriched[lng_col] <= -71.0)
                )
                
                invalid_count = (~valid_coords).sum()
                if invalid_count > 0:
                    logger.warning(f"⚠️ {invalid_count} coordonnées invalides détectées")
                
                # Filtrage des coordonnées valides
                df_enriched = df_enriched[valid_coords]
                
                # Calcul de la densité géographique
                if len(df_enriched) > 0:
                    try:
                        # Approximation de la densité (nombre de propriétés par zone)
                        df_enriched['geographic_density'] = len(df_enriched) / (
                            (47.5 - 45.0) * (-71.0 - (-74.5))
                        )
                        logger.info("✅ Densité géographique calculée")
                    except Exception as e:
                        logger.debug(f"⚠️ Erreur calcul densité: {e}")
        
        return df_enriched
    
    def _calculate_financial_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcule les métriques financières"""
        df_enriched = df.copy()
        
        # === ROI BRUT ===
        price_columns = [col for col in df.columns if any(term in col.lower() for term in ['price', 'prix'])]
        revenue_columns = [col for col in df.columns if any(term in col.lower() for term in ['revenue', 'revenu', 'income'])]
        
        if price_columns and revenue_columns:
            price_col = price_columns[0]
            revenue_col = revenue_columns[0]
            
            if price_col in df_enriched.columns and revenue_col in df_enriched.columns:
                try:
                    # ROI brut = (revenus annuels / prix d'achat) * 100
                    df_enriched['roi_brut'] = (
                        (df_enriched[revenue_col] / df_enriched[price_col]) * 100
                    ).round(2)
                    
                    # Filtrage des valeurs aberrantes
                    df_enriched['roi_brut'] = df_enriched['roi_brut'].clip(0, 50)
                    
                    logger.info("✅ ROI brut calculé")
                except Exception as e:
                    logger.debug(f"⚠️ Erreur calcul ROI: {e}")
        
        # === ROI NET ===
        expense_columns = [col for col in df.columns if any(term in col.lower() for term in ['expense', 'depense', 'charge'])]
        
        if price_columns and revenue_columns and expense_columns:
            price_col = price_columns[0]
            revenue_col = revenue_columns[0]
            expense_col = expense_columns[0]
            
            if all(col in df_enriched.columns for col in [price_col, revenue_col, expense_col]):
                try:
                    # ROI net = ((revenus - dépenses) / prix d'achat) * 100
                    df_enriched['roi_net'] = (
                        ((df_enriched[revenue_col] - df_enriched[expense_col]) / df_enriched[price_col]) * 100
                    ).round(2)
                    
                    # Filtrage des valeurs aberrantes
                    df_enriched['roi_net'] = df_enriched['roi_net'].clip(-10, 40)
                    
                    logger.info("✅ ROI net calculé")
                except Exception as e:
                    logger.debug(f"⚠️ Erreur calcul ROI net: {e}")
        
        return df_enriched

    def _validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Phase de validation des données"""
        logger.info("✅ === VALIDATION DES DONNÉES ===")
        
        # === VALIDATION DE QUALITÉ COMPLÈTE ===
        logger.info("🔍 Validation de qualité complète...")
        validation_results = self.quality_validator.validate_dataset(
            df, 
            dataset_name="real_estate_consolidated"
        )
        
        # === VALIDATION SPÉCIFIQUE AU DOMAINE ===
        logger.info("🏠 Validation spécifique au domaine immobilier...")
        domain_validation = self._validate_domain_specific_rules(df)
        
        # === VALIDATION DES MÉTRIQUES DE CONSOLIDATION ===
        logger.info("📊 Validation des métriques de consolidation...")
        consolidation_validation = self._validate_consolidation_metrics(df)
        
        # === COMPILATION DES RÉSULTATS ===
        all_validation_results = {
            "quality_validation": validation_results,
            "domain_validation": domain_validation,
            "consolidation_validation": consolidation_validation,
            "overall_status": self._determine_overall_validation_status(
                validation_results, domain_validation, consolidation_validation
            )
        }
        
        # Enregistrement des métriques
        self.quality_metrics = all_validation_results
        
        logger.info(f"✅ Validation terminée - Statut: {all_validation_results['overall_status']}")
        return all_validation_results
    
    def _validate_domain_specific_rules(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Valide les règles spécifiques au domaine immobilier"""
        validation_results = {
            "status": "PASS",
            "rules_checked": [],
            "violations": [],
            "warnings": []
        }
        
        # === VALIDATION DES PRIX ===
        price_columns = [col for col in df.columns if any(term in col.lower() for term in ['price', 'prix'])]
        for col in price_columns:
            if col in df.columns:
                series = df[col].dropna()
                if len(series) > 0:
                    # Vérification des prix négatifs
                    negative_prices = (series < 0).sum()
                    if negative_prices > 0:
                        validation_results["violations"].append({
                            "rule": "Prix négatifs interdits",
                            "column": col,
                            "count": negative_prices,
                            "severity": "ERROR"
                        })
                    
                    # Vérification des prix extrêmes
                    q99 = series.quantile(0.99)
                    extreme_prices = (series > q99 * 10).sum()
                    if extreme_prices > 0:
                        validation_results["warnings"].append({
                            "rule": "Prix extrêmes détectés",
                            "column": col,
                            "count": extreme_prices,
                            "severity": "WARNING"
                        })
                    
                    validation_results["rules_checked"].append(f"Prix - {col}")
        
        # === VALIDATION DES SURFACES ===
        surface_columns = [col for col in df.columns if any(term in col.lower() for term in ['surface', 'superficie', 'area'])]
        for col in surface_columns:
            if col in df.columns:
                series = df[col].dropna()
                if len(series) > 0:
                    # Vérification des surfaces négatives
                    negative_surfaces = (series < 0).sum()
                    if negative_surfaces > 0:
                        validation_results["violations"].append({
                            "rule": "Surfaces négatives interdites",
                            "column": col,
                            "count": negative_surfaces,
                            "severity": "ERROR"
                        })
                    
                    # Vérification des surfaces extrêmes
                    q99 = series.quantile(0.99)
                    extreme_surfaces = (series > q99 * 5).sum()
                    if extreme_surfaces > 0:
                        validation_results["warnings"].append({
                            "rule": "Surfaces extrêmes détectées",
                            "column": col,
                            "count": extreme_surfaces,
                            "severity": "WARNING"
                        })
                    
                    validation_results["rules_checked"].append(f"Surface - {col}")
        
        # === VALIDATION DES COORDONNÉES ===
        lat_columns = [col for col in df.columns if any(term in col.lower() for term in ['lat', 'latitude'])]
        lng_columns = [col for col in df.columns if any(term in col.lower() for term in ['lng', 'long', 'longitude'])]
        
        if lat_columns and lng_columns:
            lat_col = lat_columns[0]
            lng_col = lng_columns[0]
            
            if lat_col in df.columns and lng_col in df.columns:
                # Vérification des coordonnées dans les limites du Québec
                valid_coords = (
                    (df[lat_col] >= 45.0) & (df[lat_col] <= 47.5) &
                    (df[lng_col] >= -74.5) & (df[lng_col] <= -71.0)
                )
                
                invalid_coords = (~valid_coords).sum()
                if invalid_coords > 0:
                    validation_results["violations"].append({
                        "rule": "Coordonnées hors limites Québec",
                        "columns": [lat_col, lng_col],
                        "count": invalid_coords,
                        "severity": "ERROR"
                    })
                
                validation_results["rules_checked"].append("Coordonnées géographiques")
        
        # === DÉTERMINATION DU STATUT ===
        if any(v["severity"] == "ERROR" for v in validation_results["violations"]):
            validation_results["status"] = "FAIL"
        elif any(v["severity"] == "WARNING" for v in validation_results["warnings"]):
            validation_results["status"] = "WARNING"
        else:
            validation_results["status"] = "PASS"
        
        return validation_results
    
    def _validate_consolidation_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Valide les métriques de consolidation"""
        validation_results = {
            "status": "PASS",
            "metrics": {},
            "targets_met": []
        }
        
        # === VÉRIFICATION DES OBJECTIFS ===
        initial_columns = self.consolidation_results.get("initial_columns", 0)
        final_columns = len(df.columns)
        
        if initial_columns > 0:
            reduction_percentage = ((initial_columns - final_columns) / initial_columns) * 100
            
            # Objectif de réduction
            target_reduction = self.config.TARGET_REDUCTION_PERCENTAGE
            if reduction_percentage >= target_reduction:
                validation_results["targets_met"].append(f"Réduction colonnes: {reduction_percentage:.1f}% ≥ {target_reduction}%")
            else:
                validation_results["warnings"] = [f"Réduction insuffisante: {reduction_percentage:.1f}% < {target_reduction}%"]
            
            validation_results["metrics"]["reduction_percentage"] = reduction_percentage
            validation_results["metrics"]["target_reduction"] = target_reduction
        
        # === VÉRIFICATION DE LA QUALITÉ ===
        quality_score = self.quality_metrics.get("quality_validation", {}).get("overall_score", 0)
        if quality_score >= 0.8:
            validation_results["targets_met"].append(f"Qualité des données: {quality_score:.1%} ≥ 80%")
        else:
            validation_results["warnings"] = [f"Qualité insuffisante: {quality_score:.1%} < 80%"]
        
        validation_results["metrics"]["quality_score"] = quality_score
        
        # === DÉTERMINATION DU STATUT ===
        if validation_results["warnings"]:
            validation_results["status"] = "WARNING"
        elif validation_results["targets_met"]:
            validation_results["status"] = "PASS"
        
        return validation_results
    
    def _determine_overall_validation_status(self, quality_validation: Dict, 
                                           domain_validation: Dict, 
                                           consolidation_validation: Dict) -> str:
        """Détermine le statut global de validation"""
        statuses = [
            quality_validation.get("status", "UNKNOWN"),
            domain_validation.get("status", "UNKNOWN"),
            consolidation_validation.get("status", "UNKNOWN")
        ]
        
        if "FAIL" in statuses:
            return "FAIL"
        elif "WARNING" in statuses:
            return "WARNING"
        elif all(status == "PASS" for status in statuses):
            return "PASS"
        else:
            return "UNKNOWN"
    
    def _load_data(self, df: pd.DataFrame, output_config: Dict = None) -> Dict[str, Any]:
        """Phase de chargement et export des données"""
        logger.info("💾 === CHARGEMENT ET EXPORT DES DONNÉES ===")
        
        # === CONFIGURATION D'EXPORT ===
        default_output_config = {
            "formats": ["parquet", "csv", "geojson"],
            "output_directory": "exports",
            "include_metadata": True,
            "chunked_export": False
        }
        
        if output_config:
            default_output_config.update(output_config)
        
        # === EXPORT MULTI-FORMATS ===
        logger.info("📤 Export multi-formats...")
        
        if default_output_config["chunked_export"] and len(df) > 10000:
            # Export par chunks pour les gros datasets
            export_results = self.advanced_exporter.export_chunked(
                df, 
                dataset_name="real_estate_consolidated",
                chunk_size=10000,
                output_dir=default_output_config["output_directory"]
            )
        else:
            # Export standard
            export_results = self.advanced_exporter.export_dataset(
                df,
                dataset_name="real_estate_consolidated",
                formats=default_output_config["formats"],
                output_dir=default_output_config["output_directory"]
            )
        
        # === EXPORT AVEC MÉTADONNÉES ===
        if default_output_config["include_metadata"]:
            logger.info("📋 Export avec métadonnées...")
            
            metadata = {
                "pipeline_version": self.config.PIPELINE_VERSION,
                "consolidation_config": {
                    "groups_processed": self.consolidation_results.get("groups_processed", 0),
                    "reduction_percentage": self.consolidation_results.get("reduction_percentage", 0),
                    "target_reduction": self.config.TARGET_REDUCTION_PERCENTAGE
                },
                "quality_metrics": {
                    "overall_score": self.quality_metrics.get("quality_validation", {}).get("overall_score", 0),
                    "validation_status": self.quality_metrics.get("overall_status", "UNKNOWN")
                },
                "export_timestamp": datetime.now().isoformat()
            }
            
            metadata_export = self.advanced_exporter.export_with_metadata(
                df,
                dataset_name="real_estate_consolidated",
                metadata=metadata,
                output_dir=default_output_config["output_directory"]
            )
            
            export_results["metadata_export"] = metadata_export
        
        # === GÉNÉRATION DES RAPPORTS ===
        logger.info("📊 Génération des rapports...")
        
        # Rapport de qualité
        quality_report_path = os.path.join(
            default_output_config["output_directory"], 
            "quality_report.md"
        )
        quality_report = self.quality_validator.generate_quality_report(
            output_path=quality_report_path
        )
        
        # Rapport d'export
        export_report_path = os.path.join(
            default_output_config["output_directory"], 
            "export_report.md"
        )
        export_report = self.advanced_exporter.generate_export_report(
            output_path=export_report_path
        )
        
        # Rapport de performance
        performance_report_path = os.path.join(
            default_output_config["output_directory"], 
            "performance_report.md"
        )
        performance_report = self.performance_optimizer.generate_performance_report(
            output_path=performance_report_path
        )
        
        # Rapport de similarités
        similarity_report_path = os.path.join(
            default_output_config["output_directory"], 
            "similarity_report.md"
        )
        similarity_report = self.similarity_detector.generate_similarity_report(
            df, 
            output_path=similarity_report_path
        )
        
        # === COMPILATION DES RÉSULTATS ===
        load_results = {
            "export_results": export_results,
            "reports_generated": {
                "quality": quality_report_path,
                "export": export_report_path,
                "performance": performance_report_path,
                "similarity": similarity_report_path
            },
            "dataset_final_shape": df.shape,
            "export_timestamp": datetime.now().isoformat()
        }
        
        logger.info("✅ Export et rapports terminés")
        logger.info(f"📁 Fichiers exportés dans: {default_output_config['output_directory']}")
        
        return load_results
    
    def get_pipeline_summary(self) -> Dict[str, Any]:
        """Retourne un résumé du pipeline"""
        if not self.pipeline_history:
            return {"message": "Aucun pipeline exécuté"}
        
        # Dernier pipeline
        latest_pipeline = self.pipeline_history[-1]
        
        # Statistiques globales
        total_pipelines = len(self.pipeline_history)
        successful_pipelines = len([p for p in self.pipeline_history if p.get("status") == "SUCCESS"])
        failed_pipelines = len([p for p in self.pipeline_history if p.get("status") == "ERROR"])
        
        # Métriques de consolidation
        consolidation_stats = self.consolidation_results or {}
        
        # Métriques de qualité
        quality_stats = self.quality_metrics or {}
        
        return {
            "pipeline_summary": {
                "total_executions": total_pipelines,
                "successful_executions": successful_pipelines,
                "failed_executions": failed_pipelines,
                "success_rate": successful_pipelines / total_pipelines if total_pipelines > 0 else 0
            },
            "latest_execution": {
                "timestamp": latest_pipeline.get("pipeline_timestamp"),
                "duration_seconds": latest_pipeline.get("pipeline_duration_seconds"),
                "status": latest_pipeline.get("status"),
                "input_shape": latest_pipeline.get("input_shape"),
                "output_shape": latest_pipeline.get("output_shape")
            },
            "consolidation_metrics": consolidation_stats,
            "quality_metrics": quality_stats,
            "performance_summary": self.performance_optimizer.get_performance_summary()
        }
    
    def generate_comprehensive_report(self, output_path: str = None) -> str:
        """
        Génère un rapport complet du pipeline
        
        Args:
            output_path: Chemin de sauvegarde (optionnel)
            
        Returns:
            Contenu du rapport
        """
        logger.info("📊 === GÉNÉRATION RAPPORT COMPLET ===")
        
        # Récupération du résumé
        summary = self.get_pipeline_summary()
        
        # Génération du rapport
        report_content = []
        report_content.append("# " + "="*80)
        report_content.append("# RAPPORT COMPLET PIPELINE ETL ULTRA-INTELLIGENT")
        report_content.append("# " + "="*80)
        report_content.append(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_content.append(f"# Version: {self.config.PIPELINE_VERSION}")
        report_content.append("# " + "="*80 + "\n")
        
        # Résumé exécutif
        report_content.append("## RÉSUMÉ EXÉCUTIF")
        pipeline_summary = summary.get("pipeline_summary", {})
        report_content.append(f"**Pipelines exécutés:** {pipeline_summary.get('total_executions', 0)}")
        report_content.append(f"**Succès:** {pipeline_summary.get('successful_executions', 0)}")
        report_content.append(f"**Échecs:** {pipeline_summary.get('failed_executions', 0)}")
        report_content.append(f"**Taux de succès:** {pipeline_summary.get('success_rate', 0):.1%}")
        report_content.append("")
        
        # Dernière exécution
        latest = summary.get("latest_execution", {})
        report_content.append("## DERNIÈRE EXÉCUTION")
        report_content.append(f"**Statut:** {latest.get('status', 'UNKNOWN')}")
        report_content.append(f"**Date:** {latest.get('timestamp', 'N/A')}")
        report_content.append(f"**Durée:** {latest.get('duration_seconds', 0):.2f}s")
        report_content.append(f"**Forme initiale:** {latest.get('input_shape', 'N/A')}")
        report_content.append(f"**Forme finale:** {latest.get('output_shape', 'N/A')}")
        report_content.append("")
        
        # Métriques de consolidation
        consolidation = summary.get("consolidation_metrics", {})
        if consolidation:
            report_content.append("## MÉTRIQUES DE CONSOLIDATION")
            report_content.append(f"**Groupes traités:** {consolidation.get('groups_processed', 0)}")
            report_content.append(f"**Colonnes consolidées:** {consolidation.get('columns_consolidated', 0)}")
            report_content.append(f"**Colonnes supprimées:** {consolidation.get('columns_removed', 0)}")
            report_content.append(f"**Réduction:** {consolidation.get('reduction_percentage', 0):.1f}%")
            report_content.append("")
        
        # Métriques de qualité
        quality = summary.get("quality_metrics", {})
        if quality:
            report_content.append("## MÉTRIQUES DE QUALITÉ")
            quality_validation = quality.get("quality_validation", {})
            report_content.append(f"**Score global:** {quality_validation.get('overall_score', 0):.1%}")
            report_content.append(f"**Statut validation:** {quality.get('overall_status', 'UNKNOWN')}")
            report_content.append("")
        
        # Résumé des performances
        performance = summary.get("performance_summary", {})
        if "optimization_summary" in performance:
            opt_summary = performance["optimization_summary"]
            report_content.append("## RÉSUMÉ DES PERFORMANCES")
            report_content.append(f"**Optimisations effectuées:** {opt_summary.get('total_optimizations', 0)}")
            report_content.append(f"**Mémoire économisée:** {opt_summary.get('total_memory_saved_mb', 0):.2f} MB")
            report_content.append(f"**Temps moyen d'optimisation:** {opt_summary.get('average_optimization_time_seconds', 0):.3f}s")
            report_content.append("")
        
        # Configuration
        report_content.append("## CONFIGURATION")
        report_content.append(f"**Version pipeline:** {self.config.PIPELINE_VERSION}")
        report_content.append(f"**Mission:** {self.config.MISSION}")
        report_content.append(f"**Objectif:** {self.config.OBJECTIVE}")
        report_content.append(f"**Réduction cible:** {self.config.TARGET_REDUCTION_PERCENTAGE}%")
        report_content.append(f"**Récupération cible:** +{self.config.MIN_VALUES_RECOVERED_PERCENTAGE}%")
        report_content.append("")
        
        # Recommandations
        report_content.append("## RECOMMANDATIONS")
        if pipeline_summary.get("success_rate", 0) >= 0.9:
            report_content.append("✅ **Excellent** - Le pipeline fonctionne parfaitement")
        elif pipeline_summary.get("success_rate", 0) >= 0.7:
            report_content.append("✅ **Bon** - Le pipeline fonctionne bien avec quelques améliorations possibles")
        elif pipeline_summary.get("success_rate", 0) >= 0.5:
            report_content.append("⚠️ **Moyen** - Améliorations recommandées")
        else:
            report_content.append("❌ **Faible** - Actions correctives nécessaires")
        
        report_content.append("")
        report_content.append("# " + "="*80)
        report_content.append("# FIN DU RAPPORT")
        report_content.append("# " + "="*80)
        
        report_text = "\n".join(report_content)
        
        # Sauvegarde si un chemin est fourni
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                logger.info(f"📄 Rapport complet sauvegardé: {output_path}")
            except Exception as e:
                logger.error(f"❌ Erreur sauvegarde rapport: {e}")
        
        return report_text

    def _extract_categorization_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extrait les statistiques de catégorisation des opportunités
        
        Args:
            df: DataFrame avec colonnes de catégorisation
            
        Returns:
            Dict avec statistiques de catégorisation
        """
        stats = {}
        
        # === STATISTIQUES DES SEGMENTS ROI ===
        if 'segment_roi' in df.columns:
            stats['segments_roi'] = df['segment_roi'].value_counts().to_dict()
        
        # === STATISTIQUES DES CLASSES PRIX ===
        if 'classe_prix' in df.columns:
            stats['classes_prix'] = df['classe_prix'].value_counts().to_dict()
        
        # === STATISTIQUES DES TYPES D'OPPORTUNITÉS ===
        if 'type_opportunite' in df.columns:
            stats['types_opportunites'] = df['type_opportunite'].value_counts().to_dict()
        
        # === STATISTIQUES DES CLASSES D'INVESTISSEMENT ===
        if 'classe_investissement' in df.columns:
            stats['classes_investissement'] = df['classe_investissement'].value_counts().to_dict()
        
        # === STATISTIQUES DES ZONES SPATIALES ===
        if 'spatial_zone' in df.columns:
            stats['zones_spatiales'] = df['spatial_zone'].value_counts().to_dict()
        
        # === STATISTIQUES DU SCORE QUALITÉ ===
        if 'score_qualite' in df.columns:
            stats['score_qualite'] = {
                'moyenne': df['score_qualite'].mean(),
                'ecart_type': df['score_qualite'].std(),
                'min': df['score_qualite'].min(),
                'max': df['score_qualite'].max(),
                'quartiles': df['score_qualite'].quantile([0.25, 0.5, 0.75]).to_dict()
            }
        
        return stats

    def categorize_investment_opportunities(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Catégorisation automatique des opportunités d'investissement
        Respecte les spécifications du real_estate_prompt.md
        
        Args:
            df: DataFrame avec variables consolidées
            
        Returns:
            DataFrame avec nouvelles colonnes de catégorisation
        """
        logger.info("🏷️ === CATÉGORISATION AUTOMATIQUE DES OPPORTUNITÉS ===")
        
        df_categorized = df.copy()
        
        # === SEGMENTS ROI ===
        if 'roi_brut' in df_categorized.columns:
            logger.info("💰 Catégorisation des segments ROI")
            df_categorized['segment_roi'] = pd.cut(
                df_categorized['roi_brut'],
                bins=[-np.inf, 0, 0.05, 0.10, 0.15, np.inf],
                labels=['Perte', 'Faible', 'Moyen', 'Élevé', 'Premium'],
                include_lowest=True
            )
        
        # === CLASSES PRIX ===
        if 'price_final' in df_categorized.columns:
            logger.info("💎 Catégorisation des classes prix")
            price_quantiles = df_categorized['price_final'].quantile([0.25, 0.5, 0.75])
            df_categorized['classe_prix'] = pd.cut(
                df_categorized['price_final'],
                bins=[0, price_quantiles[0.25], price_quantiles[0.5], 
                      price_quantiles[0.75], np.inf],
                labels=['Économique', 'Moyen', 'Élevé', 'Premium'],
                include_lowest=True
            )
        
        # === TYPES D'OPPORTUNITÉS ===
        logger.info("🎯 Classification des types d'opportunités")
        df_categorized['type_opportunite'] = 'Standard'
        
        # Opportunités à fort potentiel
        high_potential_mask = (
            (df_categorized.get('roi_brut', 0) > 0.10) &
            (df_categorized.get('potentiel_plus_value', 0) > 0.20)
        )
        df_categorized.loc[high_potential_mask, 'type_opportunite'] = 'Fort Potentiel'
        
        # Opportunités de rénovation
        renovation_mask = (
            (df_categorized.get('year_built_final', 2024) < 1980) &
            (df_categorized.get('price_final', 0) < df_categorized.get('evaluation_total_final', 0) * 0.8)
        )
        df_categorized.loc[renovation_mask, 'type_opportunite'] = 'Rénovation'
        
        # Opportunités de revenus
        revenue_mask = (
            (df_categorized.get('revenue_final', 0) > 0) &
            (df_categorized.get('roi_brut', 0) > 0.08)
        )
        df_categorized.loc[revenue_mask, 'type_opportunite'] = 'Revenus'
        
        # Opportunités de plus-value
        appreciation_mask = (
            (df_categorized.get('potentiel_plus_value', 0) > 0.30) &
            (df_categorized.get('evaluation_year_final', 2024) < 2020)
        )
        df_categorized.loc[appreciation_mask, 'type_opportunite'] = 'Plus-Value'
        
        # === ZONES GÉOGRAPHIQUES DE PERFORMANCE ===
        if 'spatial_zone' in df_categorized.columns:
            logger.info("🌍 Analyse des zones géographiques de performance")
            
            # Calcul de la performance par zone
            zone_performance = df_categorized.groupby('spatial_zone').agg({
                'roi_brut': 'mean',
                'price_final': 'median',
                'revenue_final': 'mean'
            }).round(4)
            
            # Classification des zones
            zone_performance['classe_zone'] = pd.qcut(
                zone_performance['roi_brut'].fillna(0),
                q=4,
                labels=['Zone Faible', 'Zone Moyenne', 'Zone Élevée', 'Zone Premium']
            )
            
            # Ajout de la classe de zone au DataFrame principal
            df_categorized = df_categorized.merge(
                zone_performance[['classe_zone']],
                left_on='spatial_zone',
                right_index=True,
                how='left'
            )
        
        # === SCORE QUALITÉ GLOBAL ===
        logger.info("📊 Calcul du score qualité global")
        quality_scores = []
        
        for idx, row in df_categorized.iterrows():
            score = 0
            
            # Complétude des données (0-30 points)
            completeness = 1 - (row.isna().sum() / len(row))
            score += completeness * 30
            
            # Cohérence des données (0-25 points)
            if 'roi_brut' in row and 'price_final' in row and 'revenue_final' in row:
                if pd.notna(row['roi_brut']) and pd.notna(row['price_final']) and pd.notna(row['revenue_final']):
                    if row['roi_brut'] >= 0 and row['price_final'] > 0:
                        score += 25
            
            # Qualité géographique (0-20 points)
            if 'latitude_final' in row and 'longitude_final' in row:
                if pd.notna(row['latitude_final']) and pd.notna(row['longitude_final']):
                    # Vérification que les coordonnées sont dans des ranges raisonnables
                    if (45.0 <= row['latitude_final'] <= 75.0 and 
                        -80.0 <= row['longitude_final'] <= -50.0):  # Québec approximatif
                        score += 20
            
            # Métriques financières (0-25 points)
            if 'roi_brut' in row and pd.notna(row['roi_brut']):
                if 0 <= row['roi_brut'] <= 0.5:  # ROI raisonnable
                    score += 25
            
            quality_scores.append(min(score, 100))  # Plafonné à 100
        
        df_categorized['score_qualite'] = quality_scores
        
        # === CLASSIFICATION FINALE DES OPPORTUNITÉS ===
        logger.info("🏆 Classification finale des opportunités")
        df_categorized['classe_investissement'] = pd.cut(
            df_categorized['score_qualite'],
            bins=[0, 40, 60, 80, 100],
            labels=['Risqué', 'Moyen', 'Bon', 'Excellent'],
            include_lowest=True
        )
        
        # === STATISTIQUES DE CATÉGORISATION ===
        categorization_stats = {
            'segments_roi': df_categorized.get('segment_roi', pd.Series()).value_counts().to_dict(),
            'classes_prix': df_categorized.get('classe_prix', pd.Series()).value_counts().to_dict(),
            'types_opportunites': df_categorized['type_opportunite'].value_counts().to_dict(),
            'classes_investissement': df_categorized['classe_investissement'].value_counts().to_dict(),
            'score_qualite_moyen': df_categorized['score_qualite'].mean(),
            'score_qualite_std': df_categorized['score_qualite'].std()
        }
        
        logger.info(f"📊 Statistiques de catégorisation: {categorization_stats}")
        logger.info(f"✅ Catégorisation terminée: {len(df_categorized)} propriétés analysées")
        
        return df_categorized
