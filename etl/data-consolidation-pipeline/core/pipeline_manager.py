#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎼 GESTIONNAIRE PRINCIPAL DU PIPELINE
=====================================

Gère l'initialisation et l'orchestration du pipeline ETL modulaire
"""

import logging
import time
from typing import Dict, Any, Optional, List
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
                
                # === STRATÉGIE DE CONSOLIDATION INTELLIGENTE ===
                logger.info("🧠 Application de la stratégie de consolidation intelligente...")
                
                # Règles de consolidation complètes
                consolidation_rules = [
                    # Groupe revenus
                    (['plex-revenue', 'revenu', 'plex-revenu', 'potential_gross_revenue'], 'revenue_final'),
                    # Groupe adresses
                    (['address', 'full_address', 'location'], 'address_final'),
                    # Groupe prix
                    (['price_assessment', 'price_final', 'price', 'prix'], 'price_final'),
                    # Groupe surfaces
                    (['living_area', 'surface_final', 'surface', 'superficie'], 'surface_final'),
                    # Groupe chambres
                    (['nb_bedroom', 'bedrooms_final', 'bedroom', 'chambres'], 'bedrooms_final'),
                    # Groupe salles de bain
                    (['nb_bathroom', 'bathrooms_final', 'bathroom', 'salle_bain'], 'bathrooms_final'),
                    # Groupe année construction
                    (['construction_year', 'year_built_final', 'year_built', 'annee'], 'year_built_final'),
                    # Groupe taxes municipales
                    (['municipal_taxes', 'municipal_tax', 'taxes_municipales'], 'municipal_taxes_final'),
                    # Groupe taxes scolaires
                    (['school_taxes', 'school_tax', 'taxes_scolaires'], 'school_taxes_final'),
                    # Groupe évaluations municipales
                    (['municipal_evaluation_building', 'municipal_evaluation_land', 'municipal_evaluation_total'], 'municipal_evaluation_final')
                ]
                
                # Application de la consolidation intelligente
                columns_consolidated = 0
                for source_cols, target_col in consolidation_rules:
                    # Filtrer les colonnes disponibles
                    available_cols = [col for col in source_cols if col in df_processed.columns]
                    
                    if len(available_cols) > 1:
                        logger.info(f"🔄 Consolidation: {available_cols} → {target_col}")
                        
                        # Stratégie de consolidation intelligente
                        df_processed[target_col] = self._consolidate_columns_intelligently(df_processed, available_cols)
                        
                        # Supprimer les colonnes sources
                        df_processed = df_processed.drop(columns=available_cols)
                        columns_consolidated += len(available_cols)
                        
                        logger.info(f"✅ {len(available_cols)} colonnes consolidées dans {target_col}")
                    elif len(available_cols) == 1:
                        # Renommer la colonne unique
                        df_processed = df_processed.rename(columns={available_cols[0]: target_col})
                        logger.info(f"🔄 Renommage: {available_cols[0]} → {target_col}")
                
                # === CONSOLIDATION INTELLIGENTE DES STRUCTURES COMPLEXES ===
                logger.info("🧠 Application de la consolidation intelligente des structures complexes...")
                
                # Consolidation intelligente des unités
                df_processed = self._consolidate_units_intelligently(df_processed)
                
                # Consolidation intelligente des adresses
                df_processed = self._consolidate_address_intelligently(df_processed)
                
                # Calcul des métriques de consolidation
                original_columns = len(df.columns)
                final_columns = len(df_processed.columns)
                reduction = original_columns - final_columns
                reduction_percentage = (reduction / original_columns) * 100 if original_columns > 0 else 0
                
                logger.info(f"📊 === RÉSULTATS DE LA CONSOLIDATION ===")
                logger.info(f"Colonnes originales: {original_columns}")
                logger.info(f"Colonnes finales: {final_columns}")
                logger.info(f"Colonnes consolidées: {columns_consolidated}")
                logger.info(f"Réduction: {reduction} colonnes ({reduction_percentage:.1f}%)")
                
                logger.info(f"✅ Données traitées: {df_processed.shape[0]} lignes × {df_processed.shape[1]} colonnes")
                return df_processed
            
            def _consolidate_columns_intelligently(self, df: pd.DataFrame, source_columns: List[str]) -> pd.Series:
                """Consolidation intelligente des colonnes avec stratégie de priorité."""
                if not source_columns:
                    return pd.Series(dtype='object')
                
                # Stratégie de priorité basée sur le nom de la colonne
                priority_order = {
                    'revenue': ['plex-revenue', 'revenu', 'potential_gross_revenue'],
                    'address': ['address', 'full_address', 'location'],
                    'price': ['price_final', 'price_assessment', 'price', 'prix'],
                    'surface': ['surface_final', 'living_area', 'surface', 'superficie'],
                    'bedrooms': ['bedrooms_final', 'nb_bedroom', 'bedroom', 'chambres'],
                    'bathrooms': ['bathrooms_final', 'nb_bathroom', 'bathroom', 'salle_bain'],
                    'year': ['year_built_final', 'construction_year', 'year_built', 'annee'],
                    'taxes': ['municipal_taxes', 'municipal_tax', 'taxes_municipales'],
                    'school': ['school_taxes', 'school_tax', 'taxes_scolaires'],
                    'evaluation': ['municipal_evaluation_total', 'municipal_evaluation_building', 'municipal_evaluation_land']
                }
                
                # Déterminer le type de consolidation
                consolidation_type = None
                for key, priority_list in priority_order.items():
                    if any(col in source_columns for col in priority_list):
                        consolidation_type = key
                        break
                
                if consolidation_type and consolidation_type in priority_order:
                    # Appliquer l'ordre de priorité
                    for priority_col in priority_order[consolidation_type]:
                        if priority_col in source_columns:
                            logger.info(f"🎯 Priorité: {priority_col} pour {consolidation_type}")
                            return df[priority_col]
                
                # Fallback: première colonne non-nulle
                for col in source_columns:
                    if col in df.columns and not df[col].isna().all():
                        logger.info(f"🔄 Fallback: {col}")
                        return df[col]
                
                # Dernier fallback: première colonne disponible
                return df[source_columns[0]]
            
            def _consolidate_units_intelligently(self, df: pd.DataFrame) -> pd.DataFrame:
                """Consolidation intelligente des colonnes d'unités."""
                logger.info("🏠 === CONSOLIDATION INTELLIGENTE DES UNITÉS ===")
                
                df_consolidated = df.copy()
                
                # Colonnes sources pour les unités
                unit_columns = ['unites', 'residential_units', 'commercial_units']
                available_columns = [col for col in unit_columns if col in df.columns]
                
                # Correction: utilisation de len() sur une liste Python pure
                if len(available_columns) > 1:
                    logger.info(f"🔄 Consolidation intelligente des colonnes d'unités: {available_columns}")
                    
                    # Créer les colonnes consolidées
                    df_consolidated['total_units_final'] = self._calculate_total_units(df, available_columns)
                    df_consolidated['unit_types_final'] = self._extract_unit_types(df, available_columns)
                    df_consolidated['unit_details_final'] = self._create_unit_details(df, available_columns)
                    
                    # Supprimer les colonnes sources
                    df_consolidated = df_consolidated.drop(columns=available_columns)
                    
                    logger.info(f"✅ {len(available_columns)} colonnes d'unités consolidées intelligemment")
                
                return df_consolidated
            
            def _consolidate_address_intelligently(self, df: pd.DataFrame) -> pd.DataFrame:
                """Consolidation intelligente des colonnes d'adresses."""
                logger.info("🏠 === CONSOLIDATION INTELLIGENTE DES ADRESSES ===")
                
                df_consolidated = df.copy()
                
                # Colonnes sources pour les adresses
                address_columns = ['address', 'full_address', 'location']
                available_columns = [col for col in address_columns if col in df.columns]
                
                # Correction: utilisation de len() sur une liste Python pure
                if len(available_columns) > 1:
                    logger.info(f"🔄 Consolidation intelligente des colonnes d'adresses: {available_columns}")
                    
                    # Créer les colonnes consolidées
                    df_consolidated['street_final'] = self._extract_street(df, available_columns)
                    df_consolidated['city_final'] = self._extract_city(df, available_columns)
                    df_consolidated['postal_code_final'] = self._extract_postal_code(df, available_columns)
                    
                    # Supprimer les colonnes sources
                    df_consolidated = df_consolidated.drop(columns=available_columns)
                    
                    logger.info(f"✅ {len(available_columns)} colonnes d'adresses consolidées intelligemment")
                
                return df_consolidated
            
            def _parse_json_string(self, value):
                """Parse une chaîne JSON de manière sécurisée."""
                if pd.isna(value) or value == '':
                    return None
                
                # Si c'est déjà une liste ou un dict Python, le retourner directement
                if isinstance(value, (list, dict)):
                    return value
                
                # Si c'est une chaîne, essayer de la parser
                if isinstance(value, str):
                    try:
                        # Essayer d'abord json.loads
                        import json
                        return json.loads(value)
                    except json.JSONDecodeError:
                        try:
                            # Fallback: ast.literal_eval pour les structures Python
                            import ast
                            return ast.literal_eval(value)
                        except (ValueError, SyntaxError):
                            # Dernier fallback: traiter comme string
                            return value
                
                # Pour tout autre type, retourner tel quel
                return value
            
            def _calculate_total_units(self, df: pd.DataFrame, unit_columns: List[str]) -> pd.Series:
                """Calcule le nombre total d'unités."""
                total_units = pd.Series(0, index=df.index)
                
                for col in unit_columns:
                    if col in df.columns:
                        for idx, value in df[col].items():
                            if pd.notna(value):
                                parsed_value = self._parse_json_string(value)
                                if isinstance(parsed_value, list):
                                    # Compter les unités dans la liste
                                    count = 0
                                    for item in parsed_value:
                                        if isinstance(item, dict):
                                            # Extraire le count ou nb_unite
                                            if 'count' in item:
                                                try:
                                                    count += int(str(item['count']).strip())
                                                except (ValueError, TypeError):
                                                    count += 1
                                            elif 'nb_unite' in item:
                                                try:
                                                    count += int(str(item['nb_unite']).strip())
                                                except (ValueError, TypeError):
                                                    count += 1
                                            else:
                                                count += 1
                                        else:
                                            count += 1
                                    total_units[idx] += count
                                elif isinstance(parsed_value, dict):
                                    # Structure simple
                                    if 'count' in parsed_value:
                                        try:
                                            total_units[idx] += int(str(parsed_value['count']).strip())
                                        except (ValueError, TypeError):
                                            total_units[idx] += 1
                                    elif 'nb_unite' in parsed_value:
                                        try:
                                            total_units[idx] += int(str(parsed_value['nb_unite']).strip())
                                        except (ValueError, TypeError):
                                            total_units[idx] += 1
                
                return total_units
            
            def _extract_unit_types(self, df: pd.DataFrame, unit_columns: List[str]) -> pd.Series:
                """Extrait les types d'unités uniques."""
                unit_types = pd.Series('', index=df.index)
                
                for col in unit_columns:
                    if col in df.columns:
                        for idx, value in df[col].items():
                            # Correction: utilisation de méthodes pandas appropriées
                            current_value = unit_types.iloc[idx]
                            if pd.notna(value) and (current_value == '' or pd.isna(current_value)):
                                parsed_value = self._parse_json_string(value)
                                if isinstance(parsed_value, list):
                                    types = []
                                    for item in parsed_value:
                                        if isinstance(item, dict):
                                            # Extraire le type ou unite
                                            if 'type' in item:
                                                types.append(str(item['type']))
                                            elif 'unite' in item:
                                                types.append(str(item['unite']))
                                    if types:
                                        unit_types.iloc[idx] = ', '.join(set(types))
                                elif isinstance(parsed_value, dict):
                                    if 'type' in parsed_value:
                                        unit_types.iloc[idx] = str(parsed_value['type'])
                                    elif 'unite' in parsed_value:
                                        unit_types.iloc[idx] = str(parsed_value['unite'])
                
                return unit_types
            
            def _create_unit_details(self, df: pd.DataFrame, unit_columns: List[str]) -> pd.Series:
                """Crée une structure détaillée des unités."""
                unit_details = pd.Series('', index=df.index)
                
                for col in unit_columns:
                    if col in df.columns:
                        for idx, value in df[col].items():
                            # Correction: utilisation de méthodes pandas appropriées
                            current_value = unit_details.iloc[idx]
                            if pd.notna(value) and (current_value == '' or pd.isna(current_value)):
                                parsed_value = self._parse_json_string(value)
                                if isinstance(parsed_value, list):
                                    details = []
                                    for item in parsed_value:
                                        if isinstance(item, dict):
                                            detail = {}
                                            if 'type' in item:
                                                detail['type'] = item['type']
                                            elif 'unite' in item:
                                                detail['type'] = item['unite']
                                            
                                            if 'count' in item:
                                                detail['count'] = item['count']
                                            elif 'nb_unite' in item:
                                                detail['count'] = item['nb_unite']
                                            
                                            if detail:
                                                details.append(detail)
                                    
                                    if details:
                                        import json
                                        unit_details.iloc[idx] = json.dumps(details, ensure_ascii=False)
                                elif isinstance(parsed_value, dict):
                                    detail = {}
                                    if 'type' in parsed_value:
                                        detail['type'] = parsed_value['type']
                                    elif 'unite' in parsed_value:
                                        detail['type'] = parsed_value['unite']
                                    
                                    if 'count' in parsed_value:
                                        detail['count'] = parsed_value['count']
                                    elif 'nb_unite' in parsed_value:
                                        detail['count'] = parsed_value['nb_unite']
                                    
                                    if detail:
                                        import json
                                        unit_details.iloc[idx] = json.dumps([detail], ensure_ascii=False)
                
                return unit_details
            
            def _extract_street(self, df: pd.DataFrame, address_columns: List[str]) -> pd.Series:
                """Extrait la rue depuis les colonnes d'adresse."""
                street = pd.Series('', index=df.index)
                
                for col in address_columns:
                    if col in df.columns:
                        for idx, value in df[col].items():
                            # Correction: utilisation de méthodes pandas appropriées
                            current_value = street.iloc[idx]
                            if pd.notna(value) and (current_value == '' or pd.isna(current_value)):
                                parsed_value = self._parse_json_string(value)
                                if isinstance(parsed_value, dict):
                                    if 'street' in parsed_value:
                                        street.iloc[idx] = str(parsed_value['street'])
                                elif isinstance(parsed_value, str):
                                    # Essayer d'extraire la rue d'une adresse complète
                                    if ',' in parsed_value:
                                        street.iloc[idx] = parsed_value.split(',')[0].strip()
                                    else:
                                        street.iloc[idx] = parsed_value
                
                return street
            
            def _extract_city(self, df: pd.DataFrame, address_columns: List[str]) -> pd.Series:
                """Extrait la ville depuis les colonnes d'adresse."""
                city = pd.Series('', index=df.index)
                
                for col in address_columns:
                    if col in address_columns:
                        for idx, value in df[col].items():
                            # Correction: utilisation de méthodes pandas appropriées
                            current_value = city.iloc[idx]
                            if pd.notna(value) and (current_value == '' or pd.isna(current_value)):
                                parsed_value = self._parse_json_string(value)
                                if isinstance(parsed_value, dict):
                                    if 'locality' in parsed_value:
                                        city.iloc[idx] = str(parsed_value['locality'])
                                elif isinstance(parsed_value, str):
                                    # Essayer d'extraire la ville d'une adresse complète
                                    if ',' in parsed_value:
                                        parts = parsed_value.split(',')
                                        if len(parts) > 1:
                                            city.iloc[idx] = parts[1].strip()
                
                return city
            
            def _extract_postal_code(self, df: pd.DataFrame, address_columns: List[str]) -> pd.Series:
                """Extrait le code postal depuis les colonnes d'adresse."""
                postal_code = pd.Series('', index=df.index)
                
                for col in address_columns:
                    if col in address_columns:
                        for idx, value in df[col].items():
                            # Correction: utilisation de méthodes pandas appropriées
                            current_value = postal_code.iloc[idx]
                            if pd.notna(value) and (current_value == '' or pd.isna(current_value)):
                                parsed_value = self._parse_json_string(value)
                                if isinstance(parsed_value, dict):
                                    if 'postal_code' in parsed_value:
                                        postal_code.iloc[idx] = str(parsed_value['postal_code'])
                
                return postal_code
            
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
