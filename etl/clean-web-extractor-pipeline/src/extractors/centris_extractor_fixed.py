"""
Extracteur Centris Corrigé - Respecte la Configuration Passée
"""

from typing import List, Optional, Dict, Any
import structlog
import aiohttp
from bs4 import BeautifulSoup

from src.models.property import SearchQuery, PropertySummary, Property
from .centris.session_manager import CentrisSessionManager
from .centris.search_manager import CentrisSearchManager
from .centris.summary_extractor import CentrisSummaryExtractor
from .centris.detail_extractor_refactored import CentrisDetailExtractor
from .centris.data_validator import CentrisDataValidator

logger = structlog.get_logger()


class CentrisExtractorFixed:
    """
    Extracteur principal pour Centris.ca qui respecte VRAIMENT la configuration passée.
    
    Cette classe orchestre les différents composants spécialisés et s'assure
    que la configuration passée est utilisée partout, pas la configuration globale.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise l'extracteur avec sa configuration.
        
        Args:
            config: Configuration pour l'extraction Centris (DOIT être utilisée)
        """
        self.config = config
        logger.info(f"🔧 CentrisExtractorFixed initialisé avec configuration: {config}")
        
        # Initialiser les composants avec la configuration passée
        self.session_manager = CentrisSessionManagerFixed(config)
        self.search_manager = CentrisSearchManagerFixed(self.session_manager, config)
        self.summary_extractor = CentrisSummaryExtractor(self.session_manager)
        self.detail_extractor = CentrisDetailExtractor(config=config)
        self.data_validator = CentrisDataValidator()
        
        logger.info("🔧 CentrisExtractorFixed initialisé avec architecture modulaire")
        logger.info(f"🔒 Configuration forcée: {self.config}")
    
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
            logger.info(f"🔒 Utilisation de la configuration: {self.config}")
            
            # Recherche paginée avec le SearchManager (configuration forcée)
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
            logger.info("🔌 CentrisExtractorFixed fermé proprement")
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de la fermeture: {e}")


class CentrisSessionManagerFixed:
    """Gestionnaire de session HTTP pour Centris (Configuration Forcée)"""
    
    def __init__(self, config):
        self.config = config
        self.base_url = "https://www.centris.ca"
        self.session = None
        self._setup_session()
        logger.info(f"🔒 CentrisSessionManagerFixed initialisé avec configuration: {config}")
    
    def _setup_session(self):
        """Configure la session HTTP avec les headers appropriés"""
        
        # Utiliser la configuration passée, pas la globale
        timeout = getattr(self.config, 'request_timeout', 30)
        
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout),
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'fr-CA,fr;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def close(self):
        """Ferme la session HTTP"""
        if self.session:
            await self.session.close()
            self.session = None
    
    def get_session(self) -> aiohttp.ClientSession:
        """Retourne la session HTTP active"""
        return self.session
    
    def update_headers(self, headers: dict):
        """Met à jour les headers de la session"""
        if self.session:
            self.session.headers.update(headers)


