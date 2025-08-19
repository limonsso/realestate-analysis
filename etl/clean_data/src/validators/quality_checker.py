#!/usr/bin/env python3
"""
Vérificateur de qualité des données
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class QualityChecker:
    """Vérificateur de la qualité des données"""
    
    def __init__(self):
        self.quality_metrics = {}
        self.quality_issues = []
    
    def check_data_quality(self, df: pd.DataFrame) -> Dict:
        """
        Vérifie la qualité générale des données
        
        Args:
            df: DataFrame à vérifier
            
        Returns:
            Métriques de qualité
        """
        logger.info("🔍 Vérification de la qualité des données...")
        
        quality_metrics = {
            'completeness': self._check_completeness(df),
            'consistency': self._check_consistency(df),
            'accuracy': self._check_accuracy(df),
            'timeliness': self._check_timeliness(df),
            'validity': self._check_validity(df),
            'uniqueness': self._check_uniqueness(df)
        }
        
        # Calculer le score global
        scores = [metrics.get('score', 0) for metrics in quality_metrics.values()]
        overall_score = np.mean(scores) if scores else 0
        
        quality_metrics['overall'] = {
            'score': overall_score,
            'grade': self._get_quality_grade(overall_score),
            'issues_count': len(self.quality_issues)
        }
        
        self.quality_metrics = quality_metrics
        logger.info(f"✅ Qualité vérifiée - Score global: {overall_score:.1f}/100")
        
        return quality_metrics
    
    def _check_completeness(self, df: pd.DataFrame) -> Dict:
        """Vérifie la complétude des données"""
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        completeness_percent = ((total_cells - missing_cells) / total_cells) * 100
        
        # Colonnes avec le plus de données manquantes
        missing_by_column = df.isnull().sum().sort_values(ascending=False)
        problematic_columns = missing_by_column[missing_by_column > 0].head(5)
        
        return {
            'score': completeness_percent,
            'total_cells': total_cells,
            'missing_cells': missing_cells,
            'completeness_percent': completeness_percent,
            'problematic_columns': problematic_columns.to_dict()
        }
    
    def _check_consistency(self, df: pd.DataFrame) -> Dict:
        """Vérifie la cohérence des données"""
        consistency_issues = []
        
        # Vérifier la cohérence des prix
        if 'price' in df.columns and 'municipal_evaluation_total' in df.columns:
            price_eval_ratio = df['price'] / df['municipal_evaluation_total']
            extreme_ratios = price_eval_ratio[(price_eval_ratio < 0.1) | (price_eval_ratio > 10)]
            if len(extreme_ratios) > 0:
                consistency_issues.append(f"Ratios prix/évaluation extrêmes: {len(extreme_ratios)} cas")
        
        # Vérifier la cohérence des surfaces
        if 'surface' in df.columns and 'lot_size' in df.columns:
            invalid_surfaces = df[df['surface'] > df['lot_size']]
            if len(invalid_surfaces) > 0:
                consistency_issues.append(f"Surfaces > lot_size: {len(invalid_surfaces)} cas")
        
        consistency_score = max(0, 100 - len(consistency_issues) * 20)
        
        return {
            'score': consistency_score,
            'issues': consistency_issues,
            'issues_count': len(consistency_issues)
        }
    
    def _check_accuracy(self, df: pd.DataFrame) -> Dict:
        """Vérifie la précision des données"""
        accuracy_issues = []
        
        # Vérifier les valeurs négatives pour les colonnes qui ne devraient pas en avoir
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in ['price', 'surface', 'bedrooms', 'bathrooms']:
            if col in numeric_columns:
                negative_values = df[df[col] < 0]
                if len(negative_values) > 0:
                    accuracy_issues.append(f"Valeurs négatives dans {col}: {len(negative_values)} cas")
        
        # Vérifier les valeurs extrêmes
        for col in ['price', 'surface']:
            if col in numeric_columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
                if len(outliers) > 0:
                    accuracy_issues.append(f"Outliers dans {col}: {len(outliers)} cas")
        
        accuracy_score = max(0, 100 - len(accuracy_issues) * 15)
        
        return {
            'score': accuracy_score,
            'issues': accuracy_issues,
            'issues_count': len(accuracy_issues)
        }
    
    def _check_timeliness(self, df: pd.DataFrame) -> Dict:
        """Vérifie la fraîcheur des données"""
        timeliness_issues = []
        
        # Vérifier les dates de mise à jour
        date_columns = [col for col in df.columns if 'date' in col.lower() or 'at' in col.lower()]
        
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                recent_data = df[df[col] >= pd.Timestamp.now() - pd.DateOffset(months=6)]
                if len(recent_data) < len(df) * 0.5:  # Moins de 50% de données récentes
                    timeliness_issues.append(f"Données anciennes dans {col}: {len(df) - len(recent_data)} cas")
            except:
                continue
        
        timeliness_score = max(0, 100 - len(timeliness_issues) * 25)
        
        return {
            'score': timeliness_score,
            'issues': timeliness_issues,
            'issues_count': len(timeliness_issues)
        }
    
    def _check_validity(self, df: pd.DataFrame) -> Dict:
        """Vérifie la validité des données"""
        validity_issues = []
        
        # Vérifier les coordonnées géographiques
        if 'longitude' in df.columns and 'latitude' in df.columns:
            # Coordonnées du Québec
            quebec_mask = (
                (df['longitude'] >= -80) & (df['longitude'] <= -55) &
                (df['latitude'] >= 45) & (df['latitude'] <= 63)
            )
            invalid_coords = df[~quebec_mask]
            if len(invalid_coords) > 0:
                validity_issues.append(f"Coordonnées hors Québec: {len(invalid_coords)} cas")
        
        # Vérifier les types de propriétés valides
        if 'type' in df.columns:
            valid_types = ['residential', 'commercial', 'mixed', 'land']
            invalid_types = df[~df['type'].isin(valid_types)]
            if len(invalid_types) > 0:
                validity_issues.append(f"Types de propriétés invalides: {len(invalid_types)} cas")
        
        validity_score = max(0, 100 - len(validity_issues) * 20)
        
        return {
            'score': validity_score,
            'issues': validity_issues,
            'issues_count': len(validity_issues)
        }
    
    def _check_uniqueness(self, df: pd.DataFrame) -> Dict:
        """Vérifie l'unicité des données"""
        duplicates = df.duplicated().sum()
        duplicate_percent = (duplicates / len(df)) * 100
        
        uniqueness_score = max(0, 100 - duplicate_percent)
        
        return {
            'score': uniqueness_score,
            'duplicates_count': duplicates,
            'duplicate_percent': duplicate_percent
        }
    
    def _get_quality_grade(self, score: float) -> str:
        """Retourne une note basée sur le score"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B+"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        else:
            return "D"
    
    def generate_quality_report(self) -> str:
        """Génère un rapport de qualité en texte"""
        if not self.quality_metrics:
            return "Aucune métrique de qualité disponible"
        
        report = "📊 RAPPORT DE QUALITÉ DES DONNÉES\n"
        report += "=" * 50 + "\n\n"
        
        overall = self.quality_metrics.get('overall', {})
        report += f"🎯 SCORE GLOBAL: {overall.get('score', 0):.1f}/100 ({overall.get('grade', 'N/A')})\n"
        report += f"🚨 PROBLÈMES DÉTECTÉS: {overall.get('issues_count', 0)}\n\n"
        
        for category, metrics in self.quality_metrics.items():
            if category != 'overall':
                report += f"📋 {category.upper()}: {metrics.get('score', 0):.1f}/100\n"
                if 'issues' in metrics and metrics['issues']:
                    for issue in metrics['issues'][:3]:  # Top 3 issues
                        report += f"  ⚠️ {issue}\n"
                report += "\n"
        
        return report
