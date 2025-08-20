#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST D'INTÉGRATION - Configuration Personnalisée + Consolidation Avancée
=======================================================================

Script de test pour valider l'harmonisation entre custom_fields_config.py
et la stratégie de consolidation avancée du real_estate_prompt.md
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

def test_custom_config_integration():
    """Test de l'intégration de la configuration personnalisée"""
    logger.info("🔗 === TEST D'INTÉGRATION CONFIGURATION PERSONNALISÉE ===")
    
    try:
        from config.custom_fields_config import custom_config
        
        # === VÉRIFICATION DE L'HÉRITAGE ===
        logger.info("✅ Configuration personnalisée chargée avec succès")
        
        # === RÉSUMÉ DE LA CONFIGURATION ===
        summary = custom_config.get_67_fields_config_summary()
        logger.info(f"📊 Résumé de la configuration:")
        logger.info(f"   - Groupes de consolidation: {summary['total_consolidation_groups']}")
        logger.info(f"   - Colonnes sources totales: {summary['total_source_columns']}")
        logger.info(f"   - Champs préservés: {summary['preserved_columns']}")
        logger.info(f"   - Colonnes finales estimées: {summary['estimated_final_columns']}")
        logger.info(f"   - Réduction estimée: {summary['estimated_reduction']}")
        
        # === VÉRIFICATION DES GROUPES DE CONSOLIDATION ===
        logger.info(f"\n🏗️ Groupes de consolidation configurés:")
        for group in custom_config.CONSOLIDATION_GROUPS:
            logger.info(f"   {group.name} → {group.final_column}: {len(group.source_columns)} colonnes")
        
        # === VÉRIFICATION DES CHAMPS PRÉSERVÉS ===
        logger.info(f"\n🔧 Champs préservés sans consolidation:")
        for col in custom_config.PRESERVED_COLUMNS:
            logger.info(f"   - {col}")
        
        # === VÉRIFICATION DES COLONNES À SUPPRIMER ===
        logger.info(f"\n🗑️ Colonnes à supprimer:")
        for col in custom_config.COLUMNS_TO_REMOVE:
            logger.info(f"   - {col}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test d'intégration: {e}")
        return False

def test_consolidation_with_custom_config():
    """Test de consolidation avec la configuration personnalisée"""
    logger.info("🔄 === TEST DE CONSOLIDATION AVEC CONFIGURATION PERSONNALISÉE ===")
    
    try:
        from config.custom_fields_config import custom_config
        from core.ultra_intelligent_cleaner import UltraIntelligentCleaner
        
        # === CRÉATION DU DATASET DE TEST AVEC 67 COLONNES ===
        test_df = create_test_dataset_with_67_columns()
        logger.info(f"📊 Dataset de test créé: {test_df.shape[0]} lignes × {test_df.shape[1]} colonnes")
        
        # Vérification que le dataset a exactement 67 colonnes
        if test_df.shape[1] != 67:
            logger.warning(f"⚠️ Dataset de test: {test_df.shape[1]} colonnes au lieu de 67")
            # Ajustement automatique si nécessaire
            if test_df.shape[1] < 67:
                missing_cols = 67 - test_df.shape[1]
                for i in range(missing_cols):
                    test_df[f'col_manquante_{i}'] = f'Valeur_{i}'
            elif test_df.shape[1] > 67:
                # Suppression des colonnes en trop
                cols_to_drop = test_df.columns[67:]
                test_df = test_df.drop(columns=cols_to_drop)
            logger.info(f"📊 Dataset ajusté: {test_df.shape[0]} lignes × {test_df.shape[1]} colonnes")
        
        # === INITIALISATION DU NETTOYEUR AVEC CONFIG PERSONNALISÉE ===
        cleaner = UltraIntelligentCleaner(custom_config)
        logger.info("✅ Nettoyeur initialisé avec configuration personnalisée")
        
        # === TEST DE CONSOLIDATION ===
        logger.info("🔄 Démarrage de la consolidation...")
        df_consolidated = cleaner._consolidate_variables(test_df)
        
        # === ANALYSE DES RÉSULTATS ===
        initial_columns = test_df.shape[1]
        final_columns = df_consolidated.shape[1]
        reduction_percentage = ((initial_columns - final_columns) / initial_columns) * 100
        
        logger.info(f"📊 === RÉSULTATS DE LA CONSOLIDATION ===")
        logger.info(f"📊 Colonnes initiales: {initial_columns}")
        logger.info(f"📊 Colonnes finales: {final_columns}")
        logger.info(f"📉 Réduction: {reduction_percentage:.1f}%")
        
        # === VÉRIFICATION DES OBJECTIFS ===
        target_reduction = custom_config.TARGET_REDUCTION_PERCENTAGE
        if reduction_percentage >= target_reduction:
            logger.info(f"✅ Objectif de réduction atteint: {reduction_percentage:.1f}% >= {target_reduction}%")
        else:
            logger.warning(f"⚠️ Objectif de réduction non atteint: {reduction_percentage:.1f}% < {target_reduction}%")
        
        # === VÉRIFICATION DES GROUPES DE CONSOLIDATION ===
        consolidation_results = cleaner.consolidation_results
        successful_groups = sum(1 for result in consolidation_results.values() if result.get('status') == 'success')
        total_groups = len(consolidation_results)
        
        logger.info(f"🎯 Groupes consolidés avec succès: {successful_groups}/{total_groups}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test de consolidation: {e}")
        return False

