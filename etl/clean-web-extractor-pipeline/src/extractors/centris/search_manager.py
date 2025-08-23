"""
Gestionnaire de recherche et pagination pour Centris.ca
"""

import asyncio
import structlog
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin

from src.models.property import SearchQuery, PropertyType
from .session_manager import CentrisSessionManager

logger = structlog.get_logger()


class CentrisSearchManager:
    """Gestionnaire de recherche et pagination pour Centris"""
    
    def __init__(self, session_manager: CentrisSessionManager, config: Dict[str, Any] = None):
        self.session_manager = session_manager
        self.config = config
        self.base_url = session_manager.base_url
        
        if self.config:
            logger.debug(f"🔒 SearchManager initialisé avec configuration: {self.config}")
    
    async def initialize_search(self, search_query: SearchQuery) -> bool:
        """Initialise une nouvelle recherche sur Centris"""
        logger.debug("🔧 Initialisation de la recherche Centris")
        
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
            
            logger.debug("✅ Recherche Centris initialisée avec succès")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'initialisation de la recherche: {str(e)}")
            return False
    
    def _build_search_request(self, search_query: SearchQuery) -> Dict[str, Any]:
        """Construit la requête de recherche pour l'API Centris"""
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
        
        return {
            'query': {
                'UseGeographyShapes': 0,
                'FieldsValues': field_values
            },
            'isHomePage': False
        }
    
    def _get_property_type_condition(self, property_type: PropertyType) -> str:
        """Retourne la condition Centris pour un type de propriété"""
        conditions = {
            PropertyType.PLEX: 'IsResidential',
            PropertyType.SINGLE_FAMILY_HOME: 'IsResidential',
            PropertyType.SELL_CONDO: 'IsResidential',
            PropertyType.RESIDENTIAL_LOT: 'IsLandArea'
        }
        return conditions.get(property_type, 'IsResidentialForSale')
    
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
        Effectue une recherche avec pagination
        
        Args:
            search_query: Paramètres de recherche
            max_pages: Nombre maximum de pages à parcourir
            
        Returns:
            List[str]: Liste des pages HTML de résultats
        """
        logger.info(f"🔍 Recherche avec pagination pour {search_query.locations}")
        
        # Initialisation de la recherche
        if not await self.initialize_search(search_query):
            return []
        
        # Récupération des pages
        pages = []
        page = 1
        
        while page <= max_pages:
            logger.debug(f"📄 Récupération de la page {page}")
            
            page_content = await self.get_page_summaries(page)
            if not page_content:
                logger.info(f"🏁 Fin des résultats atteinte à la page {page - 1}")
                break
            
            pages.append(page_content)
            logger.info(f"✅ Page {page}: {len(page_content)} caractères")
            
            # Pause entre les pages
            await asyncio.sleep(1)
            page += 1
        
        logger.info(f"🎯 Total: {len(pages)} pages récupérées")
        return pages

