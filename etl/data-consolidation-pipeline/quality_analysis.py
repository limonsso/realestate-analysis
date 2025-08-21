#!/usr/bin/env python3
"""
🔍 ANALYSE DÉTAILLÉE DE LA QUALITÉ DES DONNÉES
==============================================

Script d'analyse approfondie pour identifier et résoudre les problèmes de score de qualité.
"""

import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QualityAnalyzer:
    """Analyseur de qualité des données pour identifier les problèmes spécifiques."""
    
    def __init__(self):
        self.quality_metrics = {}
        self.problems = []
        self.recommendations = []
    
    def analyze_dataframe(self, df: pd.DataFrame, source_name: str = "unknown") -> Dict[str, Any]:
        """Analyse complète d'un DataFrame pour identifier les problèmes de qualité."""
        logger.info(f"🔍 === ANALYSE DE QUALITÉ: {source_name} ===")
        logger.info(f"📊 Shape: {df.shape[0]} lignes × {df.shape[1]} colonnes")
        
        analysis = {
            'source': source_name,
            'shape': df.shape,
            'memory_usage': df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
            'columns_analysis': {},
            'quality_score': 0.0,
            'problems': [],
            'recommendations': []
        }
        
        # Analyse des colonnes
        for col in df.columns:
            col_analysis = self._analyze_column(df[col], col)
            analysis['columns_analysis'][col] = col_analysis
        
        # Calcul du score global
        analysis['quality_score'] = self._calculate_global_score(analysis['columns_analysis'])
        
        # Génération des recommandations
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _analyze_column(self, series: pd.Series, col_name: str) -> Dict[str, Any]:
        """Analyse détaillée d'une colonne."""
        analysis = {
            'name': col_name,
            'dtype': str(series.dtype),
            'null_count': series.isnull().sum(),
            'null_percentage': (series.isnull().sum() / len(series)) * 100,
            'unique_count': series.nunique(),
            'problems': [],
            'score': 100.0
        }
        
        # Détection des problèmes spécifiques
        problems = []
        
        # 1. Problème de types non-hashables
        if self._has_unhashable_types(series):
            problems.append({
                'type': 'unhashable_types',
                'severity': 'high',
                'description': 'Colonne contient des types dict/list non-hashables',
                'impact': 'Validation limitée, score réduit'
            })
            analysis['score'] -= 30
        
        # 2. Problème de valeurs manquantes
        if analysis['null_percentage'] > 50:
            problems.append({
                'type': 'high_missing_values',
                'severity': 'medium',
                'description': f"Plus de 50% de valeurs manquantes ({analysis['null_percentage']:.1f}%)",
                'impact': 'Qualité des données compromise'
            })
            analysis['score'] -= 20
        
        # 3. Problème de diversité excessive
        if analysis['unique_count'] > len(series) * 0.9:
            problems.append({
                'type': 'low_cardinality',
                'severity': 'low',
                'description': f"Cardinalité très élevée ({analysis['unique_count']} valeurs uniques)",
                'impact': 'Possible problème de normalisation'
            })
            analysis['score'] -= 10
        
        # 4. Problème de types de données
        if self._has_inconsistent_types(series):
            problems.append({
                'type': 'inconsistent_types',
                'severity': 'medium',
                'description': 'Types de données incohérents dans la colonne',
                'impact': 'Validation et traitement limités'
            })
            analysis['score'] -= 15
        
        analysis['problems'] = problems
        analysis['score'] = max(0, analysis['score'])
        
        return analysis
    
    def _has_unhashable_types(self, series: pd.Series) -> bool:
        """Vérifie si une colonne contient des types non-hashables."""
        try:
            # Test de hashabilité
            sample_values = series.dropna().head(100)
            for val in sample_values:
                if isinstance(val, (dict, list, set)):
                    return True
                try:
                    hash(val)
                except (TypeError, ValueError):
                    return True
            return False
        except Exception:
            return True
    
    def _has_inconsistent_types(self, series: pd.Series) -> bool:
        """Vérifie la cohérence des types de données."""
        try:
            non_null = series.dropna()
            if len(non_null) == 0:
                return False
            
            # Vérifier la cohérence des types
            types = set(type(val) for val in non_null.head(100))
            return len(types) > 1
        except Exception:
            return True
    
    def _calculate_global_score(self, columns_analysis: Dict) -> float:
        """Calcule le score global de qualité."""
        if not columns_analysis:
            return 0.0
        
        total_score = sum(col['score'] for col in columns_analysis.values())
        return total_score / len(columns_analysis)
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Génère des recommandations d'amélioration."""
        recommendations = []
        
        # Analyse des problèmes par type
        problem_types = {}
        for col_name, col_analysis in analysis['columns_analysis'].items():
            for problem in col_analysis['problems']:
                prob_type = problem['type']
                if prob_type not in problem_types:
                    problem_types[prob_type] = []
                problem_types[prob_type].append(col_name)
        
        # Recommandations spécifiques
        if 'unhashable_types' in problem_types:
            cols = problem_types['unhashable_types']
            recommendations.append(f"🔧 Normaliser les types complexes dans {len(cols)} colonnes: {', '.join(cols[:5])}")
            recommendations.append("   → Convertir dict/list en string avant validation")
            recommendations.append("   → Implémenter une validation MongoDB-spécifique")
        
        if 'high_missing_values' in problem_types:
            cols = problem_types['high_missing_values']
            recommendations.append(f"📊 Traiter les valeurs manquantes dans {len(cols)} colonnes: {', '.join(cols[:5])}")
            recommendations.append("   → Imputation intelligente des valeurs manquantes")
            recommendations.append("   → Analyse des patterns de manque")
        
        if 'inconsistent_types' in problem_types:
            cols = problem_types['inconsistent_types']
            recommendations.append(f"🔍 Standardiser les types dans {len(cols)} colonnes: {', '.join(cols[:5])}")
            recommendations.append("   → Conversion automatique des types")
            recommendations.append("   → Validation des conversions")
        
        # Recommandations générales
        if analysis['quality_score'] < 50:
            recommendations.append("🚨 Score critique - Révision complète de la stratégie de validation")
        elif analysis['quality_score'] < 80:
            recommendations.append("⚠️ Score faible - Améliorations ciblées nécessaires")
        else:
            recommendations.append("✅ Score acceptable - Optimisations mineures possibles")
        
        return recommendations
    
    def generate_report(self, analysis: Dict, output_file: str = None) -> str:
        """Génère un rapport d'analyse détaillé."""
        report = []
        report.append("# 🔍 RAPPORT D'ANALYSE DE QUALITÉ DÉTAILLÉ")
        report.append("")
        report.append(f"## 📊 Vue d'ensemble")
        report.append(f"- **Source:** {analysis['source']}")
        report.append(f"- **Shape:** {analysis['shape'][0]} lignes × {analysis['shape'][1]} colonnes")
        report.append(f"- **Mémoire:** {analysis['memory_usage']:.2f} MB")
        report.append(f"- **Score global:** {analysis['quality_score']:.2f}%")
        report.append("")
        
        # Problèmes identifiés
        all_problems = []
        for col_name, col_analysis in analysis['columns_analysis'].items():
            for problem in col_analysis['problems']:
                all_problems.append((col_name, problem))
        
        if all_problems:
            report.append("## 🚨 Problèmes Identifiés")
            report.append("")
            for col_name, problem in all_problems:
                report.append(f"### {col_name}")
                report.append(f"- **Type:** {problem['type']}")
                report.append(f"- **Sévérité:** {problem['severity']}")
                report.append(f"- **Description:** {problem['description']}")
                report.append(f"- **Impact:** {problem['impact']}")
                report.append("")
        else:
            report.append("## ✅ Aucun problème identifié")
            report.append("")
        
        # Analyse des colonnes
        report.append("## 📋 Analyse des Colonnes")
        report.append("")
        for col_name, col_analysis in analysis['columns_analysis'].items():
            report.append(f"### {col_name}")
            report.append(f"- **Type:** {col_analysis['dtype']}")
            report.append(f"- **Valeurs manquantes:** {col_analysis['null_count']} ({col_analysis['null_percentage']:.1f}%)")
            report.append(f"- **Valeurs uniques:** {col_analysis['unique_count']}")
            report.append(f"- **Score:** {col_analysis['score']:.1f}%")
            if col_analysis['problems']:
                report.append(f"- **Problèmes:** {len(col_analysis['problems'])}")
            report.append("")
        
        # Recommandations
        if analysis['recommendations']:
            report.append("## 💡 Recommandations d'Amélioration")
            report.append("")
            for rec in analysis['recommendations']:
                report.append(rec)
            report.append("")
        
        report_text = "\n".join(report)
        
        # Sauvegarde du rapport
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            logger.info(f"📄 Rapport sauvegardé: {output_file}")
        
        return report_text

