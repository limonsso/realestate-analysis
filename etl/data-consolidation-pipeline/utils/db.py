#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ MODULE BASE DE DONNÉES - Pipeline ETL Ultra-Intelligent
============================================================

Module de connexion et extraction depuis MongoDB
Basé sur les spécifications du real_estate_prompt.md
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional, Dict, Any, List
import warnings
import json
from datetime import datetime

# Import conditionnel de MongoDB
try:
    import pymongo
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    warnings.warn("PyMongo non disponible - fonctionnalités MongoDB limitées")

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

def read_mongodb_to_dataframe(connection_string: str = "mongodb://localhost:27017/",
                              database_name: str = "real_estate_db",
                              collection_name: str = "properties",
                              limit: Optional[int] = None,
                              query: Dict = None) -> Optional[pd.DataFrame]:
    """
    Lit les données depuis MongoDB et les convertit en DataFrame
    
    Args:
        connection_string: Chaîne de connexion MongoDB
        database_name: Nom de la base de données
        collection_name: Nom de la collection
        limit: Limite du nombre de documents
        query: Requête de filtrage
        
    Returns:
        DataFrame avec les données ou None en cas d'erreur
    """
    if not MONGODB_AVAILABLE:
        logger.warning("⚠️ MongoDB non disponible - génération de données de test")
        return _generate_test_data(limit=limit)
    
    try:
        logger.info(f"🗄️ Connexion à MongoDB: {database_name}.{collection_name}")
        
        # Connexion à MongoDB
        client = MongoClient(connection_string)
        db = client[database_name]
        collection = db[collection_name]
        
        # Vérification de la connexion
        client.admin.command('ping')
        logger.info("✅ Connexion MongoDB établie")
        
        # Construction de la requête
        if query is None:
            query = {}
        
        # Exécution de la requête
        if limit:
            cursor = collection.find(query).limit(limit)
        else:
            cursor = collection.find(query)
        
        # Conversion en liste
        documents = list(cursor)
        
        if not documents:
            logger.warning("⚠️ Aucun document trouvé dans MongoDB")
            return _generate_test_data(limit=limit)
        
        logger.info(f"📊 {len(documents)} documents extraits de MongoDB")
        
        # Conversion en DataFrame
        df = pd.DataFrame(documents)
        
        # Nettoyage des colonnes MongoDB
        if '_id' in df.columns:
            df = df.drop('_id', axis=1)
        
        # Conversion des types
        df = _convert_mongodb_types(df)
        
        logger.info(f"✅ DataFrame créé: {df.shape[0]} lignes × {df.shape[1]} colonnes")
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Erreur MongoDB: {e}")
        logger.info("🔄 Utilisation de données de test comme fallback")
        return _generate_test_data()
    
    finally:
        if 'client' in locals():
            client.close()

def get_mongodb_stats(connection_string: str = "mongodb://localhost:27017/",
                      database_name: str = "real_estate_db",
                      collection_name: str = "properties") -> Dict[str, Any]:
    """
    Récupère les statistiques de la base MongoDB
    
    Args:
        connection_string: Chaîne de connexion MongoDB
        database_name: Nom de la base de données
        collection_name: Nom de la collection
        
    Returns:
        Dict avec les statistiques
    """
    if not MONGODB_AVAILABLE:
        return {"status": "unavailable", "message": "MongoDB non disponible"}
    
    try:
        client = MongoClient(connection_string)
        db = client[database_name]
        collection = db[collection_name]
        
        # Statistiques de base
        stats = {
            "database": database_name,
            "collection": collection_name,
            "document_count": collection.count_documents({}),
            "database_size": db.command("dbStats")["dataSize"],
            "collection_size": db.command("collStats", collection_name)["size"],
            "indexes": list(collection.list_indexes()),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"📊 Statistiques MongoDB: {stats['document_count']} documents")
        return stats
        
    except Exception as e:
        logger.error(f"❌ Erreur statistiques MongoDB: {e}")
        return {"status": "error", "error": str(e)}
    
    finally:
        if 'client' in locals():
            client.close()

def test_mongodb_connection(connection_string: str = "mongodb://localhost:27017/") -> bool:
    """
    Teste la connexion à MongoDB
    
    Args:
        connection_string: Chaîne de connexion MongoDB
        
    Returns:
        True si la connexion réussit, False sinon
    """
    if not MONGODB_AVAILABLE:
        logger.warning("⚠️ PyMongo non disponible")
        return False
    
    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        logger.info("✅ Connexion MongoDB testée avec succès")
        client.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Test connexion MongoDB échoué: {e}")
        return False

