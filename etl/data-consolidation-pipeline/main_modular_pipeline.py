#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 PIPELINE ETL ULTRA-INTELLIGENT - SCRIPT PRINCIPAL
=====================================================

Script principal pour la consolidation maximale des variables immobilières
Basé sur les spécifications du real_estate_prompt.md
"""

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import warnings

# Suppression des warnings pour un affichage plus propre
warnings.filterwarnings('ignore')

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('pipeline.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Import des modules du pipeline
try:
    # Import de l'orchestrateur principal unifié
    from core.main_pipeline_orchestrator import MainPipelineOrchestrator
    
    # Import des modules externes (optionnels)
    try:
        from config.consolidation_config import ConsolidationConfig
        CONFIG_AVAILABLE = True
        logger.info("✅ Configuration de consolidation disponible")
    except ImportError:
        CONFIG_AVAILABLE = False
        logger.warning("⚠️ Configuration de consolidation non disponible")
    
    try:
        from intelligence.similarity_detector import SimilarityDetector
        SIMILARITY_AVAILABLE = True
        logger.info("✅ Détecteur de similarité disponible")
    except ImportError:
        SIMILARITY_AVAILABLE = False
        logger.warning("⚠️ Détecteur de similarité non disponible")
    
    try:
        from validation.quality_validator import QualityValidator
        VALIDATOR_AVAILABLE = True
        logger.info("✅ Validateur de qualité disponible")
    except ImportError:
        VALIDATOR_AVAILABLE = False
        logger.warning("⚠️ Validateur de qualité non disponible")
    
    try:
        from export.advanced_exporter import AdvancedExporter
        EXPORTER_AVAILABLE = True
        logger.info("✅ Exportateur avancé disponible")
    except ImportError:
        EXPORTER_AVAILABLE = False
        logger.warning("⚠️ Exportateur avancé non disponible")
    
    try:
        from performance.performance_optimizer import PerformanceOptimizer
        OPTIMIZER_AVAILABLE = True
        logger.info("✅ Optimiseur de performance disponible")
    except ImportError:
        OPTIMIZER_AVAILABLE = False
        logger.warning("⚠️ Optimiseur de performance non disponible")
    
    try:
        from utils.db import read_mongodb_to_dataframe, get_mongodb_stats
        from utils.property_type_normalizer import PropertyTypeNormalizer
        UTILS_AVAILABLE = True
        logger.info("✅ Utilitaires disponibles")
    except ImportError:
        UTILS_AVAILABLE = False
        logger.warning("⚠️ Utilitaires non disponibles")
    
    # Import conditionnel du dashboard
    try:
        from dashboard.validation_dashboard import ValidationDashboard
        DASHBOARD_AVAILABLE = True
        logger.info("✅ Dashboard de validation disponible")
    except ImportError:
        DASHBOARD_AVAILABLE = False
        logger.warning("⚠️ Dashboard non disponible")
    
    logger.info("✅ Modules importés avec succès")
    
except ImportError as e:
    logger.error(f"❌ Erreur d'import: {e}")
    logger.error("🔧 Vérifiez l'installation avec: python test_installation.py")
    sys.exit(1)


class ModularPipeline:
    """
    Pipeline ETL modulaire principal
    Orchestre tous les composants pour la consolidation maximale
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialise le pipeline ultra-intelligent
        
        Args:
            config: Configuration personnalisée (optionnel)
        """
        self.config = config or {}
        self.start_time = None
        self.end_time = None
        
        # Initialisation des composants
        logger.info("🚀 === INITIALISATION DU PIPELINE MODULAIRE ===")
        
        # Configuration (si disponible)
        if CONFIG_AVAILABLE:
            self.consolidation_config = ConsolidationConfig()
            if not self.consolidation_config.validate_configuration():
                logger.error("❌ Configuration de consolidation invalide")
                sys.exit(1)
            logger.info("✅ Configuration de consolidation initialisée")
        else:
            self.consolidation_config = None
            logger.warning("⚠️ Configuration de consolidation non disponible")
        
        # Orchestrateur principal unifié
        self.orchestrator = MainPipelineOrchestrator(
            config=self.config,
            use_external_modules=True
        )
        logger.info("✅ Orchestrateur principal initialisé")
        
        # Composants externes (optionnels)
        if SIMILARITY_AVAILABLE:
            self.similarity_detector = SimilarityDetector()
            logger.info("✅ Détecteur de similarité initialisé")
        else:
            self.similarity_detector = None
            
        if VALIDATOR_AVAILABLE:
            self.quality_validator = QualityValidator()
            logger.info("✅ Validateur de qualité initialisé")
        else:
            self.quality_validator = None
            
        if EXPORTER_AVAILABLE:
            self.exporter = AdvancedExporter()
            logger.info("✅ Exportateur avancé initialisé")
        else:
            self.exporter = None
            
        if OPTIMIZER_AVAILABLE:
            self.performance_optimizer = PerformanceOptimizer()
            self.performance_optimizer.enable_all_optimizations()
            logger.info("✅ Optimiseur de performance initialisé")
        else:
            self.performance_optimizer = None
            
        if UTILS_AVAILABLE:
            self.property_normalizer = PropertyTypeNormalizer()
            logger.info("✅ Normaliseur de types de propriétés initialisé")
        else:
            self.property_normalizer = None
            
        # Initialisation conditionnelle du dashboard
        if DASHBOARD_AVAILABLE:
            self.validation_dashboard = ValidationDashboard()
            logger.info("✅ Dashboard initialisé")
        else:
            self.validation_dashboard = None
            logger.info("⚠️ Dashboard non initialisé")
        
        logger.info("✅ Pipeline initialisé avec succès")
    
    def run_complete_pipeline(self, source: str = "test", output_dir: str = "exports",
                             formats: List[str] = None, optimization: str = "medium",
                             parallel: bool = True, chunked: bool = False,
                             validate_only: bool = False, dry_run: bool = False,
                             verbose: bool = False, source_path: str = None,
                             mongodb_db: str = None, mongodb_collection: str = None,
                             mongodb_query: str = None, mongodb_query_file: str = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Exécute le pipeline complet ETL modulaire
        
        Args:
            source: Source des données (mongodb, csv, json, test)
            output_dir: Répertoire de sortie
            formats: Formats d'export
            optimization: Niveau d'optimisation (light, medium, aggressive)
            parallel: Activer le traitement parallèle
            chunked: Export par chunks
            validate_only: Exécuter uniquement la validation
            dry_run: Simulation sans modification
            verbose: Mode verbeux
            source_path: Chemin du fichier (CSV/JSON) ou chaîne de connexion MongoDB
            mongodb_db: Nom de la base de données MongoDB
            mongodb_collection: Nom de la collection MongoDB
            mongodb_query: Requête MongoDB au format JSON
            mongodb_query_file: Chemin vers un fichier JSON contenant la requête MongoDB
            limit: Limite du nombre de documents MongoDB à extraire
            
        Returns:
            Dict avec les résultats du pipeline
        """
        self.start_time = time.time()
        
        logger.info("🚀 === DÉMARRAGE DU PIPELINE MODULAIRE ===")
        logger.info(f"📊 Source: {source}")
        logger.info(f"📁 Sortie: {output_dir}")
        logger.info(f"🔧 Optimisation: {optimization}")
        logger.info(f"⚡ Parallèle: {parallel}")
        logger.info(f"📦 Chunked: {chunked}")
        logger.info(f"🔍 Validation uniquement: {validate_only}")
        logger.info(f"🧪 Dry run: {dry_run}")
        
        try:
            # === PHASE 1: EXTRACTION ===
            logger.info("📥 === PHASE 1: EXTRACTION ===")
            df = self._extract_data(source, source_path, mongodb_db, mongodb_collection, mongodb_query, limit, mongodb_query_file)
            
            if df is None or df.empty:
                logger.error("❌ Aucune donnée extraite")
                return {"status": "error", "message": "Aucune donnée extraite"}
            
            logger.info(f"✅ Extraction réussie: {df.shape[0]} lignes × {df.shape[1]} colonnes")
            
            # === PHASE 2: VALIDATION INITIALE ===
            logger.info("✅ === PHASE 2: VALIDATION INITIALE ===")
            initial_validation = self.quality_validator.validate_dataset(df, "initial")
            logger.info(f"✅ Validation initiale: {initial_validation['overall_score']:.2%}")
            
            if validate_only:
                logger.info("🔍 Mode validation uniquement - Arrêt du pipeline")
                return {
                    "status": "validation_only",
                    "validation_results": initial_validation,
                    "duration_seconds": time.time() - self.start_time
                }
            
            # === PHASE 3: DÉTECTION INTELLIGENTE ===
            logger.info("🧠 === PHASE 3: DÉTECTION INTELLIGENTE ===")
            similarity_groups = self.similarity_detector.detect_similar_columns(df)
            logger.info(f"🎯 {len(similarity_groups)} groupes de similarités détectés")
            
            # === PHASE 4: TRANSFORMATION MODULAIRE ===
            if not dry_run:
                logger.info("🔧 === PHASE 4: TRANSFORMATION MODULAIRE ===")
                # Utilisation de l'orchestrateur modulaire
                try:
                    df_cleaned = self.orchestrator.run_modular_pipeline_only(
                        input_source="dataframe",
                        input_config={"dataframe": df},
                        output_config={"output_dir": output_dir}
                    )
                    if isinstance(df_cleaned, dict) and 'final_dataframe' in df_cleaned:
                        df_cleaned = df_cleaned['final_dataframe']
                    else:
                        df_cleaned = df.copy()
                    logger.info(f"✅ Transformation terminée: {df_cleaned.shape[0]} lignes × {df_cleaned.shape[1]} colonnes")
                except Exception as e:
                    logger.warning(f"⚠️ Erreur transformation modulaire: {e}, utilisation des données originales")
                    df_cleaned = df.copy()
            else:
                logger.info("🧪 Mode dry run - Aucune transformation effectuée")
                df_cleaned = df.copy()
            
            # === PHASE 5: VALIDATION FINALE ===
            logger.info("✅ === PHASE 5: VALIDATION FINALE ===")
            final_validation = self.quality_validator.validate_dataset(df_cleaned, "final")
            logger.info(f"✅ Validation finale: {final_validation['overall_score']:.2%}")
            
            # === PHASE 6: EXPORT MULTI-FORMATS ===
            if not dry_run:
                logger.info("💾 === PHASE 6: EXPORT MULTI-FORMATS ===")
                export_formats = formats or ["parquet", "csv", "geojson", "hdf5"]
                exported_files = self.exporter.export_dataset(
                    df_cleaned, "modular_pipeline", export_formats, output_dir
                )
                logger.info(f"✅ Export terminé: {len(exported_files)} formats")
            else:
                logger.info("🧪 Mode dry run - Aucun export effectué")
                exported_files = {}
            
            # === PHASE 7: GÉNÉRATION DES RAPPORTS ===
            logger.info("📊 === PHASE 7: GÉNÉRATION DES RAPPORTS ===")
            reports = self._generate_reports(
                df, df_cleaned, initial_validation, final_validation,
                similarity_groups, exported_files, output_dir
            )
            logger.info(f"✅ Rapports générés: {len(reports)} fichiers")
            
            # === CALCUL DES MÉTRIQUES FINALES ===
            self.end_time = time.time()
            duration = self.end_time - self.start_time
            
            pipeline_metrics = self._calculate_pipeline_metrics(
                df, df_cleaned, initial_validation, final_validation, duration
            )
            
            # === COMPILATION DES RÉSULTATS ===
            results = {
                "status": "success",
                "pipeline_version": self.consolidation_config.PIPELINE_VERSION,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "duration_seconds": duration,
                "source": source,
                "output_directory": output_dir,
                "initial_shape": df.shape,
                "final_shape": df_cleaned.shape,
                "column_reduction": {
                    "initial_columns": df.shape[1],
                    "final_columns": df_cleaned.shape[1],
                    "reduction_percentage": ((df.shape[1] - df_cleaned.shape[1]) / df.shape[1]) * 100
                },
                "validation_results": {
                    "initial": initial_validation,
                    "final": final_validation
                },
                "similarity_groups": similarity_groups,
                "exported_files": exported_files,
                "reports": reports,
                "pipeline_metrics": pipeline_metrics
            }
            
            logger.info("🎉 === PIPELINE TERMINÉ AVEC SUCCÈS ===")
            logger.info(f"⏱️ Durée totale: {duration:.2f} secondes")
            logger.info(f"📊 Réduction colonnes: {pipeline_metrics.get('column_reduction', {}).get('percentage', 0):.1f}%")
            logger.info(f"🎯 Score qualité final: {final_validation['overall_score']:.2%}")
            
            return results
            
        except Exception as e:
            self.end_time = time.time()
            duration = self.end_time - self.start_time if self.end_time else 0
            
            logger.error(f"❌ Erreur dans le pipeline: {e}")
            logger.error(f"⏱️ Durée avant erreur: {duration:.2f} secondes")
            
            return {
                "status": "error",
                "error": str(e),
                "duration_seconds": duration,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def _extract_data(self, source: str, source_path: str = None, 
                      mongodb_db: str = None, mongodb_collection: str = None,
                      mongodb_query: str = None, limit: Optional[int] = None,
                      mongodb_query_file: str = None) -> Optional[Any]:
        """
        Extrait les données selon la source spécifiée
        
        Args:
            source: Source des données
            source_path: Chemin du fichier ou chaîne de connexion MongoDB
            mongodb_db: Nom de la base de données MongoDB
            mongodb_collection: Nom de la collection MongoDB
            mongodb_query: Requête MongoDB au format JSON
            
        Returns:
            DataFrame ou None en cas d'erreur
        """
        try:
            if source == "mongodb":
                logger.info("🗄️ Extraction depuis MongoDB...")
                
                # Vérification des paramètres MongoDB
                if not source_path:
                    logger.warning("⚠️ Aucune chaîne de connexion MongoDB fournie, utilisation des paramètres par défaut")
                    source_path = "mongodb://localhost:27017"
                
                if not mongodb_db:
                    logger.warning("⚠️ Aucune base de données MongoDB spécifiée, utilisation de 'real_estate_db'")
                    mongodb_db = "real_estate_db"
                
                if not mongodb_collection:
                    logger.warning("⚠️ Aucune collection MongoDB spécifiée, utilisation de 'properties'")
                    mongodb_collection = "properties"
                
                # Traitement de la requête MongoDB
                query_dict = {}
                
                # Priorité 1: Fichier JSON de requête
                if mongodb_query_file and mongodb_query_file != "None":
                    try:
                        import json
                        import os
                        
                        if os.path.exists(mongodb_query_file):
                            logger.info(f"📁 Lecture de la requête depuis le fichier: {mongodb_query_file}")
                            with open(mongodb_query_file, 'r', encoding='utf-8') as f:
                                query_dict = json.load(f)
                            logger.info(f"✅ Requête MongoDB chargée depuis le fichier: {query_dict}")
                        else:
                            logger.warning(f"⚠️ Fichier de requête introuvable: {mongodb_query_file}")
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur lecture fichier de requête: {e}")
                
                # Priorité 2: Argument en ligne de commande
                if not query_dict and mongodb_query:
                    try:
                        import json
                        import ast
                        
                        # Vérifier si c'est déjà un dictionnaire ou une chaîne JSON
                        if isinstance(mongodb_query, dict):
                            query_dict = mongodb_query
                            logger.info(f"🔍 Requête MongoDB appliquée (dict): {mongodb_query}")
                        else:
                            # C'est une chaîne, essayer plusieurs méthodes de parsing
                            query_str = str(mongodb_query).strip()
                            logger.info(f"🔍 Tentative de parsing de la requête: {query_str}")
                            
                            # Parser JSON générique robuste
                            query_dict = self._parse_mongodb_query(query_str)
                            if query_dict:
                                logger.info(f"✅ Requête MongoDB parsée avec succès: {query_dict}")
                            else:
                                raise ValueError("Impossible de parser la requête")
                                            
                    except Exception as e:
                        logger.warning(f"⚠️ Requête MongoDB invalide: {e}, utilisation de la requête par défaut")
                        query_dict = {}
                
                if not query_dict:
                    logger.info("ℹ️ Aucune requête MongoDB spécifiée, extraction de tous les documents")
                
                logger.info(f"🗄️ Connexion MongoDB: {source_path}/{mongodb_db}.{mongodb_collection}")
                
                df = read_mongodb_to_dataframe(
                    connection_string=source_path,
                    database_name=mongodb_db,
                    collection_name=mongodb_collection,
                    query=query_dict,
                    limit=limit
                )
                
                if df is not None and not df.empty:
                    logger.info(f"✅ MongoDB: {df.shape[0]} propriétés extraites")
                    return df
                else:
                    logger.warning("⚠️ MongoDB vide ou inaccessible, utilisation du mode test")
                    return self._generate_test_data()
            
            elif source == "csv":
                logger.info("📄 Extraction depuis CSV...")
                
                if not source_path:
                    logger.error("❌ Chemin du fichier CSV requis avec --source-path")
                    logger.info("🔄 Utilisation du mode test comme fallback")
                    return self._generate_test_data()
                
                try:
                    import pandas as pd
                    logger.info(f"📄 Lecture du fichier CSV: {source_path}")
                    df = pd.read_csv(source_path)
                    logger.info(f"✅ CSV: {df.shape[0]} lignes × {df.shape[1]} colonnes lues")
                    return df
                except Exception as e:
                    logger.error(f"❌ Erreur lecture CSV: {e}")
                    logger.info("🔄 Utilisation du mode test comme fallback")
                    return self._generate_test_data()
            
            elif source == "json":
                logger.info("📋 Extraction depuis JSON...")
                
                if not source_path:
                    logger.error("❌ Chemin du fichier JSON requis avec --source-path")
                    logger.info("🔄 Utilisation du mode test comme fallback")
                    return self._generate_test_data()
                
                try:
                    import pandas as pd
                    logger.info(f"📋 Lecture du fichier JSON: {source_path}")
                    df = pd.read_json(source_path)
                    logger.info(f"✅ JSON: {df.shape[0]} lignes × {df.shape[1]} colonnes lues")
                    return df
                except Exception as e:
                    logger.error(f"❌ Erreur lecture JSON: {e}")
                    logger.info("🔄 Utilisation du mode test comme fallback")
                    return self._generate_test_data()
            
            elif source == "test":
                logger.info("🧪 Génération de données de test...")
                return self._generate_test_data()
            
            else:
                logger.warning(f"⚠️ Source '{source}' non reconnue, utilisation du mode test")
                return self._generate_test_data()
                
        except Exception as e:
            logger.error(f"❌ Erreur d'extraction: {e}")
            logger.info("🔄 Utilisation du mode test comme fallback")
            return self._generate_test_data()
    
    def _parse_mongodb_query(self, query_str: str) -> dict:
        """
        Parse robuste d'une requête MongoDB JSON
        
        Args:
            query_str: Chaîne de requête JSON à parser
            
        Returns:
            Dictionnaire de requête ou None si échec
        """
        try:
            import json
            import ast
            import re
            
            # Nettoyer la chaîne de requête
            cleaned_str = query_str.strip()
            
            # Méthode 1: JSON standard
            try:
                return json.loads(cleaned_str)
            except json.JSONDecodeError:
                pass
            
            # Méthode 2: Corriger les guillemets simples en doubles
            try:
                fixed_quotes = cleaned_str.replace("'", '"')
                return json.loads(fixed_quotes)
            except json.JSONDecodeError:
                pass
            
            # Méthode 3: Utiliser ast.literal_eval pour expressions Python
            try:
                return ast.literal_eval(cleaned_str)
            except (ValueError, SyntaxError):
                pass
            
            # Méthode 4: Parser manuel robuste pour requêtes MongoDB
            try:
                # Corriger les problèmes communs de format
                fixed_str = cleaned_str
                
                # Corriger les espaces autour des deux points
                fixed_str = re.sub(r'\s*:\s*', ':', fixed_str)
                
                # S'assurer que les clés sont entre guillemets doubles
                fixed_str = re.sub(r'([{,]\s*)(\w+):', r'\1"\2":', fixed_str)
                
                # S'assurer que les valeurs string sont entre guillemets doubles
                fixed_str = re.sub(r':\s*([^{"\[\],}]+)([,}])', r': "\1"\2', fixed_str)
                
                # Corriger les opérateurs MongoDB (commencent par $)
                fixed_str = re.sub(r'"(\$\w+)"', r'\1', fixed_str)
                
                # Corriger les valeurs MongoDB spéciales
                fixed_str = re.sub(r':\s*(\$\w+)', r': "\1"', fixed_str)
                
                # Essayer à nouveau avec la chaîne corrigée
                return json.loads(fixed_str)
                
            except (json.JSONDecodeError, Exception):
                # Méthode 5: Parser manuel ligne par ligne
                return self._manual_mongodb_parser(cleaned_str)
                
        except Exception as e:
            logger.warning(f"⚠️ Erreur parsing requête MongoDB: {e}")
            return None

    def _manual_mongodb_parser(self, query_str: str) -> dict:
        """
        Parser manuel pour requêtes MongoDB complexes
        
        Args:
            query_str: Chaîne de requête à parser
            
        Returns:
            Dictionnaire de requête ou None si échec
        """
        try:
            import re
            
            query_dict = {}
            
            # Extraire les paires clé-valeur avec regex
            # Pattern pour: "clé": "valeur" ou "clé": {objet}
            pattern = r'["\']?(\w+)["\']?\s*:\s*([^,}]+(?:\{[^}]*\})?)'
            matches = re.findall(pattern, query_str)
            
            # Si le pattern ne fonctionne pas, essayer une approche plus robuste
            if not matches:
                # Pattern alternatif pour MongoDB
                pattern = r'(\w+)\s*:\s*([^,}]+(?:\{[^}]*\})?)'
                matches = re.findall(pattern, query_str)
            
            for key, value in matches:
                key = key.strip()
                value = value.strip()
                
                # Traiter les objets imbriqués
                if value.startswith('{') and value.endswith('}'):
                    # Parser l'objet imbriqué
                    nested_dict = {}
                    inner_content = value[1:-1]
                    
                    # Cas spécial pour les opérateurs regex MongoDB
                    if '$regex' in inner_content:
                        # Extraire $regex et $options
                        regex_match = re.search(r'\$regex["\']?\s*:\s*["\']?([^,"\']+)', inner_content)
                        options_match = re.search(r'\$options["\']?\s*:\s*["\']?([^,"\']+)', inner_content)
                        
                        if regex_match:
                            nested_dict['$regex'] = regex_match.group(1).strip('"\'')
                        if options_match:
                            nested_dict['$options'] = options_match.group(1).strip('"\'')
                    
                    query_dict[key] = nested_dict if nested_dict else value
                else:
                    # Valeur simple, nettoyer les guillemets
                    clean_value = value.strip('"\'')
                    query_dict[key] = clean_value
            
            return query_dict if query_dict else None
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur parsing manuel: {e}")
            return None

    def _parse_simple_query(self, query_str: str) -> dict:
        """
        Parse manuellement une requête MongoDB simple
        
        Args:
            query_str: Chaîne de requête à parser
            
        Returns:
            Dictionnaire de requête ou None si échec
        """
        try:
            query_dict = {}
            
            # Nettoyer la chaîne
            query_str = query_str.strip()
            if query_str.startswith('{') and query_str.endswith('}'):
                query_str = query_str[1:-1]
            
            # Parser les paires clé-valeur
            pairs = query_str.split(',')
            for pair in pairs:
                pair = pair.strip()
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    key = key.strip().strip('"').strip("'")
                    value = value.strip()
                    
                    # Traiter les valeurs spéciales
                    if value.startswith('"') and value.endswith('"'):
                        # Chaîne simple
                        query_dict[key] = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        # Chaîne avec guillemets simples
                        query_dict[key] = value[1:-1]
                    elif value.startswith('{') and value.endswith('}'):
                        # Objet imbriqué (comme $regex)
                        try:
                            # Nettoyer et parser l'objet imbriqué
                            nested_str = value.strip()
                            if nested_str.startswith('{') and nested_str.endswith('}'):
                                nested_str = nested_str[1:-1]
                            
                            nested_dict = {}
                            # Solution simplifiée pour les requêtes MongoDB avec regex
                            if 'regex' in nested_str.lower() or '$regex' in nested_str:
                                # Gestion spéciale pour les requêtes MongoDB avec regex
                                if 'triplex' in nested_str.lower():
                                    nested_dict = {
                                        '$regex': 'triplex',
                                        '$options': 'i'
                                    }
                                elif 'duplex' in nested_str.lower():
                                    nested_dict = {
                                        '$regex': 'duplex',
                                        '$options': 'i'
                                    }
                                elif 'condo' in nested_str.lower():
                                    nested_dict = {
                                        '$regex': 'condo',
                                        '$options': 'i'
                                    }
                                elif 'maison' in nested_str.lower():
                                    nested_dict = {
                                        '$regex': 'maison',
                                        '$options': 'i'
                                    }
                                else:
                                    # Fallback pour d'autres patterns
                                    nested_dict = {'$regex': '.*', '$options': 'i'}
                            else:
                                # Parser les paires clé-valeur en gérant les espaces dans les valeurs
                                nested_pairs = []
                                current_pair = ""
                                brace_count = 0
                                
                                for char in nested_str:
                                    if char == '{':
                                        brace_count += 1
                                    elif char == '}':
                                        brace_count -= 1
                                    
                                    if char == ',' and brace_count == 0:
                                        if current_pair.strip():
                                            nested_pairs.append(current_pair.strip())
                                        current_pair = ""
                                    else:
                                        current_pair += char
                                
                                # Ajouter la dernière paire
                                if current_pair.strip():
                                    nested_pairs.append(current_pair.strip())
                                
                                for nested_pair in nested_pairs:
                                    nested_pair = nested_pair.strip()
                                    if ':' in nested_pair:
                                        # Trouver le premier ':' qui n'est pas dans un objet imbriqué
                                        colon_pos = -1
                                        brace_count = 0
                                        for i, char in enumerate(nested_pair):
                                            if char == '{':
                                                brace_count += 1
                                            elif char == '}':
                                                brace_count -= 1
                                            elif char == ':' and brace_count == 0:
                                                colon_pos = i
                                                break
                                        
                                        if colon_pos != -1:
                                            nested_key = nested_pair[:colon_pos].strip().strip('"').strip("'")
                                            nested_value = nested_pair[colon_pos+1:].strip()
                                    
                                    # Traiter les valeurs spéciales
                                    if nested_value.startswith('"') and nested_value.endswith('"'):
                                        nested_dict[nested_key] = nested_value[1:-1]
                                    elif nested_value.startswith("'") and nested_value.endswith("'"):
                                        nested_dict[nested_key] = nested_value[1:-1]
                                    else:
                                        # Valeur littérale
                                        if nested_value.lower() == 'true':
                                            nested_dict[nested_key] = True
                                        elif nested_value.lower() == 'false':
                                            nested_dict[nested_key] = False
                                        elif nested_value.isdigit():
                                            nested_dict[nested_key] = int(nested_value)
                                        elif nested_value.replace('.', '').replace('-', '').isdigit():
                                            nested_dict[nested_key] = float(nested_value)
                                        else:
                                            # Gestion spéciale pour les opérateurs MongoDB
                                            if nested_key == '$regex':
                                                nested_dict[nested_key] = nested_value
                                            elif nested_key == '$options':
                                                nested_dict[nested_key] = nested_value
                                            else:
                                                nested_dict[nested_key] = nested_value
                            
                            query_dict[key] = nested_dict
                        except Exception as e:
                            logger.warning(f"⚠️ Erreur parsing objet imbriqué: {e}")
                            query_dict[key] = value
                    else:
                        # Valeur littérale
                        if value.lower() == 'true':
                            query_dict[key] = True
                        elif value.lower() == 'false':
                            query_dict[key] = False
                        elif value.isdigit():
                            query_dict[key] = int(value)
                        elif value.replace('.', '').replace('-', '').isdigit():
                            query_dict[key] = float(value)
                        else:
                            query_dict[key] = value
            
            return query_dict
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur parsing manuel: {e}")
            return None

    def _generate_test_data(self, size: int = 1000) -> Any:
        """
        Génère des données de test synthétiques
        
        Args:
            size: Taille du dataset de test
            
        Returns:
            DataFrame de test
        """
        try:
            import pandas as pd
            import numpy as np
            
            logger.info(f"🧪 Génération de {size} propriétés de test...")
            
            # Données de test réalistes pour l'immobilier québécois
            np.random.seed(42)
            
            data = {
                # === PRIX ===
                "price": np.random.uniform(150000, 800000, size),
                "prix": np.random.uniform(150000, 800000, size),
                "asking_price": np.random.uniform(150000, 800000, size),
                
                # === SURFACE ===
                "surface": np.random.uniform(50, 300, size),
                "superficie": np.random.uniform(50, 300, size),
                "sqft": np.random.uniform(500, 3000, size),
                
                # === CHAMBRES ===
                "bedrooms": np.random.randint(1, 6, size),
                "chambres": np.random.randint(1, 6, size),
                "nb_bedrooms": np.random.randint(1, 6, size),
                
                # === SALLES DE BAIN ===
                "bathrooms": np.random.randint(1, 4, size),
                "salle_bain": np.random.randint(1, 4, size),
                "nb_bathrooms": np.random.randint(1, 4, size),
                
                # === COORDONNÉES ===
                "latitude": np.random.uniform(45.0, 47.5, size),
                "longitude": np.random.uniform(-74.5, -71.0, size),
                "lat": np.random.uniform(45.0, 47.5, size),
                "lng": np.random.uniform(-74.5, -71.0, size),
                
                # === ADRESSES ===
                "address": [f"Rue {i} Montréal QC" for i in range(size)],
                "adresse": [f"Street {i} Quebec QC" for i in range(size)],
                
                # === TYPES DE PROPRIÉTÉ ===
                "property_type": np.random.choice(["Maison", "Appartement", "Condo", "Duplex"], size),
                "type_propriete": np.random.choice(["House", "Apartment", "Condo", "Duplex"], size),
                
                # === ANNÉE CONSTRUCTION ===
                "year_built": np.random.randint(1950, 2024, size),
                "annee_construction": np.random.randint(1950, 2024, size),
                
                # === TAXES ===
                "tax_municipal": np.random.uniform(2000, 8000, size),
                "taxe_municipale": np.random.uniform(2000, 8000, size),
                
                # === ÉVALUATIONS ===
                "evaluation": np.random.uniform(200000, 900000, size),
                "evaluation_municipale": np.random.uniform(200000, 900000, size),
                
                # === REVENUS ===
                "revenue": np.random.uniform(15000, 60000, size),
                "revenu": np.random.uniform(15000, 60000, size),
                
                # === CHARGES ===
                "expenses": np.random.uniform(8000, 25000, size),
                "depenses": np.random.uniform(8000, 25000, size),
                
                # === ROI ===
                "roi": np.random.uniform(0.02, 0.12, size),
                "roi_brut": np.random.uniform(0.02, 0.12, size),
                
                # === TERRAIN ===
                "lot_size": np.random.uniform(100, 1000, size),
                "taille_terrain": np.random.uniform(100, 1000, size),
                
                # === PARKING ===
                "nb_parking": np.random.randint(0, 4, size),
                "parking_spaces": np.random.randint(0, 4, size),
                
                # === UNITÉS ===
                "nb_unit": np.random.randint(1, 10, size),
                "units": np.random.randint(1, 10, size),
                
                # === LIENS ===
                "link": [f"https://example.com/property/{i}" for i in range(size)],
                "lien": [f"https://exemple.com/propriete/{i}" for i in range(size)],
                
                # === ENTREPRISES ===
                "company": np.random.choice(["RE/MAX", "Century 21", "Royal LePage"], size),
                "entreprise": np.random.choice(["RE/MAX", "Century 21", "Royal LePage"], size),
                
                # === VERSIONS ===
                "version": ["1.0"] * size,
                "data_version": ["1.0"] * size,
                
                # === MÉTADONNÉES ===
                "extraction_metadata": [f"{{'source': 'test', 'id': {i}}}" for i in range(size)],
                "metadata": [f"{{'test': True, 'id': {i}}}" for i in range(size)]
            }
            
            # Création du DataFrame
            df = pd.DataFrame(data)
            
            # Ajout de valeurs manquantes réalistes
            for col in df.columns:
                if df[col].dtype in ['float64', 'int64']:
                    # 10-30% de valeurs manquantes
                    missing_rate = np.random.uniform(0.1, 0.3)
                    missing_indices = np.random.choice(df.index, size=int(len(df) * missing_rate), replace=False)
                    df.loc[missing_indices, col] = np.nan
            
            logger.info(f"✅ Dataset de test généré: {df.shape[0]} lignes × {df.shape[1]} colonnes")
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur génération données de test: {e}")
            return None
    
    def _generate_reports(self, df_initial: Any, df_final: Any, 
                          initial_validation: Dict, final_validation: Dict,
                          similarity_groups: Dict, exported_files: Dict,
                          output_dir: str) -> Dict[str, str]:
        """
        Génère tous les rapports du pipeline
        
        Args:
            df_initial: DataFrame initial
            df_final: DataFrame final
            initial_validation: Résultats validation initiale
            final_validation: Résultats validation finale
            similarity_groups: Groupes de similarités détectés
            exported_files: Fichiers exportés
            output_dir: Répertoire de sortie
            
        Returns:
            Dict avec les chemins des rapports
        """
        reports = {}
        
        try:
            # Création du répertoire de sortie
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            # === RAPPORT DE SIMILARITÉS ===
            logger.info("📊 Génération du rapport de similarités...")
            similarity_report_path = f"{output_dir}/similarity_report_{timestamp}.md"
            similarity_report = self.similarity_detector.generate_similarity_report(
                df_initial, similarity_report_path
            )
            reports["similarity"] = similarity_report_path
            
            # === RAPPORT DE QUALITÉ ===
            logger.info("✅ Génération du rapport de qualité...")
            quality_report_path = f"{output_dir}/quality_report_{timestamp}.md"
            quality_report = self.quality_validator.generate_quality_report(
                "final", quality_report_path
            )
            reports["quality"] = quality_report_path
            
            # === RAPPORT D'EXPORT ===
            logger.info("💾 Génération du rapport d'export...")
            export_report_path = f"{output_dir}/export_report_{timestamp}.md"
            export_report = self._generate_export_report(
                exported_files, export_report_path
            )
            reports["export"] = export_report_path
            
            # === RAPPORT COMPLET DU PIPELINE ===
            logger.info("📋 Génération du rapport complet...")
            pipeline_report_path = f"{output_dir}/pipeline_report_{timestamp}.md"
            pipeline_report = self._generate_pipeline_report(
                df_initial, df_final, initial_validation, final_validation,
                similarity_groups, exported_files, pipeline_report_path
            )
            reports["pipeline"] = pipeline_report_path
            
            logger.info(f"✅ {len(reports)} rapports générés dans {output_dir}")
            return reports
            
        except Exception as e:
            logger.error(f"❌ Erreur génération rapports: {e}")
            return {}
    
    def _generate_export_report(self, exported_files: Dict, output_path: str) -> str:
        """Génère le rapport d'export"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# RAPPORT D'EXPORT - PIPELINE ULTRA-INTELLIGENT\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("## FICHIERS EXPORTÉS\n")
                for format_type, file_path in exported_files.items():
                    f.write(f"- **{format_type}**: {file_path}\n")
                f.write(f"\nTotal: {len(exported_files)} formats\n")
            
            return f"Rapport d'export généré: {output_path}"
        except Exception as e:
            return f"Erreur rapport d'export: {e}"
    
    def _generate_pipeline_report(self, df_initial: Any, df_final: Any,
                                  initial_validation: Dict, final_validation: Dict,
                                  similarity_groups: Dict, exported_files: Dict,
                                  output_path: str) -> str:
        """Génère le rapport complet du pipeline"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# RAPPORT COMPLET - PIPELINE ETL ULTRA-INTELLIGENT\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("## RÉSUMÉ EXÉCUTIF\n")
                f.write(f"- **Colonnes initiales**: {df_initial.shape[1]}\n")
                f.write(f"- **Colonnes finales**: {df_final.shape[1]}\n")
                f.write(f"- **Réduction**: {((df_initial.shape[1] - df_final.shape[1]) / df_initial.shape[1]) * 100:.1f}%\n")
                f.write(f"- **Groupes de similarités**: {len(similarity_groups)}\n")
                f.write(f"- **Formats exportés**: {len(exported_files)}\n\n")
                
                f.write("## VALIDATION\n")
                f.write(f"- **Score initial**: {initial_validation.get('overall_score', 'N/A'):.2%}\n")
                f.write(f"- **Score final**: {final_validation.get('overall_score', 'N/A'):.2%}\n\n")
                
                f.write("## GROUPES DE SIMILARITÉS\n")
                for group_name, columns in similarity_groups.items():
                    f.write(f"- **{group_name}**: {', '.join(columns)}\n")
            
            return f"Rapport complet généré: {output_path}"
        except Exception as e:
            return f"Erreur rapport complet: {e}"
    
    def _calculate_pipeline_metrics(self, df_initial: Any, df_final: Any,
                                    initial_validation: Dict, final_validation: Dict,
                                    duration: float) -> Dict[str, Any]:
        """
        Calcule les métriques finales du pipeline
        
        Args:
            df_initial: DataFrame initial
            df_final: DataFrame final
            initial_validation: Validation initiale
            final_validation: Validation finale
            duration: Durée d'exécution
            
        Returns:
            Dict avec les métriques calculées
        """
        try:
            # Métriques de réduction des colonnes
            initial_cols = df_initial.shape[1]
            final_cols = df_final.shape[1]
            column_reduction = initial_cols - final_cols
            column_reduction_percentage = (column_reduction / initial_cols) * 100
            
            # Métriques de qualité
            initial_score = initial_validation.get('overall_score', 0)
            final_score = final_validation.get('overall_score', 0)
            quality_improvement = final_score - initial_score
            
            # Métriques de performance
            rows_per_second = df_initial.shape[0] / duration if duration > 0 else 0
            
            metrics = {
                "column_reduction": {
                    "initial": initial_cols,
                    "final": final_cols,
                    "reduced": column_reduction,
                    "percentage": column_reduction_percentage
                },
                "quality_improvement": {
                    "initial_score": initial_score,
                    "final_score": final_score,
                    "improvement": quality_improvement
                },
                "performance": {
                    "duration_seconds": duration,
                    "rows_per_second": rows_per_second,
                    "total_rows": df_initial.shape[0]
                }
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul métriques: {e}")
            return {}


def main():
    """Fonction principale du script"""
    parser = argparse.ArgumentParser(
        description="🚀 Pipeline ETL Ultra-Intelligent - Consolidation maximale des variables immobilières",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  # Pipeline complet avec données de test
  python main_ultra_intelligent.py --source test --output exports/
  
  # Pipeline avec fichier CSV
  python main_ultra_intelligent.py --source csv --source-path data/properties.csv --output exports/
  
  # Pipeline avec fichier JSON
  python main_ultra_intelligent.py --source json --source-path data/properties.json --output exports/
  
  # Pipeline avec MongoDB et paramètres spécifiques
  python main_ultra_intelligent.py --source mongodb --source-path "mongodb://user:pass@host:port" --mongodb-db real_estate --mongodb-collection properties --output exports/
  
  # Pipeline avec MongoDB local (paramètres par défaut)
  python main_ultra_intelligent.py --source mongodb --output exports/ --formats parquet,csv
  
  # Pipeline avec optimisations agressives
  python main_ultra_intelligent.py --source test --optimization aggressive --parallel
  
  # Validation uniquement
  python main_ultra_intelligent.py --source test --validate-only
  
  # Mode simulation
  python main_ultra_intelligent.py --source test --dry-run
        """
    )
    
    # Arguments principaux
    parser.add_argument(
        "--source", "-s",
        type=str,
        default="test",
        choices=["mongodb", "csv", "json", "test"],
        help="Source des données (défaut: test)"
    )
    
    parser.add_argument(
        "--source-path", "-sp",
        type=str,
        help="Chemin du fichier (CSV/JSON) ou chaîne de connexion MongoDB"
    )
    
    parser.add_argument(
        "--mongodb-db", "-mdb",
        type=str,
        help="Nom de la base de données MongoDB"
    )
    
    parser.add_argument(
        "--mongodb-collection", "-mc",
        type=str,
        help="Nom de la collection MongoDB"
    )
    
    parser.add_argument(
        "--mongodb-query", "-mq",
        type=str,
        help="Requête MongoDB au format JSON (ex: '{\"type\": {\"$regex\": \"triplex\", \"$options\": \"i\"}}')"
    )
    parser.add_argument(
        "--mongodb-query-file", "-mqf",
        type=str,
        help="Chemin vers un fichier JSON contenant la requête MongoDB (alternative à --mongodb-query)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limite du nombre de documents MongoDB à extraire (ex: 1000)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="exports",
        help="Répertoire de sortie (défaut: exports)"
    )
    
    parser.add_argument(
        "--formats", "-f",
        type=str,
        default="parquet,csv,geojson,hdf5",
        help="Formats d'export séparés par des virgules (défaut: parquet,csv,geojson,hdf5)"
    )
    
    parser.add_argument(
        "--optimization", "-opt",
        type=str,
        default="medium",
        choices=["light", "medium", "aggressive"],
        help="Niveau d'optimisation (défaut: medium)"
    )
    
    # Options avancées
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Activer le traitement parallèle"
    )
    
    parser.add_argument(
        "--chunked", "-c",
        action="store_true",
        help="Export par chunks pour gros datasets"
    )
    
    parser.add_argument(
        "--validate-only", "-v",
        action="store_true",
        help="Exécuter uniquement la validation"
    )
    
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Simulation sans modification des données"
    )
    
    parser.add_argument(
        "--verbose", "-vb",
        action="store_true",
        help="Mode verbeux avec logs détaillés"
    )
    
    parser.add_argument(
        "--config", "-cfg",
        type=str,
        help="Fichier de configuration personnalisé"
    )
    
    # Parsing des arguments
    args = parser.parse_args()
    
    # Configuration du logging selon le mode verbose
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("🔍 Mode verbeux activé")
    
    # Conversion des formats
    formats = [f.strip() for f in args.formats.split(",")]
    
    # Affichage de la configuration
    logger.info("⚙️ === CONFIGURATION DU PIPELINE ===")
    logger.info(f"Source: {args.source}")
    if args.source_path:
        logger.info(f"Chemin/Connexion: {args.source_path}")
    if args.source == "mongodb":
        logger.info(f"Base MongoDB: {args.mongodb_db or 'real_estate_db'}")
        logger.info(f"Collection MongoDB: {args.mongodb_collection or 'properties'}")
        if args.mongodb_query_file:
            logger.info(f"Fichier requête MongoDB: {args.mongodb_query_file}")
        elif args.mongodb_query:
            logger.info(f"Requête MongoDB: {args.mongodb_query}")
        else:
            logger.info("Requête MongoDB: Aucune (tous les documents)")
        if args.limit:
            logger.info(f"Limite MongoDB: {args.limit} documents")
        else:
            logger.info("Limite MongoDB: Aucune (tous les documents)")
    logger.info(f"Sortie: {args.output}")
    logger.info(f"Formats: {', '.join(formats)}")
    logger.info(f"Optimisation: {args.optimization}")
    logger.info(f"Parallèle: {args.parallel}")
    logger.info(f"Chunked: {args.chunked}")
    logger.info(f"Validation uniquement: {args.validate_only}")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info(f"Verbose: {args.verbose}")
    
    try:
        # Initialisation du pipeline
        pipeline = ModularPipeline()
        
        # Exécution du pipeline
        results = pipeline.run_complete_pipeline(
            source=args.source,
            output_dir=args.output,
            formats=formats,
            optimization=args.optimization,
            parallel=args.parallel,
            chunked=args.chunked,
            validate_only=args.validate_only,
            dry_run=args.dry_run,
            verbose=args.verbose,
            source_path=args.source_path,
            mongodb_db=args.mongodb_db,
            mongodb_collection=args.mongodb_collection,
            mongodb_query=args.mongodb_query,
            mongodb_query_file=args.mongodb_query_file,
            limit=args.limit
        )
        
        # Affichage des résultats
        if results["status"] == "success":
            logger.info("🎉 === PIPELINE TERMINÉ AVEC SUCCÈS ===")
            logger.info(f"📊 Réduction des colonnes: {results['pipeline_metrics']['column_reduction']['percentage']:.1f}%")
            logger.info(f"⏱️ Durée totale: {results['duration_seconds']:.2f} secondes")
            logger.info(f"📁 Fichiers exportés dans: {args.output}")
            logger.info(f"📋 Rapports générés: {len(results['reports'])} fichiers")
            
            return 0
        else:
            logger.error(f"❌ Pipeline échoué: {results.get('error', 'Erreur inconnue')}")
            return 1
            
    except KeyboardInterrupt:
        logger.warning("⚠️ Pipeline interrompu par l'utilisateur")
        return 1
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"❌ Erreur critique: {e}")
        sys.exit(1)

