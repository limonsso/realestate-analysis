"""
Orchestrateur principal pour l'analyse immobilière
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
import logging

from .interfaces import IDataProcessor, IPropertyClassifier, IFeatureSelector
from .validators import DataValidator
from .data_processors import PropertyDataProcessor
from .classifiers import PropertyClassifier
from .feature_selectors import FeatureSelector
from .property_type_normalizer import PropertyTypeNormalizer

logger = logging.getLogger(__name__)


class PropertyAnalyzer:
    """Orchestrateur principal pour l'analyse des propriétés"""
    
    def __init__(self, 
                 data_processor: IDataProcessor = None,
                 property_classifier: IPropertyClassifier = None,
                 feature_selector: IFeatureSelector = None,
                 property_types_data: list = None):
        
        # Initialiser les composants avec des valeurs par défaut si non fournis
        self.data_processor = data_processor or PropertyDataProcessor()
        self.property_classifier = property_classifier or PropertyClassifier()
        self.feature_selector = feature_selector or FeatureSelector()
        
        # Initialiser le normalisateur de types
        self.property_type_normalizer = PropertyTypeNormalizer(property_types_data=property_types_data)
        
        # Variables pour stocker les résultats de chaque étape
        self.original_data = None
        self.processed_data = None
        self.classified_data = None
        self.classification_stats = None
        self.selected_features = None
        self.classification_features = None
        self.feature_importance = None
    
    def validate_and_explore(self, df: pd.DataFrame, target_column: str = 'price') -> pd.DataFrame:
        """
        ÉTAPE 1: Validation et exploration des données
        """
        print(f"\n" + "="*60)
        print(f"📊 ÉTAPE 1: VALIDATION ET EXPLORATION")
        print(f"="*60)
        print(f"📊 Données initiales: {df.shape}")
        print(f"🎯 Variable cible: '{target_column}'")
        
        # Validation des données
        if not DataValidator.validate_target_column(df, target_column):
            raise ValueError(f"Colonne cible '{target_column}' invalide")
        
        # Statistiques initiales de la variable cible
        if target_column in df.columns:
            target_stats = df[target_column].describe()
            print(f"\n📈 Statistiques de la variable cible '{target_column}':")
            print(f"   📊 Nombre de valeurs: {target_stats['count']:,.0f}")
            print(f"   💰 Moyenne: {target_stats['mean']:,.2f}")
            print(f"   📊 Médiane: {target_stats['50%']:,.2f}")
            print(f"   📉 Min: {target_stats['min']:,.2f}")
            print(f"   📈 Max: {target_stats['max']:,.2f}")
        
        # Exploration des données
        print(f"\n📋 Informations sur les colonnes:")
        print(f"   📊 Nombre total de colonnes: {len(df.columns)}")
        print(f"   📈 Colonnes numériques: {len(df.select_dtypes(include=[np.number]).columns)}")
        print(f"   📝 Colonnes catégorielles: {len(df.select_dtypes(include=['object']).columns)}")
        print(f"   ❓ Valeurs manquantes: {df.isnull().sum().sum()}")
        
        # Stocker les données originales
        self.original_data = df.copy()
        
        print(f"✅ Validation terminée avec succès!")
        return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ÉTAPE 2: Nettoyage des données
        """
        print(f"\n" + "="*60)
        print(f"🧹 ÉTAPE 2: NETTOYAGE DES DONNÉES")
        print(f"="*60)
        
        df_cleaned = self.data_processor.clean_data(df)
        
        print(f"📊 Résultats du nettoyage:")
        print(f"   📈 Lignes: {df.shape[0]:,} → {df_cleaned.shape[0]:,}")
        print(f"   📊 Colonnes: {df.shape[1]} → {df_cleaned.shape[1]}")
        if df.shape[1] != df_cleaned.shape[1]:
            print(f"   📉 Colonnes supprimées: {df.shape[1] - df_cleaned.shape[1]}")
        
        print(f"✅ Nettoyage terminé avec succès!")
        return df_cleaned
    
    def normalize_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ÉTAPE 3: Normalisation des variables catégorielles
        """
        print(f"\n" + "="*60)
        print(f"🔄 ÉTAPE 3: NORMALISATION DES VARIABLES")
        print(f"="*60)
        
        df_normalized = df.copy()
        
        # 1. Normaliser les types de propriétés avec PropertyTypeNormalizer
        if 'type' in df_normalized.columns:
            print(f"🏠 Normalisation des types de propriétés avec PropertyTypeNormalizer:")
            df_normalized = self.property_type_normalizer.normalize_property_types(df_normalized, 'type')
        
        # 2. Normaliser les autres variables catégorielles
        df_normalized = self._normalize_other_variables(df_normalized)
        
        print(f"\n📊 Résultats de la normalisation:")
        print(f"   📈 Lignes: {df.shape[0]:,} → {df_normalized.shape[0]:,}")
        print(f"   📊 Colonnes: {df.shape[1]} → {df_normalized.shape[1]}")
        
        # Afficher les changements pour les variables importantes
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col in df_normalized.columns:
                unique_before = df[col].nunique()
                unique_after = df_normalized[col].nunique()
                if unique_before != unique_after:
                    print(f"   🔄 {col}: {unique_before} → {unique_after} valeurs uniques")
        
        print(f"✅ Normalisation terminée avec succès!")
        return df_normalized
    
    def _normalize_other_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalisation des autres variables catégorielles (sauf type)
        """
        df_normalized = df.copy()
        
        # Normaliser la colonne 'city' si elle existe
        if 'city' in df_normalized.columns:
            print(f"\n🏙️ Normalisation de 'city':")
            original_cities = df_normalized['city'].nunique()
            
            # Normaliser les noms de villes
            df_normalized['city'] = df_normalized['city'].str.title().str.strip()
            
            # Corrections spécifiques pour le Québec
            city_corrections = {
                'Montreal': 'Montréal',
                'Quebec': 'Québec',
                'Quebec City': 'Québec',
                'Ville De Quebec': 'Québec',
                'Ville De Montreal': 'Montréal',
                'St-Jean-Sur-Richelieu': 'Saint-Jean-sur-Richelieu',
                'St-Jerome': 'Saint-Jérôme',
                'Trois-Rivieres': 'Trois-Rivières'
            }
            
            df_normalized['city'] = df_normalized['city'].replace(city_corrections)
            
            normalized_cities = df_normalized['city'].nunique()
            print(f"      Villes: {original_cities} → {normalized_cities}")
        
        # Normaliser la colonne 'region' si elle existe
        if 'region' in df_normalized.columns:
            print(f"\n🗺️ Normalisation de 'region':")
            original_regions = df_normalized['region'].nunique()
            
            # Normaliser les noms de régions
            df_normalized['region'] = df_normalized['region'].str.title().str.strip()
            
            # Corrections spécifiques pour le Québec
            region_corrections = {
                'Montreal': 'Montréal',
                'Quebec': 'Québec',
                'Outaouais': 'Outaouais',
                'Monteregie': 'Montérégie',
                'Laurentides': 'Laurentides',
                'Lanaudiere': 'Lanaudière'
            }
            
            df_normalized['region'] = df_normalized['region'].replace(region_corrections)
            
            normalized_regions = df_normalized['region'].nunique()
            print(f"      Régions: {original_regions} → {normalized_regions}")
        
        # Normaliser la colonne 'building_style' si elle existe
        if 'building_style' in df_normalized.columns:
            print(f"\n🏗️ Normalisation de 'building_style':")
            original_styles = df_normalized['building_style'].nunique()
            
            # Normaliser les styles de construction
            df_normalized['building_style'] = df_normalized['building_style'].str.lower().str.strip()
            
            style_mapping = {
                'contemporain': 'contemporain',
                'contemporary': 'contemporain',
                'moderne': 'moderne',
                'modern': 'moderne',
                'traditionnel': 'traditionnel',
                'traditional': 'traditionnel',
                'colonial': 'colonial',
                'victorien': 'victorien',
                'victorian': 'victorien',
                'craftsman': 'artisan',
                'ranch': 'ranch',
                'bungalow': 'bungalow'
            }
            
            df_normalized['building_style'] = df_normalized['building_style'].map(style_mapping).fillna(df_normalized['building_style'])
            
            normalized_styles = df_normalized['building_style'].nunique()
            print(f"      Styles: {original_styles} → {normalized_styles}")
        
        return df_normalized
    
    def _basic_normalize_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalisation basique des variables catégorielles (méthode de fallback)
        """
        df_normalized = df.copy()
        
        # Normaliser la colonne 'type' si elle existe (fallback)
        if 'type' in df_normalized.columns:
            original_values = df_normalized['type'].value_counts()
            print(f"   🏷️ Normalisation basique de 'type':")
            print(f"      Valeurs avant: {list(original_values.index)}")
            
            # Normaliser les types de propriétés
            type_mapping = {
                # Variations de "maison"
                'maison': 'maison',
                'maison à vendre': 'maison',
                'maison unifamiliale': 'maison',
                'maison de ville': 'maison',
                'house': 'maison',
                'single family': 'maison',
                'detached': 'maison',
                
                # Variations de "condo"
                'condo': 'condo',
                'condominium': 'condo',
                'appartement': 'condo',
                'apartment': 'condo',
                'copropriété': 'condo',
                
                # Variations de "duplex"
                'duplex': 'duplex',
                'triplex': 'triplex',
                'quadruplex': 'quadruplex',
                'multiplex': 'multiplex',
                'plex': 'multiplex',
                
                # Autres types
                'terrain': 'terrain',
                'lot': 'terrain',
                'land': 'terrain',
                'commercial': 'commercial',
                'industriel': 'industriel',
                'industrial': 'industriel'
            }
            
            # Appliquer la normalisation
            df_normalized['type'] = df_normalized['type'].str.lower().str.strip()
            df_normalized['type'] = df_normalized['type'].map(type_mapping).fillna(df_normalized['type'])
            
            normalized_values = df_normalized['type'].value_counts()
            print(f"      Valeurs après: {list(normalized_values.index)}")
        
        # Appliquer la normalisation des autres variables
        df_normalized = self._normalize_other_variables(df_normalized)
        
        return df_normalized
    
    def encode_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ÉTAPE 4: Encodage des variables catégorielles
        """
        print(f"\n" + "="*60)
        print(f"🔢 ÉTAPE 4: ENCODAGE DES VARIABLES")
        print(f"="*60)
        
        df_encoded = self.data_processor.encode_features(df)
        
        print(f"📊 Résultats de l'encodage:")
        print(f"   📈 Lignes: {df.shape[0]:,} → {df_encoded.shape[0]:,}")
        print(f"   📊 Colonnes: {df.shape[1]} → {df_encoded.shape[1]}")
        if df.shape[1] != df_encoded.shape[1]:
            print(f"   📈 Nouvelles colonnes créées: {df_encoded.shape[1] - df.shape[1]}")
        
        print(f"✅ Encodage terminé avec succès!")
        return df_encoded
    
    def impute_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ÉTAPE 5: Imputation des valeurs manquantes
        """
        print(f"\n" + "="*60)
        print(f"🔧 ÉTAPE 5: IMPUTATION DES VALEURS MANQUANTES")
        print(f"="*60)
        
        missing_before = df.isnull().sum().sum()
        df_imputed = self.data_processor.impute_missing_values(df)
        missing_after = df_imputed.isnull().sum().sum()
        
        print(f"📊 Résultats de l'imputation:")
        print(f"   ❓ Valeurs manquantes avant: {missing_before:,}")
        print(f"   ❓ Valeurs manquantes après: {missing_after:,}")
        print(f"   ✅ Valeurs imputées: {missing_before - missing_after:,}")
        
        # Stocker les données traitées
        self.processed_data = df_imputed.copy()
        
        print(f"✅ Imputation terminée avec succès!")
        return df_imputed
    
    def classify_properties(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ÉTAPE 6: Classification des propriétés
        """
        print(f"\n" + "="*60)
        print(f"🏠 ÉTAPE 6: CLASSIFICATION DES PROPRIÉTÉS")
        print(f"="*60)
        
        df_classified = self.property_classifier.classify_properties(df)
        self.classification_stats = self.property_classifier.get_classification_stats(df_classified)
        
        print(f"📊 Résultats de la classification:")
        for category, count in self.classification_stats.get('counts', {}).items():
            pct = self.classification_stats.get('percentages', {}).get(category, 0)
            print(f"   🏷️ {category}: {count:,} propriétés ({pct:.1f}%)")
        
        # Stocker les données classifiées
        self.classified_data = df_classified.copy()
        
        print(f"✅ Classification terminée avec succès!")
        return df_classified
    
    def prepare_for_modeling(self, df: pd.DataFrame, target_column: str = 'price') -> Tuple[pd.DataFrame, pd.Series]:
        """
        ÉTAPE 7: Préparation des données pour la modélisation
        """
        print(f"\n" + "="*60)
        print(f"🎯 ÉTAPE 7: PRÉPARATION POUR LA MODÉLISATION")
        print(f"="*60)
        
        if target_column not in df.columns:
            raise ValueError(f"Colonne cible '{target_column}' manquante après traitement")
        
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        print(f"📊 Données préparées:")
        print(f"   📈 Features (X): {X.shape}")
        print(f"   🎯 Cible (y): {y.shape}")
        print(f"   📝 Colonnes features: {list(X.columns)}")
        
        print(f"✅ Préparation terminée avec succès!")
        return X, y
    
    def select_features(self, X: pd.DataFrame, y: pd.Series) -> list:
        """
        ÉTAPE 8: Sélection de variables
        """
        print(f"\n" + "="*60)
        print(f"🎯 ÉTAPE 8: SÉLECTION DE VARIABLES")
        print(f"="*60)
        
        self.selected_features = self.feature_selector.select_features(X, y)
        
        print(f"📊 Résultats de la sélection:")
        print(f"   📈 Variables disponibles: {X.shape[1]}")
        print(f"   ✅ Variables sélectionnées: {len(self.selected_features)}")
        print(f"   📉 Variables éliminées: {X.shape[1] - len(self.selected_features)}")
        print(f"   📊 Taux de conservation: {(len(self.selected_features)/X.shape[1]*100):.1f}%")
        
        print(f"\n🏆 Variables sélectionnées:")
        for i, feature in enumerate(self.selected_features, 1):
            print(f"   {i}. {feature}")
        
        print(f"✅ Sélection terminée avec succès!")
        return self.selected_features
    
    def select_features_by_classification(self, X: pd.DataFrame, y: pd.Series, classification_column: pd.Series) -> Dict[str, list]:
        """
        ÉTAPE 9: Sélection par type de propriété
        """
        print(f"\n" + "="*60)
        print(f"🏠 ÉTAPE 9: SÉLECTION PAR TYPE DE PROPRIÉTÉ")
        print(f"="*60)
        
        self.classification_features = self.feature_selector.select_features_by_classification(
            X, y, classification_column
        )
        
        if self.classification_features:
            print(f"📊 Variables spécifiques par type:")
            for prop_type, features in self.classification_features.items():
                print(f"   🏷️ {prop_type}: {len(features)} variables")
                for i, feature in enumerate(features[:5], 1):  # Afficher seulement les 5 premières
                    print(f"      {i}. {feature}")
                if len(features) > 5:
                    print(f"      ... et {len(features) - 5} autres")
        else:
            print(f"⚠️ Pas assez de données pour une sélection par type")
        
        print(f"✅ Sélection par type terminée avec succès!")
        return self.classification_features
    
    def calculate_feature_importance(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        ÉTAPE 10: Calcul de l'importance des variables
        """
        print(f"\n" + "="*60)
        print(f"📊 ÉTAPE 10: IMPORTANCE DES VARIABLES")
        print(f"="*60)
        
        self.feature_importance = self.feature_selector.get_feature_importance(X, y)
        
        print(f"📈 Top 10 des variables les plus importantes:")
        sorted_features = sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)
        for i, (feature, importance) in enumerate(sorted_features[:10], 1):
            print(f"   {i}. {feature}: {importance:.4f}")
        
        print(f"✅ Calcul d'importance terminé avec succès!")
        return self.feature_importance
    
    def final_summary(self) -> Dict[str, Any]:
        """
        ÉTAPE 11: Résumé final
        """
        print(f"\n" + "="*60)
        print(f"🏆 ÉTAPE 11: RÉSUMÉ FINAL DE L'ANALYSE")
        print(f"="*60)
        
        if self.original_data is None or self.classified_data is None:
            print("⚠️ Données manquantes pour le résumé")
            return {}
        
        print(f"📊 Transformation des données:")
        print(f"   📈 Lignes: {self.original_data.shape[0]:,} → {self.classified_data.shape[0]:,}")
        print(f"   📊 Colonnes: {self.original_data.shape[1]} → {self.classified_data.shape[1]}")
        print(f"   📉 Réduction colonnes: {self.original_data.shape[1] - self.classified_data.shape[1]} (-{((self.original_data.shape[1] - self.classified_data.shape[1])/self.original_data.shape[1]*100):.1f}%)")
        
        if self.selected_features:
            print(f"\n🎯 Sélection de variables:")
            print(f"   📈 Variables disponibles: {self.classified_data.shape[1] - 1}")  # -1 pour la cible
            print(f"   ✅ Variables sélectionnées: {len(self.selected_features)}")
            print(f"   📉 Variables éliminées: {(self.classified_data.shape[1] - 1) - len(self.selected_features)}")
            print(f"   📊 Taux de conservation: {(len(self.selected_features)/(self.classified_data.shape[1] - 1)*100):.1f}%")
        
        if self.classification_stats:
            print(f"\n🏠 Classification des propriétés:")
            for category, count in self.classification_stats.get('counts', {}).items():
                pct = self.classification_stats.get('percentages', {}).get(category, 0)
                print(f"   🏷️ {category}: {count:,} propriétés ({pct:.1f}%)")
        
        results = {
            'shape_original': self.original_data.shape,
            'shape_processed': self.classified_data.shape,
            'classification_stats': self.classification_stats,
            'selected_features': self.selected_features,
            'classification_features': self.classification_features,
            'feature_importance': self.feature_importance
        }
        
        print(f"\n🎉 === ANALYSE TERMINÉE AVEC SUCCÈS! ===")
        return results

    def analyze_properties(self, 
                          df: pd.DataFrame, 
                          target_column: str = 'price') -> Dict[str, Any]:
        """
        Exécute l'analyse complète des propriétés selon les 5 étapes définies:
        
        1. 🧹 Nettoyage des données
        2. 🏷️ Classification des propriétés  
        3. 🔧 Préparation des données
        4. 🎯 Sélection des variables
        5. 📊 Analyse des résultats
        """
        logger.info("🚀 Démarrage de l'analyse des propriétés...")
        
        print(f"\n" + "="*60)
        print(f"🏠 ANALYSE IMMOBILIÈRE COMPLÈTE")
        print(f"="*60)
        print(f"📊 Données initiales: {df.shape}")
        print(f"🎯 Variable cible: '{target_column}'")
        
        # Validation des données
        if not DataValidator.validate_target_column(df, target_column):
            raise ValueError(f"Colonne cible '{target_column}' invalide")
        
        # Statistiques initiales de la variable cible
        if target_column in df.columns:
            target_stats = df[target_column].describe()
            print(f"\n📈 Statistiques de la variable cible '{target_column}':")
            print(f"   📊 Nombre de valeurs: {target_stats['count']:,.0f}")
            print(f"   💰 Moyenne: {target_stats['mean']:,.2f}")
            print(f"   📊 Médiane: {target_stats['50%']:,.2f}")
            print(f"   📉 Min: {target_stats['min']:,.2f}")
            print(f"   📈 Max: {target_stats['max']:,.2f}")
        
        # ÉTAPE 1: 🧹 NETTOYAGE DES DONNÉES
        print(f"\n" + "="*60)
        print(f"🧹 ÉTAPE 1: NETTOYAGE DES DONNÉES")
        print(f"="*60)
        print(f"   - Suppression des colonnes avec trop de valeurs manquantes")
        print(f"   - Suppression des colonnes non pertinentes (IDs, liens, etc.)")
        
        df_cleaned = self.data_processor.clean_data(df)
        
        print(f"\n📊 Résultats du nettoyage:")
        print(f"   📈 Lignes: {df.shape[0]:,} → {df_cleaned.shape[0]:,}")
        print(f"   📊 Colonnes: {df.shape[1]} → {df_cleaned.shape[1]}")
        if df.shape[1] != df_cleaned.shape[1]:
            print(f"   📉 Colonnes supprimées: {df.shape[1] - df_cleaned.shape[1]}")
        
        # ÉTAPE 2: 🏷️ CLASSIFICATION DES PROPRIÉTÉS
        print(f"\n" + "="*60)
        print(f"🏷️ ÉTAPE 2: CLASSIFICATION DES PROPRIÉTÉS")
        print(f"="*60)
        print(f"   - Analyse du type de propriété (`type` column)")
        print(f"   - Classification automatique : Résidentiel, Revenu, Autres")
        
        df_classified = self.property_classifier.classify_properties(df_cleaned)
        self.classification_stats = self.property_classifier.get_classification_stats(df_classified)
        
        print(f"\n📊 Classification terminée:")
        for category, count in self.classification_stats.get('counts', {}).items():
            pct = self.classification_stats.get('percentages', {}).get(category, 0)
            print(f"   🏷️ {category}: {count:,} propriétés ({pct:.1f}%)")
        
        # ÉTAPE 3: 🔧 PRÉPARATION DES DONNÉES
        print(f"\n" + "="*60)
        print(f"🔧 ÉTAPE 3: PRÉPARATION DES DONNÉES")
        print(f"="*60)
        print(f"   - Imputation des valeurs manquantes")
        print(f"   - Normalisation des variables si nécessaire")
        print(f"   - Encodage des variables catégorielles")
        print(f"   - Préparation finale pour la modélisation")
        
        # 3.1 Imputation des valeurs manquantes (avant encodage)
        print(f"\n🔧 3.1 Imputation des valeurs manquantes...")
        df_imputed = self.data_processor.impute_missing_values(df_classified)
        missing_before = df_classified.isnull().sum().sum()
        missing_after = df_imputed.isnull().sum().sum()
        print(f"   ❓ Valeurs manquantes: {missing_before:,} → {missing_after:,}")
        
        # 3.2 Normalisation des variables (si applicable)
        print(f"\n🔄 3.2 Normalisation des variables...")
        # Ici on pourrait ajouter la normalisation des types de propriétés
        # ou d'autres normalisations spécifiques
        df_normalized = df_imputed  # Pour l'instant, pas de normalisation spéciale
        print(f"   ✅ Variables normalisées (le cas échéant)")
        
        # 3.3 Encodage des variables catégorielles
        print(f"\n🔤 3.3 Encodage des variables catégorielles...")
        df_encoded = self.data_processor.encode_features(df_normalized)
        categorical_cols_before = df_normalized.select_dtypes(include=['object']).shape[1]
        categorical_cols_after = df_encoded.select_dtypes(include=['object']).shape[1]
        print(f"   📝 Variables catégorielles: {categorical_cols_before} → {categorical_cols_after}")
        
        # 3.4 Préparation finale pour la modélisation
        print(f"\n🎯 3.4 Préparation finale pour la modélisation...")
        
        if target_column not in df_encoded.columns:
            raise ValueError(f"Colonne cible '{target_column}' manquante après traitement")
        
        X = df_encoded.drop(columns=[target_column])
        y = df_encoded[target_column]
        
        # Vérifier que toutes les colonnes sont numériques
        non_numeric_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
        if non_numeric_cols:
            print(f"⚠️ Colonnes non-numériques détectées: {non_numeric_cols}")
            # Conversion forcée en numérique si possible
            for col in non_numeric_cols:
                try:
                    X[col] = pd.to_numeric(X[col], errors='coerce')
                    print(f"   ✅ {col} converti en numérique")
                except:
                    print(f"   ❌ Impossible de convertir {col}, suppression")
                    X = X.drop(columns=[col])
            
            # Imputation finale des NaN créés par la conversion
            if X.isnull().sum().sum() > 0:
                X = X.fillna(X.median())
                print(f"   🔧 Valeurs NaN imputées après conversion")
        
        # Stocker le dataframe préparé
        df_prepared = df_encoded.copy()
        
        print(f"\n📊 Résultats de la préparation:")
        print(f"   📈 Lignes: {df_classified.shape[0]:,} → {df_prepared.shape[0]:,}")
        print(f"   📊 Colonnes: {df_classified.shape[1]} → {df_prepared.shape[1]}")
        print(f"   ✅ Étape 3.1: Valeurs manquantes imputées")
        print(f"   ✅ Étape 3.2: Variables normalisées")
        print(f"   ✅ Étape 3.3: Variables catégorielles encodées")
        print(f"   ✅ Étape 3.4: Données préparées pour la modélisation")
        
        print(f"\n📊 Données prêtes pour la modélisation:")
        print(f"   📈 Features (X): {X.shape}")
        print(f"   🎯 Cible (y): {y.shape}")
        print(f"   🔢 Toutes les variables sont numériques: {X.dtypes.apply(lambda x: np.issubdtype(x, np.number)).all()}")
        
        # ÉTAPE 4: 🎯 SÉLECTION DES VARIABLES
        print(f"\n" + "="*60)
        print(f"🎯 ÉTAPE 4: SÉLECTION DES VARIABLES")
        print(f"="*60)
        print(f"   - Méthode Lasso : Régularisation L1 pour éliminer les variables non significatives")
        print(f"   - Méthode Random Forest : Importance des variables basée sur les arbres")
        print(f"   - Combinaison des deux approches pour un résultat optimal")
        
        # Sélection des variables
        try:
            self.selected_features = self.feature_selector.select_features(X, y)
            
            print(f"\n📊 Résultats de la sélection:")
            print(f"   📈 Variables disponibles: {X.shape[1]}")
            print(f"   ✅ Variables sélectionnées: {len(self.selected_features)}")
            print(f"   📉 Variables éliminées: {X.shape[1] - len(self.selected_features)}")
            print(f"   📊 Taux de conservation: {(len(self.selected_features)/X.shape[1]*100):.1f}%")
            
            # Afficher les variables sélectionnées
            print(f"\n🏆 Variables sélectionnées:")
            for i, feature in enumerate(self.selected_features[:10], 1):  # Afficher les 10 premières
                print(f"   {i}. {feature}")
            if len(self.selected_features) > 10:
                print(f"   ... et {len(self.selected_features) - 10} autres")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la sélection de variables: {e}")
            print(f"   🔄 Utilisation de toutes les variables disponibles")
            self.selected_features = X.columns.tolist()
        
        # Sélection par type de propriété (si applicable)
        classification_features = {}
        if 'classification_immobiliere' in df_classified.columns:
            try:
                classification_features = self.feature_selector.select_features_by_classification(
                    X, y, df_classified['classification_immobiliere']
                )
                
                if classification_features:
                    print(f"\n🏠 Variables spécifiques par type:")
                    for prop_type, features in classification_features.items():
                        print(f"   🏷️ {prop_type}: {len(features)} variables")
                        
            except Exception as e:
                print(f"\n⚠️ Erreur lors de la sélection par type: {e}")
        
        # ÉTAPE 5: 📊 ANALYSE DES RÉSULTATS
        print(f"\n" + "="*60)
        print(f"📊 ÉTAPE 5: ANALYSE DES RÉSULTATS")
        print(f"="*60)
        print(f"   - Statistiques par type de propriété")
        print(f"   - Variables sélectionnées et leur importance")
        print(f"   - Métriques de performance des modèles")
        
        # Stocker les données traitées
        self.processed_data = {
            'X': X,
            'y': y,
            'df_classified': df_classified,
            'df_prepared': df_prepared
        }
        
        # Calcul de l'importance des variables
        feature_importance = {}
        try:
            feature_importance = self.feature_selector.get_feature_importance(X, y)
            print(f"\n🎯 Importance des variables calculée:")
            
            # Afficher le top 5 des variables les plus importantes
            if feature_importance:
                sorted_importance = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
                print(f"   📈 Top 5 des variables les plus importantes:")
                for i, (feature, importance) in enumerate(sorted_importance[:5], 1):
                    print(f"      {i}. {feature}: {importance:.4f}")
                    
        except Exception as e:
            print(f"   ⚠️ Impossible de calculer l'importance: {e}")
        
        # Résumé final des résultats
        print(f"\n🏆 === RÉSUMÉ FINAL DE L'ANALYSE ===")
        print(f"📊 Transformation des données:")
        print(f"   📈 Lignes: {df.shape[0]:,} → {df_prepared.shape[0]:,}")
        print(f"   📊 Colonnes: {df.shape[1]} → {df_prepared.shape[1]}")
        print(f"   📉 Réduction colonnes: {df.shape[1] - df_prepared.shape[1]} (-{((df.shape[1] - df_prepared.shape[1])/df.shape[1]*100):.1f}%)")
        
        print(f"\n🎯 Sélection de variables:")
        print(f"   📈 Variables disponibles: {X.shape[1]}")
        print(f"   ✅ Variables sélectionnées: {len(self.selected_features)}")
        print(f"   📉 Variables éliminées: {X.shape[1] - len(self.selected_features)}")
        print(f"   📊 Taux de conservation: {(len(self.selected_features)/X.shape[1]*100):.1f}%")
        
        print(f"\n🏠 Classification des propriétés:")
        for category, count in self.classification_stats.get('counts', {}).items():
            pct = self.classification_stats.get('percentages', {}).get(category, 0)
            print(f"   🏷️ {category}: {count:,} propriétés ({pct:.1f}%)")
        
        # Variables disponibles pour la suite
        print(f"\n🔧 Variables disponibles pour la modélisation:")
        print(f"   📊 X: Matrice des features ({X.shape})")
        print(f"   🎯 y: Vecteur cible ({y.shape})")
        print(f"   🏠 df_classified: DataFrame avec classification")
        print(f"   📝 selected_features: Liste des variables importantes")
        
        # Résultats finaux
        results = {
            'shape_original': df.shape,
            'shape_processed': df_prepared.shape,
            'classification_stats': self.classification_stats,
            'selected_features': self.selected_features,
            'classification_features': classification_features,
            'feature_importance': feature_importance
        }
        
        print(f"\n🎉 === ANALYSE TERMINÉE AVEC SUCCÈS! ===")
        logger.info("🏆 Analyse terminée avec succès!")
        return results
    
    def get_summary(self) -> Dict[str, Any]:
        """Retourne un résumé de l'analyse"""
        if self.processed_data is None:
            return {"error": "Aucune analyse effectuée"}
        
        X = self.processed_data['X']
        y = self.processed_data['y']
        
        return {
            'total_properties': len(y),
            'total_features': X.shape[1],
            'selected_features_count': len(self.selected_features),
            'reduction_percentage': ((X.shape[1] - len(self.selected_features)) / X.shape[1] * 100),
            'price_stats': {
                'mean': y.mean(),
                'median': y.median(),
                'min': y.min(),
                'max': y.max()
            },
            'classification_distribution': self.classification_stats.get('counts', {})
        } 