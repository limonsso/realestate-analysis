#!/usr/bin/env python3
"""
Exporteur de rapports et métriques
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ReportExporter:
    """Gère l'export des rapports de qualité et analyses"""
    
    def __init__(self, reports_dir: Path):
        self.reports_dir = reports_dir
        self.ensure_reports_dir()
    
    def ensure_reports_dir(self):
        """S'assure que le dossier des rapports existe"""
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def export_quality_report(self, df: pd.DataFrame, validation_results: dict = None) -> Path:
        """
        Crée et exporte un rapport de qualité des données
        
        Args:
            df: DataFrame nettoyé
            validation_results: Résultats de validation
            
        Returns:
            Chemin vers le rapport créé
        """
        logger.info("📊 Création du rapport de qualité...")
        
        # Fonction pour convertir les types pandas/numpy en types Python natifs
        def convert_to_serializable(obj):
            """Convertit les types pandas/numpy en types JSON sérialisables"""
            if isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
                return int(obj)
            elif isinstance(obj, (np.float64, np.float32)):
                return float(obj)
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif pd.isna(obj):
                return None
            else:
                return obj
        
        # Statistiques générales avec conversion
        quality_report = {
            'timestamp': datetime.now().isoformat(),
            'dataset_info': {
                'total_records': int(len(df)),
                'total_columns': int(len(df.columns)),
                'memory_usage_mb': float(df.memory_usage(deep=True).sum() / 1024**2)
            },
            'data_quality': {
                'completeness_score_mean': float(df['completeness_score'].mean()) if 'completeness_score' in df.columns else 0.0,
                'missing_data_percentage': float((df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100)
            },
            'validation_summary': validation_results or {}
        }
        
        # Sauvegarder le rapport
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.reports_dir / f"quality_report_{timestamp}.json"
        
        # Encoder personnalisé pour gérer les types pandas/numpy
        class NumpyEncoder(json.JSONEncoder):
            def default(self, obj):
                return convert_to_serializable(obj)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(quality_report, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
        
        logger.info(f"✅ Rapport de qualité créé: {report_file}")
        return report_file
    
    def export_cleaning_summary(self, df_original: pd.DataFrame, df_cleaned: pd.DataFrame, 
                               cleaning_stats: dict) -> Path:
        """
        Crée un résumé du processus de nettoyage
        
        Args:
            df_original: DataFrame original
            df_cleaned: DataFrame nettoyé
            cleaning_stats: Statistiques du nettoyage
            
        Returns:
            Chemin vers le résumé créé
        """
        logger.info("📋 Création du résumé de nettoyage...")
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'cleaning_summary': {
                'original_shape': df_original.shape,
                'cleaned_shape': df_cleaned.shape,
                'records_removed': df_original.shape[0] - df_cleaned.shape[0],
                'columns_removed': df_original.shape[1] - df_cleaned.shape[1],
                'duplicates_removed': cleaning_stats.get('duplicates_removed', 0),
                'columns_consolidated': cleaning_stats.get('columns_consolidated', 0)
            },
            'data_improvements': {
                'missing_data_reduction': self._calculate_missing_reduction(df_original, df_cleaned),
                'data_type_improvements': self._analyze_data_types(df_original, df_cleaned)
            }
        }
        
        # Sauvegarder le résumé
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_file = self.reports_dir / f"cleaning_summary_{timestamp}.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Résumé de nettoyage créé: {summary_file}")
        return summary_file
    
    def _calculate_missing_reduction(self, df_original: pd.DataFrame, df_cleaned: pd.DataFrame) -> dict:
        """Calcule la réduction des données manquantes"""
        original_missing = df_original.isnull().sum().sum()
        cleaned_missing = df_cleaned.isnull().sum().sum()
        
        if original_missing > 0:
            reduction_percent = ((original_missing - cleaned_missing) / original_missing) * 100
        else:
            reduction_percent = 0
        
        return {
            'original_missing': int(original_missing),
            'cleaned_missing': int(cleaned_missing),
            'reduction_percent': float(reduction_percent)
        }
    
    def _analyze_data_types(self, df_original: pd.DataFrame, df_cleaned: pd.DataFrame) -> dict:
        """Analyse les améliorations des types de données"""
        original_dtypes = df_original.dtypes.value_counts().to_dict()
        cleaned_dtypes = df_cleaned.dtypes.value_counts().to_dict()
        
        # Convertir en types sérialisables
        original_dtypes = {str(k): str(v) for k, v in original_dtypes.items()}
        cleaned_dtypes = {str(k): str(v) for k, v in cleaned_dtypes.items()}
        
        return {
            'original_dtypes': original_dtypes,
            'cleaned_dtypes': cleaned_dtypes
        }
