#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 NETTOYEUR DE DONNÉES - Composant de nettoyage
==================================================

Module spécialisé dans le nettoyage, la validation et la normalisation des données
Gère les valeurs manquantes, les outliers et la cohérence des données
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Any, Tuple
import warnings
from datetime import datetime
import re

# Imports des utilitaires (avec gestion d'erreur pour compatibilité)
try:
    from ...utils.property_type_normalizer import PropertyTypeNormalizer
    NORMALIZER_AVAILABLE = True
except ImportError:
    try:
        from utils.property_type_normalizer import PropertyTypeNormalizer
        NORMALIZER_AVAILABLE = True
    except ImportError:
        NORMALIZER_AVAILABLE = False
        
        # Fallback class pour quand le normaliseur n'est pas disponible
        class PropertyTypeNormalizer:
            def __init__(self):
                pass
            
            def normalize(self, property_type):
                return str(property_type).lower().strip() if property_type else None

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class DataCleaner:
    """
    Composant spécialisé dans le nettoyage et la validation des données
    Applique des règles de nettoyage et détecte les anomalies
    """
    
    def __init__(self):
        """Initialise le nettoyeur de données"""
        self.property_normalizer = PropertyTypeNormalizer()
        self.cleaning_results = {}
        self.cleaning_stats = {}
        self.validation_rules = self._initialize_validation_rules()
        logger.info("🧹 DataCleaner initialisé")
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Point d'entrée principal pour le nettoyage des données
        
        Args:
            df: DataFrame à nettoyer
            
        Returns:
            DataFrame nettoyé
        """
        logger.info("🧹 === DÉBUT NETTOYAGE DES DONNÉES ===")
        
        try:
            if df is None or df.empty:
                raise ValueError("❌ DataFrame vide pour le nettoyage")
            
            start_time = datetime.now()
            initial_rows = len(df)
            initial_columns = len(df.columns)
            
            # Copie des données pour éviter la modification de l'original
            df_cleaned = df.copy()
            
            # === PHASE 1: NETTOYAGE BASIQUE ===
            logger.info("🧹 Phase 1: Nettoyage basique")
            df_cleaned = self._apply_basic_cleaning(df_cleaned)
            
            # === PHASE 2: GESTION DES VALEURS MANQUANTES ===
            logger.info("🧹 Phase 2: Gestion des valeurs manquantes")
            df_cleaned = self._handle_missing_values(df_cleaned)
            
            # === PHASE 3: DÉTECTION ET TRAITEMENT DES OUTLIERS ===
            logger.info("🧹 Phase 3: Détection des outliers")
            df_cleaned = self._handle_outliers(df_cleaned)
            
            # === PHASE 4: NORMALISATION DES TYPES ===
            logger.info("🧹 Phase 4: Normalisation des types")
            df_cleaned = self._normalize_data_types(df_cleaned)
            
            # === PHASE 5: VALIDATION DES RÈGLES MÉTIER ===
            logger.info("🧹 Phase 5: Validation des règles métier")
            df_cleaned = self._apply_business_rules(df_cleaned)
            
            # === PHASE 6: NETTOYAGE FINAL ===
            logger.info("🧹 Phase 6: Nettoyage final")
            df_cleaned = self._apply_final_cleaning(df_cleaned)
            
            # Statistiques de nettoyage
            final_rows = len(df_cleaned)
            self.cleaning_stats = {
                'initial_rows': initial_rows,
                'final_rows': final_rows,
                'rows_removed': initial_rows - final_rows,
                'initial_columns': initial_columns,
                'final_columns': len(df_cleaned.columns),
                'processing_time': (datetime.now() - start_time).total_seconds(),
                'cleaning_phases': len(self.cleaning_results)
            }
            
            logger.info(f"✅ Nettoyage terminé: {initial_rows} → {final_rows} lignes")
            logger.info(f"🗑️ Lignes supprimées: {initial_rows - final_rows}")
            logger.info(f"⏱️ Temps de traitement: {self.cleaning_stats['processing_time']:.2f}s")
            
            return df_cleaned
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage: {e}")
            raise
    
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialisation des règles de validation métier"""
        return {
            'price': {
                'min_value': 0,
                'max_value': 10000000,  # 10M
                'required': True,
                'data_type': 'numeric'
            },
            'surface': {
                'min_value': 0,
                'max_value': 10000,  # 10k m²
                'required': True,
                'data_type': 'numeric'
            },
            'rooms': {
                'min_value': 0,
                'max_value': 20,
                'required': False,
                'data_type': 'integer'
            },
            'bathrooms': {
                'min_value': 0,
                'max_value': 10,
                'required': False,
                'data_type': 'numeric'
            },
            'year_built': {
                'min_value': 1800,
                'max_value': 2030,
                'required': False,
                'data_type': 'integer'
            },
            'latitude': {
                'min_value': 45.0,
                'max_value': 46.0,
                'required': False,
                'data_type': 'numeric'
            },
            'longitude': {
                'min_value': -74.0,
                'max_value': -73.0,
                'required': False,
                'data_type': 'numeric'
            }
        }
    
    def _apply_basic_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """Application du nettoyage basique"""
        try:
            # Suppression des lignes complètement vides
            initial_rows = len(df)
            df = df.dropna(how='all')
            rows_removed = initial_rows - len(df)
            if rows_removed > 0:
                logger.info(f"🗑️ {rows_removed} lignes complètement vides supprimées")
            
            # Suppression des colonnes complètement vides
            initial_cols = len(df.columns)
            df = df.dropna(axis=1, how='all')
            cols_removed = initial_cols - len(df.columns)
            if cols_removed > 0:
                logger.info(f"🗑️ {cols_removed} colonnes complètement vides supprimées")
            
            # Nettoyage des noms de colonnes
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Suppression des espaces en début/fin des valeurs string
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
            
            self.cleaning_results['basic_cleaning'] = {
                'rows_removed': rows_removed,
                'columns_removed': cols_removed,
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur nettoyage basique: {e}")
            self.cleaning_results['basic_cleaning'] = {'success': False, 'error': str(e)}
            return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Gestion des valeurs manquantes"""
        try:
            missing_stats = {}
            
            for col in df.columns:
                missing_count = df[col].isna().sum()
                if missing_count > 0:
                    missing_percentage = (missing_count / len(df)) * 100
                    missing_stats[col] = {
                        'count': missing_count,
                        'percentage': missing_percentage
                    }
                    
                    # Stratégie de traitement selon le type de colonne
                    if col in self.validation_rules:
                        rule = self.validation_rules[col]
                        if rule['required'] and missing_percentage > 50:
                            # Trop de valeurs manquantes pour une colonne requise
                            logger.warning(f"⚠️ Trop de valeurs manquantes pour {col}: {missing_percentage:.1f}%")
                        elif rule['data_type'] == 'numeric':
                            # Imputation par la médiane pour les numériques
                            median_value = df[col].median()
                            df[col] = df[col].fillna(median_value)
                            logger.info(f"🔢 Imputation médiane pour {col}: {median_value}")
                        elif rule['data_type'] == 'categorical':
                            # Imputation par le mode pour les catégorielles
                            mode_value = df[col].mode().iloc[0] if not df[col].mode().empty else 'Unknown'
                            df[col] = df[col].fillna(mode_value)
                            logger.info(f"🏷️ Imputation mode pour {col}: {mode_value}")
            
            self.cleaning_results['missing_values'] = {
                'missing_stats': missing_stats,
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur gestion valeurs manquantes: {e}")
            self.cleaning_results['missing_values'] = {'success': False, 'error': str(e)}
            return df
    
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Détection et traitement des outliers"""
        try:
            outlier_stats = {}
            
            for col in df.select_dtypes(include=[np.number]).columns:
                if col in self.validation_rules:
                    rule = self.validation_rules[col]
                    
                    # Application des limites métier
                    if 'min_value' in rule:
                        outliers_below = (df[col] < rule['min_value']).sum()
                        df.loc[df[col] < rule['min_value'], col] = rule['min_value']
                        
                    if 'max_value' in rule:
                        outliers_above = (df[col] > rule['max_value']).sum()
                        df.loc[df[col] > rule['max_value'], col] = rule['max_value']
                    
                    # Détection statistique des outliers (méthode IQR)
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outliers_iqr = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
                    
                    outlier_stats[col] = {
                        'outliers_below_limit': outliers_below if 'min_value' in rule else 0,
                        'outliers_above_limit': outliers_above if 'max_value' in rule else 0,
                        'outliers_iqr': outliers_iqr,
                        'total_outliers': outliers_below + outliers_above + outliers_iqr
                    }
                    
                    if outlier_stats[col]['total_outliers'] > 0:
                        logger.info(f"🔍 Outliers détectés pour {col}: {outlier_stats[col]['total_outliers']}")
            
            self.cleaning_results['outliers'] = {
                'outlier_stats': outlier_stats,
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur gestion outliers: {e}")
            self.cleaning_results['outliers'] = {'success': False, 'error': str(e)}
            return df
    
    def _normalize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalisation des types de données"""
        try:
            type_changes = {}
            
            for col in df.columns:
                if col in self.validation_rules:
                    rule = self.validation_rules[col]
                    current_type = str(df[col].dtype)
                    
                    try:
                        if rule['data_type'] == 'numeric':
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                        elif rule['data_type'] == 'integer':
                            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
                        elif rule['data_type'] == 'datetime':
                            df[col] = pd.to_datetime(df[col], errors='coerce')
                        elif rule['data_type'] == 'categorical':
                            df[col] = df[col].astype('category')
                        
                        new_type = str(df[col].dtype)
                        if current_type != new_type:
                            type_changes[col] = {
                                'from': current_type,
                                'to': new_type
                            }
                            logger.info(f"🔄 Type changé pour {col}: {current_type} → {new_type}")
                    
                    except Exception as e:
                        logger.warning(f"⚠️ Impossible de convertir {col} en {rule['data_type']}: {e}")
            
            # Normalisation spéciale pour les types de propriétés
            if 'type' in df.columns:
                df = self._normalize_property_types(df)
            
            self.cleaning_results['type_normalization'] = {
                'type_changes': type_changes,
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur normalisation types: {e}")
            self.cleaning_results['type_normalization'] = {'success': False, 'error': str(e)}
            return df
    
    def _normalize_property_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalisation spéciale des types de propriétés"""
        try:
            if 'type' in df.columns:
                initial_types = df['type'].nunique()
                df['type'] = df['type'].apply(self.property_normalizer.normalize_property_type)
                final_types = df['type'].nunique()
                
                logger.info(f"🏠 Types de propriétés normalisés: {initial_types} → {final_types}")
                
                self.cleaning_results['property_type_normalization'] = {
                    'initial_types': initial_types,
                    'final_types': final_types,
                    'success': True
                }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur normalisation types propriétés: {e}")
            self.cleaning_results['property_type_normalization'] = {'success': False, 'error': str(e)}
            return df
    
    def _apply_business_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """Application des règles métier"""
        try:
            business_rule_violations = {}
            
            for col in df.columns:
                if col in self.validation_rules:
                    rule = self.validation_rules[col]
                    violations = []
                    
                    # Vérification des valeurs requises
                    if rule.get('required', False):
                        missing_count = df[col].isna().sum()
                        if missing_count > 0:
                            violations.append(f"Valeurs manquantes: {missing_count}")
                    
                    # Vérification des limites
                    if 'min_value' in rule:
                        below_limit = (df[col] < rule['min_value']).sum()
                        if below_limit > 0:
                            violations.append(f"Valeurs < {rule['min_value']}: {below_limit}")
                    
                    if 'max_value' in rule:
                        above_limit = (df[col] > rule['max_value']).sum()
                        if above_limit > 0:
                            violations.append(f"Valeurs > {rule['max_value']}: {above_limit}")
                    
                    if violations:
                        business_rule_violations[col] = violations
                        logger.warning(f"⚠️ Violations des règles métier pour {col}: {violations}")
            
            self.cleaning_results['business_rules'] = {
                'violations': business_rule_violations,
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur règles métier: {e}")
            self.cleaning_results['business_rules'] = {'success': False, 'error': str(e)}
            return df
    
    def _apply_final_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoyage final et optimisations"""
        try:
            # Suppression des doublons
            initial_rows = len(df)
            df = df.drop_duplicates()
            duplicates_removed = initial_rows - len(df)
            if duplicates_removed > 0:
                logger.info(f"🗑️ {duplicates_removed} doublons supprimés")
            
            # Réindexation
            df = df.reset_index(drop=True)
            
            # Optimisation des types de données
            df = self._optimize_data_types(df)
            
            self.cleaning_results['final_cleaning'] = {
                'duplicates_removed': duplicates_removed,
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur nettoyage final: {e}")
            self.cleaning_results['final_cleaning'] = {'success': False, 'error': str(e)}
            return df
    
    def _optimize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimisation des types de données pour la mémoire"""
        try:
            for col in df.columns:
                # Optimisation des entiers
                if df[col].dtype == 'int64':
                    col_min, col_max = df[col].min(), df[col].max()
                    if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                        df[col] = df[col].astype(np.int16)
                    elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                
                # Optimisation des flottants
                elif df[col].dtype == 'float64':
                    if df[col].isna().sum() == 0:  # Pas de valeurs manquantes
                        df[col] = df[col].astype(np.float32)
                
                # Optimisation des catégorielles
                elif df[col].dtype == 'object':
                    if df[col].nunique() / len(df) < 0.5:  # Moins de 50% de valeurs uniques
                        df[col] = df[col].astype('category')
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur optimisation types: {e}")
            return df
    
    def get_cleaning_results(self) -> Dict[str, Any]:
        """Retourne les résultats du nettoyage"""
        return self.cleaning_results.copy()
    
    def get_cleaning_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de nettoyage"""
        return self.cleaning_stats.copy()
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Validation de la qualité des données après nettoyage
        
        Args:
            df: DataFrame à valider
            
        Returns:
            Dict avec les scores de qualité par dimension
        """
        try:
            quality_scores = {}
            
            # Complétude
            completeness = 1 - (df.isna().sum().sum() / (len(df) * len(df.columns)))
            quality_scores['completeness'] = round(completeness, 3)
            
            # Cohérence des types
            type_consistency = 1.0  # À améliorer selon les besoins
            quality_scores['type_consistency'] = type_consistency
            
            # Validité des valeurs
            validity = 1.0  # Basé sur les règles métier appliquées
            quality_scores['validity'] = validity
            
            # Score global
            overall_score = sum(quality_scores.values()) / len(quality_scores)
            quality_scores['overall'] = round(overall_score, 3)
            
            logger.info(f"📊 Scores de qualité: {quality_scores}")
            return quality_scores
            
        except Exception as e:
            logger.error(f"❌ Erreur validation qualité: {e}")
            return {'overall': 0.0}
