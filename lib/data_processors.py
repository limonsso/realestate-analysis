"""
Classes de traitement des données pour l'analyse immobilière
Optimisées pour les données MongoDB Centris
"""

import pandas as pd
import numpy as np
from typing import List, Optional
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import logging

from .interfaces import IDataProcessor
from .property_type_normalizer import PropertyTypeNormalizer

logger = logging.getLogger(__name__)


class PropertyDataProcessor(IDataProcessor):
    """Classe pour le traitement des données des propriétés MongoDB"""
    
    def __init__(self, missing_threshold: float = 0.05, property_types_data: Optional[List[dict]] = None):
        self.missing_threshold = missing_threshold
        self.label_encoders = {}
        self.imputer = None
        
        # Initialiser le normalisateur de types de propriétés
        self.type_normalizer = PropertyTypeNormalizer(property_types_data) if property_types_data else None
        
        # Colonnes spécifiques aux données MongoDB à supprimer
        self.mongodb_columns_to_drop = [
            '_id', 'link', 'images', 'img_src', 'image',
            'add_date', 'update_at', 'created_at', 'updated_at',
            'extraction_metadata', 'location', 'parking',
            'unites', 'commercial_units', 'residential_units',
            'description', 'full_address', 'address'
        ]
        
        # Colonnes de métadonnées à supprimer
        self.metadata_columns = [
            'company', 'vendue', 'version', 'add_date'
        ]
        
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données MongoDB en supprimant les colonnes problématiques"""
        logger.info("🧹 Nettoyage des données MongoDB...")
        
        # Copie pour éviter de modifier l'original
        df_clean = df.copy()
        
        # === ÉTAPE 1: ANALYSE INITIALE ===
        print(f"\n📊 === ÉTAPE 1: ANALYSE INITIALE ===")
        print(f"📋 Nombre total de colonnes au début: {df_clean.shape[1]}")
        print(f"📝 Colonnes initiales: {list(df_clean.columns)}")
        
        # Calculer les valeurs manquantes par colonne
        missing_stats = df_clean.isnull().sum()
        missing_pct = (missing_stats / len(df_clean) * 100).round(2)
        
        print(f"\n📈 Statistiques des valeurs manquantes:")
        for col in df_clean.columns:
            if missing_stats[col] > 0:
                print(f"   📉 {col}: {missing_stats[col]:,} ({missing_pct[col]:.1f}%)")
        
        # === ÉTAPE 2: SUPPRESSION DES COLONNES MONGODB SPÉCIFIQUES ===
        print(f"\n🗑️ === ÉTAPE 2: SUPPRESSION DES COLONNES MONGODB ===")
        
        # Identifier les colonnes MongoDB présentes
        mongodb_cols_present = [col for col in self.mongodb_columns_to_drop if col in df_clean.columns]
        metadata_cols_present = [col for col in self.metadata_columns if col in df_clean.columns]
        
        if mongodb_cols_present:
            print(f"❌ Colonnes MongoDB à supprimer ({len(mongodb_cols_present)}):")
            for col in mongodb_cols_present:
                print(f"   🗑️ {col}")
        
        if metadata_cols_present:
            print(f"❌ Colonnes de métadonnées à supprimer ({len(metadata_cols_present)}):")
            for col in metadata_cols_present:
                print(f"   🗑️ {col}")
        
        # Appliquer la suppression
        cols_to_drop = mongodb_cols_present + metadata_cols_present
        df_clean = df_clean.drop(columns=cols_to_drop, errors='ignore')
        
        print(f"\n📊 Résultat étape 2:")
        print(f"   📉 Colonnes supprimées: {len(cols_to_drop)}")
        print(f"   📈 Colonnes restantes: {df_clean.shape[1]}")
        
        # === ÉTAPE 3: SUPPRESSION DES COLONNES AVEC TROP DE VALEURS MANQUANTES ===
        print(f"\n🗑️ === ÉTAPE 3: SUPPRESSION DES COLONNES AVEC TROP DE VALEURS MANQUANTES ===")
        seuil_conservation = self.missing_threshold
        print(f"🎯 Seuil de conservation: {seuil_conservation*100:.1f}% (garder colonnes avec ≥{seuil_conservation*100:.1f}% de données valides)")
        
        # Identifier les colonnes à supprimer
        cols_too_many_missing = []
        cols_to_keep = []
        
        for col in df_clean.columns:
            pct_valid = df_clean[col].notnull().mean()
            if pct_valid <= seuil_conservation:
                cols_too_many_missing.append(col)
            else:
                cols_to_keep.append(col)
        
        print(f"\n❌ Colonnes à supprimer ({len(cols_too_many_missing)}):")
        for col in cols_too_many_missing:
            pct_missing = (1 - df_clean[col].notnull().mean()) * 100
            print(f"   🗑️ {col}: {pct_missing:.1f}% manquantes")
        
        print(f"\n✅ Colonnes conservées ({len(cols_to_keep)}):")
        for col in cols_to_keep:
            pct_valid = df_clean[col].notnull().mean() * 100
            print(f"   💚 {col}: {pct_valid:.1f}% valides")
        
        # Appliquer la suppression
        df_clean = df_clean[cols_to_keep]
        
        print(f"\n📊 Résultat étape 3:")
        print(f"   📉 Colonnes supprimées: {len(cols_too_many_missing)}")
        print(f"   📈 Colonnes restantes: {df_clean.shape[1]}")
        
        # === ÉTAPE 4: SUPPRESSION DES COLONNES INUTILES ===
        print(f"\n🧹 === ÉTAPE 4: SUPPRESSION DES COLONNES INUTILES ===")
        cols_before_cleaning = list(df_clean.columns)
        cols_to_drop = self._identify_useless_columns(df_clean)
        
        if cols_to_drop:
            print(f"❌ Colonnes inutiles identifiées ({len(cols_to_drop)}):")
            for col in cols_to_drop:
                reason = self._get_drop_reason(df_clean, col)
                print(f"   🗑️ {col}: {reason}")
        else:
            print("✅ Aucune colonne inutile trouvée")
        
        # Appliquer la suppression
        df_clean = df_clean.drop(columns=cols_to_drop, errors='ignore')
        cols_after_cleaning = list(df_clean.columns)
        
        print(f"\n📊 Résultat étape 4:")
        print(f"   📉 Colonnes supprimées: {len(cols_to_drop)}")
        print(f"   📈 Colonnes restantes: {df_clean.shape[1]}")
        
        if cols_after_cleaning:
            print(f"\n✅ Colonnes finales conservées ({len(cols_after_cleaning)}):")
            for i, col in enumerate(cols_after_cleaning, 1):
                print(f"   {i:2d}. {col}")
        
        # === ÉTAPE 5: NORMALISATION DES COLONNES ===
        print(f"\n🔄 === ÉTAPE 5: NORMALISATION DES COLONNES ===")
        df_clean = self._normalize_columns(df_clean)
        
        # === ÉTAPE 6: NORMALISATION DES TYPES DE PROPRIÉTÉS ===
        if self.type_normalizer and 'type' in df_clean.columns:
            print(f"\n🏷️ === ÉTAPE 6: NORMALISATION DES TYPES DE PROPRIÉTÉS ===")
            df_clean = self.type_normalizer.normalize_property_types(df_clean, 'type')
        else:
            print(f"\n⚠️ Pas de normalisation des types (normalisateur non disponible ou colonne 'type' manquante)")
        
        # === RÉSUMÉ FINAL ===
        print(f"\n🏆 === RÉSUMÉ FINAL DU NETTOYAGE ===")
        print(f"📊 Colonnes initiales: {df.shape[1]}")
        print(f"📊 Colonnes finales: {df_clean.shape[1]}")
        print(f"📉 Total supprimées: {df.shape[1] - df_clean.shape[1]}")
        print(f"📈 Pourcentage conservé: {(df_clean.shape[1] / df.shape[1] * 100):.1f}%")
        
        # Valeurs manquantes finales
        missing_before = df.isnull().sum().sum()
        missing_after = df_clean.isnull().sum().sum()
        print(f"📈 Valeurs manquantes avant: {missing_before:,}")
        print(f"📉 Valeurs manquantes après: {missing_after:,}")
        print(f"📊 Réduction valeurs manquantes: {((missing_before - missing_after) / missing_before * 100):.1f}%")
        
        return df_clean
    
    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalise les noms et types de colonnes pour les données MongoDB"""
        df_normalized = df.copy()
        
        # Normaliser les colonnes de salles de bain
        if 'nb_bathroom' in df_normalized.columns and 'bathrooms' in df_normalized.columns:
            # Utiliser bathrooms comme référence, supprimer nb_bathroom
            df_normalized = df_normalized.drop(columns=['nb_bathroom'])
            print(f"   🔄 Normalisation: nb_bathroom → bathrooms")
        
        # Normaliser les colonnes de chambres
        if 'nb_bedroom' in df_normalized.columns and 'bedrooms' in df_normalized.columns:
            # Utiliser bedrooms comme référence, supprimer nb_bedroom
            df_normalized = df_normalized.drop(columns=['nb_bedroom'])
            print(f"   🔄 Normalisation: nb_bedroom → bedrooms")
        
        # Normaliser les colonnes d'année de construction
        if 'construction_year' in df_normalized.columns and 'year_built' in df_normalized.columns:
            # Utiliser year_built comme référence, supprimer construction_year
            df_normalized = df_normalized.drop(columns=['construction_year'])
            print(f"   🔄 Normalisation: construction_year → year_built")
        
        # Normaliser les colonnes d'évaluation municipale
        if 'municipal_taxes' in df_normalized.columns and 'municipal_tax' in df_normalized.columns:
            # Utiliser municipal_tax comme référence, supprimer municipal_taxes
            df_normalized = df_normalized.drop(columns=['municipal_taxes'])
            print(f"   🔄 Normalisation: municipal_taxes → municipal_tax")
        
        # Normaliser les colonnes de taxes scolaires
        if 'school_taxes' in df_normalized.columns and 'school_tax' in df_normalized.columns:
            # Utiliser school_tax comme référence, supprimer school_taxes
            df_normalized = df_normalized.drop(columns=['school_taxes'])
            print(f"   🔄 Normalisation: school_taxes → school_tax")
        
        # Normaliser les colonnes de revenu
        if 'revenu' in df_normalized.columns and 'plex-revenu' in df_normalized.columns:
            # Utiliser revenu comme référence, supprimer plex-revenu
            df_normalized = df_normalized.drop(columns=['plex-revenu'])
            print(f"   🔄 Normalisation: plex-revenu → revenu")
        
        # Convertir les colonnes numériques en string en numérique
        numeric_columns = ['bathrooms', 'bedrooms', 'year_built', 'municipal_tax', 'school_tax']
        for col in numeric_columns:
            if col in df_normalized.columns:
                try:
                    df_normalized[col] = pd.to_numeric(df_normalized[col], errors='coerce')
                    print(f"   🔄 Conversion: {col} → numérique")
                except:
                    print(f"   ⚠️ Impossible de convertir {col} en numérique")
        
        return df_normalized
    
    def _get_drop_reason(self, df: pd.DataFrame, col: str) -> str:
        """Retourne la raison pour laquelle une colonne est supprimée"""
        try:
            if 'id' in col.lower():
                return "Colonne ID (identifiant)"
            elif 'link' in col.lower():
                return "Colonne lien/URL"
            elif 'address' in col.lower():
                return "Colonne adresse (texte libre)"
            elif 'image' in col.lower():
                return "Colonne image/URL"
            elif df[col].nunique() == 1:
                return "Une seule valeur unique"
            elif df[col].nunique() == 0:
                return "Aucune valeur unique"
            else:
                return "Colonne inutile identifiée"
        except:
            return "Erreur lors de l'analyse"
    
    def _identify_useless_columns(self, df: pd.DataFrame) -> List[str]:
        """Identifie les colonnes inutiles à supprimer"""
        cols_to_drop = []
        
        for col in df.columns:
            # Colonnes d'identifiant
            if 'id' in col.lower() and col != 'id':
                cols_to_drop.append(col)
            
            # Colonnes de liens/URLs
            elif 'link' in col.lower() or 'url' in col.lower():
                cols_to_drop.append(col)
            
            # Colonnes d'adresses (texte libre)
            elif 'address' in col.lower():
                cols_to_drop.append(col)
            
            # Colonnes d'images
            elif 'image' in col.lower():
                cols_to_drop.append(col)
            
            # Colonnes avec une seule valeur unique
            elif df[col].nunique() <= 1:
                cols_to_drop.append(col)
        
        return cols_to_drop
    
    def encode_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode les variables catégorielles"""
        logger.info("🔤 Encodage des variables catégorielles...")
        
        df_encoded = df.copy()
        categorical_columns = df_encoded.select_dtypes(include=['object', 'category']).columns
        
        if len(categorical_columns) == 0:
            print("✅ Aucune variable catégorielle à encoder")
            return df_encoded
        
        print(f"\n🔤 === ENCODAGE DES VARIABLES CATÉGORIELLES ===")
        print(f"📝 Variables catégorielles identifiées: {list(categorical_columns)}")
        
        for col in categorical_columns:
            try:
                # Nettoyer les valeurs
                df_encoded[col] = df_encoded[col].apply(self._safe_str)
                
                # Créer et appliquer le label encoder
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
                
                # Stocker l'encodeur pour référence future
                self.label_encoders[col] = le
                
                print(f"   ✅ {col}: encodé ({le.classes_.shape[0]} catégories)")
                
            except Exception as e:
                print(f"   ❌ Erreur lors de l'encodage de {col}: {e}")
                # Supprimer la colonne problématique
                df_encoded = df_encoded.drop(columns=[col])
        
        print(f"✅ Encodage terminé: {len(self.label_encoders)} variables encodées")
        return df_encoded
    
    @staticmethod
    def _safe_str(x) -> str:
        """Convertit une valeur en string de manière sécurisée"""
        if pd.isna(x) or x is None:
            return "missing"
        return str(x).strip()
    
    def impute_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute les valeurs manquantes"""
        logger.info("🔧 Imputation des valeurs manquantes...")
        
        df_imputed = df.copy()
        
        # Identifier les colonnes avec des valeurs manquantes
        missing_columns = df_imputed.columns[df_imputed.isnull().any()].tolist()
        
        if len(missing_columns) == 0:
            print("✅ Aucune valeur manquante à imputer")
            return df_imputed
        
        print(f"\n🔧 === IMPUTATION DES VALEURS MANQUANTES ===")
        print(f"📝 Colonnes avec valeurs manquantes: {missing_columns}")
        
        # Séparer les colonnes numériques et catégorielles
        numeric_columns = df_imputed[missing_columns].select_dtypes(include=[np.number]).columns
        categorical_columns = df_imputed[missing_columns].select_dtypes(include=['object', 'category']).columns
        
        # Imputation pour les variables numériques
        if len(numeric_columns) > 0:
            print(f"\n📊 Imputation des variables numériques:")
            imputer_numeric = SimpleImputer(strategy='median')
            df_imputed[numeric_columns] = imputer_numeric.fit_transform(df_imputed[numeric_columns])
            
            for col in numeric_columns:
                missing_count = df[col].isnull().sum()
                print(f"   📈 {col}: {missing_count} valeurs imputées (médiane)")
        
        # Imputation pour les variables catégorielles
        if len(categorical_columns) > 0:
            print(f"\n🏷️ Imputation des variables catégorielles:")
            imputer_categorical = SimpleImputer(strategy='most_frequent')
            df_imputed[categorical_columns] = imputer_categorical.fit_transform(df_imputed[categorical_columns])
            
            for col in categorical_columns:
                missing_count = df[col].isnull().sum()
                print(f"   🏷️ {col}: {missing_count} valeurs imputées (mode)")
        
        # Vérification finale
        remaining_missing = df_imputed.isnull().sum().sum()
        print(f"\n✅ Imputation terminée: {remaining_missing} valeurs manquantes restantes")
        
        return df_imputed 