#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📥 EXTRACTEUR DE DONNÉES - Composant d'extraction
==================================================

Module spécialisé dans l'extraction de données depuis différentes sources
(MongoDB, CSV, JSON, etc.) avec gestion d'erreurs et validation
"""

import pandas as pd
import logging
from typing import Dict, Optional, Any
import warnings
from datetime import datetime
import json
import os
import numpy as np

# Imports des utilitaires (avec gestion d'erreur pour compatibilité)
try:
    from ...utils.db import read_mongodb_to_dataframe, get_mongodb_stats
    from ...utils.property_type_normalizer import PropertyTypeNormalizer
    UTILS_AVAILABLE = True
except ImportError:
    try:
        from utils.db import read_mongodb_to_dataframe, get_mongodb_stats
        from utils.property_type_normalizer import PropertyTypeNormalizer
        UTILS_AVAILABLE = True
    except ImportError:
        UTILS_AVAILABLE = False
        
        # Fallback functions pour quand les utilitaires ne sont pas disponibles
        def read_mongodb_to_dataframe(*args, **kwargs):
            raise ImportError("MongoDB utilities not available")
        
        def get_mongodb_stats(*args, **kwargs):
            return {"error": "MongoDB utilities not available"}
        
        class PropertyTypeNormalizer:
            def __init__(self):
                pass

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class DataExtractor:
    """
    Composant spécialisé dans l'extraction de données
    Supporte MongoDB, CSV, JSON et datasets de test
    """
    
    def __init__(self):
        """Initialise l'extracteur de données"""
        self.property_normalizer = PropertyTypeNormalizer()
        self.extraction_stats = {}
        logger.info("📥 DataExtractor initialisé")
    
    def extract_data(self, input_source: str, input_config: Dict = None) -> pd.DataFrame:
        """
        Point d'entrée principal pour l'extraction de données
        
        Args:
            input_source: Source des données ("mongodb", "csv", "json", "test")
            input_config: Configuration d'entrée spécifique à la source
            
        Returns:
            DataFrame pandas avec les données extraites
        """
        logger.info(f"📥 Extraction depuis la source: {input_source}")
        
        try:
            if input_source == "mongodb":
                df = self._extract_from_mongodb(input_config)
            elif input_source == "csv":
                df = self._extract_from_csv(input_config)
            elif input_source == "json":
                df = self._extract_from_json(input_config)
            elif input_source == "test":
                df = self._create_test_dataset()
            else:
                raise ValueError(f"❌ Source non supportée: {input_source}")
            
            if df is None or df.empty:
                raise ValueError("❌ Aucune donnée extraite")
            
            # Statistiques d'extraction
            self.extraction_stats = {
                'source': input_source,
                'rows': len(df),
                'columns': len(df.columns),
                'timestamp': datetime.now().isoformat(),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
            }
            
            logger.info(f"✅ Extraction réussie: {df.shape[0]} lignes × {df.shape[1]} colonnes")
            logger.info(f"📊 Utilisation mémoire: {self.extraction_stats['memory_usage_mb']:.2f} MB")
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction: {e}")
            raise
    
    def _extract_from_mongodb(self, input_config: Dict = None) -> pd.DataFrame:
        """
        Extraction depuis MongoDB
        
        Args:
            input_config: Configuration MongoDB (db, collection, query, limit)
            
        Returns:
            DataFrame avec les données MongoDB
        """
        try:
            if not input_config:
                raise ValueError("❌ Configuration MongoDB manquante")
            
            # Configuration par défaut
            db_name = input_config.get('db_name', 'real_estate_db')
            collection_name = input_config.get('collection_name', 'properties')
            query = input_config.get('query', {})
            limit = input_config.get('limit', 1000)
            
            logger.info(f"🗄️ Connexion MongoDB: {db_name}.{collection_name}")
            logger.info(f"🔍 Requête: {query}")
            logger.info(f"📊 Limite: {limit}")
            
            # Extraction des données
            df = read_mongodb_to_dataframe(
                db_name=db_name,
                collection_name=collection_name,
                query=query,
                limit=limit
            )
            
            if df is None or df.empty:
                logger.warning("⚠️ Aucune donnée trouvée dans MongoDB")
                return pd.DataFrame()
            
            # Statistiques MongoDB
            mongo_stats = get_mongodb_stats(db_name, collection_name)
            logger.info(f"📊 Statistiques MongoDB: {mongo_stats}")
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur extraction MongoDB: {e}")
            raise
    
    def _extract_from_csv(self, input_config: Dict = None) -> pd.DataFrame:
        """
        Extraction depuis un fichier CSV
        
        Args:
            input_config: Configuration CSV (file_path, encoding, separator)
            
        Returns:
            DataFrame avec les données CSV
        """
        try:
            if not input_config or 'file_path' not in input_config:
                raise ValueError("❌ Chemin du fichier CSV manquant")
            
            file_path = input_config['file_path']
            encoding = input_config.get('encoding', 'utf-8')
            separator = input_config.get('separator', ',')
            
            logger.info(f"📁 Lecture CSV: {file_path}")
            logger.info(f"🔤 Encodage: {encoding}")
            logger.info(f"📝 Séparateur: {separator}")
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"❌ Fichier CSV introuvable: {file_path}")
            
            # Lecture du CSV
            df = pd.read_csv(
                file_path,
                encoding=encoding,
                sep=separator,
                low_memory=False
            )
            
            logger.info(f"✅ CSV lu avec succès: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur lecture CSV: {e}")
            raise
    
    def _extract_from_json(self, input_config: Dict = None) -> pd.DataFrame:
        """
        Extraction depuis un fichier JSON
        
        Args:
            input_config: Configuration JSON (file_path, orient)
            
        Returns:
            DataFrame avec les données JSON
        """
        try:
            if not input_config or 'file_path' not in input_config:
                raise ValueError("❌ Chemin du fichier JSON manquant")
            
            file_path = input_config['file_path']
            orient = input_config.get('orient', 'records')
            
            logger.info(f"📁 Lecture JSON: {file_path}")
            logger.info(f"🔄 Orientation: {orient}")
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"❌ Fichier JSON introuvable: {file_path}")
            
            # Lecture du JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Conversion en DataFrame
            if orient == 'records':
                df = pd.DataFrame(data)
            else:
                df = pd.read_json(file_path, orient=orient)
            
            logger.info(f"✅ JSON lu avec succès: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur lecture JSON: {e}")
            raise
    
    def _create_test_dataset(self) -> pd.DataFrame:
        """
        Création d'un dataset de test pour le développement
        
        Returns:
            DataFrame de test avec des données immobilières simulées
        """
        try:
            logger.info("🧪 Création d'un dataset de test")
            
            # Données de test réalistes
            test_data = {
                'id': range(1, 101),
                'type': ['maison', 'appartement', 'duplex', 'triplex'] * 25,
                'city': ['Montréal', 'Trois-Rivières', 'Québec', 'Laval'] * 25,
                'price': np.random.randint(200000, 800000, 100),
                'surface': np.random.randint(800, 2500, 100),
                'rooms': np.random.randint(2, 6, 100),
                'bathrooms': np.random.randint(1, 4, 100),
                'year_built': np.random.randint(1950, 2024, 100),
                'latitude': np.random.uniform(45.4, 45.7, 100),
                'longitude': np.random.uniform(-73.8, -73.5, 100)
            }
            
            df = pd.DataFrame(test_data)
            
            # Ajout de quelques valeurs manquantes pour tester la robustesse
            df.loc[10:15, 'price'] = np.nan
            df.loc[20:25, 'surface'] = np.nan
            
            logger.info(f"✅ Dataset de test créé: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur création dataset de test: {e}")
            raise
    
    def get_extraction_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'extraction"""
        return self.extraction_stats.copy()
    
    def validate_extracted_data(self, df: pd.DataFrame) -> bool:
        """
        Validation basique des données extraites
        
        Args:
            df: DataFrame à valider
            
        Returns:
            True si les données sont valides
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ DataFrame vide ou None")
                return False
            
            # Vérifications de base
            checks = {
                'non_null': df.notna().sum().sum() > 0,
                'has_columns': len(df.columns) > 0,
                'has_rows': len(df) > 0,
                'memory_usage': df.memory_usage(deep=True).sum() < 1024 * 1024 * 100  # 100 MB max
            }
            
            all_valid = all(checks.values())
            
            if all_valid:
                logger.info("✅ Validation des données extraites réussie")
            else:
                failed_checks = [k for k, v in checks.items() if not v]
                logger.warning(f"⚠️ Échec des validations: {failed_checks}")
            
            return all_valid
            
        except Exception as e:
            logger.error(f"❌ Erreur validation des données: {e}")
            return False
