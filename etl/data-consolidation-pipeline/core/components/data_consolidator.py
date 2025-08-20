#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 CONSOLIDATEUR DE DONNÉES - Composant de consolidation
=========================================================

Module spécialisé dans la consolidation intelligente des variables similaires
Basé sur la détection automatique de similarités et la logique métier
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Any, Tuple
import warnings
from datetime import datetime

# Imports des modules spécialisés (avec gestion d'erreur pour compatibilité)
try:
    from ...config.consolidation_config import ConsolidationConfig, ConsolidationGroup
    from ...intelligence.similarity_detector import SimilarityDetector
    SPECIALIZED_MODULES_AVAILABLE = True
except ImportError:
    try:
        from config.consolidation_config import ConsolidationConfig, ConsolidationGroup
        from intelligence.similarity_detector import SimilarityDetector
        SPECIALIZED_MODULES_AVAILABLE = True
    except ImportError:
        SPECIALIZED_MODULES_AVAILABLE = False
        
        # Fallback classes pour quand les modules spécialisés ne sont pas disponibles
        class ConsolidationGroup:
            def __init__(self, name="default", source_columns=None, target_column="consolidated", 
                        consolidation_type="numeric", consolidation_strategy="first_valid",
                        remove_source_columns=False, post_processing=None):
                self.name = name
                self.source_columns = source_columns or []
                self.target_column = target_column
                self.consolidation_type = consolidation_type
                self.consolidation_strategy = consolidation_strategy
                self.remove_source_columns = remove_source_columns
                self.post_processing = post_processing or {}
        
        class ConsolidationConfig:
            def __init__(self):
                self.consolidation_groups = {}
        
        class SimilarityDetector:
            def __init__(self):
                pass

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class DataConsolidator:
    """
    Composant spécialisé dans la consolidation des variables similaires
    Applique la logique de consolidation basée sur la configuration
    """
    
    def __init__(self, config: ConsolidationConfig = None):
        """
        Initialise le consolidateur de données
        
        Args:
            config: Configuration de consolidation
        """
        self.config = config or ConsolidationConfig()
        self.similarity_detector = SimilarityDetector()
        self.consolidation_results = {}
        self.consolidation_stats = {}
        logger.info("🔗 DataConsolidator initialisé")
    
    def consolidate_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Point d'entrée principal pour la consolidation des variables
        
        Args:
            df: DataFrame à consolider
            
        Returns:
            DataFrame avec les variables consolidées
        """
        logger.info("🔗 === DÉBUT CONSOLIDATION DES VARIABLES ===")
        
        try:
            if df is None or df.empty:
                raise ValueError("❌ DataFrame vide pour la consolidation")
            
            start_time = datetime.now()
            initial_columns = len(df.columns)
            
            # Application de la consolidation par groupe
            df_consolidated = df.copy()
            
            for group_name, group in self.config.consolidation_groups.items():
                logger.info(f"🔗 Consolidation du groupe: {group_name}")
                
                # Vérification de la disponibilité des colonnes sources
                available_columns = [col for col in group.source_columns if col in df.columns]
                
                if not available_columns:
                    logger.warning(f"⚠️ Aucune colonne source disponible pour le groupe {group_name}")
                    continue
                
                if len(available_columns) < len(group.source_columns):
                    missing_columns = set(group.source_columns) - set(available_columns)
                    logger.warning(f"⚠️ Colonnes manquantes pour {group_name}: {missing_columns}")
                
                # Consolidation du groupe
                consolidated_column = self._consolidate_group(
                    df_consolidated, 
                    available_columns, 
                    group
                )
                
                if consolidated_column is not None:
                    # Ajout de la colonne consolidée
                    df_consolidated[group.target_column] = consolidated_column
                    
                    # Suppression des colonnes sources si demandé
                    if group.remove_source_columns:
                        df_consolidated = df_consolidated.drop(columns=available_columns)
                        logger.info(f"🗑️ Colonnes sources supprimées: {available_columns}")
                    
                    # Enregistrement des résultats
                    self.consolidation_results[group_name] = {
                        'source_columns': available_columns,
                        'target_column': group.target_column,
                        'rows_processed': len(df_consolidated),
                        'success': True
                    }
                    
                    logger.info(f"✅ Groupe {group_name} consolidé: {group.target_column}")
                else:
                    logger.warning(f"⚠️ Échec de la consolidation du groupe {group_name}")
                    self.consolidation_results[group_name] = {
                        'source_columns': available_columns,
                        'target_column': group.target_column,
                        'rows_processed': len(df_consolidated),
                        'success': False
                    }
            
            # Statistiques de consolidation
            final_columns = len(df_consolidated.columns)
            self.consolidation_stats = {
                'initial_columns': initial_columns,
                'final_columns': final_columns,
                'columns_reduced': initial_columns - final_columns,
                'reduction_percentage': ((initial_columns - final_columns) / initial_columns) * 100,
                'groups_processed': len(self.consolidation_results),
                'groups_successful': sum(1 for r in self.consolidation_results.values() if r['success']),
                'processing_time': (datetime.now() - start_time).total_seconds()
            }
            
            logger.info(f"✅ Consolidation terminée: {initial_columns} → {final_columns} colonnes")
            logger.info(f"📊 Réduction: {self.consolidation_stats['reduction_percentage']:.1f}%")
            logger.info(f"⏱️ Temps de traitement: {self.consolidation_stats['processing_time']:.2f}s")
            
            return df_consolidated
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la consolidation: {e}")
            raise
    
    def _consolidate_group(self, df: pd.DataFrame, source_columns: List[str], 
                          group: ConsolidationGroup) -> Optional[pd.Series]:
        """
        Consolidation d'un groupe spécifique de variables
        
        Args:
            df: DataFrame source
            source_columns: Colonnes sources disponibles
            group: Configuration du groupe de consolidation
            
        Returns:
            Série pandas consolidée ou None en cas d'échec
        """
        try:
            if not source_columns:
                return None
            
            # Sélection des données du groupe
            group_data = df[source_columns].copy()
            
            # Application de la stratégie de consolidation selon le type
            if group.consolidation_type == 'numeric':
                consolidated = self._consolidate_numeric_group(group_data, group)
            elif group.consolidation_type == 'categorical':
                consolidated = self._consolidate_categorical_group(group_data, group)
            elif group.consolidation_type == 'datetime':
                consolidated = self._consolidate_datetime_group(group_data, group)
            elif group.consolidation_type == 'mixed':
                consolidated = self._consolidate_mixed_group(group_data, group)
            else:
                logger.warning(f"⚠️ Type de consolidation non supporté: {group.consolidation_type}")
                return None
            
            # Validation de la colonne consolidée
            if consolidated is not None and self._validate_consolidated_column(consolidated, group):
                return consolidated
            else:
                logger.warning(f"⚠️ Validation échouée pour le groupe {group.name}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erreur consolidation groupe {group.name}: {e}")
            return None
    
    def _consolidate_numeric_group(self, data: pd.DataFrame, group: ConsolidationGroup) -> pd.Series:
        """
        Consolidation d'un groupe de variables numériques
        
        Args:
            data: Données du groupe
            group: Configuration du groupe
            
        Returns:
            Série consolidée
        """
        try:
            # Conversion en numérique
            numeric_data = data.apply(pd.to_numeric, errors='coerce')
            
            # Application de la stratégie de consolidation
            if group.consolidation_strategy == 'mean':
                consolidated = numeric_data.mean(axis=1)
            elif group.consolidation_strategy == 'median':
                consolidated = numeric_data.median(axis=1)
            elif group.consolidation_strategy == 'sum':
                consolidated = numeric_data.sum(axis=1)
            elif group.consolidation_strategy == 'max':
                consolidated = numeric_data.max(axis=1)
            elif group.consolidation_strategy == 'min':
                consolidated = numeric_data.min(axis=1)
            elif group.consolidation_strategy == 'first_valid':
                consolidated = numeric_data.apply(lambda x: x.dropna().iloc[0] if not x.dropna().empty else np.nan, axis=1)
            else:
                # Stratégie par défaut: première valeur valide
                consolidated = numeric_data.apply(lambda x: x.dropna().iloc[0] if not x.dropna().empty else np.nan, axis=1)
            
            # Application des transformations post-consolidation
            if group.post_processing:
                consolidated = self._apply_post_processing(consolidated, group.post_processing)
            
            return consolidated
            
        except Exception as e:
            logger.error(f"❌ Erreur consolidation numérique: {e}")
            return None
    
    def _consolidate_categorical_group(self, data: pd.DataFrame, group: ConsolidationGroup) -> pd.Series:
        """
        Consolidation d'un groupe de variables catégorielles
        
        Args:
            data: Données du groupe
            group: Configuration du groupe
            
        Returns:
            Série consolidée
        """
        try:
            # Conversion en string
            string_data = data.astype(str)
            
            # Application de la stratégie de consolidation
            if group.consolidation_strategy == 'first_valid':
                consolidated = string_data.apply(lambda x: x[x != 'nan'].iloc[0] if not (x == 'nan').all() else np.nan, axis=1)
            elif group.consolidation_strategy == 'most_frequent':
                consolidated = string_data.apply(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan, axis=1)
            elif group.consolidation_strategy == 'concatenate':
                consolidated = string_data.apply(lambda x: ' | '.join(x[x != 'nan']), axis=1)
            else:
                # Stratégie par défaut: première valeur valide
                consolidated = string_data.apply(lambda x: x[x != 'nan'].iloc[0] if not (x == 'nan').all() else np.nan, axis=1)
            
            # Application des transformations post-consolidation
            if group.post_processing:
                consolidated = self._apply_post_processing(consolidated, group.post_processing)
            
            return consolidated
            
        except Exception as e:
            logger.error(f"❌ Erreur consolidation catégorielle: {e}")
            return None
    
    def _consolidate_datetime_group(self, data: pd.DataFrame, group: ConsolidationGroup) -> pd.Series:
        """
        Consolidation d'un groupe de variables datetime
        
        Args:
            data: Données du groupe
            group: Configuration du groupe
            
        Returns:
            Série consolidée
        """
        try:
            # Conversion en datetime
            datetime_data = data.apply(pd.to_datetime, errors='coerce')
            
            # Application de la stratégie de consolidation
            if group.consolidation_strategy == 'latest':
                consolidated = datetime_data.max(axis=1)
            elif group.consolidation_strategy == 'earliest':
                consolidated = datetime_data.min(axis=1)
            elif group.consolidation_strategy == 'first_valid':
                consolidated = datetime_data.apply(lambda x: x.dropna().iloc[0] if not x.dropna().empty else pd.NaT, axis=1)
            else:
                # Stratégie par défaut: première valeur valide
                consolidated = datetime_data.apply(lambda x: x.dropna().iloc[0] if not x.dropna().empty else pd.NaT, axis=1)
            
            return consolidated
            
        except Exception as e:
            logger.error(f"❌ Erreur consolidation datetime: {e}")
            return None
    
    def _consolidate_mixed_group(self, data: pd.DataFrame, group: ConsolidationGroup) -> pd.Series:
        """
        Consolidation d'un groupe de variables mixtes
        
        Args:
            data: Données du groupe
            group: Configuration du groupe
            
        Returns:
            Série consolidée
        """
        try:
            # Détection automatique du type dominant
            type_counts = {}
            for col in data.columns:
                col_type = self._detect_column_type(data[col])
                type_counts[col_type] = type_counts.get(col_type, 0) + 1
            
            dominant_type = max(type_counts.items(), key=lambda x: x[1])[0]
            logger.info(f"🔍 Type dominant détecté: {dominant_type}")
            
            # Application de la consolidation selon le type dominant
            if dominant_type == 'numeric':
                return self._consolidate_numeric_group(data, group)
            elif dominant_type == 'categorical':
                return self._consolidate_categorical_group(data, group)
            elif dominant_type == 'datetime':
                return self._consolidate_datetime_group(data, group)
            else:
                # Fallback: consolidation catégorielle
                return self._consolidate_categorical_group(data, group)
                
        except Exception as e:
            logger.error(f"❌ Erreur consolidation mixte: {e}")
            return None
    
    def _detect_column_type(self, series: pd.Series) -> str:
        """Détection automatique du type de colonne"""
        try:
            # Test datetime
            if pd.api.types.is_datetime64_any_dtype(series):
                return 'datetime'
            
            # Test numérique
            if pd.api.types.is_numeric_dtype(series):
                return 'numeric'
            
            # Test catégoriel
            if pd.api.types.is_object_dtype(series) or pd.api.types.is_categorical_dtype(series):
                return 'categorical'
            
            return 'categorical'  # Par défaut
            
        except Exception:
            return 'categorical'
    
    def _validate_consolidated_column(self, consolidated_column: pd.Series, 
                                    group: ConsolidationGroup) -> bool:
        """
        Validation de la colonne consolidée
        
        Args:
            consolidated_column: Colonne à valider
            group: Configuration du groupe
            
        Returns:
            True si la validation réussit
        """
        try:
            if consolidated_column is None or consolidated_column.empty:
                return False
            
            # Vérifications de base
            checks = {
                'not_all_null': not consolidated_column.isna().all(),
                'has_values': len(consolidated_column.dropna()) > 0,
                'type_consistency': True  # À améliorer selon les besoins
            }
            
            # Vérifications spécifiques au type
            if group.consolidation_type == 'numeric':
                checks['numeric_range'] = consolidated_column.dropna().apply(lambda x: isinstance(x, (int, float, np.number))).all()
            elif group.consolidation_type == 'datetime':
                checks['datetime_format'] = consolidated_column.dropna().apply(lambda x: pd.api.types.is_datetime64_any_dtype(x) or isinstance(x, pd.Timestamp)).all()
            
            all_valid = all(checks.values())
            
            if not all_valid:
                failed_checks = [k for k, v in checks.items() if not v]
                logger.warning(f"⚠️ Validation échouée pour {group.name}: {failed_checks}")
            
            return all_valid
            
        except Exception as e:
            logger.error(f"❌ Erreur validation: {e}")
            return False
    
    def _apply_post_processing(self, series: pd.Series, post_processing: Dict) -> pd.Series:
        """Application du post-traitement sur une série"""
        try:
            result = series.copy()
            
            # Arrondi
            if 'round' in post_processing:
                result = result.round(post_processing['round'])
            
            # Normalisation
            if 'normalize' in post_processing and post_processing['normalize']:
                if result.dtype in ['float64', 'int64']:
                    result = (result - result.mean()) / result.std()
            
            # Limitation des valeurs
            if 'min_value' in post_processing:
                result = result.clip(lower=post_processing['min_value'])
            if 'max_value' in post_processing:
                result = result.clip(upper=post_processing['max_value'])
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur post-traitement: {e}")
            return series
    
    def get_consolidation_results(self) -> Dict[str, Any]:
        """Retourne les résultats de consolidation"""
        return self.consolidation_results.copy()
    
    def get_consolidation_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de consolidation"""
        return self.consolidation_stats.copy()
    
    def calculate_column_quality(self, series: pd.Series) -> float:
        """
        Calcul de la qualité d'une colonne consolidée
        
        Args:
            series: Série à évaluer
            
        Returns:
            Score de qualité entre 0 et 1
        """
        try:
            if series is None or series.empty:
                return 0.0
            
            # Métriques de qualité
            completeness = 1 - (series.isna().sum() / len(series))
            uniqueness = 1 - (series.nunique() / len(series)) if len(series) > 0 else 0
            consistency = 1.0  # À améliorer selon les besoins
            
            # Score global
            quality_score = (completeness + uniqueness + consistency) / 3
            
            return round(quality_score, 3)
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul qualité: {e}")
            return 0.0
