"""
Pipeline principal d'extraction web immobilière
Système d'exécution autonome sans dépendances externes
"""

import asyncio
import argparse
import sys
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import signal

from config.settings import config
from src.models.property import Property, PropertySummary, SearchQuery, PropertyType
from src.extractors.centris_extractor import CentrisExtractor
from src.services.database_service import DatabaseService
from src.utils.logging import setup_logging, LogContext, get_logger


class PipelineExecutor:
    """Exécuteur de pipeline autonome avec gestion des paramètres"""
    
    def __init__(self, args):
        self.args = args
        self.logger = get_logger()
        self.db_service = None
        self.running = True
        
        # Configuration des signaux pour arrêt propre
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Gestionnaire de signaux pour arrêt propre"""
        self.logger.info(f"📡 Signal reçu: {signum}, arrêt en cours...")
        self.running = False
    
    async def setup_database(self) -> DatabaseService:
        """Configure et initialise la base de données"""
        self.logger.info("🔧 Configuration de la base de données...")
        
        try:
            # Application des paramètres de ligne de commande
            db_config = config.database.copy()
            
            if self.args.database_name:
                db_config.database_name = self.args.database_name
                self.logger.info(f"📊 Utilisation de la base de données: {db_config.database_name}")
            
            if self.args.table_name:
                # Remplace la configuration par défaut
                db_config.properties_collection = self.args.table_name
                db_config.summaries_collection = f"{self.args.table_name}_summaries"
                db_config.logs_collection = f"{self.args.table_name}_logs"
                self.logger.info(f"📋 Utilisation de la collection: {self.args.table_name}")
            
            db_service = DatabaseService(db_config)
            db_service.connect()
            
            # Les noms des collections sont maintenant configurés automatiquement
            # via la configuration, mais on peut encore les surcharger si nécessaire
            if self.args.table_name:
                db_service.set_collection_names(
                    properties_collection=self.args.table_name,
                    summaries_collection=f"{self.args.table_name}_summaries",
                    logs_collection=f"{self.args.table_name}_logs"
                )
            
            db_service.ensure_indexes()
            self.logger.info("✅ Base de données configurée avec succès")
            return db_service
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la configuration de la base de données: {str(e)}")
            raise
    
    async def extract_property_summaries(
        self,
        location: str,
        property_type: PropertyType,
        extractor: CentrisExtractor
    ) -> List[PropertySummary]:
        """Extrait les résumés de propriétés pour une localisation et un type donnés"""
        self.logger.info(f"🔍 Extraction des résumés pour {location} - {property_type}")
        
        try:
            # Création de la requête de recherche
            search_query = SearchQuery(
                locations=[location],
                property_types=[property_type],
                price_min=config.centris.sale_price_min,
                price_max=config.centris.sale_price_max
            )
            
            # Extraction des résumés
            summaries = await extractor.extract_summaries(search_query)
            self.logger.info(f"✅ {len(summaries)} résumés extraits pour {location} - {property_type}")
            
            return summaries
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'extraction des résumés: {str(e)}")
            raise
    
    async def extract_property_details(
        self,
        property_summary: PropertySummary,
        extractor: CentrisExtractor
    ) -> Optional[Property]:
        """Extrait les détails complets d'une propriété"""
        self.logger.debug(f"🔍 Extraction des détails pour {property_summary.id}")
        
        try:
            if not property_summary.url:
                self.logger.warning(f"⚠️ Pas d'URL pour la propriété {property_summary.id}")
                return None
            
            property_details = await extractor.extract_details(property_summary.url)
            
            if property_details:
                self.logger.debug(f"✅ Détails extraits pour {property_summary.id}")
                return property_details
            else:
                self.logger.warning(f"⚠️ Aucun détail extrait pour {property_summary.id}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'extraction des détails pour {property_summary.id}: {str(e)}")
            return None
    
    async def save_property(
        self,
        property_data: Property,
        db_service: DatabaseService
    ) -> bool:
        """Sauvegarde une propriété dans la base de données"""
        try:
            success = db_service.save_property(property_data)
            if success:
                self.logger.debug(f"💾 Propriété {property_data.id} sauvegardée avec succès")
            else:
                self.logger.warning(f"⚠️ Échec de la sauvegarde pour {property_data.id}")
            return success
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la sauvegarde de {property_data.id}: {str(e)}")
            return False
    
    async def process_location_property_type(
        self,
        location: str,
        property_type: PropertyType,
        db_service: DatabaseService
    ) -> Dict[str, Any]:
        """Traite une combinaison localisation/type de propriété complète"""
        self.logger.info(f"🚀 Début du traitement pour {location} - {property_type}")
        
        start_time = datetime.now()
        
        try:
            # Initialisation de l'extracteur
            extractor = CentrisExtractor(config.centris)
            
            # Extraction des résumés
            summaries = await self.extract_property_summaries(location, property_type, extractor)
            
            if not summaries:
                self.logger.info(f"ℹ️ Aucune propriété trouvée pour {location} - {property_type}")
                return {
                    "location": location,
                    "property_type": property_type,
                    "summaries_count": 0,
                    "details_count": 0,
                    "success_count": 0,
                    "duration": datetime.now() - start_time
                }
            
            # Extraction des détails en parallèle
            self.logger.info(f"🔍 Extraction des détails pour {len(summaries)} propriétés...")
            
            # Traitement par lots pour éviter la surcharge
            batch_size = config.batch_size
            total_details = 0
            total_success = 0
            
            for i in range(0, len(summaries), batch_size):
                if not self.running:
                    self.logger.info("⚠️ Arrêt demandé, traitement interrompu")
                    break
                
                batch = summaries[i:i + batch_size]
                self.logger.info(f"📦 Traitement du lot {i//batch_size + 1}/{(len(summaries) + batch_size - 1)//batch_size}")
                
                # Extraction des détails pour ce lot
                detail_tasks = []
                for summary in batch:
                    task = asyncio.create_task(
                        self.extract_property_details(summary, extractor)
                    )
                    detail_tasks.append(task)
                
                # Attendre la completion de tous les détails du lot
                batch_details = []
                for task in asyncio.as_completed(detail_tasks):
                    if not self.running:
                        break
                    result = await task
                    if result:
                        batch_details.append(result)
                
                total_details += len(batch_details)
                
                # Sauvegarde des propriétés du lot
                save_tasks = []
                for property_data in batch_details:
                    task = asyncio.create_task(
                        self.save_property(property_data, db_service)
                    )
                    save_tasks.append(task)
                
                # Compter les succès
                batch_successes = []
                for task in asyncio.as_completed(save_tasks):
                    if not self.running:
                        break
                    result = await task
                    batch_successes.append(result)
                
                total_success += sum(batch_successes)
                
                # Pause entre les lots pour éviter la surcharge
                if i + batch_size < len(summaries) and self.running:
                    self.logger.info("⏳ Pause entre les lots...")
                    await asyncio.sleep(2)
            
            duration = datetime.now() - start_time
            
            self.logger.info(f"✅ Traitement terminé pour {location} - {property_type}")
            self.logger.info(f"📊 Résultats: {len(summaries)} résumés, {total_details} détails, {total_success} sauvegardés")
            self.logger.info(f"⏱️ Durée: {duration}")
            
            return {
                "location": location,
                "property_type": property_type,
                "summaries_count": len(summaries),
                "details_count": total_details,
                "success_count": total_success,
                "duration": duration
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du traitement de {location} - {property_type}: {str(e)}")
            raise
    
    async def run_pipeline(self) -> Dict[str, Any]:
        """Exécute le pipeline principal d'extraction immobilière"""
        self.logger.info("🚀 Démarrage du pipeline d'extraction immobilière")
        
        start_time = datetime.now()
        
        try:
            # Configuration de la base de données
            self.db_service = await self.setup_database()
            
            # Filtrage des localisations et types selon les paramètres
            locations_to_process = self._filter_locations()
            property_types_to_process = self._filter_property_types()
            
            self.logger.info(f"🎯 Traitement de {len(locations_to_process)} localisations et {len(property_types_to_process)} types de propriétés")
            
            # Traitement de toutes les combinaisons localisation/type
            results = []
            
            for location_config in locations_to_process:
                location_name = location_config.value
                
                for property_type_str in property_types_to_process:
                    if not self.running:
                        break
                    
                    try:
                        property_type = PropertyType(property_type_str)
                        
                        self.logger.info(f"🎯 Traitement de {location_name} - {property_type}")
                        
                        result = await self.process_location_property_type(
                            location_name,
                            property_type,
                            self.db_service
                        )
                        results.append(result)
                        
                    except ValueError as e:
                        self.logger.error(f"❌ Type de propriété invalide: {property_type_str}")
                        continue
                    except Exception as e:
                        self.logger.error(f"❌ Erreur lors du traitement de {location_name} - {property_type_str}: {str(e)}")
                        continue
                
                if not self.running:
                    break
            
            # Résumé final
            total_summaries = sum(r["summaries_count"] for r in results)
            total_details = sum(r["details_count"] for r in results)
            total_success = sum(r["success_count"] for r in results)
            total_duration = datetime.now() - start_time
            
            if self.running:
                self.logger.info("🎉 Pipeline terminé avec succès!")
            else:
                self.logger.info("⚠️ Pipeline interrompu par l'utilisateur")
            
            self.logger.info(f"📊 Résumé global:")
            self.logger.info(f"   - Résumés extraits: {total_summaries}")
            self.logger.info(f"   - Détails extraits: {total_details}")
            self.logger.info(f"   - Propriétés sauvegardées: {total_success}")
            self.logger.info(f"   - Durée totale: {total_duration}")
            
            return {
                "success": self.running,
                "interrupted": not self.running,
                "results": results,
                "summary": {
                    "total_summaries": total_summaries,
                    "total_details": total_details,
                    "total_success": total_success,
                    "total_duration": total_duration
                }
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur fatale dans le pipeline: {str(e)}")
            raise
        finally:
            # Fermeture de la connexion à la base de données
            if self.db_service:
                self.db_service.close()
    
    def _filter_locations(self) -> List:
        """Filtre les localisations selon les paramètres de ligne de commande"""
        all_locations = config.centris.locations_searched
        
        if self.args.location:
            # Filtrer par nom de localisation
            filtered = [loc for loc in all_locations if loc.value.lower() in self.args.location.lower()]
            if not filtered:
                self.logger.warning(f"⚠️ Aucune localisation trouvée pour '{self.args.location}'")
                return []
            return filtered
        
        if self.args.region:
            # Filtrer par région
            filtered = [loc for loc in all_locations if loc.region.lower() in self.args.region.lower()]
            if not filtered:
                self.logger.warning(f"⚠️ Aucune localisation trouvée pour la région '{self.args.region}'")
                return []
            return filtered
        
        # Retourner toutes les localisations si aucun filtre
        return all_locations
    
    def _filter_property_types(self) -> List[str]:
        """Filtre les types de propriétés selon les paramètres de ligne de commande"""
        all_types = config.centris.property_types
        
        if self.args.property_type:
            # Filtrer par type de propriété
            filtered = [pt for pt in all_types if pt.lower() in self.args.property_type.lower()]
            if not filtered:
                self.logger.warning(f"⚠️ Aucun type de propriété trouvé pour '{self.args.property_type}'")
                return []
            return filtered
        
        # Retourner tous les types si aucun filtre
        return all_types


def parse_arguments():
    """Parse les arguments de ligne de commande"""
    parser = argparse.ArgumentParser(
        description="Pipeline d'extraction web immobilière",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  # Exécution complète
  python scripts/run_pipeline.py
  
  # Extraction pour une localisation spécifique
  python scripts/run_pipeline.py --location "Montréal"
  
  # Extraction pour un type de propriété spécifique
  python scripts/run_pipeline.py --property-type "Condo"
  
  # Extraction pour une région spécifique
  python scripts/run_pipeline.py --region "Québec"
  
  # Mode debug avec plus de logs
  python scripts/run_pipeline.py --debug
  
  # Limitation du nombre de propriétés
  python scripts/run_pipeline.py --max-properties 100
  
  # Spécification du nom de la table/collection
  python scripts/run_pipeline.py --table-name "properties_2024"
        """
    )
    
    # Filtres de localisation
    location_group = parser.add_mutually_exclusive_group()
    location_group.add_argument(
        '--location', '-l',
        type=str,
        help='Localisation spécifique à traiter (ex: "Montréal", "Laval")'
    )
    location_group.add_argument(
        '--region', '-r',
        type=str,
        help='Région spécifique à traiter (ex: "Québec", "Ontario")'
    )
    
    # Filtres de propriété
    parser.add_argument(
        '--property-type', '-t',
        type=str,
        help='Type de propriété spécifique à traiter (ex: "Condo", "House")'
    )
    
    # Options de base de données
    parser.add_argument(
        '--table-name', '-n',
        type=str,
        help='Nom de la table/collection MongoDB (ex: "properties_2024", "real_estate_data")'
    )
    parser.add_argument(
        '--database-name',
        type=str,
        help='Nom de la base de données MongoDB (ex: "real_estate_db", "property_data")'
    )
    
    # Options de performance
    parser.add_argument(
        '--max-properties',
        type=int,
        help='Nombre maximum de propriétés à traiter'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        help='Taille des lots de traitement'
    )
    
    # Options de debug
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Mode debug avec logs détaillés'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulation sans sauvegarde en base'
    )
    
    # Options de sortie
    parser.add_argument(
        '--output-format',
        choices=['json', 'csv', 'console'],
        default='console',
        help='Format de sortie des résultats'
    )
    parser.add_argument(
        '--output-file',
        type=str,
        help='Fichier de sortie pour les résultats'
    )
    
    return parser.parse_args()


async def main():
    """Fonction principale asynchrone"""
    # Parse des arguments
    args = parse_arguments()
    
    # Configuration du logging selon le mode debug
    log_level = "DEBUG" if args.debug else config.log_level
    setup_logging(
        log_level=log_level,
        log_file=config.log_file,
        log_format="json"
    )
    
    # Application des paramètres de ligne de commande
    if args.batch_size:
        config.batch_size = args.batch_size
    
    # Application des paramètres de base de données
    if args.database_name:
        config.database.database_name = args.database_name
    
    with LogContext("pipeline_execution", args=vars(args)):
        try:
            # Création et exécution du pipeline
            executor = PipelineExecutor(args)
            result = await executor.run_pipeline()
            
            # Affichage des résultats
            display_results(result, args)
            
            # Code de sortie approprié
            if result.get("success"):
                print("🎉 Pipeline exécuté avec succès!")
                sys.exit(0)
            elif result.get("interrupted"):
                print("⚠️ Pipeline interrompu par l'utilisateur")
                sys.exit(130)
            else:
                print("❌ Pipeline échoué")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\n⚠️ Pipeline interrompu par l'utilisateur")
            sys.exit(130)
        except Exception as e:
            print(f"❌ Erreur fatale: {str(e)}")
            sys.exit(1)


def display_results(result: Dict[str, Any], args):
    """Affiche les résultats selon le format demandé"""
    if args.output_format == 'json':
        import json
        output = json.dumps(result, indent=2, default=str)
        
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"📄 Résultats sauvegardés dans {args.output_file}")
        else:
            print(output)
    
    elif args.output_format == 'csv':
        import csv
        output_file = args.output_file or 'pipeline_results.csv'
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Location', 'Property Type', 'Summaries', 'Details', 'Success', 'Duration'])
            
            for r in result.get('results', []):
                writer.writerow([
                    r['location'],
                    r['property_type'],
                    r['summaries_count'],
                    r['details_count'],
                    r['success_count'],
                    str(r['duration'])
                ])
        
        print(f"📄 Résultats sauvegardés dans {output_file}")
    
    else:  # console
        print("\n📊 Résultats du pipeline:")
        print("=" * 50)
        
        for r in result.get('results', []):
            print(f"📍 {r['location']} - {r['property_type']}")
            print(f"   📋 Résumés: {r['summaries_count']}")
            print(f"   🔍 Détails: {r['details_count']}")
            print(f"   💾 Sauvegardés: {r['success_count']}")
            print(f"   ⏱️ Durée: {r['duration']}")
            print("-" * 30)
        
        summary = result.get('summary', {})
        print(f"\n🎯 Résumé global:")
        print(f"   Total résumés: {summary.get('total_summaries', 0)}")
        print(f"   Total détails: {summary.get('total_details', 0)}")
        print(f"   Total sauvegardés: {summary.get('total_success', 0)}")
        print(f"   Durée totale: {summary.get('total_duration', 'N/A')}")


def run_sync():
    """Version synchrone pour compatibilité"""
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_sync()
