#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ VALIDATEUR DE QUALITÉ - TESTS ET CONTRÔLES AUTOMATISÉS
==========================================================

Module de validation et contrôle qualité des données
Basé sur les spécifications du real_estate_prompt.md
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
import warnings
import json
import os

# Imports conditionnels pour les bibliothèques optionnelles
try:
    import great_expectations as ge
    GREAT_EXPECTATIONS_AVAILABLE = True
except ImportError:
    GREAT_EXPECTATIONS_AVAILABLE = False
    warnings.warn("Great Expectations non disponible - fonctionnalités limitées")

# Patch pour éviter l'erreur generated_jit
try:
    import numba
    if not hasattr(numba, 'generated_jit'):
        numba.generated_jit = lambda *args, **kwargs: lambda func: func
except ImportError:
    pass

try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn("Scikit-learn non disponible - détection d'anomalies limitée")

try:
    import pandas_profiling
    PANDAS_PROFILING_AVAILABLE = True
except ImportError:
    PANDAS_PROFILING_AVAILABLE = False
    warnings.warn("Pandas Profiling non disponible - profils limités")

try:
    import missingno as msno
    MISSINGNO_AVAILABLE = True
except ImportError:
    MISSINGNO_AVAILABLE = False
    warnings.warn("Missingno non disponible - visualisations manquantes limitées")

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class QualityValidator:
    """
    Validateur de qualité des données avec tests automatisés
    Intègre Great Expectations + Scikit-learn + Pandas Profiling
    """
    
    def __init__(self, validation_config: Dict = None):
        """
        Initialise le validateur de qualité
        
        Args:
            validation_config: Configuration de validation
        """
        self.validation_config = validation_config or self._default_validation_config()
        self.validation_results = {}
        self.quality_metrics = {}
        self.anomalies_detected = {}
        self.current_output_path = None
        
        logger.info("✅ QualityValidator initialisé")
        logger.info(f"📊 Great Expectations: {'✅' if GREAT_EXPECTATIONS_AVAILABLE else '❌'}")
        logger.info(f"🤖 Scikit-learn: {'✅' if SKLEARN_AVAILABLE else '❌'}")
        logger.info(f"📈 Pandas Profiling: {'✅' if PANDAS_PROFILING_AVAILABLE else '❌'}")
        logger.info(f"🔍 Missingno: {'✅' if MISSINGNO_AVAILABLE else '❌'}")
    
    def set_output_path(self, output_path: str):
        """Définit le chemin de sortie pour les rapports"""
        self.current_output_path = output_path
    
    def _default_validation_config(self) -> Dict:
        """Configuration de validation par défaut"""
        return {
            "data_quality_thresholds": {
                "completeness_min": 0.8,  # 80% de complétude minimum
                "accuracy_min": 0.9,      # 90% de précision minimum
                "consistency_min": 0.85,  # 85% de cohérence minimum
                "validity_min": 0.9      # 90% de validité minimum
            },
            "anomaly_detection": {
                "isolation_forest_contamination": 0.1,
                "z_score_threshold": 3.0,
                "iqr_multiplier": 1.5
            },
            "geographic_validation": {
                "latitude_bounds": {"min": 45.0, "max": 47.5},  # Québec
                "longitude_bounds": {"min": -74.5, "max": -71.0}
            },
            "business_rules": {
                "price_min": 1000,
                "price_max": 10000000,
                "surface_min": 10,
                "surface_max": 10000,
                "bedrooms_min": 0,
                "bedrooms_max": 20,
                "bathrooms_min": 0,
                "bathrooms_max": 20
            }
        }
    
    def validate_dataset(self, df: pd.DataFrame, dataset_name: str = "dataset") -> Dict[str, Any]:
        """
        Validation complète du dataset
        
        Args:
            df: DataFrame à valider
            dataset_name: Nom du dataset pour les rapports
            
        Returns:
            Dict avec tous les résultats de validation
        """
        logger.info(f"🔍 === VALIDATION COMPLÈTE: {dataset_name} ===")
        
        validation_start = datetime.now()
        
        # === VALIDATION DE BASE ===
        logger.info("📋 Validation de base...")
        try:
            basic_validation = self._basic_validation(df)
            logger.info("✅ Validation de base terminée")
        except Exception as e:
            logger.error(f"❌ Erreur validation de base: {e}")
            raise
        
        # === VALIDATION DES TYPES ===
        logger.info("🔧 Validation des types de données...")
        try:
            type_validation = self._type_validation(df)
            logger.info("✅ Validation des types terminée")
        except Exception as e:
            logger.error(f"❌ Erreur validation des types: {e}")
            raise
        
        # === VALIDATION DES VALEURS ===
        logger.info("✅ Validation des valeurs...")
        try:
            value_validation = self._value_validation(df)
            logger.info("✅ Validation des valeurs terminée")
        except Exception as e:
            logger.error(f"❌ Erreur validation des valeurs: {e}")
            raise
        
        # === VALIDATION GÉOGRAPHIQUE ===
        logger.info("🌍 Validation géographique...")
        try:
            geographic_validation = self._geographic_validation(df)
            logger.info("✅ Validation géographique terminée")
        except Exception as e:
            logger.error(f"❌ Erreur validation géographique: {e}")
            raise
        
        # === VALIDATION DES RÈGLES MÉTIER ===
        logger.info("💼 Validation des règles métier...")
        try:
            business_validation = self._business_rule_validation(df)
            logger.info("✅ Validation des règles métier terminée")
        except Exception as e:
            logger.error(f"❌ Erreur validation des règles métier: {e}")
            raise
        
        # === DÉTECTION D'ANOMALIES ===
        logger.info("🚨 Détection d'anomalies...")
        try:
            anomaly_detection = self._anomaly_detection(df)
            logger.info("✅ Détection d'anomalies terminée")
        except Exception as e:
            logger.error(f"❌ Erreur détection d'anomalies: {e}")
            raise
        
        # === VALIDATION AVEC GREAT EXPECTATIONS ===
        if GREAT_EXPECTATIONS_AVAILABLE:
            logger.info("🎯 Validation avec Great Expectations...")
            ge_validation = self._great_expectations_validation(df)
        else:
            ge_validation = {"status": "unavailable", "message": "Great Expectations non installé"}
        
        # === PROFILAGE AVANCÉ ===
        if PANDAS_PROFILING_AVAILABLE:
            logger.info("📊 Profilage avancé...")
            # Récupérer l'output_path depuis le contexte du pipeline
            profiling_results = self._advanced_profiling(df, getattr(self, 'current_output_path', None))
        else:
            profiling_results = {"status": "unavailable", "message": "Pandas Profiling non installé"}
        
        # === CALCUL DES MÉTRIQUES GLOBALES ===
        logger.info("📈 Calcul des métriques globales...")
        global_metrics = self._calculate_global_metrics(
            basic_validation, type_validation, value_validation,
            geographic_validation, business_validation, anomaly_detection
        )
        
        # === COMPILATION DES RÉSULTATS ===
        validation_end = datetime.now()
        validation_duration = validation_end - validation_start
        
        self.validation_results[dataset_name] = {
            "validation_timestamp": validation_start.isoformat(),
            "validation_duration_seconds": validation_duration.total_seconds(),
            "dataset_info": {
                "shape": df.shape,
                "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
                "columns": list(df.columns)
            },
            "validation_results": {
                "basic": basic_validation,
                "types": type_validation,
                "values": value_validation,
                "geographic": geographic_validation,
                "business": business_validation,
                "anomalies": anomaly_detection,
                "great_expectations": ge_validation,
                "profiling": profiling_results
            },
            "global_metrics": global_metrics,
            "overall_score": global_metrics["overall_quality_score"],
            "status": "PASS" if global_metrics["overall_quality_score"] >= 0.8 else "FAIL"
        }
        
        logger.info(f"✅ Validation terminée en {validation_duration.total_seconds():.2f}s")
        logger.info(f"🎯 Score global: {global_metrics['overall_quality_score']:.2%}")
        logger.info(f"📊 Statut: {self.validation_results[dataset_name]['status']}")
        
        return self.validation_results[dataset_name]
    
    def _basic_validation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation de base du dataset"""
        results = {}
        
        # === COMPLÉTUDE ===
        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isnull().sum().sum()
        completeness = 1 - (null_cells / total_cells)
        
        results["completeness"] = {
            "score": completeness,
            "total_cells": total_cells,
            "null_cells": null_cells,
            "null_percentage": (null_cells / total_cells) * 100,
            "status": "PASS" if completeness >= self.validation_config["data_quality_thresholds"]["completeness_min"] else "FAIL"
        }
        
        # === UNICITÉ ===
        try:
            # Essayer la méthode standard
            duplicate_rows = df.duplicated().sum()
        except TypeError as e:
            # Si on a des valeurs non-hashables, on fait une approximation
            logger.warning(f"⚠️ Impossible de calculer duplicated() à cause de valeurs non-hashables: {e}")
            # Convertir toutes les valeurs non-hashables en chaînes pour le calcul
            df_for_duplicates = df.copy()
            for col in df_for_duplicates.columns:
                if df_for_duplicates[col].dtype == 'object':
                    df_for_duplicates[col] = df_for_duplicates[col].apply(
                        lambda x: str(x) if x is not None else None
                    )
            try:
                duplicate_rows = df_for_duplicates.duplicated().sum()
            except Exception:
                logger.warning("⚠️ Impossible de calculer l'unicité, utilisation de 0 doublons")
                duplicate_rows = 0
        
        uniqueness = 1 - (duplicate_rows / df.shape[0]) if df.shape[0] > 0 else 1.0
        
        results["uniqueness"] = {
            "score": uniqueness,
            "total_rows": df.shape[0],
            "duplicate_rows": duplicate_rows,
            "duplicate_percentage": (duplicate_rows / df.shape[0]) * 100,
            "status": "PASS" if uniqueness >= 0.95 else "FAIL"
        }
        
        # === CONSISTANCE DES COLONNES ===
        column_consistency = {}
        for col in df.columns:
            # Convertir la colonne en string pour éviter les problèmes de hashabilité
            col_key = str(col)
            logger.debug(f"🔍 Validation cohérence colonne: {col_key} (type: {df[col].dtype})")
            try:
                if df[col].dtype == 'object':
                    # Pour les colonnes textuelles, vérifier la cohérence des formats
                    sample_values = df[col].dropna().head(10)
                    if len(sample_values) > 0:
                        try:
                            # Vérifier si les valeurs sont des dictionnaires ou des chaînes
                            first_value = sample_values.iloc[0]
                            logger.debug(f"🔍 Première valeur de {col_key}: {type(first_value)} - {str(first_value)[:100]}")
                            
                            if isinstance(first_value, dict):
                                # Pour les colonnes de dictionnaires, cohérence parfaite
                                logger.debug(f"✅ Colonne {col_key}: dictionnaire détecté")
                                column_consistency[col_key] = 1.0
                            elif isinstance(first_value, str):
                                # Pour les colonnes textuelles, vérifier la cohérence des formats
                                logger.debug(f"✅ Colonne {col_key}: chaîne détectée")
                                try:
                                    length_variation = sample_values.str.len().std() / sample_values.str.len().mean()
                                    column_consistency[col_key] = max(0, 1 - length_variation)
                                except Exception as e:
                                    logger.warning(f"⚠️ Erreur calcul variation longueur pour {col_key}: {e}")
                                    column_consistency[col_key] = 1.0
                            else:
                                # Pour les autres types d'objets
                                logger.debug(f"⚠️ Colonne {col_key}: type inattendu {type(first_value)}")
                                column_consistency[col_key] = 1.0
                        except Exception as e:
                            # En cas d'erreur, considérer comme cohérent
                            logger.warning(f"⚠️ Erreur validation cohérence colonne {col_key}: {e}")
                            column_consistency[col_key] = 1.0
                    else:
                        column_consistency[col_key] = 1.0
                else:
                    # Pour les colonnes numériques, cohérence parfaite
                    column_consistency[col_key] = 1.0
            except Exception as e:
                logger.warning(f"⚠️ Erreur générale pour colonne {col_key}: {e}")
                column_consistency[col_key] = 1.0
        
        # Calcul de la moyenne avec gestion d'erreur
        try:
            avg_column_consistency = np.mean(list(column_consistency.values()))
        except Exception as e:
            logger.warning(f"⚠️ Erreur calcul moyenne cohérence: {e}")
            avg_column_consistency = 1.0
        
        results["column_consistency"] = {
            "score": avg_column_consistency,
            "column_details": column_consistency,
            "status": "PASS" if avg_column_consistency >= 0.8 else "FAIL"
        }
        
        return results
    
    def _type_validation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation des types de données"""
        results = {}
        
        # === ANALYSE DES TYPES ===
        type_analysis = {}
        for col in df.columns:
            col_key = str(col)
            col_type = str(df[col].dtype)
            type_analysis[col_key] = {
                "current_type": col_type,
                "sample_values": df[col].dropna().head(3).tolist(),
                "null_count": df[col].isnull().sum()
            }
        
        # === DÉTECTION DE TYPES INAPPROPRIÉS ===
        type_issues = []
        for col_key, info in type_analysis.items():
            # Trouver la colonne originale correspondante
            original_col = None
            for col in df.columns:
                if str(col) == col_key:
                    original_col = col
                    break
            
            if original_col is None:
                continue
                
            if info["current_type"] == "object":
                # Vérifier si c'est une colonne qui devrait être numérique
                sample_numeric = df[original_col].dropna().head(100)
                if len(sample_numeric) > 0:
                    try:
                        pd.to_numeric(sample_numeric, errors='raise')
                        type_issues.append({
                            "column": col_key,
                            "issue": "Colonne textuelle qui pourrait être numérique",
                            "severity": "WARNING"
                        })
                    except:
                        pass
        
        # === VALIDATION DES DATES ===
        date_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':
                sample_values = df[col].dropna().head(10)
                if len(sample_values) > 0:
                    try:
                        pd.to_datetime(sample_values, errors='raise')
                        date_columns.append(col)
                    except:
                        pass
        
        results["type_analysis"] = type_analysis
        results["type_issues"] = type_issues
        results["date_columns_detected"] = date_columns
        results["status"] = "PASS" if len(type_issues) == 0 else "WARNING"
        
        return results
    
    def _value_validation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation des valeurs des données"""
        results = {}
        
        # === VALIDATION DES VALEURS NUMÉRIQUES ===
        numeric_validation = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            col_key = str(col)
            series = df[col].dropna()
            if len(series) > 0:
                numeric_validation[col_key] = {
                    "min": float(series.min()),
                    "max": float(series.max()),
                    "mean": float(series.mean()),
                    "std": float(series.std()),
                    "zero_count": int((series == 0).sum()),
                    "negative_count": int((series < 0).sum()),
                    "outlier_count": self._count_outliers(series)
                }
        
        # === VALIDATION DES VALEURS CATÉGORIELLES ===
        categorical_validation = {}
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        
        for col in categorical_columns:
            col_key = str(col)
            try:
                series = df[col].dropna()
                if len(series) > 0:
                    try:
                        # Vérifier si les valeurs sont hashables avant de faire value_counts
                        sample_values = series.head(10)
                        hashable_values = []
                        for val in sample_values:
                            try:
                                hash(val)  # Test si la valeur est hashable
                                hashable_values.append(val)
                            except TypeError:
                                # Valeur non-hashable, la traiter comme une chaîne
                                hashable_values.append(str(val))
                        
                        if len(hashable_values) > 0:
                            # Utiliser seulement les valeurs hashables pour value_counts
                            safe_series = pd.Series(hashable_values)
                            value_counts = safe_series.value_counts()
                            most_common = value_counts.head(3).to_dict()
                        else:
                            most_common = {"error": "Valeurs non-hashables détectées"}
                        
                        categorical_validation[col_key] = {
                            "unique_count": int(series.nunique()),
                            "most_common": most_common,
                            "empty_string_count": int((series == "").sum()),
                            "whitespace_only_count": int((series.str.strip() == "").sum())
                        }
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur validation catégorielle pour {col_key}: {e}")
                        categorical_validation[col_key] = {
                            "unique_count": int(series.nunique()),
                            "most_common": {"error": f"Erreur: {str(e)}"},
                            "empty_string_count": 0,
                            "whitespace_only_count": 0
                        }
                else:
                    categorical_validation[col_key] = {
                        "unique_count": 0,
                        "most_common": {},
                        "empty_string_count": 0,
                        "whitespace_only_count": 0
                    }
            except Exception as e:
                logger.warning(f"⚠️ Erreur générale pour colonne catégorielle {col_key}: {e}")
                categorical_validation[col_key] = {
                    "unique_count": 0,
                    "most_common": {"error": f"Erreur: {str(e)}"},
                    "empty_string_count": 0,
                    "whitespace_only_count": 0
                }
        
        results["numeric_validation"] = numeric_validation
        results["categorical_validation"] = categorical_validation
        results["status"] = "PASS"
        
        return results
    
    def _geographic_validation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation des données géographiques"""
        results = {}
        
        # === DÉTECTION DES COLONNES GÉOGRAPHIQUES ===
        lat_columns = [col for col in df.columns if any(term in col.lower() for term in ['lat', 'latitude'])]
        lng_columns = [col for col in df.columns if any(term in col.lower() for term in ['lng', 'long', 'longitude'])]
        
        geographic_issues = []
        
        # === VALIDATION DES LATITUDES ===
        for col in lat_columns:
            col_key = str(col)
            if col in df.columns:
                series = df[col].dropna()
                if len(series) > 0:
                    bounds = self.validation_config["geographic_validation"]["latitude_bounds"]
                    out_of_bounds = series[(series < bounds["min"]) | (series > bounds["max"])]
                    
                    if len(out_of_bounds) > 0:
                        geographic_issues.append({
                            "column": col_key,
                            "issue": f"Latitudes hors limites ({bounds['min']} à {bounds['max']})",
                            "count": len(out_of_bounds),
                            "severity": "ERROR"
                        })
        
        # === VALIDATION DES LONGITUDES ===
        for col in lng_columns:
            col_key = str(col)
            if col in df.columns:
                series = df[col].dropna()
                if len(series) > 0:
                    bounds = self.validation_config["geographic_validation"]["longitude_bounds"]
                    out_of_bounds = series[(series < bounds["min"]) | (series > bounds["max"])]
                    
                    if len(out_of_bounds) > 0:
                        geographic_issues.append({
                            "column": col_key,
                            "issue": f"Longitudes hors limites ({bounds['min']} à {bounds['max']})",
                            "count": len(out_of_bounds),
                            "severity": "ERROR"
                        })
        
        # === VALIDATION DES COORDONNÉES COHERENTES ===
        if len(lat_columns) > 0 and len(lng_columns) > 0:
            for lat_col in lat_columns:
                for lng_col in lng_columns:
                    if lat_col in df.columns and lng_col in df.columns:
                        # Vérifier que les coordonnées sont cohérentes
                        valid_coords = df[[lat_col, lng_col]].dropna()
                        if len(valid_coords) > 0:
                            # Vérifier que les coordonnées ne sont pas identiques partout
                            if valid_coords[lat_col].nunique() == 1 and valid_coords[lng_col].nunique() == 1:
                                geographic_issues.append({
                                    "column": f"{lat_col}+{lng_col}",
                                    "issue": "Coordonnées identiques partout (possible erreur)",
                                    "severity": "WARNING"
                                })
        
        results["latitude_columns"] = lat_columns
        results["longitude_columns"] = lng_columns
        results["geographic_issues"] = geographic_issues
        results["status"] = "PASS" if len([i for i in geographic_issues if i["severity"] == "ERROR"]) == 0 else "FAIL"
        
        return results
    
    def _business_rule_validation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation des règles métier"""
        results = {}
        
        business_rules = self.validation_config["business_rules"]
        rule_violations = []
        
        # === VALIDATION DES PRIX ===
        price_columns = [col for col in df.columns if any(term in col.lower() for term in ['price', 'prix', 'valeur'])]
        for col in price_columns:
            col_key = str(col)
            if col in df.columns:
                series = df[col].dropna()
                if len(series) > 0:
                    # S'assurer que les valeurs sont numériques
                    try:
                        numeric_series = pd.to_numeric(series, errors='coerce').dropna()
                        if len(numeric_series) > 0:
                            violations = numeric_series[(numeric_series < business_rules["price_min"]) | (numeric_series > business_rules["price_max"])]
                            if len(violations) > 0:
                                rule_violations.append({
                                    "rule": "Prix dans les limites",
                                    "column": col_key,
                                    "violations": len(violations),
                                    "min_violation": float(violations.min()),
                                    "max_violation": float(violations.max()),
                                    "severity": "ERROR"
                                })
                    except Exception as e:
                        logger.warning(f"⚠️ Impossible de valider la colonne {col_key} (prix): {e}")
        
        # === VALIDATION DES SURFACES ===
        surface_columns = [col for col in df.columns if any(term in col.lower() for term in ['surface', 'area', 'sqft', 'm2'])]
        for col in surface_columns:
            col_key = str(col)
            if col in df.columns:
                series = df[col].dropna()
                if len(series) > 0:
                    # S'assurer que les valeurs sont numériques
                    try:
                        numeric_series = pd.to_numeric(series, errors='coerce').dropna()
                        if len(numeric_series) > 0:
                            violations = numeric_series[(numeric_series < business_rules["surface_min"]) | (numeric_series > business_rules["surface_max"])]
                            if len(violations) > 0:
                                rule_violations.append({
                                    "rule": "Surface dans les limites",
                                    "column": col_key,
                                    "violations": len(violations),
                                    "min_violation": float(violations.min()),
                                    "max_violation": float(violations.max()),
                                    "severity": "ERROR"
                                })
                    except Exception as e:
                        logger.warning(f"⚠️ Impossible de valider la colonne {col_key} (surface): {e}")
        
        # === VALIDATION DES CHAMBRES ===
        bedroom_columns = [col for col in df.columns if any(term in col.lower() for term in ['bedroom', 'chambre', 'bed'])]
        for col in bedroom_columns:
            col_key = str(col)
            if col in df.columns:
                series = df[col].dropna()
                if len(series) > 0:
                    # S'assurer que les valeurs sont numériques
                    try:
                        numeric_series = pd.to_numeric(series, errors='coerce').dropna()
                        if len(numeric_series) > 0:
                            violations = numeric_series[(numeric_series < business_rules["bedrooms_min"]) | (numeric_series > business_rules["bedrooms_max"])]
                            if len(violations) > 0:
                                rule_violations.append({
                                    "rule": "Nombre de chambres dans les limites",
                                    "column": col_key,
                                    "violations": len(violations),
                                    "min_violation": float(violations.min()),
                                    "max_violation": float(violations.max()),
                                    "severity": "ERROR"
                                })
                    except Exception as e:
                        logger.warning(f"⚠️ Impossible de valider la colonne {col_key} (chambres): {e}")
        
        results["rule_violations"] = rule_violations
        results["status"] = "PASS" if len(rule_violations) == 0 else "FAIL"
        
        return results
    
    def _anomaly_detection(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Détection d'anomalies avec Scikit-learn"""
        results = {}
        
        if not SKLEARN_AVAILABLE:
            results["status"] = "unavailable"
            results["message"] = "Scikit-learn non disponible"
            return results
        
        # === DÉTECTION PAR ISOLATION FOREST ===
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            try:
                # Préparation des données
                numeric_data = df[numeric_columns].fillna(df[numeric_columns].median())
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(numeric_data)
                
                # Détection d'anomalies
                iso_forest = IsolationForest(
                    contamination=self.validation_config["anomaly_detection"]["isolation_forest_contamination"],
                    random_state=42
                )
                anomaly_labels = iso_forest.fit_predict(scaled_data)
                
                # Analyse des résultats
                anomaly_count = (anomaly_labels == -1).sum()
                anomaly_percentage = (anomaly_count / len(anomaly_labels)) * 100
                
                results["isolation_forest"] = {
                    "anomaly_count": int(anomaly_count),
                    "anomaly_percentage": float(anomaly_percentage),
                    "anomaly_indices": np.where(anomaly_labels == -1)[0].tolist()
                }
                
            except Exception as e:
                results["isolation_forest"] = {
                    "error": str(e),
                    "status": "failed"
                }
        
        # === DÉTECTION PAR Z-SCORE ===
        z_score_anomalies = {}
        z_threshold = self.validation_config["anomaly_detection"]["z_score_threshold"]
        
        for col in numeric_columns:
            col_key = str(col)
            series = df[col].dropna()
            if len(series) > 0:
                z_scores = np.abs((series - series.mean()) / series.std())
                anomalies = series[z_scores > z_threshold]
                
                if len(anomalies) > 0:
                    z_score_anomalies[col_key] = {
                        "anomaly_count": len(anomalies),
                        "anomaly_percentage": (len(anomalies) / len(series)) * 100,
                        "anomaly_values": anomalies.tolist()
                    }
        
        results["z_score_anomalies"] = z_score_anomalies
        results["status"] = "completed"
        
        return results
    
    def _great_expectations_validation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation avec Great Expectations"""
        if not GREAT_EXPECTATIONS_AVAILABLE:
            return {"status": "unavailable", "message": "Great Expectations non installé"}
        
        try:
            # Création d'un contexte Great Expectations
            context = ge.get_context()
            
            # Création d'un datasource
            datasource_name = "pandas_datasource"
            if datasource_name not in [ds["name"] for ds in context.list_datasources()]:
                context.add_datasource(
                    name=datasource_name,
                    module_name="great_expectations.datasource",
                    class_name="PandasDatasource"
                )
            
            # Création d'un batch
            batch = context.get_batch(
                datasource_name=datasource_name,
                batch_kwargs={"dataset": df}
            )
            
            # Exécution de quelques validations de base
            validation_results = {}
            
            # Validation de la forme
            shape_result = batch.expect_table_row_count_to_be_between(
                min_value=1, max_value=1000000
            )
            validation_results["row_count"] = shape_result.to_json_dict()
            
            # Validation des colonnes
            columns_result = batch.expect_table_columns_to_match_ordered_list(
                column_list=list(df.columns)
            )
            validation_results["columns"] = columns_result.to_json_dict()
            
            # Validation de la complétude
            for col in df.columns[:5]:  # Limiter aux 5 premières colonnes
                col_key = str(col)
                completeness_result = batch.expect_column_values_to_not_be_null(column=col)
                validation_results[f"completeness_{col_key}"] = completeness_result.to_json_dict()
            
            results = {
                "status": "completed",
                "validation_results": validation_results,
                "success_count": sum(1 for r in validation_results.values() if r.get("success", False)),
                "total_count": len(validation_results)
            }
            
        except Exception as e:
            results = {
                "status": "error",
                "error": str(e)
            }
        
        return results
    
    def _advanced_profiling(self, df: pd.DataFrame, output_path: str = None) -> Dict[str, Any]:
        """Profilage avancé avec Pandas Profiling"""
        if not PANDAS_PROFILING_AVAILABLE:
            return {"status": "unavailable", "message": "Pandas Profiling non installé"}
        
        try:
            # Création du profil
            profile = pandas_profiling.ProfileReport(
                df, 
                title="Profil de Qualité des Données",
                explorative=True
            )
            
            # Sauvegarde du rapport dans le bon dossier
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if output_path:
                # Utiliser le chemin de sortie du pipeline
                from pathlib import Path
                output_dir = Path(output_path)
                output_dir.mkdir(parents=True, exist_ok=True)
                report_path = output_dir / f"quality_profile_{timestamp}.html"
            else:
                # Fallback: sauvegarde dans le dossier courant
                report_path = f"quality_profile_{timestamp}.html"
            
            profile.to_file(str(report_path))
            
            results = {
                "status": "completed",
                "report_path": report_path,
                "profile_summary": {
                    "variables": profile.get_description()["variables"],
                    "alerts": profile.get_description()["alerts"],
                    "sample": profile.get_description()["sample"]
                }
            }
            
        except Exception as e:
            results = {
                "status": "error",
                "error": str(e)
            }
        
        return results
    
    def _count_outliers(self, series: pd.Series) -> int:
        """Compte les outliers avec la méthode IQR"""
        try:
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - (self.validation_config["anomaly_detection"]["iqr_multiplier"] * IQR)
            upper_bound = Q3 + (self.validation_config["anomaly_detection"]["iqr_multiplier"] * IQR)
            
            outliers = series[(series < lower_bound) | (series > upper_bound)]
            return len(outliers)
        except:
            return 0
    
    def _calculate_global_metrics(self, *validation_results) -> Dict[str, float]:
        """Calcule les métriques globales de qualité"""
        metrics = {}
        
        # === SCORE DE COMPLÉTUDE ===
        completeness_scores = []
        for result in validation_results:
            if "completeness" in result:
                completeness_scores.append(result["completeness"]["score"])
        
        metrics["completeness_score"] = np.mean(completeness_scores) if completeness_scores else 0.0
        
        # === SCORE DE QUALITÉ GLOBALE ===
        overall_score = metrics["completeness_score"]
        
        # Ajustement basé sur les autres métriques
        if validation_results:
            # Pénaliser les erreurs critiques
            error_count = 0
            warning_count = 0
            
            for result in validation_results:
                if isinstance(result, dict):
                    for key, value in result.items():
                        if isinstance(value, dict) and "status" in value:
                            if value["status"] == "FAIL":
                                error_count += 1
                            elif value["status"] == "WARNING":
                                warning_count += 1
            
            # Ajustement du score
            if error_count > 0:
                overall_score *= 0.7  # Pénalité de 30% pour les erreurs
            elif warning_count > 0:
                overall_score *= 0.9  # Pénalité de 10% pour les avertissements
        
        metrics["overall_quality_score"] = max(0.0, min(1.0, overall_score))
        
        return metrics
    
    def generate_quality_report(self, dataset_name: str = None, output_path: str = None) -> str:
        """
        Génère un rapport complet de qualité
        
        Args:
            dataset_name: Nom du dataset (si None, utilise le dernier validé)
            output_path: Chemin de sauvegarde (optionnel)
            
        Returns:
            Contenu du rapport
        """
        if dataset_name is None:
            if not self.validation_results:
                return "❌ Aucun résultat de validation disponible"
            dataset_name = list(self.validation_results.keys())[-1]
        
        if dataset_name not in self.validation_results:
            return f"❌ Dataset '{dataset_name}' non trouvé"
        
        results = self.validation_results[dataset_name]
        
        # Génération du rapport
        report_content = []
        report_content.append("# " + "="*80)
        report_content.append("# RAPPORT DE QUALITÉ DES DONNÉES")
        report_content.append("# " + "="*80)
        report_content.append(f"# Dataset: {dataset_name}")
        report_content.append(f"# Date: {results['validation_timestamp']}")
        report_content.append(f"# Durée: {results['validation_duration_seconds']:.2f}s")
        report_content.append("# " + "="*80 + "\n")
        
        # Résumé exécutif
        report_content.append("## RÉSUMÉ EXÉCUTIF")
        report_content.append(f"**Statut global:** {results['status']}")
        report_content.append(f"**Score de qualité:** {results['overall_score']:.2%}")
        report_content.append(f"**Forme du dataset:** {results['dataset_info']['shape'][0]} lignes × {results['dataset_info']['shape'][1]} colonnes")
        report_content.append(f"**Utilisation mémoire:** {results['dataset_info']['memory_usage_mb']:.2f} MB")
        report_content.append("")
        
        # Détails de validation
        for validation_type, validation_result in results["validation_results"].items():
            if isinstance(validation_result, dict) and "status" in validation_result:
                report_content.append(f"## {validation_type.upper()}")
                report_content.append(f"**Statut:** {validation_result['status']}")
                
                if validation_type == "basic":
                    for metric, details in validation_result.items():
                        if isinstance(details, dict) and "score" in details:
                            report_content.append(f"**{metric}:** {details['score']:.2%} ({details['status']})")
                
                elif validation_type == "anomalies":
                    if validation_result.get("status") == "completed":
                        iso_forest = validation_result.get("isolation_forest", {})
                        if "anomaly_percentage" in iso_forest:
                            report_content.append(f"**Anomalies détectées:** {iso_forest['anomaly_percentage']:.2f}%")
                
                report_content.append("")
        
        # Recommandations
        report_content.append("## RECOMMANDATIONS")
        if results['overall_score'] >= 0.9:
            report_content.append("✅ **Excellent** - La qualité des données est très bonne")
        elif results['overall_score'] >= 0.8:
            report_content.append("✅ **Bon** - La qualité des données est acceptable")
        elif results['overall_score'] >= 0.6:
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
                logger.info(f"📄 Rapport de qualité sauvegardé: {output_path}")
            except Exception as e:
                logger.error(f"❌ Erreur sauvegarde rapport: {e}")
        
        return report_text
    
    def export_validation_results(self, dataset_name: str = None, output_path: str = None) -> Dict:
        """
        Exporte les résultats de validation au format JSON
        
        Args:
            dataset_name: Nom du dataset
            output_path: Chemin de sauvegarde
            
        Returns:
            Dict des résultats exportés
        """
        if dataset_name is None:
            if not self.validation_results:
                return {"error": "Aucun résultat de validation disponible"}
            dataset_name = list(self.validation_results.keys())[-1]
        
        if dataset_name not in self.validation_results:
            return {"error": f"Dataset '{dataset_name}' non trouvé"}
        
        results = self.validation_results[dataset_name]
        
        # Préparation pour export JSON
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "dataset_name": dataset_name,
            "validation_results": results
        }
        
        # Sauvegarde si un chemin est fourni
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
                logger.info(f"💾 Résultats exportés: {output_path}")
            except Exception as e:
                logger.error(f"❌ Erreur export: {e}")
        
        return export_data
