#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ GESTIONNAIRE DE CONFIGURATION
=================================

Gère la configuration et la validation des paramètres du pipeline
"""

import logging
import argparse
from typing import Dict, Any, Optional, List
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Gestionnaire de configuration pour le pipeline ETL
    
    Responsable de la validation et de la gestion
    des paramètres de configuration
    """
    
    def __init__(self):
        """Initialise le gestionnaire de configuration"""
        self.config = {}
        self.validated = False
    
    def parse_arguments(self, args: List[str] = None) -> Dict[str, Any]:
        """
        Parse les arguments de ligne de commande
        
        Args:
            args: Liste des arguments (optionnel)
            
        Returns:
            Dict avec la configuration parsée
        """
        parser = argparse.ArgumentParser(
            description="Pipeline ETL Modulaire pour la consolidation de données immobilières",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemples d'utilisation:
  # Test avec données simulées
  python main_modular_pipeline.py --source test --output exports/test --formats csv --limit 100
  
  # MongoDB avec requête personnalisée
  python main_modular_pipeline.py --source mongodb --mongodb-db real_estate_db \\
    --mongodb-collection properties --mongodb-query '{"city": "Montréal"}' \\
    --output exports/montreal --formats csv json --limit 500
  
  # MongoDB avec fichier de requête
  python main_modular_pipeline.py --source mongodb --mongodb-db real_estate_db \\
    --mongodb-collection properties --mongodb-query-file query.json \\
    --output exports/custom --formats csv --limit 1000
            """
        )
        
        # === SOURCE DE DONNÉES ===
        parser.add_argument(
            '--source', 
            choices=['mongodb', 'csv', 'json', 'test'],
            default='test',
            help='Source des données (défaut: test)'
        )
        
        parser.add_argument(
            '--source-path',
            help='Chemin du fichier (CSV/JSON) ou chaîne de connexion MongoDB'
        )
        
        # === CONFIGURATION MONGODB ===
        parser.add_argument(
            '--mongodb-db',
            help='Nom de la base de données MongoDB'
        )
        
        parser.add_argument(
            '--mongodb-collection',
            help='Nom de la collection MongoDB'
        )
        
        parser.add_argument(
            '--mongodb-query',
            help='Requête MongoDB au format JSON'
        )
        
        parser.add_argument(
            '--mongodb-query-file',
            help='Chemin vers un fichier JSON contenant la requête MongoDB'
        )
        
        parser.add_argument(
            '--limit',
            type=int,
            help='Limite du nombre de documents MongoDB à extraire'
        )
        
        # === CONFIGURATION DE SORTIE ===
        parser.add_argument(
            '--output',
            default='exports',
            help='Répertoire de sortie (défaut: exports)'
        )
        
        parser.add_argument(
            '--formats',
            nargs='+',
            choices=['csv', 'json', 'parquet', 'geojson', 'hdf5'],
            default=['csv'],
            help='Formats d\'export (défaut: csv)'
        )
        
        # === OPTIMISATION ET PERFORMANCE ===
        parser.add_argument(
            '--optimization',
            choices=['light', 'medium', 'aggressive'],
            default='medium',
            help='Niveau d\'optimisation (défaut: medium)'
        )
        
        parser.add_argument(
            '--parallel',
            action='store_true',
            help='Activer le traitement parallèle'
        )
        
        parser.add_argument(
            '--chunked',
            action='store_true',
            help='Export par chunks'
        )
        
        # === MODES SPÉCIAUX ===
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Exécuter uniquement la validation'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulation sans modification'
        )
        
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mode verbeux'
        )
        
        # === CONFIGURATION AVANCÉE ===
        parser.add_argument(
            '--config',
            help='Fichier de configuration JSON'
        )
        
        # Parse des arguments
        if args:
            parsed_args = parser.parse_args(args)
        else:
            parsed_args = parser.parse_args()
        
        # Conversion en dictionnaire
        config = vars(parsed_args)
        
        # Validation de la configuration
        if self._validate_config(config):
            self.config = config
            self.validated = True
            return config
        else:
            raise ValueError("Configuration invalide")
    
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Valide la configuration
        
        Args:
            config: Configuration à valider
            
        Returns:
            True si la configuration est valide
        """
        logger.info("⚙️ === CONFIGURATION DU PIPELINE ===")
        
        # === VALIDATION DE LA SOURCE ===
        source = config.get('source')
        logger.info(f"Source: {source}")
        
        if source == 'mongodb':
            # Validation des paramètres MongoDB
            if not config.get('mongodb_db'):
                logger.error("❌ Base de données MongoDB requise")
                return False
            
            if not config.get('mongodb_collection'):
                logger.error("❌ Collection MongoDB requise")
                return False
            
            logger.info(f"Base MongoDB: {config['mongodb_db']}")
            logger.info(f"Collection MongoDB: {config['mongodb_collection']}")
            
            # Vérification de la requête
            if config.get('mongodb_query_file'):
                query_file = Path(config['mongodb_query_file'])
                if not query_file.exists():
                    logger.error(f"❌ Fichier de requête non trouvé: {query_file}")
                    return False
                logger.info(f"Fichier requête MongoDB: {config['mongodb_query_file']}")
            elif config.get('mongodb_query'):
                logger.info(f"Requête MongoDB: {config['mongodb_query']}")
            else:
                logger.warning("⚠️ Aucune requête MongoDB spécifiée, extraction complète")
            
            if config.get('limit'):
                logger.info(f"Limite MongoDB: {config['limit']} documents")
        
        elif source in ['csv', 'json']:
            if not config.get('source_path'):
                logger.error(f"❌ Chemin source requis pour {source}")
                return False
            
            source_path = Path(config['source_path'])
            if not source_path.exists():
                logger.error(f"❌ Fichier source non trouvé: {source_path}")
                return False
            
            logger.info(f"Chemin source: {config['source_path']}")
        
        # === VALIDATION DE LA SORTIE ===
        output_dir = config.get('output', 'exports')
        logger.info(f"Sortie: {output_dir}")
        
        # Création du répertoire de sortie si nécessaire
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # === VALIDATION DES FORMATS ===
        formats = config.get('formats', ['csv'])
        logger.info(f"Formats: {', '.join(formats)}")
        
        # === VALIDATION DE L'OPTIMISATION ===
        optimization = config.get('optimization', 'medium')
        logger.info(f"Optimisation: {optimization}")
        
        # === VALIDATION DES MODES ===
        logger.info(f"Parallèle: {config.get('parallel', False)}")
        logger.info(f"Chunked: {config.get('chunked', False)}")
        logger.info(f"Validation uniquement: {config.get('validate_only', False)}")
        logger.info(f"Dry run: {config.get('dry_run', False)}")
        logger.info(f"Verbose: {config.get('verbose', False)}")
        
        logger.info("✅ Configuration validée avec succès")
        return True
    
    def get_config(self) -> Dict[str, Any]:
        """Retourne la configuration actuelle"""
        return self.config.copy()
    
    def is_validated(self) -> bool:
        """Vérifie si la configuration a été validée"""
        return self.validated
    
    def get_source_config(self) -> Dict[str, Any]:
        """Retourne la configuration de la source"""
        source = self.config.get('source')
        if source == 'mongodb':
            return {
                'source': source,
                'mongodb_db': self.config.get('mongodb_db'),
                'mongodb_collection': self.config.get('mongodb_collection'),
                'mongodb_query': self.config.get('mongodb_query'),
                'mongodb_query_file': self.config.get('mongodb_query_file'),
                'limit': self.config.get('limit')
            }
        elif source in ['csv', 'json']:
            return {
                'source': source,
                'source_path': self.config.get('source_path')
            }
        else:  # test
            return {
                'source': source
            }
    
    def get_output_config(self) -> Dict[str, Any]:
        """Retourne la configuration de sortie"""
        return {
            'output_dir': self.config.get('output', 'exports'),
            'formats': self.config.get('formats', ['csv']),
            'optimization': self.config.get('optimization', 'medium'),
            'parallel': self.config.get('parallel', False),
            'chunked': self.config.get('chunked', False)
        }
    
    def get_pipeline_config(self) -> Dict[str, Any]:
        """Retourne la configuration du pipeline"""
        return {
            'validate_only': self.config.get('validate_only', False),
            'dry_run': self.config.get('dry_run', False),
            'verbose': self.config.get('verbose', False)
        }
