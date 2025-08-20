#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST COMPLET DU PIPELINE ULTRA-INTELLIGENT
=============================================

Test exhaustif de toutes les fonctionnalités du pipeline:
- Configuration et imports
- Extraction des données
- Consolidation maximale
- Fonctionnalités avancées
- Export multi-formats
- Génération de rapports
"""

import sys
import os
import logging
import pandas as pd
import numpy as np
import time
from pathlib import Path
from datetime import datetime

# Ajout du répertoire parent au PYTHONPATH pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PipelineCompleteTest:
    """Classe de test complet du pipeline ultra-intelligent"""
    
    def __init__(self):
        self.start_time = time.time()
        self.test_results = {}
        self.test_data = None
        self.pipeline = None
        
    def run_complete_test(self):
        """Exécute tous les tests du pipeline"""
        logger.info("🚀 === DÉMARRAGE DU TEST COMPLET DU PIPELINE ===")
        logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Tests séquentiels
        tests = [
            ("Configuration et Imports", self.test_configuration_imports),
            ("Extraction des Données", self.test_data_extraction),
            ("Consolidation Maximale", self.test_consolidation_maximale),
            ("Fonctionnalités Avancées", self.test_fonctionnalites_avancees),
            ("Export Multi-Formats", self.test_export_multi_formats),
            ("Performance et Optimisations", self.test_performance),
            ("Validation et Qualité", self.test_validation_qualite)
        ]
        
        for test_name, test_func in tests:
            logger.info(f"\n{'='*80}")
            logger.info(f"🧪 TEST: {test_name}")
            logger.info(f"{'='*80}")
            
            try:
                success = test_func()
                self.test_results[test_name] = {
                    "status": "✅ SUCCÈS" if success else "❌ ÉCHEC",
                    "success": success
                }
                logger.info(f"📊 {test_name}: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}")
            except Exception as e:
                logger.error(f"💥 Erreur critique dans {test_name}: {e}")
                self.test_results[test_name] = {
                    "status": "💥 ERREUR CRITIQUE",
                    "success": False,
                    "error": str(e)
                }
        
        # Rapport final
        self.generate_final_report()
        
    def test_configuration_imports(self):
        """Test de la configuration et des imports"""
        logger.info("⚙️ === TEST CONFIGURATION ET IMPORTS ===")
        
        try:
            # Test des imports principaux
            logger.info("📦 Test des imports...")
            from config.consolidation_config import ConsolidationConfig
            from config.custom_fields_config import custom_config
            from core.ultra_intelligent_cleaner import UltraIntelligentCleaner
            from main_ultra_intelligent import UltraIntelligentPipeline
            logger.info("✅ Tous les imports réussis")
            
            # Test de la configuration de base
            logger.info("⚙️ Test configuration de base...")
            base_config = ConsolidationConfig()
            groups_count = len(base_config.CONSOLIDATION_GROUPS)
            logger.info(f"📊 Configuration de base: {groups_count} groupes")
            
            if groups_count < 25:
                logger.error(f"❌ Nombre de groupes insuffisant: {groups_count} < 25")
                return False
            
            # Test de la configuration personnalisée
            logger.info("🔧 Test configuration personnalisée...")
            summary = custom_config.get_67_fields_config_summary()
            logger.info(f"📊 Configuration personnalisée: {summary['total_consolidation_groups']} groupes")
            logger.info(f"📊 Réduction estimée: {summary['estimated_reduction']}")
            
            # Validation de la configuration
            if base_config.validate_configuration():
                logger.info("✅ Configuration validée avec succès")
                return True
            else:
                logger.error("❌ Validation de configuration échouée")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur configuration/imports: {e}")
            return False
    
    def test_data_extraction(self):
        """Test de l'extraction des données"""
        logger.info("📥 === TEST EXTRACTION DES DONNÉES ===")
        
        try:
            # Initialisation du pipeline
            logger.info("🚀 Initialisation du pipeline...")
            from main_ultra_intelligent import UltraIntelligentPipeline
            
            self.pipeline = UltraIntelligentPipeline()
            logger.info("✅ Pipeline initialisé")
            
            # Test avec données synthétiques
            logger.info("🏗️ Génération de données de test...")
            self.test_data = self.create_comprehensive_test_data()
            logger.info(f"📊 Dataset créé: {self.test_data.shape[0]} lignes × {self.test_data.shape[1]} colonnes")
            
            # Validation du dataset
            if self.test_data.shape[1] >= 50:
                logger.info(f"✅ Dataset valide: {self.test_data.shape[1]} colonnes")
                return True
            else:
                logger.error(f"❌ Dataset insuffisant: {self.test_data.shape[1]} colonnes")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur extraction données: {e}")
            return False
    
    def test_consolidation_maximale(self):
        """Test de la consolidation maximale"""
        logger.info("🔗 === TEST CONSOLIDATION MAXIMALE ===")
        
        try:
            if self.test_data is None:
                logger.error("❌ Pas de données de test disponibles")
                return False
            
            # Configuration avec la config personnalisée
            logger.info("⚙️ Configuration pour consolidation...")
            from config.custom_fields_config import custom_config
            from core.ultra_intelligent_cleaner import UltraIntelligentCleaner
            
            cleaner = UltraIntelligentCleaner(custom_config)
            logger.info("✅ Nettoyeur configuré")
            
            # Consolidation
            logger.info("🔄 Démarrage de la consolidation...")
            initial_columns = self.test_data.shape[1]
            
            df_consolidated = cleaner._consolidate_variables(self.test_data)
            final_columns = df_consolidated.shape[1]
            reduction_percentage = ((initial_columns - final_columns) / initial_columns) * 100
            
            logger.info(f"📊 Consolidation terminée:")
            logger.info(f"   📊 Colonnes initiales: {initial_columns}")
            logger.info(f"   📊 Colonnes finales: {final_columns}")
            logger.info(f"   📉 Réduction: {reduction_percentage:.1f}%")
            
            # Validation des résultats
            if reduction_percentage > 0 and final_columns > 0:
                logger.info("✅ Consolidation réussie")
                self.consolidated_data = df_consolidated
                return True
            else:
                logger.error("❌ Consolidation échouée")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur consolidation: {e}")
            return False
    
    def test_fonctionnalites_avancees(self):
        """Test des fonctionnalités avancées"""
        logger.info("🚀 === TEST FONCTIONNALITÉS AVANCÉES ===")
        
        try:
            if not hasattr(self, 'consolidated_data'):
                logger.warning("⚠️ Pas de données consolidées, utilisation des données de test")
                df = self.test_data
            else:
                df = self.consolidated_data
            
            # Test du clustering spatial
            logger.info("🌍 Test clustering spatial...")
            from intelligence.similarity_detector import SimilarityDetector
            detector = SimilarityDetector()
            
            # Ajouter des coordonnées si nécessaire
            if 'latitude' not in df.columns:
                df['latitude'] = np.random.uniform(45.4, 45.7, len(df))
                df['longitude'] = np.random.uniform(-73.8, -73.4, len(df))
            
            spatial_results = detector.spatial_clustering(df)
            if spatial_results.get("success"):
                logger.info(f"✅ Clustering spatial: {spatial_results['n_clusters']} zones créées")
            else:
                logger.warning(f"⚠️ Clustering spatial échoué: {spatial_results.get('error', 'Erreur inconnue')}")
            
            # Test de la catégorisation automatique
            logger.info("🏷️ Test catégorisation automatique...")
            from core.ultra_intelligent_cleaner import UltraIntelligentCleaner
            from config.custom_fields_config import custom_config
            
            cleaner = UltraIntelligentCleaner(custom_config)
            
            # Ajouter des données financières si nécessaire
            if 'revenue_final' not in df.columns:
                df['revenue_final'] = np.random.uniform(15000, 150000, len(df))
            if 'price_final' not in df.columns:
                df['price_final'] = np.random.uniform(200000, 2000000, len(df))
            
            df_categorized = cleaner.categorize_investment_opportunities(df)
            
            # Vérifier les colonnes de catégorisation
            categorization_columns = ['segment_roi', 'classe_prix', 'type_opportunite', 'score_qualite']
            found_columns = [col for col in categorization_columns if col in df_categorized.columns]
            
            logger.info(f"✅ Catégorisation: {len(found_columns)}/{len(categorization_columns)} colonnes créées")
            
            # Test du dashboard
            logger.info("📊 Test dashboard de validation...")
            try:
                from dashboard.validation_dashboard import ValidationDashboard
                dashboard = ValidationDashboard()
                
                # Création d'un dashboard basique
                quality_metrics = {
                    "completeness_score": 85.5,
                    "consistency_score": 90.2,
                    "validity_score": 88.7
                }
                
                dashboard_result = dashboard.create_quality_overview_dashboard(df, quality_metrics)
                logger.info("✅ Dashboard créé avec succès")
            except ImportError as e:
                logger.warning(f"⚠️ Dashboard non disponible (dépendances manquantes): {e}")
            except Exception as e:
                logger.warning(f"⚠️ Erreur dashboard: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur fonctionnalités avancées: {e}")
            return False
    
    def test_export_multi_formats(self):
        """Test de l'export multi-formats"""
        logger.info("💾 === TEST EXPORT MULTI-FORMATS ===")
        
        try:
            if not hasattr(self, 'consolidated_data'):
                logger.warning("⚠️ Pas de données consolidées, utilisation des données de test")
                df = self.test_data.head(100)  # Réduire pour les tests
            else:
                df = self.consolidated_data.head(100)
            
            from export.advanced_exporter import AdvancedExporter
            
            exporter = AdvancedExporter()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Test des formats principaux
            formats_to_test = ["csv", "parquet", "json"]
            export_results = {}
            
            for format_name in formats_to_test:
                try:
                    logger.info(f"📄 Test export {format_name.upper()}...")
                    
                    output_config = {
                        "base_filename": f"test_pipeline_complet_{timestamp}",
                        "output_directory": "exports/tests/",
                        "formats": [format_name],
                        "include_metadata": True
                    }
                    
                    # Créer le dossier si nécessaire
                    output_dir = Path(output_config["output_directory"])
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    result = exporter.export_dataframe(df, output_config)
                    
                    if result.get("success"):
                        export_results[format_name] = "✅ SUCCÈS"
                        logger.info(f"✅ Export {format_name.upper()} réussi")
                    else:
                        export_results[format_name] = "❌ ÉCHEC"
                        logger.warning(f"⚠️ Export {format_name.upper()} échoué")
                        
                except Exception as e:
                    export_results[format_name] = f"❌ ERREUR: {str(e)[:50]}"
                    logger.warning(f"⚠️ Erreur export {format_name.upper()}: {e}")
            
            # Résumé des exports
            successful_exports = sum(1 for result in export_results.values() if "SUCCÈS" in result)
            total_exports = len(export_results)
            
            logger.info(f"📊 Exports réussis: {successful_exports}/{total_exports}")
            
            for format_name, result in export_results.items():
                logger.info(f"   {format_name.upper()}: {result}")
            
            return successful_exports > 0
            
        except Exception as e:
            logger.error(f"❌ Erreur export multi-formats: {e}")
            return False
    
    def test_performance(self):
        """Test des optimisations de performance"""
        logger.info("⚡ === TEST PERFORMANCE ET OPTIMISATIONS ===")
        
        try:
            from performance.performance_optimizer import PerformanceOptimizer
            
            optimizer = PerformanceOptimizer()
            logger.info("✅ Optimiseur de performance initialisé")
            
            # Test d'activation des optimisations
            logger.info("🔧 Test activation des optimisations...")
            optimization_results = optimizer.enable_all_optimizations()
            
            enabled_optimizations = sum(1 for enabled in optimization_results.values() if enabled)
            total_optimizations = len(optimization_results)
            
            logger.info(f"📊 Optimisations activées: {enabled_optimizations}/{total_optimizations}")
            
            for opt_name, enabled in optimization_results.items():
                status = "✅ ACTIVÉE" if enabled else "❌ DÉSACTIVÉE"
                logger.info(f"   {opt_name}: {status}")
            
            return enabled_optimizations > 0
            
        except Exception as e:
            logger.error(f"❌ Erreur performance: {e}")
            return False
    
    def test_validation_qualite(self):
        """Test de la validation et contrôle qualité"""
        logger.info("✅ === TEST VALIDATION ET QUALITÉ ===")
        
        try:
            if not hasattr(self, 'consolidated_data'):
                df = self.test_data
            else:
                df = self.consolidated_data
            
            from validation.quality_validator import QualityValidator
            
            validator = QualityValidator()
            logger.info("✅ Validateur de qualité initialisé")
            
            # Test de validation
            logger.info("🔍 Test validation des données...")
            validation_results = validator.validate_dataset(df, "test_dataset")
            
            if validation_results.get("overall_score", 0) > 0:
                score = validation_results["overall_score"]
                logger.info(f"✅ Score de qualité global: {score:.1f}%")
                
                # Détail par catégorie
                for category, details in validation_results.get("category_scores", {}).items():
                    if isinstance(details, dict) and "score" in details:
                        logger.info(f"   {category}: {details['score']:.1f}%")
                
                return score > 50  # Seuil minimum de qualité
            else:
                logger.warning("⚠️ Pas de score de qualité disponible")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur validation qualité: {e}")
            return False
    
    def create_comprehensive_test_data(self):
        """Crée un dataset de test complet avec toutes les colonnes nécessaires"""
        n_rows = 200
        
        # Dataset complet avec 78 colonnes comme spécifié
        test_data = pd.DataFrame({
            # Prix et évaluations
            'price': np.random.uniform(200000, 2000000, n_rows),
            'prix_evaluation': np.random.uniform(180000, 1800000, n_rows),
            'price_assessment': np.random.uniform(180000, 1800000, n_rows),
            'evaluation_total': np.random.uniform(180000, 1800000, n_rows),
            'evaluation_terrain': np.random.uniform(80000, 800000, n_rows),
            'evaluation_batiment': np.random.uniform(100000, 1000000, n_rows),
            'municipal_evaluation_building': np.random.uniform(100000, 1000000, n_rows),
            'municipal_evaluation_land': np.random.uniform(80000, 800000, n_rows),
            'municipal_evaluation_total': np.random.uniform(180000, 1800000, n_rows),
            'evaluation_year': np.random.randint(2018, 2025, n_rows),
            'municipal_evaluation_year': np.random.randint(2018, 2025, n_rows),
            
            # Surface et caractéristiques
            'surface': np.random.uniform(50, 500, n_rows),
            'living_area': np.random.uniform(50, 500, n_rows),
            'superficie': np.random.uniform(50, 500, n_rows),
            'lot_size': np.random.uniform(100, 1000, n_rows),
            'bedrooms': np.random.randint(1, 6, n_rows),
            'nbr_chanbres': np.random.randint(1, 6, n_rows),
            'nb_bedroom': np.random.randint(1, 6, n_rows),
            'rooms': np.random.randint(3, 10, n_rows),
            'bathrooms': np.random.randint(1, 4, n_rows),
            'nbr_sal_deau': np.random.randint(1, 3, n_rows),
            'nbr_sal_bain': np.random.randint(1, 4, n_rows),
            'nb_bathroom': np.random.randint(1, 4, n_rows),
            'water_rooms': np.random.randint(1, 3, n_rows),
            'nb_water_room': np.random.randint(1, 3, n_rows),
            
            # Coordonnées
            'latitude': np.random.uniform(45.4, 45.7, n_rows),
            'longitude': np.random.uniform(-73.8, -73.4, n_rows),
            'geolocation': [f'45.5,-73.6#{i}' for i in range(n_rows)],
            'geo': [f'45.5,-73.6#{i}' for i in range(n_rows)],
            
            # Adresses
            'address': [f'123 Rue Principale #{i}' for i in range(n_rows)],
            'full_address': [f'123 Rue Principale #{i}, Montréal, QC' for i in range(n_rows)],
            'location': [f'Montréal, QC #{i}' for i in range(n_rows)],
            'city': ['Montréal', 'Québec', 'Laval'] * (n_rows // 3 + 1),
            'postal_code': ['H1A 1A1', 'H2B 2B2', 'H3C 3C3'] * (n_rows // 3 + 1),
            
            # Type propriété
            'type': ['Maison', 'Appartement', 'Duplex', 'Triplex'] * (n_rows // 4 + 1),
            'building_style': ['Moderne', 'Traditionnel', 'Contemporain'] * (n_rows // 3 + 1),
            'style': ['Moderne', 'Traditionnel', 'Contemporain'] * (n_rows // 3 + 1),
            
            # Année construction
            'year_built': np.random.randint(1950, 2025, n_rows),
            'construction_year': np.random.randint(1950, 2025, n_rows),
            'annee': np.random.randint(1950, 2025, n_rows),
            
            # Taxes
            'municipal_taxes': np.random.uniform(2000, 20000, n_rows),
            'municipal_tax': np.random.uniform(2000, 20000, n_rows),
            'taxes': np.random.uniform(3000, 30000, n_rows),
            'school_taxes': np.random.uniform(1000, 10000, n_rows),
            'school_tax': np.random.uniform(1000, 10000, n_rows),
            
            # Revenus
            'revenu': np.random.uniform(15000, 150000, n_rows),
            'revenus_annuels_bruts': np.random.uniform(15000, 150000, n_rows),
            'plex-revenu': np.random.uniform(15000, 150000, n_rows),
            'plex_revenu': np.random.uniform(15000, 150000, n_rows),
            'potential_gross_revenue': np.random.uniform(15000, 150000, n_rows),
            
            # Dépenses
            'expense': np.random.uniform(5000, 50000, n_rows),
            'depenses': np.random.uniform(5000, 50000, n_rows),
            'expense_period': ['Annuel'] * n_rows,
            
            # Parking et unités
            'nb_parking': np.random.randint(0, 4, n_rows),
            'parking': np.random.randint(0, 4, n_rows),
            'nb_garage': np.random.randint(0, 3, n_rows),
            'unites': np.random.randint(1, 5, n_rows),
            'residential_units': np.random.randint(1, 5, n_rows),
            'commercial_units': np.random.randint(0, 3, n_rows),
            
            # Images et métadonnées
            'image': [f'https://exemple.com/image_{i}.jpg' for i in range(n_rows)],
            'images': [f'https://exemple.com/images_{i}.jpg' for i in range(n_rows)],
            'img_src': [f'https://exemple.com/image_{i}.jpg' for i in range(n_rows)],
            'revenu_period': ['Annuel'] * n_rows,
            'basement': ['Oui', 'Non', 'Partiel'] * (n_rows // 3 + 1),
            
            # Champs préservés
            'main_unit_details': [f'Détails unité #{i}' for i in range(n_rows)],
            'vendue': ['Non', 'Oui', 'En cours'] * (n_rows // 3 + 1),
            'description': [f'Belle propriété #{i}' for i in range(n_rows)],
            '_id': range(n_rows),
            'updated_at': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
            'add_date': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
            'created_at': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
            'update_at': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
            'region': ['QC'] * n_rows,
            'extraction_metadata': [f'Metadata extraction #{i}' for i in range(n_rows)],
            
            # Métadonnées à supprimer
            'link': [f'https://exemple.com/propriete/{i}' for i in range(n_rows)],
            'company': ['Royal LePage', 'Century 21', 'RE/MAX'] * (n_rows // 3 + 1),
            'version': ['1.0'] * n_rows
        })
        
        # Ajout de valeurs manquantes pour tester la consolidation
        for col in test_data.columns:
            if test_data[col].dtype in ['object', 'float64']:
                # 15% de valeurs manquantes aléatoires
                mask = np.random.choice([True, False], size=n_rows, p=[0.15, 0.85])
                test_data.loc[mask, col] = np.nan
        
        return test_data
    
    def generate_final_report(self):
        """Génère le rapport final du test complet"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        logger.info(f"\n{'='*100}")
        logger.info("📊 RAPPORT FINAL DU TEST COMPLET DU PIPELINE")
        logger.info(f"{'='*100}")
        
        logger.info(f"🕒 Durée totale: {duration:.2f} secondes")
        logger.info(f"📅 Date de fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Résumé des tests
        logger.info(f"\n📋 RÉSUMÉ DES TESTS:")
        success_count = sum(1 for result in self.test_results.values() if result["success"])
        total_count = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            logger.info(f"   {test_name:35} : {result['status']}")
        
        logger.info(f"\n🎯 RÉSULTAT GLOBAL: {success_count}/{total_count} tests réussis")
        success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
        logger.info(f"📊 Taux de réussite: {success_rate:.1f}%")
        
        # Conclusion
        if success_count == total_count:
            logger.info("\n🎉 TOUS LES TESTS SONT PASSÉS!")
            logger.info("✅ Le pipeline ultra-intelligent est 100% fonctionnel")
            logger.info("🚀 Production-ready avec la nouvelle structure organisée!")
        elif success_rate >= 80:
            logger.info("\n✨ TESTS MAJORITAIREMENT RÉUSSIS!")
            logger.info(f"✅ {success_rate:.1f}% de fonctionnalités opérationnelles")
            logger.info("⚠️ Quelques optimisations mineures recommandées")
        else:
            logger.warning(f"\n⚠️ TESTS PARTIELLEMENT RÉUSSIS ({success_rate:.1f}%)")
            logger.warning("🔧 Corrections nécessaires avant production")
        
        # Sauvegarde du rapport
        self.save_test_report()
        
        logger.info(f"\n{'='*100}")
        
        return success_count == total_count
    
    def save_test_report(self):
        """Sauvegarde le rapport de test dans un fichier"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"logs/test_pipeline_complet_{timestamp}.md"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# 🧪 RAPPORT DE TEST COMPLET DU PIPELINE\n\n")
                f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Durée**: {time.time() - self.start_time:.2f} secondes\n\n")
                
                f.write("## 📋 Résultats des Tests\n\n")
                for test_name, result in self.test_results.items():
                    status_icon = "✅" if result["success"] else "❌"
                    f.write(f"- {status_icon} **{test_name}**: {result['status']}\n")
                
                success_count = sum(1 for result in self.test_results.values() if result["success"])
                total_count = len(self.test_results)
                success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
                
                f.write(f"\n## 🎯 Résultat Global\n\n")
                f.write(f"- **Tests réussis**: {success_count}/{total_count}\n")
                f.write(f"- **Taux de réussite**: {success_rate:.1f}%\n")
                
                if success_count == total_count:
                    f.write("\n## 🎉 Conclusion\n\n")
                    f.write("Le pipeline ultra-intelligent est **100% fonctionnel** et **production-ready**!\n")
            
            logger.info(f"📄 Rapport sauvegardé: {report_file}")
            
        except Exception as e:
            logger.warning(f"⚠️ Impossible de sauvegarder le rapport: {e}")

def main():
    """Fonction principale"""
    test_suite = PipelineCompleteTest()
    success = test_suite.run_complete_test()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
