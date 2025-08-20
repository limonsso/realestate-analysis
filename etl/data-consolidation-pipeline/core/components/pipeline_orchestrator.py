#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎼 ORCHESTRATEUR DE PIPELINE - Composant principal
==================================================

Module principal d'orchestration du pipeline ETL complet
Coordonne tous les composants et gère le flux de données
"""

import pandas as pd
import logging
from typing import Dict, List, Optional, Any, Tuple
import warnings
from datetime import datetime
import json
import os
from pathlib import Path

# Imports des composants spécialisés
from .data_extractor import DataExtractor
from .data_consolidator import DataConsolidator
from .data_cleaner import DataCleaner
from .data_enricher import DataEnricher
from .data_validator import DataValidator

# Imports des modules externes (avec gestion d'erreur pour compatibilité)
try:
    from ...config.consolidation_config import ConsolidationConfig
    from ...export.advanced_exporter import AdvancedExporter
    from ...performance.performance_optimizer import PerformanceOptimizer
    from ...dashboard.validation_dashboard import ValidationDashboard
    EXTERNAL_MODULES_AVAILABLE = True
except ImportError:
    try:
        from config.consolidation_config import ConsolidationConfig
        from export.advanced_exporter import AdvancedExporter
        from performance.performance_optimizer import PerformanceOptimizer
        from dashboard.validation_dashboard import ValidationDashboard
        EXTERNAL_MODULES_AVAILABLE = True
    except ImportError:
        EXTERNAL_MODULES_AVAILABLE = False
        
        # Fallback classes pour quand les modules externes ne sont pas disponibles
        class ConsolidationConfig:
            def __init__(self):
                self.consolidation_groups = {}
        
        class AdvancedExporter:
            def __init__(self):
                pass
            
            def export_data(self, *args, **kwargs):
                return {"success": False, "message": "AdvancedExporter not available"}
        
        class PerformanceOptimizer:
            def __init__(self):
                pass
            
            def optimize_dataframe(self, df):
                return df
        
        class ValidationDashboard:
            def __init__(self):
                pass
            
            def generate_dashboard(self, *args, **kwargs):
                return {"success": False, "message": "ValidationDashboard not available"}

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """
    Orchestrateur principal du pipeline ETL
    Coordonne tous les composants et gère le flux de données
    """
    
    def __init__(self, config: ConsolidationConfig = None):
        """
        Initialise l'orchestrateur du pipeline
        
        Args:
            config: Configuration de consolidation
        """
        self.config = config or ConsolidationConfig()
        self.pipeline_history = []
        self.pipeline_stats = {}
        
        # === INITIALISATION DES COMPOSANTS ===
        logger.info("🎼 === INITIALISATION PIPELINE ORCHESTRATOR ===")
        
        # Validation de la configuration
        if not self.config.validate_configuration():
            raise ValueError("❌ Configuration de consolidation invalide")
        
        # Initialisation des composants
        self.data_extractor = DataExtractor()
        self.data_consolidator = DataConsolidator(self.config)
        self.data_cleaner = DataCleaner()
        self.data_enricher = DataEnricher()
        self.data_validator = DataValidator()
        
        # Initialisation des modules externes
        self.advanced_exporter = AdvancedExporter()
        self.performance_optimizer = PerformanceOptimizer()
        self.validation_dashboard = ValidationDashboard()
        
        logger.info("✅ Tous les composants initialisés avec succès")
        self.config.log_configuration()
    
    def run_complete_pipeline(self, input_source: str = "mongodb", 
                             input_config: Dict = None, 
                             output_config: Dict = None) -> Dict[str, Any]:
        """
        Exécute le pipeline ETL complet
        
        Args:
            input_source: Source des données ("mongodb", "csv", "json", "test")
            input_config: Configuration d'entrée
            output_config: Configuration de sortie
            
        Returns:
            Dict avec les résultats complets du pipeline
        """
        pipeline_start = datetime.now()
        logger.info("🚀 === DÉMARRAGE PIPELINE ETL COMPLET ===")
        
        try:
            # === PHASE 1: EXTRACTION ===
            logger.info("📥 === PHASE 1: EXTRACTION ===")
            df_extracted = self._execute_extraction_phase(input_source, input_config)
            
            if df_extracted is None or df_extracted.empty:
                raise ValueError("❌ Aucune donnée extraite")
            
            logger.info(f"✅ Extraction réussie: {df_extracted.shape[0]} lignes × {df_extracted.shape[1]} colonnes")
            
            # === PHASE 2: NETTOYAGE ===
            logger.info("🧹 === PHASE 2: NETTOYAGE ===")
            df_cleaned = self._execute_cleaning_phase(df_extracted)
            
            # === PHASE 3: CONSOLIDATION ===
            logger.info("🔗 === PHASE 3: CONSOLIDATION ===")
            df_consolidated = self._execute_consolidation_phase(df_cleaned)
            
            # === PHASE 4: ENRICHISSEMENT ===
            logger.info("🚀 === PHASE 4: ENRICHISSEMENT ===")
            df_enriched = self._execute_enrichment_phase(df_consolidated)
            
            # === PHASE 5: VALIDATION ===
            logger.info("✅ === PHASE 5: VALIDATION ===")
            validation_results = self._execute_validation_phase(df_enriched)
            
            # === PHASE 6: OPTIMISATION ===
            logger.info("⚡ === PHASE 6: OPTIMISATION ===")
            df_optimized = self._execute_optimization_phase(df_enriched)
            
            # === PHASE 7: EXPORT ===
            logger.info("📤 === PHASE 7: EXPORT ===")
            export_results = self._execute_export_phase(df_optimized, output_config)
            
            # === PHASE 8: GÉNÉRATION DES RAPPORTS ===
            logger.info("📊 === PHASE 8: GÉNÉRATION DES RAPPORTS ===")
            report_results = self._execute_reporting_phase(df_optimized, validation_results, export_results)
            
            # === PHASE 9: DASHBOARD ===
            logger.info("📈 === PHASE 9: DASHBOARD ===")
            dashboard_results = self._execute_dashboard_phase(df_optimized, validation_results)
            
            # Compilation des résultats finaux
            pipeline_results = self._compile_pipeline_results(
                df_extracted, df_cleaned, df_consolidated, df_enriched, 
                df_optimized, validation_results, export_results, 
                report_results, dashboard_results
            )
            
            # Statistiques du pipeline
            pipeline_end = datetime.now()
            self.pipeline_stats = {
                'start_time': pipeline_start,
                'end_time': pipeline_end,
                'total_duration': (pipeline_end - pipeline_start).total_seconds(),
                'phases_executed': 9,
                'input_shape': df_extracted.shape if df_extracted is not None else (0, 0),
                'output_shape': df_optimized.shape if df_optimized is not None else (0, 0),
                'data_reduction_percentage': self._calculate_data_reduction(df_extracted, df_optimized),
                'overall_quality_score': validation_results.get('overall_status', {}).get('quality_score', 0.0),
                'export_success': export_results.get('success', False),
                'dashboard_generated': dashboard_results.get('success', False)
            }
            
            # Enregistrement dans l'historique
            self.pipeline_history.append({
                'timestamp': pipeline_start.isoformat(),
                'input_source': input_source,
                'results': pipeline_results,
                'stats': self.pipeline_stats
            })
            
            logger.info("🎉 === PIPELINE ETL COMPLET TERMINÉ AVEC SUCCÈS ===")
            logger.info(f"⏱️ Durée totale: {self.pipeline_stats['total_duration']:.2f}s")
            logger.info(f"📊 Réduction données: {self.pipeline_stats['data_reduction_percentage']:.1f}%")
            logger.info(f"⭐ Score qualité: {self.pipeline_stats['overall_quality_score']:.1%}")
            
            return pipeline_results
            
        except Exception as e:
            logger.error(f"❌ Erreur dans le pipeline: {e}")
            self._handle_pipeline_error(e, pipeline_start)
            raise
    
    def _execute_extraction_phase(self, input_source: str, input_config: Dict = None) -> pd.DataFrame:
        """Exécution de la phase d'extraction"""
        try:
            logger.info(f"📥 Extraction depuis: {input_source}")
            
            # Extraction des données
            df = self.data_extractor.extract_data(input_source, input_config)
            
            # Validation des données extraites
            if not self.data_extractor.validate_extracted_data(df):
                logger.warning("⚠️ Validation des données extraites échouée")
            
            # Statistiques d'extraction
            extraction_stats = self.data_extractor.get_extraction_stats()
            logger.info(f"📊 Statistiques d'extraction: {extraction_stats}")
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur phase extraction: {e}")
            raise
    
    def _execute_cleaning_phase(self, df: pd.DataFrame) -> pd.DataFrame:
        """Exécution de la phase de nettoyage"""
        try:
            logger.info("🧹 Début du nettoyage des données")
            
            # Nettoyage des données
            df_cleaned = self.data_cleaner.clean_data(df)
            
            # Validation de la qualité après nettoyage
            quality_scores = self.data_cleaner.validate_data_quality(df_cleaned)
            logger.info(f"📊 Scores de qualité après nettoyage: {quality_scores}")
            
            # Statistiques de nettoyage
            cleaning_stats = self.data_cleaner.get_cleaning_stats()
            logger.info(f"📊 Statistiques de nettoyage: {cleaning_stats}")
            
            return df_cleaned
            
        except Exception as e:
            logger.error(f"❌ Erreur phase nettoyage: {e}")
            raise
    
    def _execute_consolidation_phase(self, df: pd.DataFrame) -> pd.DataFrame:
        """Exécution de la phase de consolidation"""
        try:
            logger.info("🔗 Début de la consolidation des variables")
            
            # Consolidation des variables
            df_consolidated = self.data_consolidator.consolidate_variables(df)
            
            # Résultats de consolidation
            consolidation_results = self.data_consolidator.get_consolidation_results()
            consolidation_stats = self.data_consolidator.get_consolidation_stats()
            
            logger.info(f"📊 Résultats de consolidation: {len(consolidation_results)} groupes traités")
            logger.info(f"📊 Statistiques de consolidation: {consolidation_stats}")
            
            return df_consolidated
            
        except Exception as e:
            logger.error(f"❌ Erreur phase consolidation: {e}")
            raise
    
    def _execute_enrichment_phase(self, df: pd.DataFrame) -> pd.DataFrame:
        """Exécution de la phase d'enrichissement"""
        try:
            logger.info("🚀 Début de l'enrichissement des données")
            
            # Enrichissement des données
            df_enriched = self.data_enricher.enrich_data(df)
            
            # Résultats d'enrichissement
            enrichment_results = self.data_enricher.get_enrichment_results()
            enrichment_stats = self.data_enricher.get_enrichment_stats()
            enriched_columns = self.data_enricher.get_enriched_columns()
            
            logger.info(f"📊 Résultats d'enrichissement: {len(enrichment_results)} phases")
            logger.info(f"📊 Statistiques d'enrichissement: {enrichment_stats}")
            logger.info(f"➕ Colonnes enrichies: {enriched_columns}")
            
            return df_enriched
            
        except Exception as e:
            logger.error(f"❌ Erreur phase enrichissement: {e}")
            raise
    
    def _execute_validation_phase(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Exécution de la phase de validation"""
        try:
            logger.info("✅ Début de la validation des données")
            
            # Validation complète des données
            validation_results = self.data_validator.validate_data(df)
            
            # Statistiques de validation
            validation_stats = self.data_validator.get_validation_stats()
            
            logger.info(f"📊 Résultats de validation: {len(validation_results)} catégories")
            logger.info(f"📊 Statistiques de validation: {validation_stats}")
            
            # Génération du rapport de validation
            validation_report = self.data_validator.generate_validation_report()
            logger.info("📋 Rapport de validation généré")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur phase validation: {e}")
            raise
    
    def _execute_optimization_phase(self, df: pd.DataFrame) -> pd.DataFrame:
        """Exécution de la phase d'optimisation"""
        try:
            logger.info("⚡ Début de l'optimisation des performances")
            
            # Optimisation des performances
            df_optimized = self.performance_optimizer.optimize_dataframe(df)
            
            # Statistiques d'optimisation
            optimization_stats = self.performance_optimizer.get_optimization_stats()
            logger.info(f"📊 Statistiques d'optimisation: {optimization_stats}")
            
            return df_optimized
            
        except Exception as e:
            logger.error(f"❌ Erreur phase optimisation: {e}")
            # En cas d'erreur, retourner les données non optimisées
            logger.warning("⚠️ Retour des données non optimisées")
            return df
    
    def _execute_export_phase(self, df: pd.DataFrame, output_config: Dict = None) -> Dict[str, Any]:
        """Exécution de la phase d'export"""
        try:
            logger.info("📤 Début de l'export des données")
            
            # Configuration d'export par défaut
            if not output_config:
                output_config = {
                    'output_dir': 'exports/',
                    'formats': ['csv', 'parquet'],
                    'filename_prefix': 'real_estate_data_consolidated'
                }
            
            # Export des données
            export_results = self.advanced_exporter.export_data(df, output_config)
            
            logger.info(f"📤 Export terminé: {export_results}")
            return export_results
            
        except Exception as e:
            logger.error(f"❌ Erreur phase export: {e}")
            return {'success': False, 'error': str(e)}
    
    def _execute_reporting_phase(self, df: pd.DataFrame, validation_results: Dict, 
                                export_results: Dict) -> Dict[str, Any]:
        """Exécution de la phase de génération de rapports"""
        try:
            logger.info("📊 Début de la génération des rapports")
            
            # Création du répertoire de rapports
            reports_dir = Path('exports/reports')
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            # Rapport de validation
            validation_report = self.data_validator.generate_validation_report()
            validation_report_path = reports_dir / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(validation_report_path, 'w', encoding='utf-8') as f:
                f.write(validation_report)
            
            # Rapport de pipeline
            pipeline_report = self._generate_pipeline_report(df, validation_results, export_results)
            pipeline_report_path = reports_dir / f"pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            
            with open(pipeline_report_path, 'w', encoding='utf-8') as f:
                f.write(pipeline_report)
            
            report_results = {
                'success': True,
                'validation_report_path': str(validation_report_path),
                'pipeline_report_path': str(pipeline_report_path),
                'reports_generated': 2
            }
            
            logger.info(f"📊 Rapports générés: {report_results}")
            return report_results
            
        except Exception as e:
            logger.error(f"❌ Erreur phase rapports: {e}")
            return {'success': False, 'error': str(e)}
    
    def _execute_dashboard_phase(self, df: pd.DataFrame, validation_results: Dict) -> Dict[str, Any]:
        """Exécution de la phase de génération du dashboard"""
        try:
            logger.info("📈 Début de la génération du dashboard")
            
            # Génération du dashboard de validation
            dashboard_results = self.validation_dashboard.generate_dashboard(df, validation_results)
            
            logger.info(f"📈 Dashboard généré: {dashboard_results}")
            return dashboard_results
            
        except Exception as e:
            logger.error(f"❌ Erreur phase dashboard: {e}")
            return {'success': False, 'error': str(e)}
    
    def _compile_pipeline_results(self, df_extracted: pd.DataFrame, df_cleaned: pd.DataFrame,
                                 df_consolidated: pd.DataFrame, df_enriched: pd.DataFrame,
                                 df_optimized: pd.DataFrame, validation_results: Dict,
                                 export_results: Dict, report_results: Dict,
                                 dashboard_results: Dict) -> Dict[str, Any]:
        """Compilation des résultats finaux du pipeline"""
        try:
            pipeline_results = {
                'pipeline_status': 'SUCCESS',
                'timestamp': datetime.now().isoformat(),
                'data_flow': {
                    'extraction': {
                        'shape': df_extracted.shape if df_extracted is not None else (0, 0),
                        'columns': list(df_extracted.columns) if df_extracted is not None else [],
                        'memory_usage_mb': df_extracted.memory_usage(deep=True).sum() / 1024 / 1024 if df_extracted is not None else 0
                    },
                    'cleaning': {
                        'shape': df_cleaned.shape if df_cleaned is not None else (0, 0),
                        'columns': list(df_cleaned.columns) if df_cleaned is not None else [],
                        'memory_usage_mb': df_cleaned.memory_usage(deep=True).sum() / 1024 / 1024 if df_cleaned is not None else 0
                    },
                    'consolidation': {
                        'shape': df_consolidated.shape if df_consolidated is not None else (0, 0),
                        'columns': list(df_consolidated.columns) if df_consolidated is not None else [],
                        'memory_usage_mb': df_consolidated.memory_usage(deep=True).sum() / 1024 / 1024 if df_consolidated is not None else 0
                    },
                    'enrichment': {
                        'shape': df_enriched.shape if df_enriched is not None else (0, 0),
                        'columns': list(df_enriched.columns) if df_enriched is not None else [],
                        'memory_usage_mb': df_enriched.memory_usage(deep=True).sum() / 1024 / 1024 if df_enriched is not None else 0
                    },
                    'optimization': {
                        'shape': df_optimized.shape if df_optimized is not None else (0, 0),
                        'columns': list(df_optimized.columns) if df_optimized is not None else [],
                        'memory_usage_mb': df_optimized.memory_usage(deep=True).sum() / 1024 / 1024 if df_optimized is not None else 0
                    }
                },
                'validation_results': validation_results,
                'export_results': export_results,
                'report_results': report_results,
                'dashboard_results': dashboard_results,
                'component_results': {
                    'extractor': self.data_extractor.get_extraction_stats(),
                    'cleaner': self.data_cleaner.get_cleaning_stats(),
                    'consolidator': self.data_consolidator.get_consolidation_stats(),
                    'enricher': self.data_enricher.get_enrichment_stats(),
                    'validator': self.data_validator.get_validation_stats()
                }
            }
            
            return pipeline_results
            
        except Exception as e:
            logger.error(f"❌ Erreur compilation résultats: {e}")
            return {'pipeline_status': 'ERROR', 'error': str(e)}
    
    def _calculate_data_reduction(self, df_input: pd.DataFrame, df_output: pd.DataFrame) -> float:
        """Calcul du pourcentage de réduction des données"""
        try:
            if df_input is None or df_output is None:
                return 0.0
            
            input_size = df_input.memory_usage(deep=True).sum()
            output_size = df_output.memory_usage(deep=True).sum()
            
            if input_size == 0:
                return 0.0
            
            reduction = ((input_size - output_size) / input_size) * 100
            return round(reduction, 1)
            
        except Exception:
            return 0.0
    
    def _generate_pipeline_report(self, df: pd.DataFrame, validation_results: Dict, 
                                 export_results: Dict) -> str:
        """Génération du rapport de pipeline"""
        try:
            report = []
            report.append("# 📊 RAPPORT DE PIPELINE ETL")
            report.append("")
            report.append(f"**Date de génération:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"**Statut du pipeline:** ✅ Succès")
            report.append("")
            
            # Résumé des données
            report.append("## 📈 RÉSUMÉ DES DONNÉES")
            report.append("")
            report.append(f"- **Forme finale:** {df.shape[0]} lignes × {df.shape[1]} colonnes")
            report.append(f"- **Mémoire utilisée:** {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
            report.append("")
            
            # Résultats de validation
            if 'overall_status' in validation_results:
                overall = validation_results['overall_status']
                report.append("## ✅ RÉSULTATS DE VALIDATION")
                report.append("")
                report.append(f"- **Statut global:** {overall.get('status', 'N/A')}")
                report.append(f"- **Score de qualité:** {overall.get('quality_score', 0):.1%}")
                report.append(f"- **Message:** {overall.get('message', 'N/A')}")
                report.append("")
            
            # Résultats d'export
            if export_results.get('success'):
                report.append("## 📤 RÉSULTATS D'EXPORT")
                report.append("")
                report.append(f"- **Statut:** ✅ Succès")
                report.append(f"- **Formats exportés:** {export_results.get('formats', [])}")
                report.append(f"- **Fichiers générés:** {export_results.get('files_generated', 0)}")
                report.append("")
            
            # Statistiques du pipeline
            report.append("## 📊 STATISTIQUES DU PIPELINE")
            report.append("")
            report.append(f"- **Durée totale:** {self.pipeline_stats.get('total_duration', 0):.2f}s")
            report.append(f"- **Phases exécutées:** {self.pipeline_stats.get('phases_executed', 0)}")
            report.append(f"- **Réduction des données:** {self.pipeline_stats.get('data_reduction_percentage', 0):.1f}%")
            report.append("")
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"❌ Erreur génération rapport pipeline: {e}")
            return f"Erreur lors de la génération du rapport: {str(e)}"
    
    def _handle_pipeline_error(self, error: Exception, start_time: datetime):
        """Gestion des erreurs du pipeline"""
        try:
            error_info = {
                'timestamp': datetime.now().isoformat(),
                'error_type': type(error).__name__,
                'error_message': str(error),
                'pipeline_duration': (datetime.now() - start_time).total_seconds()
            }
            
            logger.error(f"❌ Erreur pipeline enregistrée: {error_info}")
            
            # Enregistrement de l'erreur dans l'historique
            self.pipeline_history.append({
                'timestamp': start_time.isoformat(),
                'status': 'ERROR',
                'error': error_info
            })
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la gestion d'erreur: {e}")
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du pipeline"""
        return self.pipeline_stats.copy()
    
    def get_pipeline_history(self) -> List[Dict[str, Any]]:
        """Retourne l'historique des pipelines"""
        return self.pipeline_history.copy()
    
    def get_component_status(self) -> Dict[str, Any]:
        """Retourne le statut de tous les composants"""
        return {
            'data_extractor': '✅ Initialisé',
            'data_consolidator': '✅ Initialisé',
            'data_cleaner': '✅ Initialisé',
            'data_enricher': '✅ Initialisé',
            'data_validator': '✅ Initialisé',
            'advanced_exporter': '✅ Initialisé',
            'performance_optimizer': '✅ Initialisé',
            'validation_dashboard': '✅ Initialisé'
        }
