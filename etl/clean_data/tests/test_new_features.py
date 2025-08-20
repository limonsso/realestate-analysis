#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST DES NOUVELLES FONCTIONNALITÉS - PIPELINE ULTRA-INTELLIGENT
===================================================================

Script de test pour valider l'intégration des nouvelles fonctionnalités
Basé sur les spécifications du real_estate_prompt.md
"""

import sys
import os
import logging
import pandas as pd
import numpy as np
from pathlib import Path

# Ajout du répertoire parent au PYTHONPATH pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_spatial_clustering():
    """Test du clustering spatial DBSCAN"""
    logger.info("🌍 === TEST CLUSTERING SPATIAL ===")
    
    try:
        from intelligence.similarity_detector import SimilarityDetector
        
        # Création de données de test avec coordonnées
        test_data = pd.DataFrame({
            'latitude': [45.5017, 45.5018, 45.5019, 45.5020, 45.5021, 45.5022],
            'longitude': [-73.5673, -73.5674, -73.5675, -73.5676, -73.5677, -73.5678],
            'price': [500000, 550000, 600000, 650000, 700000, 750000],
            'surface': [1000, 1100, 1200, 1300, 1400, 1500]
        })
        
        detector = SimilarityDetector()
        results = detector.spatial_clustering(test_data, eps=0.001, min_samples=2)
        
        if results.get("success"):
            logger.info(f"✅ Clustering spatial réussi: {results['n_clusters']} zones")
            logger.info(f"📊 Zones créées: {results['zones_spatiales']}")
            return True
        else:
            logger.error(f"❌ Clustering spatial échoué: {results.get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur test clustering spatial: {e}")
        return False

def test_categorization():
    """Test de la catégorisation automatique"""
    logger.info("🏷️ === TEST CATÉGORISATION AUTOMATIQUE ===")
    
    try:
        from core.ultra_intelligent_cleaner import UltraIntelligentCleaner
        from config.consolidation_config import ConsolidationConfig
        
        # Création de données de test
        test_data = pd.DataFrame({
            'price_final': [500000, 750000, 1000000, 1500000, 2000000],
            'roi_brut': [0.05, 0.08, 0.12, 0.15, 0.20],
            'revenue_final': [25000, 60000, 120000, 225000, 400000],
            'year_built_final': [1980, 1990, 2000, 2010, 2020],
            'evaluation_total_final': [450000, 700000, 950000, 1400000, 1900000],
            'latitude_final': [45.5017, 45.5018, 45.5019, 45.5020, 45.5021],
            'longitude_final': [-73.5673, -73.5674, -73.5675, -73.5676, -73.5677]
        })
        
        config = ConsolidationConfig()
        cleaner = UltraIntelligentCleaner(config)
        
        # Test de la catégorisation
        df_categorized = cleaner.categorize_investment_opportunities(test_data)
        
        # Vérification des nouvelles colonnes
        expected_columns = ['segment_roi', 'classe_prix', 'type_opportunite', 'score_qualite', 'classe_investissement']
        missing_columns = [col for col in expected_columns if col not in df_categorized.columns]
        
        if not missing_columns:
            logger.info("✅ Catégorisation réussie")
            logger.info(f"📊 Segments ROI: {df_categorized['segment_roi'].value_counts().to_dict()}")
            logger.info(f"💎 Classes prix: {df_categorized['classe_prix'].value_counts().to_dict()}")
            logger.info(f"🎯 Types opportunités: {df_categorized['type_opportunite'].value_counts().to_dict()}")
            return True
        else:
            logger.error(f"❌ Colonnes manquantes: {missing_columns}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur test catégorisation: {e}")
        return False

def test_dashboard():
    """Test du dashboard de validation"""
    logger.info("📊 === TEST DASHBOARD DE VALIDATION ===")
    
    try:
        from dashboard.validation_dashboard import ValidationDashboard
        
        # Création de données de test
        test_data = pd.DataFrame({
            'price': [500000, 750000, 1000000, 1500000, 2000000],
            'surface': [1000, 1100, 1200, 1300, 1400],
            'roi': [0.05, 0.08, 0.12, 0.15, 0.20],
            'latitude': [45.5017, 45.5018, 45.5019, 45.5020, 45.5021],
            'longitude': [-73.5673, -73.5674, -73.5675, -73.5676, -73.5677]
        })
        
        # Ajout de valeurs manquantes pour tester la complétude
        test_data.loc[0, 'price'] = np.nan
        test_data.loc[1, 'surface'] = np.nan
        
        dashboard = ValidationDashboard()
        
        # Test de création du dashboard
        quality_metrics = {
            'completeness': 0.9,
            'accuracy': 0.95,
            'consistency': 0.88
        }
        
        dashboard_result = dashboard.create_quality_overview_dashboard(test_data, quality_metrics)
        
        if 'error' not in dashboard_result:
            logger.info("✅ Dashboard créé avec succès")
            logger.info(f"📊 Figures créées: {len(dashboard_result['figures'])}")
            
            # Test d'export
            export_path = dashboard.export_dashboard(dashboard_result, "test_dashboard")
            if export_path:
                logger.info(f"✅ Dashboard exporté: {export_path}")
                return True
            else:
                logger.warning("⚠️ Export du dashboard échoué")
                return False
        else:
            logger.error(f"❌ Erreur création dashboard: {dashboard_result['error']}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur test dashboard: {e}")
        return False

def test_performance_optimizations():
    """Test des optimisations de performance"""
    logger.info("🚀 === TEST OPTIMISATIONS DE PERFORMANCE ===")
    
    try:
        from performance.performance_optimizer import PerformanceOptimizer
        
        optimizer = PerformanceOptimizer()
        optimizations_status = optimizer.enable_all_optimizations()
        
        active_count = sum(optimizations_status.values())
        total_count = len(optimizations_status)
        
        logger.info(f"🎯 Optimisations activées: {active_count}/{total_count}")
        logger.info(f"📊 Status: {optimizations_status}")
        
        if active_count > 0:
            logger.info("✅ Au moins une optimisation activée")
            return True
        else:
            logger.warning("⚠️ Aucune optimisation activée")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur test optimisations: {e}")
        return False

def main():
    """Fonction principale de test"""
    logger.info("🧪 === DÉMARRAGE DES TESTS DES NOUVELLES FONCTIONNALITÉS ===")
    
    tests = [
        ("Clustering Spatial", test_spatial_clustering),
        ("Catégorisation Automatique", test_categorization),
        ("Dashboard de Validation", test_dashboard),
        ("Optimisations de Performance", test_performance_optimizations)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"🧪 TEST: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            success = test_func()
            results[test_name] = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        except Exception as e:
            logger.error(f"❌ Erreur critique dans {test_name}: {e}")
            results[test_name] = "💥 ERREUR CRITIQUE"
    
    # === RÉSUMÉ DES TESTS ===
    logger.info(f"\n{'='*60}")
    logger.info("📊 RÉSUMÉ DES TESTS")
    logger.info(f"{'='*60}")
    
    for test_name, result in results.items():
        logger.info(f"{test_name:30} : {result}")
    
    success_count = sum(1 for result in results.values() if "SUCCÈS" in result)
    total_count = len(results)
    
    logger.info(f"\n🎯 RÉSULTAT GLOBAL: {success_count}/{total_count} tests réussis")
    
    if success_count == total_count:
        logger.info("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        return 0
    else:
        logger.warning(f"⚠️ {total_count - success_count} test(s) ont échoué")
        return 1

if __name__ == "__main__":
    sys.exit(main())