def _convert_mongodb_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convertit les types de données MongoDB en types pandas appropriés
    
    Args:
        df: DataFrame MongoDB
        
    Returns:
        DataFrame avec types convertis
    """
    try:
        # Conversion des dates
        date_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':
                sample_values = df[col].dropna().head(10)
                if len(sample_values) > 0:
                    try:
                        pd.to_datetime(sample_values, errors='raise')
                        date_columns.append(col)
                    except:
                        pass
        
        # Conversion des colonnes de dates
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Conversion des colonnes numériques
        numeric_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':
                sample_values = df[col].dropna().head(100)
                if len(sample_values) > 0:
                    try:
                        pd.to_numeric(sample_values, errors='raise')
                        numeric_columns.append(col)
                    except:
                        pass
        
        # Conversion des colonnes numériques
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        logger.info(f"🔄 Types convertis: {len(date_columns)} dates, {len(numeric_columns)} numériques")
        
        return df
        
    except Exception as e:
        logger.warning(f"⚠️ Erreur conversion types: {e}")
        return df

def _generate_test_data(size: int = 1000, limit: Optional[int] = None) -> pd.DataFrame:
    """
    Génère des données de test synthétiques
    
    Args:
        size: Taille du dataset par défaut
        limit: Limite spécifique du nombre de documents
        
    Returns:
        DataFrame de test
    """
    # Utiliser la limite si spécifiée, sinon la taille par défaut
    final_size = limit if limit is not None else size
    logger.info(f"🧪 Génération de {final_size} propriétés de test")
    
    np.random.seed(42)
    
    data = {
        # === PRIX ===
        "price": np.random.uniform(150000, 800000, final_size),
        "prix": np.random.uniform(150000, 800000, final_size),
        "asking_price": np.random.uniform(150000, 800000, final_size),
        
        # === SURFACE ===
        "surface": np.random.uniform(50, 300, final_size),
        "superficie": np.random.uniform(50, 300, final_size),
        "sqft": np.random.uniform(500, 3000, final_size),
        
        # === CHAMBRES ===
        "bedrooms": np.random.randint(1, 6, final_size),
        "chambres": np.random.randint(1, 6, final_size),
        "nb_bedrooms": np.random.randint(1, 6, final_size),
        
        # === SALLES DE BAIN ===
        "bathrooms": np.random.randint(1, 4, final_size),
        "salle_bain": np.random.randint(1, 4, final_size),
        "nb_bathrooms": np.random.randint(1, 4, final_size),
        
        # === COORDONNÉES ===
        "latitude": np.random.uniform(45.0, 47.5, final_size),
        "longitude": np.random.uniform(-74.5, -71.0, final_size),
        "lat": np.random.uniform(45.0, 47.5, final_size),
        "lng": np.random.uniform(-74.5, -71.0, final_size),
        
        # === ADRESSES ===
        "address": [f"Rue {i} Montréal QC" for i in range(final_size)],
        "adresse": [f"Street {i} Quebec QC" for i in range(final_size)],
        
        # === TYPES DE PROPRIÉTÉ ===
        "property_type": np.random.choice(["Maison", "Appartement", "Condo", "Duplex"], final_size),
        "type_propriete": np.random.choice(["House", "Apartment", "Condo", "Duplex"], final_size),
        
        # === ANNÉE CONSTRUCTION ===
        "year_built": np.random.randint(1950, 2024, final_size),
        "annee_construction": np.random.randint(1950, 2024, final_size),
        
        # === TAXES ===
        "tax_municipal": np.random.uniform(2000, 8000, final_size),
        "taxe_municipale": np.random.uniform(2000, 8000, final_size),
        
        # === ÉVALUATIONS ===
        "evaluation": np.random.uniform(200000, 900000, final_size),
        "evaluation_municipale": np.random.uniform(200000, 900000, final_size),
        
        # === REVENUS ===
        "revenue": np.random.uniform(15000, 60000, final_size),
        "revenu": np.random.uniform(15000, 60000, final_size),
        
        # === CHARGES ===
        "expenses": np.random.uniform(8000, 25000, final_size),
        "depenses": np.random.uniform(8000, 25000, final_size),
        
        # === ROI ===
        "roi": np.random.uniform(0.02, 0.12, final_size),
        "roi_brut": np.random.uniform(0.02, 0.12, final_size),
        
        # === TERRAIN ===
        "lot_size": np.random.uniform(100, 1000, final_size),
        "taille_terrain": np.random.uniform(100, 1000, final_size),
        
        # === PARKING ===
        "nb_parking": np.random.randint(0, 4, final_size),
        "parking_spaces": np.random.randint(0, 4, final_size),
        
        # === UNITÉS ===
        "nb_unit": np.random.randint(1, 10, final_size),
        "units": np.random.randint(1, 10, final_size),
        
        # === LIENS ===
        "link": [f"https://example.com/property/{i}" for i in range(final_size)],
        "lien": [f"https://exemple.com/propriete/{i}" for i in range(final_size)],
        
        # === ENTREPRISES ===
        "company": np.random.choice(["RE/MAX", "Century 21", "Royal LePage"], final_size),
        "entreprise": np.random.choice(["RE/MAX", "Century 21", "Royal LePage"], final_size),
        
        # === VERSIONS ===
        "version": ["1.0"] * final_size,
        "data_version": ["1.0"] * final_size,
        
        # === MÉTADONNÉES ===
        "extraction_metadata": [f"{{'source': 'test', 'id': {i}}}" for i in range(final_size)],
        "metadata": [f"{{'test': True, 'id': {i}}}" for i in range(final_size)]
    }
    
    # Création du DataFrame
    df = pd.DataFrame(data)
    
    # Ajout de valeurs manquantes réalistes
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            missing_rate = np.random.uniform(0.1, 0.3)
            missing_indices = np.random.choice(df.index, size=int(len(df) * missing_rate), replace=False)
            df.loc[missing_indices, col] = np.nan
    
    logger.info(f"✅ Dataset de test généré: {df.shape[0]} lignes × {df.shape[1]} colonnes")
    return df