class CentrisSearchManagerFixed:
    """Gestionnaire de recherche pour Centris (Configuration Forcée)"""
    
    def __init__(self, session_manager, config):
        self.session_manager = session_manager
        self.config = config
        self.base_url = session_manager.base_url
        logger.info(f"🔒 CentrisSearchManagerFixed initialisé avec configuration: {config}")
    
    async def initialize_search(self, search_query: SearchQuery) -> bool:
        """Initialise une nouvelle recherche sur Centris (Configuration Forcée)"""
        logger.debug("🔧 Initialisation de la recherche Centris (Configuration Forcée)")
        logger.debug(f"🔒 Configuration utilisée: {self.config}")
        
        try:
            # Construction de la requête de recherche
            search_data = self._build_search_request(search_query)
            
            # Initialisation de la recherche
            async with self.session_manager.session.post(
                f"{self.base_url}/api/property/UpdateQuery",
                json=search_data
            ) as response:
                if response.status != 200:
                    raise Exception(f"Échec de l'initialisation de la recherche: {response.status}")
                
                # Verrouillage du contexte utilisateur
                async with self.session_manager.session.post(
                    f"{self.base_url}/UserContext/Lock",
                    json={'uc': 0}
                ) as lock_response:
                    if lock_response.status != 200:
                        raise Exception("Échec du verrouillage du contexte utilisateur")
                    
                    uck_data = await lock_response.json()
                    
                    # Gestion du cas où l'API retourne directement la chaîne UCK
                    if isinstance(uck_data, str):
                        uck = uck_data
                    else:
                        uck = uck_data.get('uck', '')
                    
                    # Mise à jour des headers avec l'UCK
                    self.session_manager.update_headers({
                        'X-CENTRIS-UC': '0',
                        'X-CENTRIS-UCK': uck,
                        'X-Requested-With': 'XMLHttpRequest'
                    })
            
            logger.debug("✅ Recherche Centris initialisée avec succès (Configuration Forcée)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'initialisation de la recherche: {str(e)}")
            return False
    
    def _build_search_request(self, search_query: SearchQuery) -> Dict[str, Any]:
        """Construit la requête de recherche pour l'API Centris (Configuration Forcée)"""
        logger.debug(f"🔒 Construction de la requête avec configuration: {self.config}")
        
        # Champs de localisation (comme dans l'ancien pipeline)
        field_values = []
        for location in search_query.locations:
            field_values.append({
                'fieldId': location.type,      # ex: "CityDistrict", "GeographicArea"
                'value': location.type_id,     # ex: 449, "RARA16"
            })
        
        # Filtres de type de propriété
        for prop_type in search_query.property_types:
            field_values.append({
                'fieldId': 'PropertyType',
                'value': prop_type.value,
                'valueConditionId': self._get_property_type_condition(prop_type)
            })
        
        # Filtres de prix
        if search_query.price_min is not None:
            field_values.append({
                'fieldId': 'SalePrice',
                'value': search_query.price_min,
                'fieldConditionId': 'ForSale'
            })
        
        if search_query.price_max is not None:
            field_values.append({
                'fieldId': 'SalePrice',
                'value': search_query.price_max,
                'fieldConditionId': 'ForSale'
            })
        
        logger.debug(f"🔒 Requête construite avec field_values: {field_values}")
        
        return {
            'query': {
                'UseGeographyShapes': 0,
                'FieldsValues': field_values
            },
            'isHomePage': False
        }
    
    def _get_property_type_condition(self, property_type) -> str:
        """Retourne la condition Centris pour un type de propriété"""
        conditions = {
            'Plex': 'IsResidential',
            'SingleFamilyHome': 'IsResidential',
            'SellCondo': 'IsResidential',
            'ResidentialLot': 'IsLandArea'
        }
        return conditions.get(property_type.value, 'IsResidentialForSale')
    
    async def get_page_summaries(self, page: int) -> Optional[str]:
        """Récupère le contenu HTML d'une page de résultats"""
        try:
            async with self.session_manager.session.post(
                f"{self.base_url}/property/GetInscriptions",
                json={"startPosition": (page - 1) * 20}
            ) as response:
                if response.status != 200:
                    logger.warning(f"⚠️ Statut HTTP {response.status} pour la page {page}")
                    return None
                
                data = await response.json()
                html_content = data.get('d', {}).get('Result', {}).get('html', '')
                
                return html_content if html_content else None
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction de la page {page}: {str(e)}")
            return None
    
    async def search_with_pagination(self, search_query: SearchQuery, max_pages: int = 50) -> List[str]:
        """
        Effectue une recherche avec pagination (Configuration Forcée)
        
        Args:
            search_query: Paramètres de recherche
            max_pages: Nombre maximum de pages à parcourir
            
        Returns:
            List[str]: Liste des pages HTML de résultats
        """
        logger.info(f"🔍 Recherche avec pagination (Configuration Forcée)")
        logger.info(f"🔒 Configuration utilisée: {self.config}")
        
        try:
            # Initialiser la recherche
            if not await self.initialize_search(search_query):
                raise Exception("Échec de l'initialisation de la recherche")
            
            # Récupérer les pages de résultats
            pages = []
            page = 1
            
            while page <= max_pages:
                logger.debug(f"🔍 Récupération de la page {page}")
                
                page_content = await self.get_page_summaries(page)
                if not page_content:
                    logger.debug(f"🔍 Plus de contenu à la page {page}")
                    break
                
                pages.append(page_content)
                page += 1
            
            logger.info(f"✅ {len(pages)} pages de résultats récupérées")
            return pages
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la recherche avec pagination: {str(e)}")
            raise
