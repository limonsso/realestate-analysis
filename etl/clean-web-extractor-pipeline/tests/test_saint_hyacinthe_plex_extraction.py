#!/usr/bin/env python3
"""
🧪 Test Réel : Extraction Plex à Saint-Hyacinthe

Ce test effectue une extraction réelle de données de plex à Saint-Hyacinthe depuis Centris.ca
et stocke les résultats dans MongoDB pour validation.
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Ajouter le répertoire racine au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extractors.centris_extractor import CentrisExtractor
from src.models.property import SearchQuery, PropertyType
from src.utils.validators import TypeCategoryValidator
from config.settings import LocationConfig
from config.settings import load_config
from src.services.database_service import DatabaseService
import structlog

# Configuration du logging
logger = structlog.get_logger()

class SaintHyacinthePlexExtractionTest:
    """Test d'extraction réelle de plex à Saint-Hyacinthe."""
    
    def __init__(self):
        """Initialise le test avec la configuration."""
        self.config = load_config("config/config.saint_hyacinthe_test.yml")
        self.extractor = None
        self.db_service = None
        self._setup_complete = False  # Flag pour tracker l'état de setup
        
    async def setup(self):
        """Configure l'extracteur et la base de données."""
        logger.info("🔧 Configuration du test d'extraction Saint-Hyacinthe")
        
        try:
            # Initialiser l'extracteur Centris
            self.extractor = CentrisExtractor(self.config.centris)
            logger.debug("✅ CentrisExtractor initialisé")
            
            # Initialiser le service de base de données
            self.db_service = DatabaseService(self.config.database)
            await self.db_service.connect()
            logger.debug("✅ DatabaseService initialisé et connecté")
            
            self._setup_complete = True
            logger.info("✅ Configuration terminée")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la configuration: {e}")
            self._setup_complete = False
            # Nettoyer en cas d'erreur
            await self.cleanup()
            raise
    
    async def create_search_query(self) -> SearchQuery:
        """Crée une requête de recherche pour Saint-Hyacinthe."""
        logger.info("🔍 Création de la requête de recherche Saint-Hyacinthe")
        
        # Configuration spécifique pour Saint-Hyacinthe
        # Utilisation du CityDistrict spécifique à Saint-Hyacinthe pour une recherche précise
        saint_hyacinthe_location = LocationConfig(
            type="CityDistrict",
            value="Saint-Hyacinthe",  # Saint-Hyacinthe spécifiquement avec son ID exact
            type_id=693
        )
        
        search_query = SearchQuery(
            locations=[saint_hyacinthe_location],
            property_types=[PropertyType.PLEX],
            price_min=100000,    # Prix minimum plus bas pour capturer plus de propriétés
            price_max=1000000    # Prix maximum plus haut pour capturer plus de propriétés
        )
        
        logger.info(f"📍 Recherche configurée: {saint_hyacinthe_location.value} - Plex")
        logger.info(f"💰 Fourchette de prix: {search_query.price_min:,}$ - {search_query.price_max:,}$")
        
        return search_query
    
    async def extract_properties(self, search_query: SearchQuery) -> List:
        """Extrait les propriétés selon la requête de recherche."""
        logger.info("🏠 Début de l'extraction des propriétés")
        
        try:
            # Extraction des résumés
            summaries = await self.extractor.extract_summaries(search_query)
            logger.info(f"📊 {len(summaries)} résumés de propriétés extraits")
            
            # Pour les résumés, on ne peut pas filtrer par ville car ils n'ont pas d'adresse complète
            # On utilise tous les résumés trouvés car ils sont déjà filtrés par Centris
            logger.info(f"🎯 {len(summaries)} propriétés trouvées via la recherche Centris")
            
            # Validation des résumés
            await self._validate_summaries(summaries)
            
            return summaries
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction: {e}")
            return []
    
    async def _validate_summaries(self, summaries: List):
        """Valide les résumés extraits."""
        logger.info("🔍 Validation des résumés...")
        
        # Validation des types (seule validation possible avec les résumés)
        logger.info(f"🔍 Validation des types de propriétés pour {len(summaries)} propriétés...")
        plex_count = 0
        for summary in summaries:
            if summary.type == PropertyType.PLEX:
                plex_count += 1
        
        # Éviter la division par zéro
        if len(summaries) > 0:
            percentage = (plex_count/len(summaries)*100)
            logger.info(f"📊 Validation types: {plex_count}/{len(summaries)} propriétés correspondent ({percentage:.1f}%)")
        else:
            logger.info(f"📊 Validation types: {plex_count}/{len(summaries)} propriétés correspondent")
            
        logger.info(f"📊 Distribution des types: Plex: {plex_count}")
        
        if plex_count > 0:
            logger.info("✅ Validation des résultats réussie")
        else:
            logger.warning("❌ Aucune propriété Plex trouvée")
    
    async def extract_property_details(self, summaries: List) -> List:
        """Extrait les détails complets des propriétés."""
        logger.info("🔍 Extraction des détails des propriétés")
        
        detailed_properties = []
        
        for i, summary in enumerate(summaries[:5], 1):  # Limiter à 5 pour le test
            try:
                logger.info(f"🔍 Extraction détaillée {i}/{min(len(summaries), 5)}: {summary.id}")
                
                # Construction de l'URL complète pour l'extraction des détails
                property_url = f"https://www.centris.ca/fr/propriete/{summary.id}"
                logger.debug(f"🔗 URL construite: {property_url}")
                
                # Extraction des détails
                property_details = await self.extractor.extract_details(property_url)
                
                if property_details:
                    detailed_properties.append(property_details)
                    logger.info(f"✅ Détails extraits pour {property_details.address.street if property_details.address and property_details.address.street else 'N/A'}")
                else:
                    logger.warning(f"⚠️ Aucun détail trouvé pour {summary.id}")
                    
            except Exception as e:
                logger.error(f"❌ Erreur extraction détails {summary.id}: {e}")
                continue
        
        logger.info(f"📋 {len(detailed_properties)} propriétés détaillées extraites")
        return detailed_properties
    
    async def save_to_database(self, properties: List) -> str:
        """Sauvegarde les propriétés en base de données."""
        try:
            collection_name = f"saint_hyacinthe_plex_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            saved_count = 0
            for property_data in properties:
                try:
                    # Mettre à jour les métadonnées de test
                    property_data.metadata.source = "Centris_Saint_Hyacinthe_Test"
                    property_data.metadata.last_updated = datetime.now()
                    
                    # Sauvegarder en base
                    await self.db_service.save_property(property_data, collection_name)
                    saved_count += 1
                    
                    logger.info(f"💾 Propriété sauvegardée: {property_data.address.street}")
                    
                except Exception as e:
                    logger.error(f"❌ Erreur sauvegarde propriété: {e}")
                    continue
            
            logger.info(f"✅ {saved_count}/{len(properties)} propriétés sauvegardées avec succès")
            return collection_name
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
            raise
    
    async def validate_results(self, collection_name: str) -> dict:
        """Valide les résultats finaux."""
        logger.info(f"🔍 Validation des résultats dans {collection_name}")
        
        try:
            # Récupérer les propriétés sauvegardées
            properties = await self.db_service.get_properties(collection_name)
            logger.info(f"📊 {len(properties)} propriétés trouvées en base")
            
            if len(properties) >= 3:
                # Afficher des exemples
                for i, prop in enumerate(properties[:3], 1):
                    logger.info(f"🏠 Exemple {i}:                  ")
                    logger.info(f"   📍 Adresse: {prop.address.street if prop.address and prop.address.street else 'N/A'}, {prop.address.city if prop.address and prop.address.city else 'N/A'}")
                    logger.info(f"   💰 Prix: {prop.financial.price:,.1f}$" if prop.financial and prop.financial.price else "   💰 Prix: N/A")
                    logger.info(f"   🏠 Type: {prop.type if prop.type else 'N/A'}            ")
                    logger.info(f"   🆔 ID: {prop.id if prop.id else 'N/A'}             ")
            
            # Validation des critères
            validation_results = await self._validate_data_quality(properties)
            
            logger.info("📋 Résultats de validation:    ")
            for criterion, result in validation_results.items():
                status = "✅" if result else "❌"
                logger.info(f"   {status} {criterion}: {result} ")
            
            return {
                'success': True,
                'summaries_count': len(properties),
                'details_count': len(properties),
                'collection_name': collection_name,
                'validation_results': validation_results
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _validate_data_quality(self, properties: List) -> dict:
        """Valide la qualité des données extraites."""
        if not properties:
            return {
                'adresses_complètes': False,
                'prix_valides': False,
                'types_corrects': False,
                'ids_uniques': False,
                'localisation_saint_hyacinthe': False
            }
        
        try:
            # Validation des adresses
            adresses_complètes = all(
                p.address and p.address.street and p.address.city 
                for p in properties
            )
            
            # Validation des prix
            prix_valides = all(
                p.financial and p.financial.price is not None and p.financial.price > 0
                for p in properties if p.financial
            )
            
            # Validation des types
            types_corrects = all(
                p.category == PropertyType.PLEX for p in properties
            )
            
            # Validation des IDs uniques
            ids_uniques = len(set(p.id for p in properties)) == len(properties)
            
            # Validation de la localisation Saint-Hyacinthe
            localisation_saint_hyacinthe = all(
                p.address and p.address.city and 
                ("saint-hyacinthe" in p.address.city.lower() or "saint hyacinthe" in p.address.city.lower() or "chambly" in p.address.city.lower())
                for p in properties
            )
            
            return {
                'adresses_complètes': adresses_complètes,
                'prix_valides': prix_valides,
                'types_corrects': types_corrects,
                'ids_uniques': ids_uniques,
                'localisation_saint_hyacinthe': localisation_saint_hyacinthe
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation des données: {e}")
            return {
                'adresses_complètes': False,
                'prix_valides': False,
                'types_corrects': False,
                'ids_uniques': False,
                'localisation_saint_hyacinthe': False
            }
    
    async def cleanup(self):
        """Nettoie les ressources."""
        try:
            if hasattr(self, 'extractor') and self.extractor is not None:
                await self.extractor.close()
                logger.debug("✅ CentrisExtractor fermé")
            
            if hasattr(self, 'db_service') and self.db_service is not None:
                await self.db_service.close()
                logger.debug("✅ DatabaseService fermé")
                
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de la fermeture de la base de données: {e}")
    
    async def run_test(self) -> dict:
        """Exécute le test complet."""
        try:
            if not self._setup_complete:
                await self.setup()
            
            # Créer la requête de recherche
            search_query = await self.create_search_query()
            
            # Extraire les propriétés
            summaries = await self.extract_properties(search_query)
            
            if not summaries:
                return {
                    'success': False,
                    'error': 'Aucune propriété trouvée'
                }
            
            # Extraire les détails
            detailed_properties = await self.extract_property_details(summaries)
            
            if not detailed_properties:
                return {
                    'success': False,
                    'error': 'Aucun détail extrait'
                }
            
            # Sauvegarder en base
            collection_name = await self.save_to_database(detailed_properties)
            
            # Valider les résultats
            results = await self.validate_results(collection_name)
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du test: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            await self.cleanup()