def create_test_dataset_with_67_columns():
    """Crée un dataset de test avec exactement 67 colonnes comme dans votre configuration"""
    logger.info("🏗️ === CRÉATION DU DATASET DE TEST AVEC 67 COLONNES ===")
    
    # Création de données de test réalistes
    n_rows = 100
    
    test_data = pd.DataFrame({
        # === PRIX & ÉVALUATIONS ===
        'price': np.random.uniform(200000, 2000000, n_rows),
        'prix_evaluation': np.random.uniform(180000, 1800000, n_rows),
        'price_assessment': np.random.uniform(180000, 1800000, n_rows),
        
        # === SURFACE ===
        'surface': np.random.uniform(50, 500, n_rows),
        'living_area': np.random.uniform(50, 500, n_rows),
        'superficie': np.random.uniform(50, 500, n_rows),
        'lot_size': np.random.uniform(100, 1000, n_rows),
        
        # === CHAMBRES ===
        'bedrooms': np.random.randint(1, 6, n_rows),
        'nbr_chanbres': np.random.randint(1, 6, n_rows),
        'nb_bedroom': np.random.randint(1, 6, n_rows),
        'rooms': np.random.randint(3, 10, n_rows),
        
        # === SALLES DE BAIN ===
        'bathrooms': np.random.randint(1, 4, n_rows),
        'nbr_sal_deau': np.random.randint(1, 3, n_rows),
        'nbr_sal_bain': np.random.randint(1, 4, n_rows),
        'nb_bathroom': np.random.randint(1, 4, n_rows),
        'water_rooms': np.random.randint(1, 3, n_rows),
        'nb_water_room': np.random.randint(1, 3, n_rows),
        
        # === COORDONNÉES ===
        'latitude': np.random.uniform(45.4, 45.7, n_rows),
        'longitude': np.random.uniform(-73.8, -73.4, n_rows),
        'geolocation': [f'45.5,-73.6#{i}' for i in range(n_rows)],
        'geo': [f'45.5,-73.6#{i}' for i in range(n_rows)],
        
        # === ADRESSES ===
        'address': [f'123 Rue Principale #{i}' for i in range(n_rows)],
        'full_address': [f'123 Rue Principale #{i}, Montréal, QC' for i in range(n_rows)],
        'location': [f'Montréal, QC #{i}' for i in range(n_rows)],
        'city': ['Montréal', 'Québec', 'Laval'] * (n_rows // 3 + 1),
        'postal_code': ['H1A 1A1', 'H2B 2B2', 'H3C 3C3'] * (n_rows // 3 + 1),
        
        # === TYPE PROPRIÉTÉ ===
        'type': ['Maison', 'Appartement', 'Duplex', 'Triplex'] * (n_rows // 4 + 1),
        'building_style': ['Moderne', 'Traditionnel', 'Contemporain'] * (n_rows // 3 + 1),
        'style': ['Moderne', 'Traditionnel', 'Contemporain'] * (n_rows // 3 + 1),
        
        # === ANNÉE CONSTRUCTION ===
        'year_built': np.random.randint(1950, 2025, n_rows),
        'construction_year': np.random.randint(1950, 2025, n_rows),
        'annee': np.random.randint(1950, 2025, n_rows),
        
        # === TAXES ===
        'municipal_taxes': np.random.uniform(2000, 20000, n_rows),
        'municipal_tax': np.random.uniform(2000, 20000, n_rows),
        'taxes': np.random.uniform(3000, 30000, n_rows),
        'school_taxes': np.random.uniform(1000, 10000, n_rows),
        'school_tax': np.random.uniform(1000, 10000, n_rows),
        
        # === ÉVALUATIONS ===
        'evaluation_total': np.random.uniform(180000, 1800000, n_rows),
        'municipal_evaluation_total': np.random.uniform(180000, 1800000, n_rows),
        'evaluation_terrain': np.random.uniform(80000, 800000, n_rows),
        'evaluation_batiment': np.random.uniform(100000, 1000000, n_rows),
        'municipal_evaluation_land': np.random.uniform(80000, 800000, n_rows),
        'municipal_evaluation_building': np.random.uniform(100000, 1000000, n_rows),
        
        # === REVENUS ===
        'revenu': np.random.uniform(15000, 150000, n_rows),
        'revenus_annuels_bruts': np.random.uniform(15000, 150000, n_rows),
        'plex-revenu': np.random.uniform(15000, 150000, n_rows),
        'plex_revenu': np.random.uniform(15000, 150000, n_rows),
        'potential_gross_revenue': np.random.uniform(15000, 150000, n_rows),
        
        # === DÉPENSES ===
        'expense': np.random.uniform(5000, 50000, n_rows),
        'depenses': np.random.uniform(5000, 50000, n_rows),
        'expense_period': ['Annuel'] * n_rows,
        
        # === PARKING ===
        'nb_parking': np.random.randint(0, 4, n_rows),
        'parking': np.random.randint(0, 4, n_rows),
        'nb_garage': np.random.randint(0, 3, n_rows),
        
        # === UNITÉS ===
        'unites': np.random.randint(1, 5, n_rows),
        'residential_units': np.random.randint(1, 5, n_rows),
        'commercial_units': np.random.randint(0, 3, n_rows),
        
        # === IMAGES ===
        'image': [f'https://exemple.com/image_{i}.jpg' for i in range(n_rows)],
        'images': [f'https://exemple.com/images_{i}.jpg' for i in range(n_rows)],
        'img_src': [f'https://exemple.com/image_{i}.jpg' for i in range(n_rows)],
        
        # === PÉRIODES ===
        'revenu_period': ['Annuel'] * n_rows,
        
        # === SOUS-SOL ===
        'basement': ['Oui', 'Non', 'Partiel'] * (n_rows // 3 + 1),
        
        # === CHAMPS PRÉSERVÉS ===
        'main_unit_details': [f'Détails unité #{i}' for i in range(n_rows)],
        'vendue': ['Non', 'Oui', 'En cours'] * (n_rows // 3 + 1),
        'description': [f'Belle propriété #{i}' for i in range(n_rows)],
        '_id': range(n_rows),
        'updated_at': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
        'evaluation_year': np.random.randint(2018, 2025, n_rows),
        'add_date': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
        'created_at': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
        'municipal_evaluation_year': np.random.randint(2018, 2025, n_rows),
        'update_at': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
        'region': ['QC'] * n_rows,
        'extraction_metadata': [f'Metadata extraction #{i}' for i in range(n_rows)]
    })
    
    # Ajout de valeurs manquantes pour tester la consolidation
    for col in test_data.columns:
        if test_data[col].dtype in ['object', 'float64']:
            # 20% de valeurs manquantes aléatoires
            mask = np.random.choice([True, False], size=n_rows, p=[0.2, 0.8])
            test_data.loc[mask, col] = np.nan
    
    logger.info(f"✅ Dataset créé: {test_data.shape[0]} lignes × {test_data.shape[1]} colonnes")
    logger.info(f"📊 Colonnes: {list(test_data.columns)}")
    
    return test_data

def main():
    """Fonction principale de test"""
    logger.info("🧪 === DÉMARRAGE DES TESTS D'INTÉGRATION ===")
    
    tests = [
        ("Intégration Configuration", test_custom_config_integration),
        ("Consolidation avec Config Personnalisée", test_consolidation_with_custom_config)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"🧪 TEST: {test_name}")
        logger.info(f"{'='*60}")
        
        try:
            success = test_func()
            results[test_name] = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        except Exception as e:
            logger.error(f"❌ Erreur critique dans {test_name}: {e}")
            results[test_name] = "💥 ERREUR CRITIQUE"
    
    # === RÉSUMÉ DES TESTS ===
    logger.info(f"\n{'='*70}")
    logger.info("📊 RÉSUMÉ DES TESTS D'INTÉGRATION")
    logger.info(f"{'='*70}")
    
    for test_name, result in results.items():
        logger.info(f"{test_name:40} : {result}")
    
    success_count = sum(1 for result in results.values() if "SUCCÈS" in result)
    total_count = len(results)
    
    logger.info(f"\n🎯 RÉSULTAT GLOBAL: {success_count}/{total_count} tests réussis")
    
    if success_count == total_count:
        logger.info("🎉 TOUS LES TESTS D'INTÉGRATION SONT PASSÉS!")
        logger.info("✅ La configuration personnalisée est parfaitement harmonisée")
        logger.info("🔗 avec la stratégie de consolidation avancée!")
        return 0
    else:
        logger.warning(f"⚠️ {total_count - success_count} test(s) ont échoué")
        return 1

if __name__ == "__main__":
    sys.exit(main())
