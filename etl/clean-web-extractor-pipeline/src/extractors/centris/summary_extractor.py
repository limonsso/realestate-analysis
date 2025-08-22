"""
Extracteur de résumés de propriétés pour Centris.ca
"""

import structlog
from typing import List, Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from src.models.property import PropertySummary, Address, PropertyType
from .session_manager import CentrisSessionManager

logger = structlog.get_logger()


class CentrisSummaryExtractor:
    """Extracteur de résumés de propriétés depuis les pages de résultats"""
    
    def __init__(self, session_manager: CentrisSessionManager):
        self.session_manager = session_manager
        self.base_url = session_manager.base_url
    
    def extract_summaries_from_html(self, html_content: str) -> List[PropertySummary]:
        """
        Extrait les résumés de propriétés depuis le HTML d'une page
        
        Args:
            html_content: Contenu HTML de la page de résultats
            
        Returns:
            List[PropertySummary]: Liste des résumés de propriétés
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            return self._parse_summaries_from_soup(soup)
        except Exception as e:
            logger.error(f"❌ Erreur lors du parsing HTML: {str(e)}")
            return []
    
    def _parse_summaries_from_soup(self, soup: BeautifulSoup) -> List[PropertySummary]:
        """Parse le HTML pour extraire les résumés de propriétés"""
        summaries = []
        
        # Recherche des conteneurs de propriétés
        # Centris utilise 'property-thumbnail-item' pour les cartes de propriétés
        property_containers = soup.find_all('div', class_='property-thumbnail-item')
        
        # Si aucun trouvé, essayer d'autres sélecteurs
        if not property_containers:
            property_containers = soup.find_all('div', class_='thumbnailItem')
        
        if not property_containers:
            # Recherche par itemscope (schema.org)
            property_containers = soup.find_all('div', attrs={'itemscope': True, 'itemtype': 'http://schema.org/Product'})
        
        logger.info(f"🔍 Trouvé {len(property_containers)} conteneurs de propriétés")
        
        for container in property_containers:
            try:
                summary = self._extract_single_summary(container)
                if summary:
                    summaries.append(summary)
            except Exception as e:
                logger.warning(f"⚠️ Erreur lors de l'extraction d'un résumé: {str(e)}")
                continue
        
        return summaries
    
    def _extract_single_summary(self, container: BeautifulSoup) -> Optional[PropertySummary]:
        """Extrait le résumé d'une propriété depuis son conteneur HTML"""
        try:
            # Extraction de l'ID
            property_id = self._extract_property_id(container)
            if not property_id:
                return None
            
            # Extraction des autres informations
            address = self._extract_address(container)
            price = self._extract_price(container)
            property_type = self._extract_property_type(container)
            image_url = self._extract_main_image(container)
            property_url = self._extract_property_url(container)
            
            # Création du résumé
            return PropertySummary(
                id=property_id,
                address=address,
                price=price,
                type=property_type,
                image_url=image_url,
                url=property_url,
                source="Centris"
            )
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de l'extraction d'un résumé: {str(e)}")
            return None
    
    def _extract_property_id(self, container: BeautifulSoup) -> Optional[str]:
        """Extrait l'ID de la propriété"""
        try:
            # Recherche de l'ID dans les attributs data ou dans les liens
            id_element = container.find('a', href=True)
            if id_element:
                href = id_element.get('href', '')
                logger.debug(f"🔍 Lien trouvé: {href}")
                
                # Format Centris: /fr/duplex~a-vendre~saint-hyacinthe/16871982
                if '/' in href:
                    # Prendre le dernier segment qui devrait être l'ID
                    segments = href.split('/')
                    if len(segments) > 1:
                        potential_id = segments[-1]
                        # Vérifier que c'est un ID numérique
                        if potential_id.isdigit():
                            logger.debug(f"✅ ID extrait depuis l'URL: {potential_id}")
                            return potential_id
                        else:
                            logger.debug(f"⚠️ Segment non numérique: {potential_id}")
                
                # Fallback: chercher dans les meta tags (Centris utilise itemprop="sku")
                meta_sku = container.find('meta', attrs={'itemprop': 'sku'})
                if meta_sku:
                    sku_value = meta_sku.get('content', '')
                    if sku_value and sku_value.isdigit():
                        logger.debug(f"✅ ID extrait depuis meta sku: {sku_value}")
                        return sku_value
            
            # Fallback: recherche dans les attributs data
            data_id = container.get('data-property-id') or container.get('data-id')
            if data_id:
                logger.debug(f"✅ ID extrait depuis data: {data_id}")
                return str(data_id)
            
            logger.warning("⚠️ Aucun ID trouvé")
            return None
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction ID: {str(e)}")
            return None
    
    def _extract_address(self, container: BeautifulSoup) -> Address:
        """Extrait l'adresse de la propriété"""
        try:
            # Recherche des éléments d'adresse selon la structure Centris
            # D'après le débogage, Centris utilise 'location-container' et 'address'
            address_element = (
                container.find('div', {'class': 'location-container'}) or
                container.find('div', {'class': 'address'}) or
                container.find('span', {'class': 'address'})
            )
            
            if address_element:
                # Chercher le texte d'adresse dans le conteneur
                address_text_element = address_element.find('div', {'class': 'address'})
                if address_text_element:
                    address_text = address_text_element.get_text(strip=True)
                else:
                    address_text = address_element.get_text(strip=True)
                
                # Parse l'adresse pour extraire ville et région
                city, region = self._parse_address_text(address_text)
                
                return Address(
                    street=address_text,
                    city=city,
                    region=region,
                    country="Canada"
                )
            
            return Address()
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction adresse: {str(e)}")
            return Address()
    
    def _parse_address_text(self, address_text: str) -> tuple[str, str]:
        """Parse le texte d'adresse pour extraire ville et région"""
        try:
            # Logique de parsing basique (à améliorer selon la structure réelle)
            parts = address_text.split(',')
            if len(parts) >= 2:
                city = parts[-2].strip()
                region = parts[-1].strip()
                return city, region
            elif len(parts) == 1:
                return parts[0].strip(), ""
            else:
                return "", ""
        except Exception:
            return "", ""
    
    def _extract_price(self, container: BeautifulSoup) -> Optional[float]:
        """Extrait le prix de la propriété"""
        try:
            # Recherche du prix selon la structure Centris
            # D'après le débogage, Centris utilise 'plex-revenue' pour les Plex
            price_element = (
                container.find('div', {'class': 'plex-revenue'}) or
                container.find('div', {'class': 'price'}) or
                container.find('span', {'class': 'price'})
            )
            
            if price_element:
                price_text = price_element.get_text(strip=True)
                logger.debug(f"🔍 Texte prix trouvé: '{price_text}'")
                
                # Nettoyer le texte du prix (enlever $, espaces, etc.)
                price_clean = ''.join(filter(str.isdigit, price_text))
                if price_clean:
                    return float(price_clean)
                else:
                    logger.debug(f"⚠️ Impossible d'extraire le prix numérique de: '{price_text}'")
            
            return None
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction prix: {str(e)}")
            return None
    
    def _extract_property_type(self, container: BeautifulSoup) -> PropertyType:
        """Extrait le type de propriété"""
        try:
            # Recherche du type selon la structure Centris
            # D'après le débogage, Centris utilise 'category' pour le type
            type_element = (
                container.find('div', {'class': 'category'}) or
                container.find('span', {'class': 'property-type'}) or
                container.find('div', {'class': 'property-type'})
            )
            
            if type_element:
                type_text = type_element.get_text(strip=True).lower()
                logger.debug(f"🔍 Type de propriété trouvé: '{type_text}'")
                
                # Mapping des types selon la structure Centris
                if 'condo' in type_text or 'condominium' in type_text:
                    return PropertyType.SELL_CONDO
                elif 'plex' in type_text or 'duplex' in type_text or 'triplex' in type_text:
                    return PropertyType.PLEX
                elif 'lot' in type_text or 'terrain' in type_text:
                    return PropertyType.RESIDENTIAL_LOT
                elif 'maison' in type_text or 'house' in type_text or 'single' in type_text:
                    return PropertyType.SINGLE_FAMILY_HOME
            
            # Type par défaut
            return PropertyType.SINGLE_FAMILY_HOME
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction type: {str(e)}")
            return PropertyType.SINGLE_FAMILY_HOME
    
    def _extract_main_image(self, container: BeautifulSoup) -> Optional[str]:
        """Extrait l'URL de l'image principale"""
        try:
            img_element = container.select_one('img[itemprop="image"]') or \
                         container.find('img')
            
            if img_element:
                src = img_element.get('src')
                if src:
                    return urljoin(self.base_url, src)
            
            return None
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction image: {str(e)}")
            return None
    
    def _extract_property_url(self, container: BeautifulSoup) -> Optional[str]:
        """Extrait l'URL de la page de détail de la propriété"""
        try:
            link_element = container.select_one('a[href*="/property/"]')
            if link_element:
                href = link_element.get('href')
                if href:
                    return urljoin(self.base_url, href)
            
            return None
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction URL: {str(e)}")
            return None

