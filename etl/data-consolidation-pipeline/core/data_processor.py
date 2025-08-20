#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 PROCESSEUR DE DONNÉES
========================

Gère l'extraction, la validation et le traitement des données
"""

import logging
import pandas as pd
from typing import Dict, Any, Optional, Union
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Processeur de données pour le pipeline ETL
    
    Responsable de l'extraction, de la validation
    et du traitement des données
    """
    
    def __init__(self, pipeline_manager):
        """
        Initialise le processeur de données
        
        Args:
            pipeline_manager: Instance du gestionnaire de pipeline
        """
        self.pipeline_manager = pipeline_manager
        self.data = None
        self.validation_results = {}
    
    def extract_data(self, source: str, source_path: str = None, 
                     mongodb_db: str = None, mongodb_collection: str = None,
                     mongodb_query: str = None, limit: Optional[int] = None,
                     mongodb_query_file: str = None) -> Optional[pd.DataFrame]:
        """
        Extrait les données selon la source spécifiée
        
        Args:
            source: Source des données (mongodb, csv, json, test)
            source_path: Chemin du fichier (CSV/JSON) ou chaîne de connexion MongoDB
            mongodb_db: Nom de la base de données MongoDB
            mongodb_collection: Nom de la collection MongoDB
            mongodb_query: Requête MongoDB au format JSON
            limit: Limite du nombre de documents MongoDB à extraire
            mongodb_query_file: Chemin vers un fichier JSON contenant la requête MongoDB
            
        Returns:
            DataFrame pandas avec les données extraites
        """
        logger.info(f"📥 === PHASE 1: EXTRACTION ===")
        
        try:
            if source == "mongodb":
                return self._extract_from_mongodb(
                    mongodb_db, mongodb_collection, mongodb_query, 
                    limit, mongodb_query_file
                )
            elif source == "csv":
                return self._extract_from_csv(source_path)
            elif source == "json":
                return self._extract_from_json(source_path)
            elif source == "test":
                return self._extract_test_data()
            else:
                logger.error(f"❌ Source non supportée: {source}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction: {e}")
            return None
    
    def _extract_from_mongodb(self, db: str, collection: str, 
                              query: str = None, limit: int = None,
                              query_file: str = None) -> pd.DataFrame:
        """Extrait les données depuis MongoDB"""
        logger.info("🗄️ Extraction depuis MongoDB...")
        
        # Lecture de la requête depuis le fichier si spécifié
        if query_file:
            logger.info(f"📁 Lecture de la requête depuis le fichier: {query_file}")
            try:
                with open(query_file, 'r', encoding='utf-8') as f:
                    query = json.load(f)
                logger.info(f"✅ Requête MongoDB chargée depuis le fichier: {query}")
            except Exception as e:
                logger.error(f"❌ Erreur lecture fichier requête: {e}")
                return pd.DataFrame()
        
        # Utilisation de l'orchestrateur pour l'extraction
        try:
            result = self.pipeline_manager.orchestrator.data_extractor.extract_data(
                "mongodb",
                {
                    "database": db,
                    "collection": collection,
                    "query": query,
                    "limit": limit
                }
            )
            
            if isinstance(result, dict) and 'dataframe' in result:
                df = result['dataframe']
                logger.info(f"✅ MongoDB: {len(df)} propriétés extraites")
                return df
            else:
                logger.error("❌ Format de réponse MongoDB invalide")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"❌ Erreur extraction MongoDB: {e}")
            return pd.DataFrame()
    
    def _extract_from_csv(self, file_path: str) -> pd.DataFrame:
        """Extrait les données depuis un fichier CSV"""
        logger.info(f"📄 Extraction depuis CSV: {file_path}")
        try:
            df = pd.read_csv(file_path)
            logger.info(f"✅ CSV: {len(df)} lignes extraites")
            return df
        except Exception as e:
            logger.error(f"❌ Erreur lecture CSV: {e}")
            return pd.DataFrame()
    
    def _extract_from_json(self, file_path: str) -> pd.DataFrame:
        """Extrait les données depuis un fichier JSON"""
        logger.info(f"📄 Extraction depuis JSON: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            logger.info(f"✅ JSON: {len(df)} lignes extraites")
            return df
        except Exception as e:
            logger.error(f"❌ Erreur lecture JSON: {e}")
            return pd.DataFrame()
    
    def _extract_test_data(self) -> pd.DataFrame:
        """Génère des données de test"""
        logger.info("🧪 Génération de données de test...")
        try:
            # Génération simple de données de test
            import numpy as np
            import pandas as pd
            
            # Création de 1000 propriétés de test
            np.random.seed(42)
            num_properties = 1000
            
            data = {
                'price': np.random.uniform(200000, 2000000, num_properties),
                'prix': np.random.uniform(200000, 2000000, num_properties),
                'surface': np.random.uniform(50, 500, num_properties),
                'superficie': np.random.uniform(50, 500, num_properties),
                'bedrooms': np.random.randint(1, 6, num_properties),
                'chambres': np.random.randint(1, 6, num_properties),
                'bathrooms': np.random.randint(1, 4, num_properties),
                'salle_bain': np.random.randint(1, 4, num_properties),
                'latitude': np.random.uniform(45.0, 46.0, num_properties),
                'longitude': np.random.uniform(-74.0, -73.0, num_properties),
                'city': np.random.choice(['Montréal', 'Québec', 'Laval', 'Gatineau'], num_properties),
                'type': np.random.choice(['Maison', 'Appartement', 'Condo', 'Duplex'], num_properties),
                'year_built': np.random.randint(1950, 2024, num_properties),
                'annee_construction': np.random.randint(1950, 2024, num_properties)
            }
            
            df = pd.DataFrame(data)
            logger.info(f"✅ Dataset de test généré: {len(df)} lignes × {len(df.columns)} colonnes")
            return df
                
        except Exception as e:
            logger.error(f"❌ Erreur génération données de test: {e}")
            return pd.DataFrame()
    
    def validate_data(self, df: pd.DataFrame, validation_type: str = "initial") -> Dict[str, Any]:
        """
        Valide les données selon le type spécifié
        
        Args:
            df: DataFrame à valider
            validation_type: Type de validation (initial, final)
            
        Returns:
            Dict avec les résultats de validation
        """
        logger.info(f"✅ === PHASE 2: VALIDATION {validation_type.upper()} ===")
        
        if self.pipeline_manager.quality_validator is None:
            logger.warning("⚠️ QualityValidator non disponible, validation ignorée")
            return {"overall_score": 0.0, "status": "SKIP"}
        
        try:
            validation_result = self.pipeline_manager.quality_validator.validate_dataset(
                df, validation_type
            )
            
            score = validation_result.get('overall_score', 0.0)
            status = validation_result.get('status', 'UNKNOWN')
            
            logger.info(f"✅ Validation {validation_type}: {score:.2%}")
            logger.info(f"📊 Statut: {status}")
            
            self.validation_results[validation_type] = validation_result
            return validation_result
            
        except Exception as e:
            logger.error(f"❌ Erreur validation {validation_type}: {e}")
            return {"overall_score": 0.0, "status": "ERROR", "error": str(e)}
    
    def detect_similarities(self, df: pd.DataFrame) -> list:
        """
        Détecte les similarités entre colonnes
        
        Args:
            df: DataFrame à analyser
            
        Returns:
            Liste des groupes de similarités détectés
        """
        logger.info("🧠 === PHASE 3: DÉTECTION INTELLIGENTE ===")
        
        if self.pipeline_manager.similarity_detector is None:
            logger.warning("⚠️ SimilarityDetector non disponible, détection ignorée")
            return []
        
        try:
            similarity_groups = self.pipeline_manager.similarity_detector.detect_similar_columns(df)
            logger.info(f"🎯 {len(similarity_groups)} groupes de similarités détectés")
            return similarity_groups
            
        except Exception as e:
            logger.error(f"❌ Erreur détection similarités: {e}")
            return []
    
    def process_data(self, df: pd.DataFrame, output_dir: str) -> pd.DataFrame:
        """
        Traite les données via l'orchestrateur modulaire
        
        Args:
            df: DataFrame à traiter
            output_dir: Répertoire de sortie
            
        Returns:
            DataFrame traité
        """
        logger.info("🔧 === PHASE 4: TRANSFORMATION MODULAIRE ===")
        
        try:
            df_processed = self.pipeline_manager.orchestrator.run_modular_pipeline_only(
                input_source="dataframe",
                input_config={"dataframe": df},
                output_config={"output_dir": output_dir}
            )
            
            if isinstance(df_processed, dict) and 'final_dataframe' in df_processed:
                df_processed = df_processed['final_dataframe']
                logger.info(f"✅ Transformation terminée: {df_processed.shape[0]} lignes × {df_processed.shape[1]} colonnes")
            else:
                logger.warning("⚠️ Format de réponse invalide, utilisation des données originales")
                df_processed = df.copy()
                
            return df_processed
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur transformation modulaire: {e}, utilisation des données originales")
            return df.copy()
