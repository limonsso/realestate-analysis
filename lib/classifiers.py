"""
Classes de classification pour l'analyse immobilière
Optimisées pour les données MongoDB Centris
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

from .interfaces import IPropertyClassifier

logger = logging.getLogger(__name__)


class PropertyClassifier(IPropertyClassifier):
    """Classe pour classifier les propriétés MongoDB selon différents critères"""
    
    def __init__(self):
        # Seuils adaptés aux données MongoDB (prix en dollars canadiens)
        self.classification_rules = {
            'luxe': {
                'price_threshold': 1500000,  # 1.5M$ et plus
                'living_area_threshold': 3000,  # 3000 pi² et plus
                'bathroom_threshold': 3,
                'municipal_evaluation_threshold': 1000000  # 1M$ et plus
            },
            'moyen_haut': {
                'price_threshold': 800000,  # 800k$ et plus
                'living_area_threshold': 2000,  # 2000 pi² et plus
                'bathroom_threshold': 2,
                'municipal_evaluation_threshold': 600000  # 600k$ et plus
            },
            'moyen': {
                'price_threshold': 500000,  # 500k$ et plus
                'living_area_threshold': 1500,  # 1500 pi² et plus
                'bathroom_threshold': 1,
                'municipal_evaluation_threshold': 400000  # 400k$ et plus
            }
        }
    
    def classify_properties(self, df: pd.DataFrame) -> pd.DataFrame:
        """Classifie les propriétés MongoDB selon différents critères"""
        logger.info("🏠 Classification des propriétés MongoDB...")
        
        df_classified = df.copy()
        
        print(f"\n🏠 === CLASSIFICATION DES PROPRIÉTÉS MONGODB ===")
        
        # Vérifier les colonnes nécessaires pour MongoDB
        required_columns = ['price']
        optional_columns = ['living_area', 'bathrooms', 'municipal_evaluation_total']
        
        missing_required = [col for col in required_columns if col not in df_classified.columns]
        available_optional = [col for col in optional_columns if col in df_classified.columns]
        
        if missing_required:
            print(f"❌ Colonnes requises manquantes: {missing_required}")
            raise ValueError(f"Colonne requise manquante: {missing_required}")
        
        print(f"✅ Colonnes requises présentes: {required_columns}")
        print(f"📊 Colonnes optionnelles disponibles: {available_optional}")
        
        # Classification selon les données disponibles
        if len(available_optional) >= 2:
            print("🎯 Classification multi-critères (prix + surface + salles de bain + évaluation)")
            df_classified['classification_immobiliere'] = self._classify_by_multiple_criteria(df_classified)
        elif 'living_area' in available_optional:
            print("🎯 Classification par prix et surface")
            df_classified['classification_immobiliere'] = self._classify_by_price_and_area(df_classified)
        else:
            print("💰 Classification par prix uniquement")
            df_classified['classification_immobiliere'] = self._classify_by_price_only(df_classified)
        
        # Afficher les statistiques de classification
        classification_counts = df_classified['classification_immobiliere'].value_counts()
        print(f"\n📊 Distribution des classifications:")
        for category, count in classification_counts.items():
            percentage = (count / len(df_classified)) * 100
            print(f"   🏷️ {category}: {count:,} propriétés ({percentage:.1f}%)")
        
        return df_classified
    
    def _classify_by_price_only(self, df: pd.DataFrame) -> pd.Series:
        """Classification basée uniquement sur le prix"""
        print("💰 Classification par prix uniquement...")
        
        def classify_price(price):
            if pd.isna(price):
                return 'non_classifie'
            elif price >= self.classification_rules['luxe']['price_threshold']:
                return 'luxe'
            elif price >= self.classification_rules['moyen_haut']['price_threshold']:
                return 'moyen_haut'
            elif price >= self.classification_rules['moyen']['price_threshold']:
                return 'moyen'
            else:
                return 'economique'
        
        return df['price'].apply(classify_price)
    
    def _classify_by_price_and_area(self, df: pd.DataFrame) -> pd.Series:
        """Classification basée sur le prix et la surface habitable"""
        print("📐 Classification par prix et surface...")
        
        classifications = []
        
        for idx, row in df.iterrows():
            price = row.get('price', 0)
            living_area = row.get('living_area', 0)
            
            # Vérifier si les valeurs sont valides
            if pd.isna(price) or pd.isna(living_area):
                classifications.append('non_classifie')
                continue
            
            # Calculer un score de classification
            score = 0
            
            # Score basé sur le prix
            if price >= self.classification_rules['luxe']['price_threshold']:
                score += 3
            elif price >= self.classification_rules['moyen_haut']['price_threshold']:
                score += 2
            elif price >= self.classification_rules['moyen']['price_threshold']:
                score += 1
            
            # Score basé sur la surface habitable
            if living_area >= self.classification_rules['luxe']['living_area_threshold']:
                score += 3
            elif living_area >= self.classification_rules['moyen_haut']['living_area_threshold']:
                score += 2
            elif living_area >= self.classification_rules['moyen']['living_area_threshold']:
                score += 1
            
            # Classification finale basée sur le score total
            if score >= 5:
                classifications.append('luxe')
            elif score >= 3:
                classifications.append('moyen_haut')
            elif score >= 1:
                classifications.append('moyen')
            else:
                classifications.append('economique')
        
        return pd.Series(classifications, index=df.index)
    
    def _classify_by_multiple_criteria(self, df: pd.DataFrame) -> pd.Series:
        """Classification basée sur plusieurs critères MongoDB"""
        print("🎯 Classification multi-critères...")
        
        classifications = []
        
        for idx, row in df.iterrows():
            price = row.get('price', 0)
            living_area = row.get('living_area', 0)
            bathrooms = row.get('bathrooms', 0)
            municipal_evaluation = row.get('municipal_evaluation_total', 0)
            
            # Vérifier si les valeurs sont valides
            if pd.isna(price):
                classifications.append('non_classifie')
                continue
            
            # Calculer un score de classification
            score = 0
            
            # Score basé sur le prix (poids: 3)
            if price >= self.classification_rules['luxe']['price_threshold']:
                score += 3
            elif price >= self.classification_rules['moyen_haut']['price_threshold']:
                score += 2
            elif price >= self.classification_rules['moyen']['price_threshold']:
                score += 1
            
            # Score basé sur la surface habitable (poids: 2)
            if not pd.isna(living_area):
                if living_area >= self.classification_rules['luxe']['living_area_threshold']:
                    score += 2
                elif living_area >= self.classification_rules['moyen_haut']['living_area_threshold']:
                    score += 1.5
                elif living_area >= self.classification_rules['moyen']['living_area_threshold']:
                    score += 1
            
            # Score basé sur le nombre de salles de bain (poids: 1)
            if not pd.isna(bathrooms):
                if bathrooms >= self.classification_rules['luxe']['bathroom_threshold']:
                    score += 1
                elif bathrooms >= self.classification_rules['moyen_haut']['bathroom_threshold']:
                    score += 0.8
                elif bathrooms >= self.classification_rules['moyen']['bathroom_threshold']:
                    score += 0.5
            
            # Score basé sur l'évaluation municipale (poids: 1)
            if not pd.isna(municipal_evaluation):
                if municipal_evaluation >= self.classification_rules['luxe']['municipal_evaluation_threshold']:
                    score += 1
                elif municipal_evaluation >= self.classification_rules['moyen_haut']['municipal_evaluation_threshold']:
                    score += 0.8
                elif municipal_evaluation >= self.classification_rules['moyen']['municipal_evaluation_threshold']:
                    score += 0.5
            
            # Classification finale basée sur le score total
            if score >= 6:
                classifications.append('luxe')
            elif score >= 4:
                classifications.append('moyen_haut')
            elif score >= 2:
                classifications.append('moyen')
            else:
                classifications.append('economique')
        
        return pd.Series(classifications, index=df.index)
    
    def get_classification_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Retourne les statistiques de classification détaillées"""
        if 'classification_immobiliere' not in df.columns:
            return {'error': 'Aucune classification effectuée'}
        
        classification_counts = df['classification_immobiliere'].value_counts()
        classification_percentages = (classification_counts / len(df) * 100).round(2)
        
        # Statistiques par catégorie
        stats_by_category = {}
        for category in classification_counts.index:
            category_data = df[df['classification_immobiliere'] == category]
            
            stats_by_category[category] = {
                'count': len(category_data),
                'percentage': classification_percentages[category],
                'avg_price': category_data['price'].mean() if 'price' in category_data.columns else None,
                'avg_living_area': category_data['living_area'].mean() if 'living_area' in category_data.columns else None,
                'avg_bathrooms': category_data['bathrooms'].mean() if 'bathrooms' in category_data.columns else None,
                'avg_municipal_evaluation': category_data['municipal_evaluation_total'].mean() if 'municipal_evaluation_total' in category_data.columns else None,
                'price_range': {
                    'min': category_data['price'].min() if 'price' in category_data.columns else None,
                    'max': category_data['price'].max() if 'price' in category_data.columns else None
                }
            }
        
        # Statistiques globales
        global_stats = {
            'total_properties': len(df),
            'price_stats': {
                'mean': df['price'].mean() if 'price' in df.columns else None,
                'median': df['price'].median() if 'price' in df.columns else None,
                'min': df['price'].min() if 'price' in df.columns else None,
                'max': df['price'].max() if 'price' in df.columns else None
            },
            'living_area_stats': {
                'mean': df['living_area'].mean() if 'living_area' in df.columns else None,
                'median': df['living_area'].median() if 'living_area' in df.columns else None
            } if 'living_area' in df.columns else None
        }
        
        return {
            'counts': classification_counts.to_dict(),
            'percentages': classification_percentages.to_dict(),
            'stats_by_category': stats_by_category,
            'global_stats': global_stats,
            'total_properties': len(df)
        } 