def main():
    """Fonction principale d'analyse de qualité."""
    logger.info("🚀 === DÉMARRAGE ANALYSE DE QUALITÉ ===")
    
    # Créer l'analyseur
    analyzer = QualityAnalyzer()
    
    # Analyser les données MongoDB exportées
    csv_file = "exports/trois_rivieres_plex/real_estate_data_modular_pipeline_20250820_200043.csv"
    
    if Path(csv_file).exists():
        logger.info(f"📁 Lecture du fichier CSV: {csv_file}")
        df = pd.read_csv(csv_file)
        
        # Analyse complète
        analysis = analyzer.analyze_dataframe(df, "Trois-Rivières Plex (MongoDB)")
        
        # Génération du rapport
        output_file = "exports/trois_rivieres_plex/quality_analysis_detailed.md"
        report = analyzer.generate_report(analysis, output_file)
        
        # Affichage du résumé
        logger.info("📊 === RÉSUMÉ DE L'ANALYSE ===")
        logger.info(f"Score global: {analysis['quality_score']:.2f}%")
        logger.info(f"Problèmes identifiés: {sum(len(col['problems']) for col in analysis['columns_analysis'].values())}")
        logger.info(f"Recommandations: {len(analysis['recommendations'])}")
        
        # Affichage des problèmes principaux
        if analysis['recommendations']:
            logger.info("💡 Principales recommandations:")
            for rec in analysis['recommendations'][:3]:
                logger.info(f"  - {rec}")
        
        logger.info(f"📄 Rapport détaillé: {output_file}")
        
    else:
        logger.error(f"❌ Fichier non trouvé: {csv_file}")
        logger.info("💡 Exécutez d'abord le pipeline MongoDB pour générer les données")

if __name__ == "__main__":
    main()
