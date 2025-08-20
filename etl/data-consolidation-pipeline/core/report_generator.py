#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 GÉNÉRATEUR DE RAPPORTS
==========================

Gère la génération des rapports de qualité, similarités et export
"""

import logging
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
import time
import json

logger = logging.getLogger(__name__)

class ReportGenerator:
    """
    Générateur de rapports pour le pipeline ETL
    
    Responsable de la génération des rapports de qualité,
    de similarités et d'export
    """
    
    def __init__(self, pipeline_manager):
        """
        Initialise le générateur de rapports
        
        Args:
            pipeline_manager: Instance du gestionnaire de pipeline
        """
        self.pipeline_manager = pipeline_manager
        self.reports = {}
    
    def generate_all_reports(self, df_initial: pd.DataFrame, df_final: pd.DataFrame,
                            initial_validation: Dict, final_validation: Dict,
                            similarity_groups: List, exported_files: Dict,
                            output_dir: str) -> Dict[str, str]:
        """
        Génère tous les rapports du pipeline
        
        Args:
            df_initial: DataFrame initial
            df_final: DataFrame final traité
            initial_validation: Résultats validation initiale
            final_validation: Résultats validation finale
            similarity_groups: Groupes de similarités détectés
            exported_files: Fichiers exportés
            output_dir: Répertoire de sortie
            
        Returns:
            Dict avec les chemins des rapports générés
        """
        logger.info("📊 === PHASE 7: GÉNÉRATION DES RAPPORTS ===")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        try:
            # === RAPPORT DE SIMILARITÉS ===
            logger.info("📊 Génération du rapport de similarités...")
            similarity_report = self._generate_similarity_report(
                similarity_groups, output_path, timestamp
            )
            self.reports["similarity"] = similarity_report
            
            # === RAPPORT DE QUALITÉ ===
            logger.info("✅ Génération du rapport de qualité...")
            quality_report = self._generate_quality_report(
                initial_validation, final_validation, output_path, timestamp
            )
            self.reports["quality"] = quality_report
            
            # === RAPPORT D'EXPORT ===
            logger.info("💾 Génération du rapport d'export...")
            export_report = self._generate_export_report(
                exported_files, output_path, timestamp
            )
            self.reports["export"] = export_report
            
            # === RAPPORT COMPLET ===
            logger.info("📋 Génération du rapport complet...")
            complete_report = self._generate_complete_report(
                df_initial, df_final, initial_validation, final_validation,
                similarity_groups, exported_files, output_path, timestamp
            )
            self.reports["complete"] = complete_report
            
            logger.info(f"✅ {len(self.reports)} rapports générés dans {output_dir}")
            return self.reports
            
        except Exception as e:
            logger.error(f"❌ Erreur génération rapports: {e}")
            return {}
    
    def _generate_similarity_report(self, similarity_groups: List, 
                                   output_path: Path, timestamp: str) -> str:
        """Génère le rapport de similarités"""
        try:
            if self.pipeline_manager.similarity_detector:
                # Utilisation du détecteur de similarités pour générer le rapport
                report_content = self.pipeline_manager.similarity_detector.generate_similarity_report(
                    similarity_groups, output_path, timestamp
                )
                return report_content
            else:
                # Rapport basique
                filename = f"similarity_report_{timestamp}.md"
                filepath = output_path / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# 📊 Rapport de Similarités - {timestamp}\n\n")
                    f.write(f"## 🎯 Groupes de Similarités Détectés\n\n")
                    f.write(f"**Total:** {len(similarity_groups)} groupes\n\n")
                    
                    for i, group in enumerate(similarity_groups, 1):
                        f.write(f"### Groupe {i}\n")
                        f.write(f"- **Colonnes:** {', '.join(group.get('columns', []))}\n")
                        f.write(f"- **Score de similarité:** {group.get('similarity_score', 'N/A')}\n")
                        f.write(f"- **Type de similarité:** {group.get('similarity_type', 'N/A')}\n\n")
                
                logger.info(f"📄 Rapport sauvegardé: {filepath}")
                return str(filepath)
                
        except Exception as e:
            logger.error(f"❌ Erreur rapport similarités: {e}")
            return ""
    
    def _generate_quality_report(self, initial_validation: Dict, final_validation: Dict,
                                output_path: Path, timestamp: str) -> str:
        """Génère le rapport de qualité"""
        try:
            filename = f"quality_report_{timestamp}.md"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# ✅ Rapport de Qualité - {timestamp}\n\n")
                
                # Validation initiale
                f.write("## 📊 Validation Initiale\n\n")
                f.write(f"- **Score global:** {initial_validation.get('overall_score', 0):.2%}\n")
                f.write(f"- **Statut:** {initial_validation.get('status', 'UNKNOWN')}\n")
                f.write(f"- **Métriques:**\n")
                
                metrics = initial_validation.get('metrics', {})
                for metric_name, metric_value in metrics.items():
                    if isinstance(metric_value, (int, float)):
                        f.write(f"  - {metric_name}: {metric_value:.2f}\n")
                    else:
                        f.write(f"  - {metric_name}: {metric_value}\n")
                
                f.write("\n## 📊 Validation Finale\n\n")
                f.write(f"- **Score global:** {final_validation.get('overall_score', 0):.2%}\n")
                f.write(f"- **Statut:** {final_validation.get('status', 'UNKNOWN')}\n")
                f.write(f"- **Métriques:**\n")
                
                metrics = final_validation.get('metrics', {})
                for metric_name, metric_value in metrics.items():
                    if isinstance(metric_value, (int, float)):
                        f.write(f"  - {metric_name}: {metric_value:.2f}\n")
                    else:
                        f.write(f"  - {metric_name}: {metric_value}\n")
            
            logger.info(f"📄 Rapport de qualité sauvegardé: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erreur rapport qualité: {e}")
            return ""
    
    def _generate_export_report(self, exported_files: Dict, 
                                output_path: Path, timestamp: str) -> str:
        """Génère le rapport d'export"""
        try:
            filename = f"export_report_{timestamp}.md"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# 💾 Rapport d'Export - {timestamp}\n\n")
                f.write(f"## 📊 Résumé des Exports\n\n")
                f.write(f"- **Total formats:** {len(exported_files)}\n")
                f.write(f"- **Statut:** {'✅ Succès' if exported_files else '❌ Échec'}\n\n")
                
                f.write("## 📁 Fichiers Exportés\n\n")
                for format_type, filepath_export in exported_files.items():
                    f.write(f"### {format_type.upper()}\n")
                    f.write(f"- **Chemin:** {filepath_export}\n")
                    f.write(f"- **Taille:** {Path(filepath_export).stat().st_size / 1024:.1f} KB\n\n")
            
            logger.info(f"📄 Rapport d'export sauvegardé: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erreur rapport export: {e}")
            return ""
    
    def _generate_complete_report(self, df_initial: pd.DataFrame, df_final: pd.DataFrame,
                                 initial_validation: Dict, final_validation: Dict,
                                 similarity_groups: List, exported_files: Dict,
                                 output_path: Path, timestamp: str) -> str:
        """Génère le rapport complet du pipeline"""
        try:
            filename = f"pipeline_report_{timestamp}.md"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# 🚀 Rapport Complet du Pipeline - {timestamp}\n\n")
                
                # Résumé exécutif
                f.write("## 📋 Résumé Exécutif\n\n")
                f.write(f"- **Date d'exécution:** {timestamp}\n")
                f.write(f"- **Données initiales:** {df_initial.shape[0]} lignes × {df_initial.shape[1]} colonnes\n")
                f.write(f"- **Données finales:** {df_final.shape[0]} lignes × {df_final.shape[1]} colonnes\n")
                f.write(f"- **Réduction colonnes:** {((df_initial.shape[1] - df_final.shape[1]) / df_initial.shape[1]) * 100:.1f}%\n")
                f.write(f"- **Groupes de similarités:** {len(similarity_groups)}\n")
                f.write(f"- **Formats exportés:** {len(exported_files)}\n\n")
                
                # Qualité des données
                f.write("## ✅ Qualité des Données\n\n")
                f.write(f"- **Score initial:** {initial_validation.get('overall_score', 0):.2%}\n")
                f.write(f"- **Score final:** {final_validation.get('overall_score', 0):.2%}\n")
                f.write(f"- **Amélioration:** {final_validation.get('overall_score', 0) - initial_validation.get('overall_score', 0):.2%}\n\n")
                
                # Similarités détectées
                f.write("## 🧠 Similarités Détectées\n\n")
                for i, group in enumerate(similarity_groups, 1):
                    f.write(f"### Groupe {i}\n")
                    f.write(f"- **Colonnes:** {', '.join(group.get('columns', []))}\n")
                    f.write(f"- **Score:** {group.get('similarity_score', 'N/A')}\n\n")
                
                # Exports
                f.write("## 💾 Exports\n\n")
                for format_type, filepath_export in exported_files.items():
                    f.write(f"- **{format_type.upper()}:** {filepath_export}\n")
            
            logger.info(f"📄 Rapport complet sauvegardé: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Erreur rapport complet: {e}")
            return ""
    
    def get_reports_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des rapports générés"""
        return {
            "total_reports": len(self.reports),
            "report_types": list(self.reports.keys()),
            "reports": self.reports,
            "generation_status": "success" if self.reports else "failed"
        }
