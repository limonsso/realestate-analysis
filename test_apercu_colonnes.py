#!/usr/bin/env python3
"""
Script de test pour démontrer l'aperçu amélioré des colonnes
"""

import sys
import os
sys.path.append('lib')

from mongodb_loader import MongoDBLoader
import pandas as pd

def main():
    """Fonction principale pour tester l'aperçu des colonnes"""
    print("🧪 === TEST APERÇU AMÉLIORÉ DES COLONNES ===")
    
    # Créer un loader MongoDB
    loader = MongoDBLoader()
    
    # Créer un DataFrame d'exemple avec différents types de colonnes
    print("\n📊 Création d'un DataFrame d'exemple...")
    
    # Données d'exemple
    data = {
        'price': [500000, 750000, 1200000, 350000, 900000],
        'surface': [1200, 1800, 2500, 800, 2000],
        'nb_bedrooms': [3, 4, 5, 2, 4],
        'nb_bathrooms': [2, 3, 4, 1, 3],
        'city': ['Montréal', 'Laval', 'Brossard', 'Longueuil', 'Saint-Laurent'],
        'type': ['Maison', 'Maison', 'Maison', 'Condo', 'Maison'],
        'address': ['123 Rue Principale', '456 Ave des Fleurs', '789 Blvd du Lac', '321 Rue du Parc', '654 Ave Centrale'],
        'construction_year': [1990, 2005, 2010, 1985, 2000],
        'is_sold': [True, False, True, False, True],
        'add_date': pd.to_datetime(['2024-01-15', '2024-02-20', '2024-03-10', '2024-01-30', '2024-02-15']),
        'longitude': [-73.5673, -73.7123, -73.4567, -73.7890, -73.3456],
        'latitude': [45.5017, 45.5500, 45.4500, 45.5000, 45.5200]
    }
    
    df = pd.DataFrame(data)
    
    print(f"✅ DataFrame créé: {df.shape[0]} propriétés × {df.shape[1]} colonnes")
    
    # === TEST 1: APERÇU GÉNÉRAL ===
    print("\n" + "="*60)
    print("🧪 TEST 1: APERÇU GÉNÉRAL DES DONNÉES")
    print("="*60)
    loader.print_data_summary(df)
    
    # === TEST 2: APERÇU DÉTAILLÉ ===
    print("\n" + "="*60)
    print("🧪 TEST 2: APERÇU DÉTAILLÉ DES COLONNES")
    print("="*60)
    loader.print_detailed_columns_info(df)
    
    # === TEST 3: APERÇU AVEC LIMITE ===
    print("\n" + "="*60)
    print("🧪 TEST 3: APERÇU DÉTAILLÉ AVEC LIMITE (3 colonnes max)")
    print("="*60)
    loader.print_detailed_columns_info(df, max_cols_per_section=3)
    
    print("\n🎉 Tests terminés avec succès!")
    print("💡 L'aperçu général inclut maintenant la liste complète des colonnes")
    print("🔍 L'aperçu détaillé fournit des statistiques pour chaque colonne")

if __name__ == "__main__":
    main() 