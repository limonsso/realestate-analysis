"""
Extracteur Centris Modulaire - Point d'entrée principal
"""

from typing import List, Optional, Dict, Any
import structlog
from bs4 import BeautifulSoup

from src.models.property import SearchQuery, PropertySummary, Property
from .centris.session_manager import CentrisSessionManager
from .centris.search_manager import CentrisSearchManager
from .centris.summary_extractor import CentrisSummaryExtractor
from .centris.detail_extractor_refactored import CentrisDetailExtractor
from .centris.data_validator import CentrisDataValidator

logger = structlog.get_logger()


class CentrisExtractor:
    """
    Extracteur principal pour Centris.ca utilisant une architecture modulaire.
    
    Cette classe orchestre les différents composants spécialisés :
    - SessionManager : Gestion des sessions HTTP
    - SearchManager : Gestion des requêtes de recherche
    - SummaryExtractor : Extraction des résumés de propriétés
    - DetailExtractor : Extraction des détails complets
    - DataValidator : Validation des données extraites
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise l'extracteur avec sa configuration.
        
        Args:
            config: Configuration pour l'extraction Centris
        """
        self.config = config
        self.session_manager = CentrisSessionManager(config)
        self.search_manager = CentrisSearchManager(self.session_manager, config)
        self.summary_extractor = CentrisSummaryExtractor(self.session_manager)
        self.detail_extractor = CentrisDetailExtractor(config=config)
        self.data_validator = CentrisDataValidator()
        
        logger.info("🔧 CentrisExtractor initialisé avec architecture modulaire")
        logger.info(f"🔒 Configuration utilisée: {self.config}")
    
    async def extract_summaries(self, search_query: SearchQuery) -> List[PropertySummary]:
        """
        Extrait les résumés de propriétés pour une requête donnée.
        
        Args:
            search_query: Requête de recherche
            
        Returns:
            List[PropertySummary]: Liste des résumés extraits
        """
        try:
            logger.info(f"🔍 Extraction des résumés pour {search_query.locations} - {search_query.property_types}")
            
            # Recherche paginée avec le SearchManager
            search_results = await self.search_manager.search_with_pagination(search_query)
            
            # Extraction des résumés avec le SummaryExtractor
            summaries = []
            for page_content in search_results:
                page_summaries = self.summary_extractor.extract_summaries_from_html(page_content)
                summaries.extend(page_summaries)
            
            # Validation des résumés
            validation_success = self.data_validator.validate_search_results(summaries, search_query)
            
            if validation_success:
                logger.info(f"🎉 Extraction terminée: {len(summaries)} propriétés trouvées au total")
            else:
                logger.warning(f"⚠️ Validation échouée mais {len(summaries)} propriétés extraites")
            
            return summaries
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des résumés: {e}")
            raise
    
    async def extract_details(self, property_url: str) -> Optional[Property]:
        """
        Extrait les détails complets d'une propriété.
        
        Args:
            property_url: URL de la propriété
            
        Returns:
            Optional[Property]: Propriété avec détails complets ou None
        """
        try:
            # Récupérer le contenu HTML de la page
            async with self.session_manager.session.get(property_url) as response:
                if response.status != 200:
                    logger.error(f"❌ Erreur HTTP {response.status} pour {property_url}")
                    return None
                
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Appeler l'extracteur avec soup et URL
                return await self.detail_extractor.extract_property_details(soup, property_url)
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des détails: {e}")
            return None
    
    async def extract_property_batch(self, urls: List[str]) -> List[Property]:
        """
        Extrait les détails d'un lot de propriétés en parallèle.
        
        Args:
            urls: Liste des URLs de propriétés
            
        Returns:
            List[Property]: Liste des propriétés extraites
        """
        return await self.detail_extractor.extract_properties_batch(urls)
    
    async def close(self):
        """Ferme les ressources de l'extracteur."""
        try:
            await self.session_manager.close()
            logger.info("🔌 CentrisExtractor fermé proprement")
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de la fermeture: {e}")
