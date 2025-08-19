"""
Chargeur de données MongoDB pour l'analyse immobilière
"""

import pandas as pd
from typing import List, Dict, Optional
from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)


class MongoDBLoader:
    """Classe pour charger les données depuis MongoDB"""
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        """
        Initialise le chargeur MongoDB
        
        Args:
            connection_string: Chaîne de connexion MongoDB
        """
        self.connection_string = connection_string
        self.client = None
        self.db = None
    
    def connect(self, database_name: str = "real_estate_db"):
        """Établit la connexion à MongoDB"""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[database_name]
            logger.info(f"✅ Connexion MongoDB établie: {database_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur de connexion MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion MongoDB"""
        if self.client:
            self.client.close()
            logger.info("🔌 Connexion MongoDB fermée")
    
    def load_property_types(self) -> List[Dict]:
        """Charge la collection property_types"""
        if self.db is None:
            logger.error("❌ Connexion MongoDB non établie")
            return []
        
        try:
            collection = self.db['property_types']
            property_types = list(collection.find({}))
            logger.info(f"✅ {len(property_types)} types de propriétés chargés")
            return property_types
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement des types: {e}")
            return []
    
    def load_properties(self, 
                       collection_name: str = "properties",
                       filters: Optional[Dict] = None,
                       limit: Optional[int] = None) -> pd.DataFrame:
        """
        Charge les propriétés depuis MongoDB
        
        Args:
            collection_name: Nom de la collection
            filters: Filtres MongoDB (ex: {"vendue": False})
            limit: Limite du nombre de documents
            
        Returns:
            DataFrame avec les propriétés
        """
        if self.db is None:
            logger.error("❌ Connexion MongoDB non établie")
            return pd.DataFrame()
        
        try:
            collection = self.db[collection_name]
            
            # Construire la requête
            query = filters or {}
            cursor = collection.find(query)
            
            if limit:
                cursor = cursor.limit(limit)
            
            # Convertir en DataFrame
            properties = list(cursor)
            df = pd.DataFrame(properties)
            
            logger.info(f"✅ {len(df)} propriétés chargées depuis {collection_name}")
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement des propriétés: {e}")
            return pd.DataFrame()
    
    def get_collection_stats(self, collection_name: str = "properties") -> Dict:
        """Retourne les statistiques d'une collection"""
        if not self.db:
            return {}
        
        try:
            collection = self.db[collection_name]
            stats = {
                'total_documents': collection.count_documents({}),
                'vendues': collection.count_documents({"vendue": True}),
                'non_vendues': collection.count_documents({"vendue": False}),
                'avec_prix': collection.count_documents({"price": {"$exists": True, "$ne": None}}),
                'sans_prix': collection.count_documents({"price": {"$exists": False}})
            }
            
            # Statistiques par type
            pipeline = [
                {"$group": {"_id": "$type", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            type_stats = list(collection.aggregate(pipeline))
            stats['types_distribution'] = {item['_id']: item['count'] for item in type_stats}
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du calcul des statistiques: {e}")
            return {}
    
    def load_sample_data(self, 
                        collection_name: str = "properties",
                        sample_size: int = 1000,
                        filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Charge un échantillon de données pour les tests
        
        Args:
            collection_name: Nom de la collection
            sample_size: Taille de l'échantillon
            filters: Filtres à appliquer
            
        Returns:
            DataFrame avec l'échantillon
        """
        logger.info(f"📊 Chargement d'un échantillon de {sample_size} propriétés...")
        
        # Ajouter des filtres pour avoir des données valides
        base_filters = {
            "price": {"$exists": True, "$ne": None, "$gt": 0}
        }
        
        if filters:
            base_filters.update(filters)
        
        return self.load_properties(collection_name, base_filters, sample_size)
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict:
        """Valide la qualité des données chargées"""
        validation_results = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_price': df['price'].isna().sum() if 'price' in df.columns else 0,
            'missing_living_area': df['living_area'].isna().sum() if 'living_area' in df.columns else 0,
            'missing_bathrooms': df['bathrooms'].isna().sum() if 'bathrooms' in df.columns else 0,
            'missing_bedrooms': df['bedrooms'].isna().sum() if 'bedrooms' in df.columns else 0,
            'price_range': {
                'min': df['price'].min() if 'price' in df.columns else None,
                'max': df['price'].max() if 'price' in df.columns else None,
                'mean': df['price'].mean() if 'price' in df.columns else None
            },
            'required_columns': ['price', 'living_area', 'bathrooms', 'bedrooms'],
            'missing_required_columns': []
        }
        
        # Vérifier les colonnes requises
        for col in validation_results['required_columns']:
            if col not in df.columns:
                validation_results['missing_required_columns'].append(col)
        
        return validation_results
    
    def print_data_summary(self, df: pd.DataFrame):
        """Affiche un résumé des données chargées"""
        print(f"\n📊 === APERÇU GÉNÉRAL DES DONNÉES ===")
        print(f"📈 Lignes: {len(df):,}")
        print(f"📊 Colonnes: {len(df.columns)}")
        
        # === LISTE COMPLÈTE DES COLONNES ===
        print(f"\n📋 === LISTE DES COLONNES ===")
        print(f"🎯 Total: {len(df.columns)} colonnes disponibles")
        
        # Grouper les colonnes par type de données
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        object_cols = df.select_dtypes(include=['object']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime']).columns.tolist()
        bool_cols = df.select_dtypes(include=['bool']).columns.tolist()
        
        print(f"\n🔢 Colonnes numériques ({len(numeric_cols)}):")
        for i, col in enumerate(numeric_cols, 1):
            print(f"   {i:2d}. {col}")
        
        print(f"\n📝 Colonnes texte ({len(object_cols)}):")
        for i, col in enumerate(object_cols, 1):
            print(f"   {i:2d}. {col}")
        
        if datetime_cols:
            print(f"\n📅 Colonnes date/heure ({len(datetime_cols)}):")
            for i, col in enumerate(datetime_cols, 1):
                print(f"   {i:2d}. {col}")
        
        if bool_cols:
            print(f"\n✅ Colonnes booléennes ({len(bool_cols)}):")
            for i, col in enumerate(bool_cols, 1):
                print(f"   {i:2d}. {col}")
        
        # === STATISTIQUES PRINCIPALES ===
        print(f"\n💰 === STATISTIQUES PRINCIPALES ===")
        if 'price' in df.columns:
            print(f"💰 Prix - Min: ${df['price'].min():,.0f}, Max: ${df['price'].max():,.0f}, Moy: ${df['price'].mean():,.0f}")
        
        if 'living_area' in df.columns:
            print(f"📐 Surface habitable - Min: {df['living_area'].min():.0f} pi², Max: {df['living_area'].max():.0f} pi², Moy: {df['living_area'].mean():.0f} pi²")
        
        if 'type' in df.columns:
            type_counts = df['type'].value_counts()
            print(f"🏠 Types de propriétés:")
            for prop_type, count in type_counts.head(5).items():
                print(f"   🏷️ {prop_type}: {count:,} propriétés")
        
        # === ANALYSE DES VALEURS MANQUANTES ===
        print(f"\n⚠️ === ANALYSE DES VALEURS MANQUANTES ===")
        missing_cols = df.columns[df.isnull().any()].tolist()
        if missing_cols:
            print(f"📉 Colonnes avec valeurs manquantes ({len(missing_cols)}):")
            for col in missing_cols:
                missing_count = df[col].isnull().sum()
                missing_pct = (missing_count / len(df)) * 100
                print(f"   📉 {col}: {missing_count:,} manquantes ({missing_pct:.1f}%)")
        else:
            print("✅ Aucune valeur manquante détectée")
        
        # === RÉSUMÉ FINAL ===
        print(f"\n🏆 === RÉSUMÉ FINAL ===")
        print(f"📊 Dataset: {len(df):,} propriétés × {len(df.columns)} variables")
        print(f"🔢 Types: {len(numeric_cols)} numériques, {len(object_cols)} texte, {len(datetime_cols)} dates, {len(bool_cols)} booléennes")
        print(f"📈 Qualité: {((df.count().sum() / (len(df) * len(df.columns))) * 100):.1f}% de complétude globale")
    
    def print_detailed_columns_info(self, df: pd.DataFrame, max_cols_per_section: int = 10):
        """Affiche un aperçu détaillé de toutes les colonnes avec leurs statistiques"""
        print(f"\n🔍 === APERÇU DÉTAILLÉ DES COLONNES ===")
        print(f"📊 Dataset: {len(df):,} propriétés × {len(df.columns)} variables")
        
        # === COLONNES NUMÉRIQUES ===
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            print(f"\n🔢 === COLONNES NUMÉRIQUES ({len(numeric_cols)}) ===")
            for i, col in enumerate(numeric_cols[:max_cols_per_section], 1):
                col_stats = df[col].describe()
                missing_pct = (df[col].isnull().sum() / len(df)) * 100
                print(f"   {i:2d}. {col}")
                print(f"       📊 Min: {col_stats['min']:.2f}, Max: {col_stats['max']:.2f}, Moy: {col_stats['mean']:.2f}")
                print(f"       📉 Manquantes: {missing_pct:.1f}%")
            
            if len(numeric_cols) > max_cols_per_section:
                print(f"   ... et {len(numeric_cols) - max_cols_per_section} autres colonnes numériques")
        
        # === COLONNES TEXTE ===
        object_cols = df.select_dtypes(include=['object']).columns.tolist()
        if object_cols:
            print(f"\n📝 === COLONNES TEXTE ({len(object_cols)}) ===")
            for i, col in enumerate(object_cols[:max_cols_per_section], 1):
                unique_count = df[col].nunique()
                missing_pct = (df[col].isnull().sum() / len(df)) * 100
                print(f"   {i:2d}. {col}")
                print(f"       🔤 Valeurs uniques: {unique_count:,}")
                print(f"       📉 Manquantes: {missing_pct:.1f}%")
                if unique_count <= 10:
                    top_values = df[col].value_counts().head(3)
                    print(f"       🏆 Top valeurs: {dict(top_values)}")
            
            if len(object_cols) > max_cols_per_section:
                print(f"   ... et {len(object_cols) - max_cols_per_section} autres colonnes texte")
        
        # === COLONNES DATE/HEURE ===
        datetime_cols = df.select_dtypes(include=['datetime']).columns.tolist()
        if datetime_cols:
            print(f"\n📅 === COLONNES DATE/HEURE ({len(datetime_cols)}) ===")
            for i, col in enumerate(datetime_cols, 1):
                missing_pct = (df[col].isnull().sum() / len(df)) * 100
                date_range = df[col].dropna()
                if len(date_range) > 0:
                    print(f"   {i:2d}. {col}")
                    print(f"       📅 Période: {date_range.min()} à {date_range.max()}")
                    print(f"       📉 Manquantes: {missing_pct:.1f}%")
        
        # === COLONNES BOOLÉENNES ===
        bool_cols = df.select_dtypes(include=['bool']).columns.tolist()
        if bool_cols:
            print(f"\n✅ === COLONNES BOOLÉENNES ({len(bool_cols)}) ===")
            for i, col in enumerate(bool_cols, 1):
                value_counts = df[col].value_counts()
                missing_pct = (df[col].isnull().sum() / len(df)) * 100
                print(f"   {i:2d}. {col}")
                print(f"       📊 Distribution: {dict(value_counts)}")
                print(f"       📉 Manquantes: {missing_pct:.1f}%")
        
        print(f"\n💡 Utilisez 'print_detailed_columns_info()' pour un aperçu complet de toutes les colonnes") 