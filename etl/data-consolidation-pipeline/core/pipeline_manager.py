#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎼 GESTIONNAIRE PRINCIPAL DU PIPELINE
=====================================

Gère l'initialisation et l'orchestration du pipeline ETL modulaire
"""

import logging
import time
from typing import Dict, Any, Optional
from pathlib import Path
import pandas as pd

# Orchestrateur simple intégré pour éviter les dépendances complexes

logger = logging.getLogger(__name__)

class PipelineManager:
    """
    Gestionnaire principal du pipeline ETL modulaire
    
    Responsable de l'initialisation, de la configuration
    et de l'orchestration des composants
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialise le gestionnaire de pipeline
        
        Args:
            config: Configuration du pipeline
        """
        self.config = config or {}
        self.start_time = None
        self.end_time = None
        
        # === INITIALISATION DE L'ORCHESTRATEUR INTÉGRÉ ===
        logger.info("🎼 === INITIALISATION ORCHESTRATEUR INTÉGRÉ ===")
        try:
            # Création d'un orchestrateur intégré
            self.orchestrator = self._create_integrated_orchestrator()
            logger.info("✅ Orchestrateur intégré initialisé")
        except Exception as e:
            logger.error(f"❌ Erreur initialisation orchestrateur: {e}")
            raise
        
        # === INITIALISATION DES MODULES EXTERNES ===
        self._initialize_external_modules()
        
        logger.info("✅ Pipeline initialisé avec succès")
    
    def _create_integrated_orchestrator(self):
        """Crée un orchestrateur intégré pour le pipeline modulaire"""
        class IntegratedOrchestrator:
            def __init__(self):
                self.data_extractor = self._create_data_extractor()
                self.pipeline_version = '7.0.0_modular'
                self.optimization_level = 'medium'
            
            def _create_data_extractor(self):
                """Crée un extracteur de données intégré"""
                class DataExtractor:
                    def extract_data(self, source: str, source_config: Dict):
                        if source == "test":
                            return self._generate_test_data()
                        elif source == "mongodb":
                            return self._extract_mongodb(source_config)
                        else:
                            return {"dataframe": pd.DataFrame()}
                    
                    def _generate_test_data(self):
                        """Génère des données de test"""
                        import numpy as np
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
                        return {"dataframe": df}
                    
                    def _extract_mongodb(self, source_config: Dict):
                        """Extraction MongoDB intégrée"""
                        try:
                            import pymongo
                            
                            # Connexion MongoDB
                            client = pymongo.MongoClient("mongodb://localhost:27017/")
                            db = client[source_config.get('database', 'real_estate_db')]
                            collection = db[source_config.get('collection', 'properties')]
                            
                            # Requête
                            query = source_config.get('query', {})
                            limit = source_config.get('limit', 1000)
                            
                            # Extraction
                            cursor = collection.find(query).limit(limit)
                            data = list(cursor)
                            
                            if data:
                                df = pd.DataFrame(data)
                                # Conversion des ObjectId en string
                                if '_id' in df.columns:
                                    df['_id'] = df['_id'].astype(str)
                                
                                logger.info(f"✅ MongoDB: {len(df)} documents extraits")
                                client.close()
                                return {"dataframe": df}
                            else:
                                logger.warning("⚠️ Aucun document trouvé dans MongoDB")
                                client.close()
                                return {"dataframe": pd.DataFrame()}
                                
                        except Exception as e:
                            logger.error(f"❌ Erreur extraction MongoDB: {e}")
                            return {"dataframe": pd.DataFrame()}
                
                return DataExtractor()
            
            def run_modular_pipeline_only(self, input_source: str, input_config: Dict, 
                                         output_config: Dict) -> Dict[str, Any]:
                """Exécute le pipeline modulaire intégré"""
                logger.info("🎼 === EXÉCUTION PIPELINE MODULAIRE INTÉGRÉ ===")
                
                try:
                    # Récupération des données d'entrée
                    if input_source == "dataframe" and "dataframe" in input_config:
                        df = input_config["dataframe"]
                        logger.info(f"📊 Traitement de {len(df)} lignes × {len(df.columns)} colonnes")
                        
                        # Traitement intégré (consolidation avancée)
                        df_processed = self._process_data(df)
                        
                        # Ajout de métadonnées de traitement
                        df_processed.attrs['pipeline_version'] = self.pipeline_version
                        df_processed.attrs['optimization_level'] = self.optimization_level
                        df_processed.attrs['processed'] = True
                        
                        logger.info("✅ Pipeline modulaire intégré terminé")
                        
                        return {
                            'status': 'success',
                            'final_dataframe': df_processed,
                            'processing_info': {
                                'pipeline_version': self.pipeline_version,
                                'optimization_level': self.optimization_level,
                                'input_shape': df.shape,
                                'output_shape': df_processed.shape
                            }
                        }
                    else:
                        logger.error(f"❌ Source d'entrée non supportée: {input_source}")
                        return {
                            'status': 'error',
                            'error': f'Source non supportée: {input_source}'
                        }
                        
                except Exception as e:
                    logger.error(f"❌ Erreur pipeline modulaire intégré: {e}")
                    return {
                        'status': 'error',
                        'error': str(e)
                    }
            
            def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
                """Traitement intégré des données (consolidation avancée)"""
                logger.info("🔧 Traitement des données...")
                
                df_processed = df.copy()
                
                # Consolidation avancée des colonnes similaires
                consolidation_rules = [
                    (['price', 'prix'], 'price_final'),
                    (['surface', 'superficie'], 'surface_final'),
                    (['bedrooms', 'chambres'], 'bedrooms_final'),
                    (['bathrooms', 'salle_bain'], 'bathrooms_final'),
                    (['year_built', 'annee_construction'], 'year_built_final')
                ]
                
                for source_cols, target_col in consolidation_rules:
                    available_cols = [col for col in source_cols if col in df_processed.columns]
                    if available_cols:
                        # Prendre la première colonne non-nulle
                        df_processed[target_col] = df_processed[available_cols].bfill(axis=1).iloc[:, 0]
                        # Supprimer les colonnes sources
                        df_processed = df_processed.drop(columns=available_cols)
                
                logger.info(f"✅ Données traitées: {df_processed.shape[0]} lignes × {df_processed.shape[1]} colonnes")
                return df_processed
            
            def get_status(self) -> Dict[str, Any]:
                """Retourne le statut de l'orchestrateur"""
                return {
                    'pipeline_version': self.pipeline_version,
                    'optimization_level': self.optimization_level,
                    'status': 'ready',
                    'type': 'integrated'
                }
        
        return IntegratedOrchestrator()
    
    def _initialize_external_modules(self):
        """Initialise les modules externes disponibles"""
        logger.info("🔧 Initialisation des modules externes...")
        
        # === SIMILARITY DETECTOR ===
        try:
            from intelligence.similarity_detector import SimilarityDetector
            self.similarity_detector = SimilarityDetector()
            logger.info("✅ Détecteur de similarité initialisé")
        except ImportError:
            logger.warning("⚠️ SimilarityDetector non disponible")
            self.similarity_detector = None
        
        # === QUALITY VALIDATOR ===
        try:
            from validation.quality_validator import QualityValidator
            self.quality_validator = QualityValidator()
            logger.info("✅ Validateur de qualité initialisé")
        except ImportError:
            logger.warning("⚠️ QualityValidator non disponible")
            self.quality_validator = None
        
        # === ADVANCED EXPORTER ===
        try:
            from export.advanced_exporter import AdvancedExporter
            self.exporter = AdvancedExporter()
            logger.info("✅ Exportateur avancé initialisé")
        except ImportError:
            logger.warning("⚠️ AdvancedExporter non disponible")
            self.exporter = None
        
        # === PERFORMANCE OPTIMIZER ===
        try:
            from performance.performance_optimizer import PerformanceOptimizer
            self.performance_optimizer = PerformanceOptimizer()
            self.performance_optimizer.enable_all_optimizations()
            logger.info("✅ Optimiseur de performance initialisé")
        except ImportError:
            logger.warning("⚠️ PerformanceOptimizer non disponible")
            self.performance_optimizer = None
        
        # === PROPERTY TYPE NORMALIZER ===
        try:
            from utils.property_type_normalizer import PropertyTypeNormalizer
            self.property_normalizer = PropertyTypeNormalizer()
            logger.info("✅ Normaliseur de types de propriétés initialisé")
        except ImportError:
            logger.warning("⚠️ PropertyTypeNormalizer non disponible")
            self.property_normalizer = None
        
        # === VALIDATION DASHBOARD ===
        try:
            from dashboard.validation_dashboard import ValidationDashboard
            self.validation_dashboard = ValidationDashboard()
            logger.info("✅ Dashboard de validation initialisé")
        except ImportError:
            logger.warning("⚠️ ValidationDashboard non disponible")
            self.validation_dashboard = None
    
    def start_pipeline(self):
        """Démarre le pipeline et enregistre le temps de début"""
        self.start_time = time.time()
        logger.info("🚀 === DÉMARRAGE DU PIPELINE MODULAIRE ===")
    
    def end_pipeline(self):
        """Termine le pipeline et calcule la durée"""
        self.end_time = time.time()
        duration = self.end_time - self.start_time if self.start_time else 0
        logger.info(f"⏱️ Durée totale: {duration:.2f} secondes")
        return duration
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel du pipeline"""
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": (self.end_time - self.start_time) if self.start_time and self.end_time else 0,
            "orchestrator_ready": hasattr(self, 'orchestrator') and self.orchestrator is not None,
            "external_modules": {
                "similarity_detector": self.similarity_detector is not None,
                "quality_validator": self.quality_validator is not None,
                "exporter": self.exporter is not None,
                "performance_optimizer": self.performance_optimizer is not None,
                "property_normalizer": self.property_normalizer is not None,
                "validation_dashboard": self.validation_dashboard is not None
            }
        }
