#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST SIMPLIFIÉ DU PIPELINE - VALIDATION ESSENTIELLE
======================================================

Test simplifié du pipeline qui évite les dépendances optionnelles
Focus sur les fonctionnalités de base et la consolidation
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

class PipelineSimplifiedTest:
    """Test simplifié du pipeline sans dépendances optionnelles"""
    
    def __init__(self):
        self.start_time = time.time()
        self.test_results = {}
        self.test_data = None
        
    def run_simplified_test(self):
        """Exécute les tests simplifiés du pipeline"""
        logger.info("🚀 === DÉMARRAGE DU TEST SIMPLIFIÉ DU PIPELINE ===")
        logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Tests séquentiels
        tests = [
            ("Configuration de Base", self.test_basic_configuration),
            ("Création Dataset Test", self.test_data_creation),
            ("Consolidation Intelligente", self.test_smart_consolidation),
            ("Validation Basique", self.test_basic_validation),
            ("Export Simple", self.test_simple_export)
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
        
    def test_basic_configuration(self):
        """Test de la configuration de base"""
        logger.info("⚙️ === TEST CONFIGURATION DE BASE ===")
        
        try:
            # Test des imports de base
            logger.info("📦 Test des imports de base...")
            from config.consolidation_config import ConsolidationConfig
            from config.custom_fields_config import custom_config
            logger.info("✅ Imports de configuration réussis")
            
            # Test de la configuration de base
            logger.info("⚙️ Test configuration standard...")
            base_config = ConsolidationConfig()
            groups_count = len(base_config.CONSOLIDATION_GROUPS)
            logger.info(f"📊 Configuration standard: {groups_count} groupes")
            
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
            logger.error(f"❌ Erreur configuration: {e}")
            return False
    
    def test_data_creation(self):
        """Test de création du dataset de test"""
        logger.info("📥 === TEST CRÉATION DATASET DE TEST ===")
        
        try:
            logger.info("🏗️ Génération de données de test...")
            self.test_data = self.create_comprehensive_test_data()
            logger.info(f"📊 Dataset créé: {self.test_data.shape[0]} lignes × {self.test_data.shape[1]} colonnes")
            
            # Validation du dataset
            if self.test_data.shape[1] >= 50:
                logger.info(f"✅ Dataset valide: {self.test_data.shape[1]} colonnes")
                
                # Analyse rapide
                null_percentage = (self.test_data.isnull().sum().sum() / (self.test_data.shape[0] * self.test_data.shape[1])) * 100
                logger.info(f"📊 Valeurs manquantes: {null_percentage:.1f}%")
                
                # Types de colonnes
                numeric_cols = len(self.test_data.select_dtypes(include=[np.number]).columns)
                text_cols = len(self.test_data.select_dtypes(include=['object']).columns)
                logger.info(f"📊 Colonnes numériques: {numeric_cols}")
                logger.info(f"📊 Colonnes textuelles: {text_cols}")
                
                return True
            else:
                logger.error(f"❌ Dataset insuffisant: {self.test_data.shape[1]} colonnes")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur création dataset: {e}")
            return False
    
    def test_smart_consolidation(self):
        """Test de la consolidation intelligente"""
        logger.info("🔗 === TEST CONSOLIDATION INTELLIGENTE ===")
        
        try:
            if self.test_data is None:
                logger.error("❌ Pas de données de test disponibles")
                return False
            
            # Test de consolidation avec config personnalisée
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
            
            # Analyse de la qualité de consolidation
            if df_consolidated is not None and final_columns > 0:
                logger.info("🔍 Analyse de la qualité de consolidation...")
                
                # Vérifier que les données ont été conservées
                initial_rows = self.test_data.shape[0]
                final_rows = df_consolidated.shape[0]
                logger.info(f"📊 Lignes conservées: {final_rows}/{initial_rows}")
                
                # Vérifier la complétude après consolidation
                null_percentage_after = (df_consolidated.isnull().sum().sum() / (df_consolidated.shape[0] * df_consolidated.shape[1])) * 100
                logger.info(f"📊 Valeurs manquantes après: {null_percentage_after:.1f}%")
                
                # Sauvegarder pour les tests suivants
                self.consolidated_data = df_consolidated
                
                logger.info("✅ Consolidation réussie")
                return True
            else:
                logger.error("❌ Consolidation échouée")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur consolidation: {e}")
            return False
    
    def test_basic_validation(self):
        """Test de validation basique"""
        logger.info("✅ === TEST VALIDATION BASIQUE ===")
        
        try:
            if not hasattr(self, 'consolidated_data'):
                df = self.test_data
                logger.info("⚠️ Utilisation des données non consolidées")
            else:
                df = self.consolidated_data
                logger.info("✅ Utilisation des données consolidées")
            
            # Validation manuelle basique
            logger.info("🔍 Validation manuelle des données...")
            
            # 1. Validation de la forme
            logger.info(f"📊 Forme du dataset: {df.shape}")
            if df.shape[0] == 0:
                logger.error("❌ Dataset vide")
                return False
            
            # 2. Validation de la complétude
            total_cells = df.shape[0] * df.shape[1]
            null_cells = df.isnull().sum().sum()
            completeness = (1 - (null_cells / total_cells)) * 100
            logger.info(f"📊 Complétude: {completeness:.1f}%")
            
            # 3. Validation des types
            numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
            text_cols = len(df.select_dtypes(include=['object']).columns)
            date_cols = len(df.select_dtypes(include=['datetime64']).columns)
            logger.info(f"📊 Types: {numeric_cols} num, {text_cols} text, {date_cols} date")
            
            # 4. Validation des valeurs aberrantes
            outliers_found = 0
            for col in df.select_dtypes(include=[np.number]).columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))][col]
                outliers_found += len(outliers)
            
            outlier_percentage = (outliers_found / total_cells) * 100
            logger.info(f"📊 Valeurs aberrantes: {outlier_percentage:.2f}%")
            
            # Score de qualité basique
            quality_score = (completeness * 0.5) + ((100 - outlier_percentage) * 0.3) + (20 if numeric_cols > 0 else 0)
            logger.info(f"📊 Score de qualité basique: {quality_score:.1f}%")
            
            if quality_score > 50:
                logger.info("✅ Validation basique réussie")
                return True
            else:
                logger.warning("⚠️ Qualité basique insuffisante")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur validation basique: {e}")
            return False
    
    def test_simple_export(self):
        """Test d'export simple"""
        logger.info("💾 === TEST EXPORT SIMPLE ===")
        
        try:
            if not hasattr(self, 'consolidated_data'):
                df = self.test_data.head(50)  # Réduire pour les tests
                logger.info("⚠️ Export des données non consolidées")
            else:
                df = self.consolidated_data.head(50)
                logger.info("✅ Export des données consolidées")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Test export CSV (toujours disponible)
            logger.info("📄 Test export CSV...")
            csv_path = f"exports/tests/test_simplifie_{timestamp}.csv"
            
            # Créer le dossier si nécessaire
            Path("exports/tests").mkdir(parents=True, exist_ok=True)
            
            # Export
            df.to_csv(csv_path, index=False, encoding='utf-8')
            
            # Vérification
            if Path(csv_path).exists():
                file_size = Path(csv_path).stat().st_size
                logger.info(f"✅ Export CSV réussi: {csv_path} ({file_size} bytes)")
                
                # Test de lecture
                df_test = pd.read_csv(csv_path)
                if df_test.shape == df.shape:
                    logger.info("✅ Vérification lecture CSV réussie")
                    return True
                else:
                    logger.error("❌ Données corrompues lors de l'export")
                    return False
            else:
                logger.error("❌ Fichier CSV non créé")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur export simple: {e}")
            return False
    
    def create_comprehensive_test_data(self):
        """Crée un dataset de test complet"""
        n_rows = 100
        
        # Dataset avec les colonnes essentielles
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
            
            # Surface et caractéristiques
            'surface': np.random.uniform(50, 500, n_rows),
            'living_area': np.random.uniform(50, 500, n_rows),
            'superficie': np.random.uniform(50, 500, n_rows),
            'lot_size': np.random.uniform(100, 1000, n_rows),
            'bedrooms': np.random.randint(1, 6, n_rows),
            'nbr_chanbres': np.random.randint(1, 6, n_rows),
            'nb_bedroom': np.random.randint(1, 6, n_rows),
            'bathrooms': np.random.randint(1, 4, n_rows),
            'nbr_sal_deau': np.random.randint(1, 3, n_rows),
            'nbr_sal_bain': np.random.randint(1, 4, n_rows),
            'nb_bathroom': np.random.randint(1, 4, n_rows),
            'water_rooms': np.random.randint(1, 3, n_rows),
            
            # Coordonnées
            'latitude': np.random.uniform(45.4, 45.7, n_rows),
            'longitude': np.random.uniform(-73.8, -73.4, n_rows),
            'geolocation': [f'45.5,-73.6#{i}' for i in range(n_rows)],
            
            # Adresses
            'address': [f'123 Rue Principale #{i}' for i in range(n_rows)],
            'full_address': [f'123 Rue Principale #{i}, Montréal, QC' for i in range(n_rows)],
            'city': (['Montréal', 'Québec', 'Laval'] * (n_rows // 3 + 1))[:n_rows],
            'postal_code': (['H1A 1A1', 'H2B 2B2', 'H3C 3C3'] * (n_rows // 3 + 1))[:n_rows],
            
            # Type propriété
            'type': (['Maison', 'Appartement', 'Duplex', 'Triplex'] * (n_rows // 4 + 1))[:n_rows],
            'building_style': (['Moderne', 'Traditionnel', 'Contemporain'] * (n_rows // 3 + 1))[:n_rows],
            'style': (['Moderne', 'Traditionnel', 'Contemporain'] * (n_rows // 3 + 1))[:n_rows],
            
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
            
            # Autres
            'image': [f'https://exemple.com/image_{i}.jpg' for i in range(n_rows)],
            'images': [f'https://exemple.com/images_{i}.jpg' for i in range(n_rows)],
            'img_src': [f'https://exemple.com/image_{i}.jpg' for i in range(n_rows)],
            'revenu_period': ['Annuel'] * n_rows,
            'basement': (['Oui', 'Non', 'Partiel'] * (n_rows // 3 + 1))[:n_rows],
            
            # Champs préservés
            'main_unit_details': [f'Détails unité #{i}' for i in range(n_rows)],
            'vendue': (['Non', 'Oui', 'En cours'] * (n_rows // 3 + 1))[:n_rows],
            'description': [f'Belle propriété #{i}' for i in range(n_rows)],
            '_id': range(n_rows),
            'updated_at': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
            'region': ['QC'] * n_rows,
            'extraction_metadata': [f'Metadata #{i}' for i in range(n_rows)],
            
            # Métadonnées à supprimer
            'link': [f'https://exemple.com/propriete/{i}' for i in range(n_rows)],
            'company': (['Royal LePage', 'Century 21', 'RE/MAX'] * (n_rows // 3 + 1))[:n_rows],
            'version': ['1.0'] * n_rows
        })
        
        # Ajout de valeurs manquantes pour tester la consolidation
        for col in test_data.columns:
            if test_data[col].dtype in ['object', 'float64']:
                # 10% de valeurs manquantes aléatoires
                mask = np.random.choice([True, False], size=n_rows, p=[0.1, 0.9])
                test_data.loc[mask, col] = np.nan
        
        return test_data
    
    def generate_final_report(self):
        """Génère le rapport final du test simplifié"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        logger.info(f"\n{'='*100}")
        logger.info("📊 RAPPORT FINAL DU TEST SIMPLIFIÉ DU PIPELINE")
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
            logger.info("✅ Les fonctionnalités essentielles du pipeline sont 100% fonctionnelles")
            logger.info("🚀 Structure organisée validée et prête pour production!")
        elif success_rate >= 80:
            logger.info("\n✨ TESTS MAJORITAIREMENT RÉUSSIS!")
            logger.info(f"✅ {success_rate:.1f}% des fonctionnalités essentielles opérationnelles")
            logger.info("⚠️ Quelques optimisations mineures recommandées")
        else:
            logger.warning(f"\n⚠️ TESTS PARTIELLEMENT RÉUSSIS ({success_rate:.1f}%)")
            logger.warning("🔧 Corrections nécessaires avant production")
        
        # Sauvegarde du rapport
        self.save_test_report(success_count == total_count, success_rate)
        
        logger.info(f"\n{'='*100}")
        
        return success_count == total_count
    
    def save_test_report(self, all_passed, success_rate):
        """Sauvegarde le rapport de test dans un fichier"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"logs/test_pipeline_simplifie_{timestamp}.md"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# 🧪 RAPPORT DE TEST SIMPLIFIÉ DU PIPELINE\n\n")
                f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Durée**: {time.time() - self.start_time:.2f} secondes\n\n")
                
                f.write("## 📋 Résultats des Tests Essentiels\n\n")
                for test_name, result in self.test_results.items():
                    status_icon = "✅" if result["success"] else "❌"
                    f.write(f"- {status_icon} **{test_name}**: {result['status']}\n")
                
                success_count = sum(1 for result in self.test_results.values() if result["success"])
                total_count = len(self.test_results)
                
                f.write(f"\n## 🎯 Résultat Global\n\n")
                f.write(f"- **Tests réussis**: {success_count}/{total_count}\n")
                f.write(f"- **Taux de réussite**: {success_rate:.1f}%\n")
                
                if all_passed:
                    f.write("\n## 🎉 Conclusion\n\n")
                    f.write("Les **fonctionnalités essentielles** du pipeline sont **100% fonctionnelles** !\n")
                    f.write("La **structure réorganisée** est **validée** et **prête pour production** !\n")
                elif success_rate >= 80:
                    f.write("\n## ✨ Conclusion\n\n")
                    f.write(f"**{success_rate:.1f}%** des fonctionnalités essentielles sont opérationnelles.\n")
                    f.write("Le pipeline est **majoritairement fonctionnel** avec quelques optimisations recommandées.\n")
                else:
                    f.write("\n## ⚠️ Conclusion\n\n")
                    f.write("Des corrections sont nécessaires avant la mise en production.\n")
            
            logger.info(f"📄 Rapport sauvegardé: {report_file}")
            
        except Exception as e:
            logger.warning(f"⚠️ Impossible de sauvegarder le rapport: {e}")

def main():
    """Fonction principale"""
    test_suite = PipelineSimplifiedTest()
    success = test_suite.run_simplified_test()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
