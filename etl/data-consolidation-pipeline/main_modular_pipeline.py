#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 PIPELINE ETL MODULAIRE - Point d'entrée principal
=====================================================

Pipeline ETL modulaire pour la consolidation de données immobilières
Utilise une architecture modulaire pour une meilleure maintenabilité
"""

import sys
import logging
import time
from typing import Dict, Any

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Import des modules modulaires
try:
    from core import (
        PipelineManager, DataProcessor, ExportManager, 
        ReportGenerator, ConfigManager
    )
except ImportError as e:
    logger.error(f"❌ Erreur import modules: {e}")
    sys.exit(1)

class ModularPipeline:
    """
    Pipeline ETL modulaire principal
    
    Orchestre tous les composants modulaires pour offrir
    une expérience complète et maintenable
    """
    
    def __init__(self):
        """Initialise le pipeline modulaire"""
        self.pipeline_manager = None
        self.data_processor = None
        self.export_manager = None
        self.report_generator = None
        self.config_manager = None
        
        logger.info("🚀 === INITIALISATION PIPELINE MODULAIRE ===")
    
    def initialize_pipeline(self, config: Dict[str, Any]):
        """
        Initialise tous les composants du pipeline
        
        Args:
            config: Configuration du pipeline
        """
        try:
            # === GESTIONNAIRE DE PIPELINE ===
            self.pipeline_manager = PipelineManager(config)
            logger.info("✅ PipelineManager initialisé")
            
            # === PROCESSEUR DE DONNÉES ===
            self.data_processor = DataProcessor(self.pipeline_manager)
            logger.info("✅ DataProcessor initialisé")
            
            # === GESTIONNAIRE D'EXPORT ===
            self.export_manager = ExportManager(self.pipeline_manager)
            logger.info("✅ ExportManager initialisé")
            
            # === GÉNÉRATEUR DE RAPPORTS ===
            self.report_generator = ReportGenerator(self.pipeline_manager)
            logger.info("✅ ReportGenerator initialisé")
            
            logger.info("✅ Tous les composants initialisés avec succès")
            
        except Exception as e:
            logger.error(f"❌ Erreur initialisation pipeline: {e}")
            raise
    
    def run_pipeline(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute le pipeline complet
        
        Args:
            config: Configuration du pipeline
            
        Returns:
            Dict avec les résultats du pipeline
        """
        try:
            # === DÉMARRAGE ===
            self.pipeline_manager.start_pipeline()
            
            # === EXTRACTION ===
            source_config = self.config_manager.get_source_config()
            df_initial = self.data_processor.extract_data(**source_config)
            
            if df_initial is None or df_initial.empty:
                logger.error("❌ Aucune donnée extraite")
                return {"status": "error", "message": "Aucune donnée extraite"}
            
            logger.info(f"✅ Extraction réussie: {df_initial.shape[0]} lignes × {df_initial.shape[1]} colonnes")
            
            # === VALIDATION INITIALE ===
            initial_validation = self.data_processor.validate_data(df_initial, "initial")
            
            # === MODE VALIDATION UNIQUEMENT ===
            if config.get('validate_only'):
                logger.info("🔍 Mode validation uniquement - Arrêt du pipeline")
                duration = self.pipeline_manager.end_pipeline()
                return {
                    "status": "validation_only",
                    "validation_results": initial_validation,
                    "duration_seconds": duration
                }
            
            # === DÉTECTION DE SIMILARITÉS ===
            similarity_groups = self.data_processor.detect_similarities(df_initial)
            
            # === TRAITEMENT DES DONNÉES ===
            if not config.get('dry_run'):
                df_final = self.data_processor.process_data(df_initial, config['output'])
            else:
                logger.info("🧪 Mode dry run - Aucune transformation effectuée")
                df_final = df_initial.copy()
            
            # === VALIDATION FINALE ===
            final_validation = self.data_processor.validate_data(df_final, "final")
            
            # === EXPORT ===
            if not config.get('dry_run'):
                output_config = self.config_manager.get_output_config()
                exported_files = self.export_manager.export_data(
                    df_final, "modular_pipeline", 
                    output_config['formats'], output_config['output_dir']
                )
            else:
                logger.info("🧪 Mode dry run - Aucun export effectué")
                exported_files = {}
            
            # === GÉNÉRATION DES RAPPORTS ===
            if not config.get('dry_run'):
                reports = self.report_generator.generate_all_reports(
                    df_initial, df_final, initial_validation, final_validation,
                    similarity_groups, exported_files, config['output']
                )
            else:
                logger.info("🧪 Mode dry run - Aucun rapport généré")
                reports = {}
            
            # === FINALISATION ===
            duration = self.pipeline_manager.end_pipeline()
            
            # === RÉSULTATS ===
            results = {
                "status": "success",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "duration_seconds": duration,
                "source": config.get('source'),
                "output_directory": config.get('output'),
                "initial_shape": df_initial.shape,
                "final_shape": df_final.shape,
                "column_reduction": {
                    "initial_columns": df_initial.shape[1],
                    "final_columns": df_final.shape[1],
                    "reduction_percentage": ((df_initial.shape[1] - df_final.shape[1]) / df_initial.shape[1]) * 100
                },
                "validation_results": {
                    "initial": initial_validation,
                    "final": final_validation
                },
                "similarity_groups": similarity_groups,
                "exported_files": exported_files,
                "reports": reports
            }
            
            logger.info("🎉 === PIPELINE TERMINÉ AVEC SUCCÈS ===")
            logger.info(f"📊 Réduction colonnes: {results['column_reduction']['reduction_percentage']:.1f}%")
            logger.info(f"🎯 Score qualité final: {final_validation.get('overall_score', 0):.2%}")
            
            return results
            
        except Exception as e:
            duration = self.pipeline_manager.end_pipeline() if self.pipeline_manager else 0
            logger.error(f"❌ Erreur dans le pipeline: {e}")
            
            return {
                "status": "error",
                "error": str(e),
                "duration_seconds": duration,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

def main():
    """Point d'entrée principal du pipeline"""
    try:
        # === INITIALISATION ===
        pipeline = ModularPipeline()
        config_manager = ConfigManager()
        
        # === PARSE DES ARGUMENTS ===
        config = config_manager.parse_arguments()
        pipeline.config_manager = config_manager
        
        # === INITIALISATION DU PIPELINE ===
        pipeline.initialize_pipeline(config)
        
        # === EXÉCUTION ===
        results = pipeline.run_pipeline(config)
        
        # === AFFICHAGE DES RÉSULTATS ===
        if results["status"] == "success":
            print(f"\n🎉 Pipeline terminé avec succès !")
            print(f"📁 Fichiers exportés dans: {results['output_directory']}")
            print(f"📋 Rapports générés: {len(results['reports'])} fichiers")
            print(f"⏱️ Durée totale: {results['duration_seconds']:.2f} secondes")
        else:
            print(f"\n❌ Pipeline échoué: {results.get('error', 'Erreur inconnue')}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ Pipeline interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
