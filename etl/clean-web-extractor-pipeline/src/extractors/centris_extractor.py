"""
Extracteur de données pour Centris.ca
Architecture modulaire et maintenable
"""

import asyncio
import structlog
from typing import List, Optional
from bs4 import BeautifulSoup

from config.settings import config
from src.models.property import Property, PropertySummary, SearchQuery
from src.extractors.centris.session_manager import CentrisSessionManager
from src.extractors.centris.search_manager import CentrisSearchManager
from src.extractors.centris.summary_extractor import CentrisSummaryExtractor
from src.extractors.centris.detail_extractor import CentrisDetailExtractor
from src.extractors.centris.data_validator import CentrisDataValidator

logger = structlog.get_logger()


class CentrisExtractionError(Exception):
    """Exception personnalisée pour les erreurs d'extraction Centris"""
    pass


class CentrisExtractor:
    """Extracteur de données pour Centris.ca - Architecture modulaire"""
    
    def __init__(self, centris_config):
        self.config = centris_config
        
        # Initialisation des composants spécialisés
        self.session_manager = CentrisSessionManager(centris_config)
        self.search_manager = CentrisSearchManager(self.session_manager)
        self.summary_extractor = CentrisSummaryExtractor(self.session_manager)
        self.detail_extractor = CentrisDetailExtractor()
        self.data_validator = CentrisDataValidator()
        
        logger.info("🔧 CentrisExtractor initialisé avec architecture modulaire")
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session_manager.close()
    
    async def extract_summaries(self, search_query: SearchQuery) -> List[PropertySummary]:
        """
        Extrait les résumés de propriétés depuis les résultats de recherche
        
        Args:
            search_query: Paramètres de recherche
            
        Returns:
            Liste des résumés de propriétés
        """
        logger.info(f"🔍 Extraction des résumés pour {search_query.locations} - {search_query.property_types}")
        
        try:
            # Utilisation du gestionnaire de recherche
            pages_html = await self.search_manager.search_with_pagination(search_query)
            
            if not pages_html:
                logger.warning("⚠️ Aucune page de résultats trouvée")
                return []
            
            all_summaries = []
            
            # Traitement de chaque page
            for page_num, page_html in enumerate(pages_html, 1):
                logger.debug(f"📄 Traitement de la page {page_num}")
                
                # Extraction des résumés depuis le HTML
                page_summaries = self.summary_extractor.extract_summaries_from_html(page_html)
                
                # Validation des résultats de la première page
                if page_num == 1:
                    valid = self.data_validator.validate_search_results(page_summaries, search_query)
                    if not valid:
                        logger.warning("⚠️ Les résultats de la première page ne sont pas valides")
                        logger.warning("⚠️ Vérifiez les paramètres de recherche")
                        return []
                
                all_summaries.extend(page_summaries)
                logger.info(f"✅ Page {page_num}: {len(page_summaries)} propriétés trouvées")
            
            logger.info(f"🎉 Extraction terminée: {len(all_summaries)} propriétés trouvées au total")
            return all_summaries
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des résumés: {str(e)}")
            raise CentrisExtractionError(f"Échec de l'extraction des résumés: {str(e)}")
    
    async def extract_details(self, property_url: str) -> Optional[Property]:
        """
        Extrait les détails complets d'une propriété depuis sa page dédiée
        
        Args:
            property_url: URL de la page de détail de la propriété
            
        Returns:
            Objet Property avec tous les détails ou None en cas d'échec
        """
        logger.debug(f"🔍 Extraction des détails depuis {property_url}")
        
        try:
            # Utilisation du gestionnaire de session
            async with self.session_manager.session.get(property_url) as response:
                if response.status != 200:
                    logger.warning(f"⚠️ Statut HTTP {response.status} pour {property_url}")
                    return None
                
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Utilisation de l'extracteur de détails spécialisé
                property_data = await self.detail_extractor.extract_property_details(soup, property_url)
                
                if property_data:
                    logger.debug(f"✅ Détails extraits avec succès pour {property_url}")
                    return property_data
                else:
                    logger.warning(f"⚠️ Aucun détail extrait pour {property_url}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des détails: {str(e)}")
            return None
    
    def set_validation_threshold(self, threshold: float):
        """Définit le seuil de validation pour les résultats de recherche"""
        self.data_validator.set_validation_threshold(threshold)
    
    def get_validation_threshold(self) -> float:
        """Retourne le seuil de validation actuel"""
        return self.data_validator.get_validation_threshold()
    
    async def close(self):
        """Ferme proprement l'extracteur"""
        await self.session_manager.close()
        logger.info("🔌 CentrisExtractor fermé proprement")
