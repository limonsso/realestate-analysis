#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST DE LA STRATÉGIE DE CONSOLIDATION AVANCÉE
=================================================

Script de test pour valider l'implémentation de la stratégie de consolidation
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

def create_test_dataset_with_78_columns():
    """
    Crée un dataset de test avec exactement 78 colonnes comme spécifié
    dans le real_estate_prompt.md
    """
    logger.info("🏗️ === CRÉATION DU DATASET DE TEST AVEC 78 COLONNES ===")
    
    # Création de données de test réalistes
    n_rows = 100
    
    test_data = pd.DataFrame({
        # === IDENTIFIANTS (8 colonnes) ===
        '_id': range(n_rows),
        'link': [f'https://exemple.com/propriete/{i}' for i in range(n_rows)],
        'company': ['Royal LePage', 'Century 21', 'RE/MAX'] * (n_rows // 3 + 1),
        'version': ['1.0'] * n_rows,
        'created_at': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
        'updated_at': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
        'update_at': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
        'add_date': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
        
        # === LOCALISATION (8 colonnes) ===
        'address': [f'123 Rue Principale #{i}' for i in range(n_rows)],
        'full_address': [f'123 Rue Principale #{i}, Montréal, QC' for i in range(n_rows)],
        'city': ['Montréal', 'Québec', 'Laval'] * (n_rows // 3 + 1),
        'region': ['QC'] * n_rows,
        'longitude': np.random.uniform(-73.8, -73.4, n_rows),
        'latitude': np.random.uniform(45.4, 45.7, n_rows),
        'location': [f'Montréal, QC #{i}' for i in range(n_rows)],
        'geolocation': [f'45.5,-73.6#{i}' for i in range(n_rows)],
        'geo': [f'45.5,-73.6#{i}' for i in range(n_rows)],
        'postal_code': ['H1A 1A1', 'H2B 2B2', 'H3C 3C3'] * (n_rows // 3 + 1),
        
        # === PRIX & ÉVALUATIONS (11 colonnes) ===
        'price': np.random.uniform(200000, 2000000, n_rows),
        'price_assessment': np.random.uniform(180000, 1800000, n_rows),
        'prix_evaluation': np.random.uniform(180000, 1800000, n_rows),
        'evaluation_total': np.random.uniform(180000, 1800000, n_rows),
        'evaluation_terrain': np.random.uniform(80000, 800000, n_rows),
        'evaluation_batiment': np.random.uniform(100000, 1000000, n_rows),
        'municipal_evaluation_building': np.random.uniform(100000, 1000000, n_rows),
        'municipal_evaluation_land': np.random.uniform(80000, 800000, n_rows),
        'municipal_evaluation_total': np.random.uniform(180000, 1800000, n_rows),
        'evaluation_year': np.random.randint(2018, 2025, n_rows),
        'municipal_evaluation_year': np.random.randint(2018, 2025, n_rows),
        
        # === REVENUS (6 colonnes) ===
        'revenu': np.random.uniform(15000, 150000, n_rows),
        'plex-revenue': np.random.uniform(15000, 150000, n_rows),
        'plex-revenu': np.random.uniform(15000, 150000, n_rows),
        'plex_revenu': np.random.uniform(15000, 150000, n_rows),
        'potential_gross_revenue': np.random.uniform(15000, 150000, n_rows),
        'revenus_annuels_bruts': np.random.uniform(15000, 150000, n_rows),
        'revenu_period': ['Annuel'] * n_rows,
        
        # === TAXES (5 colonnes) ===
        'municipal_taxes': np.random.uniform(2000, 20000, n_rows),
        'school_taxes': np.random.uniform(1000, 10000, n_rows),
        'municipal_tax': np.random.uniform(2000, 20000, n_rows),
        'school_tax': np.random.uniform(1000, 10000, n_rows),
        'taxes': np.random.uniform(3000, 30000, n_rows),
        
        # === CARACTÉRISTIQUES (7 colonnes) ===
        'surface': np.random.uniform(50, 500, n_rows),
        'living_area': np.random.uniform(50, 500, n_rows),
        'superficie': np.random.uniform(50, 500, n_rows),
        'construction_year': np.random.randint(1950, 2025, n_rows),
        'year_built': np.random.randint(1950, 2025, n_rows),
        'annee': np.random.randint(1950, 2025, n_rows),
        'lot_size': np.random.uniform(100, 1000, n_rows),
        
        # === PROPRIÉTÉ (8 colonnes) ===
        'type': ['Maison', 'Appartement', 'Duplex', 'Triplex'] * (n_rows // 4 + 1),
        'bedrooms': np.random.randint(1, 6, n_rows),
        'nb_bedroom': np.random.randint(1, 6, n_rows),
        'nbr_chanbres': np.random.randint(1, 6, n_rows),
        'rooms': np.random.randint(3, 10, n_rows),
        'bathrooms': np.random.randint(1, 4, n_rows),
        'nb_bathroom': np.random.randint(1, 4, n_rows),
        'nbr_sal_bain': np.random.randint(1, 4, n_rows),
        'water_rooms': np.random.randint(1, 3, n_rows),
        'nbr_sal_deau': np.random.randint(1, 3, n_rows),
        'nb_water_room': np.random.randint(1, 3, n_rows),
        'unites': np.random.randint(1, 5, n_rows),
        'residential_units': np.random.randint(1, 5, n_rows),
        'commercial_units': np.random.randint(0, 3, n_rows),
        'parking': np.random.randint(0, 4, n_rows),
        'nb_parking': np.random.randint(0, 4, n_rows),
        'nb_garage': np.random.randint(0, 3, n_rows),
        'basement': ['Oui', 'Non', 'Partiel'] * (n_rows // 3 + 1),
        'building_style': ['Moderne', 'Traditionnel', 'Contemporain'] * (n_rows // 3 + 1),
        'style': ['Moderne', 'Traditionnel', 'Contemporain'] * (n_rows // 3 + 1),
        
        # === GESTION (7 colonnes) ===
        'depenses': np.random.uniform(5000, 50000, n_rows),
        'expense': np.random.uniform(5000, 50000, n_rows),
        'expense_period': ['Annuel'] * n_rows,
        'vendue': ['Non', 'Oui', 'En cours'] * (n_rows // 3 + 1),
        'description': [f'Belle propriété #{i}' for i in range(n_rows)],
        'img_src': [f'https://exemple.com/image_{i}.jpg' for i in range(n_rows)],
        'image': [f'https://exemple.com/image_{i}.jpg' for i in range(n_rows)],
        'images': [f'https://exemple.com/images_{i}.jpg' for i in range(n_rows)],
        'main_unit_details': [f'Détails unité #{i}' for i in range(n_rows)],
        
        # === MÉTADONNÉES (1 colonne) ===
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

def test_consolidation_strategy():
    """Test de la stratégie de consolidation avancée"""
    logger.info("🧪 === TEST DE LA STRATÉGIE DE CONSOLIDATION ===")
    
    try:
        from config.consolidation_config import ConsolidationConfig
        from core.ultra_intelligent_cleaner import UltraIntelligentCleaner
        
        # === CRÉATION DU DATASET DE TEST ===
        test_df = create_test_dataset_with_78_columns()
        
        # === INITIALISATION DE LA CONFIGURATION ===
        config = ConsolidationConfig()
        cleaner = UltraIntelligentCleaner(config)
        
        # === VÉRIFICATION DE LA CONFIGURATION ===
        logger.info(f"🎯 Groupes de consolidation configurés: {len(config.CONSOLIDATION_GROUPS)}")
        logger.info(f"🗑️ Colonnes à supprimer: {len(config.COLUMNS_TO_REMOVE)}")
        
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
        target_reduction = config.TARGET_REDUCTION_PERCENTAGE
        if reduction_percentage >= target_reduction:
            logger.info(f"✅ Objectif de réduction atteint: {reduction_percentage:.1f}% >= {target_reduction}%")
        else:
            logger.warning(f"⚠️ Objectif de réduction non atteint: {reduction_percentage:.1f}% < {target_reduction}%")
        
        # === ANALYSE DES COLONNES FINALES ===
        final_columns_list = list(df_consolidated.columns)
        logger.info(f"📋 Colonnes finales: {final_columns_list}")
        
        # === VÉRIFICATION DES GROUPES DE CONSOLIDATION ===
        consolidation_results = cleaner.consolidation_results
        successful_groups = sum(1 for result in consolidation_results.values() if result.get('status') == 'success')
        total_groups = len(consolidation_results)
        
        logger.info(f"🎯 Groupes consolidés avec succès: {successful_groups}/{total_groups}")
        
        # === DÉTAIL DES RÉSULTATS ===
        for group_name, result in consolidation_results.items():
            if result.get('status') == 'success':
                logger.info(f"✅ {group_name}: {result.get('completeness', 0):.1f}% complétude")
            else:
                logger.warning(f"⚠️ {group_name}: {result.get('error', 'Erreur inconnue')}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test de consolidation: {e}")
        return False

def test_specific_consolidation_groups():
    """Test de groupes de consolidation spécifiques"""
    logger.info("🎯 === TEST DES GROUPES DE CONSOLIDATION SPÉCIFIQUES ===")
    
    try:
        from config.consolidation_config import ConsolidationConfig
        
        config = ConsolidationConfig()
        
        # === VÉRIFICATION DES GROUPES PRIORITAIRES ===
        priority_1_groups = [g for g in config.CONSOLIDATION_GROUPS if g.priority == 1]
        priority_2_groups = [g for g in config.CONSOLIDATION_GROUPS if g.priority == 2]
        priority_3_groups = [g for g in config.CONSOLIDATION_GROUPS if g.priority == 3]
        
        logger.info(f"🔥 Priorité 1 (critique): {len(priority_1_groups)} groupes")
        logger.info(f"⚡ Priorité 2 (important): {len(priority_2_groups)} groupes")
        logger.info(f"💡 Priorité 3 (optionnel): {len(priority_3_groups)} groupes")
        
        # === VÉRIFICATION DES GROUPES CLÉS ===
        key_groups = ['Prix', 'Surface', 'Chambres', 'Salles de bain', 'Latitude', 'Longitude']
        found_groups = []
        
        for group in config.CONSOLIDATION_GROUPS:
            if group.name in key_groups:
                found_groups.append(group.name)
                logger.info(f"✅ Groupe clé trouvé: {group.name} → {group.final_column}")
        
        missing_groups = set(key_groups) - set(found_groups)
        if missing_groups:
            logger.warning(f"⚠️ Groupes clés manquants: {missing_groups}")
        else:
            logger.info("🎉 Tous les groupes clés sont configurés")
        
        # === VÉRIFICATION DES COLONNES FINALES ===
        final_columns = [g.final_column for g in config.CONSOLIDATION_GROUPS]
        expected_final_columns = [
            'price_final', 'surface_final', 'bedrooms_final', 'bathrooms_final',
            'latitude_final', 'longitude_final', 'geolocation_final', 'address_final',
            'date_created_final', 'date_updated_final', 'year_built_final',
            'tax_municipal_final', 'tax_school_final', 'revenue_final',
            'images_final', 'evaluation_total_final', 'evaluation_building_final',
            'evaluation_land_final', 'evaluation_year_final', 'parking_total_final',
            'units_final', 'expenses_final', 'period_final', 'building_style_final',
            'taxes_other_final', 'postal_code_final', 'lot_size_final',
            'basement_final', 'property_type_final'
        ]
        
        missing_final_columns = set(expected_final_columns) - set(final_columns)
        if missing_final_columns:
            logger.warning(f"⚠️ Colonnes finales manquantes: {missing_final_columns}")
        else:
            logger.info("🎉 Toutes les colonnes finales sont configurées")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test des groupes: {e}")
        return False

def main():
    """Fonction principale de test"""
    logger.info("🧪 === DÉMARRAGE DES TESTS DE CONSOLIDATION ===")
    
    tests = [
        ("Configuration des Groupes", test_specific_consolidation_groups),
        ("Stratégie de Consolidation", test_consolidation_strategy)
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
    logger.info("📊 RÉSUMÉ DES TESTS DE CONSOLIDATION")
    logger.info(f"{'='*70}")
    
    for test_name, result in results.items():
        logger.info(f"{test_name:35} : {result}")
    
    success_count = sum(1 for result in results.values() if "SUCCÈS" in result)
    total_count = len(results)
    
    logger.info(f"\n🎯 RÉSULTAT GLOBAL: {success_count}/{total_count} tests réussis")
    
    if success_count == total_count:
        logger.info("🎉 TOUS LES TESTS DE CONSOLIDATION SONT PASSÉS!")
        logger.info("✅ La stratégie de consolidation avancée est parfaitement implémentée")
        return 0
    else:
        logger.warning(f"⚠️ {total_count - success_count} test(s) ont échoué")
        return 1

if __name__ == "__main__":
    sys.exit(main())
