"""
Extracteur de détails de propriétés pour Centris.ca
"""

import structlog
from typing import Optional
from bs4 import BeautifulSoup

from src.models.property import (
    Property, PropertyType, PropertyStatus, Address, FinancialInfo, 
    PropertyFeatures, PropertyDimensions, PropertyMedia, PropertyDescription, 
    PropertyMetadata
)
from src.utils.validators import RegionValidator, PropertyValidator, DataValidator

logger = structlog.get_logger()


class CentrisDetailExtractor:
    """Extracteur de détails de propriétés depuis les pages de détail"""
    
    def __init__(self):
        self.validators = {
            'region': RegionValidator(),
            'property': PropertyValidator(),
            'data': DataValidator()
        }
    
    async def extract_property_details(self, soup: BeautifulSoup, url: str) -> Optional[Property]:
        """
        Extrait toutes les données d'une propriété depuis sa page de détail
        
        Args:
            soup: BeautifulSoup object de la page
            url: URL de la page de détail
            
        Returns:
            Property: Objet Property avec tous les détails ou None en cas d'échec
        """
        try:
            # Extraction des informations de base
            property_id = self._extract_property_id(soup)
            if not property_id:
                return None
            
            # Extraction des différentes sections
            address = self._extract_address(soup)
            financial = self._extract_financial(soup)
            features = self._extract_features(soup)
            dimensions = self._extract_dimensions(soup)
            media = self._extract_media(soup)
            description = self._extract_description(soup)
            
            # Création de l'objet Property
            property_data = Property(
                id=property_id,
                type=PropertyType.SINGLE_FAMILY_HOME,  # À améliorer selon la logique métier
                status=PropertyStatus.FOR_SALE,
                address=address,
                financial=financial,
                features=features,
                dimensions=dimensions,
                media=media,
                description=description,
                metadata=PropertyMetadata(
                    source="Centris",
                    source_id=property_id,
                    url=url
                )
            )
            
            # Validation et nettoyage des données
            validated_property = self._validate_and_clean_property(property_data)
            
            return validated_property
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des données détaillées: {str(e)}")
            return None
    
    def _extract_property_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait l'ID de la propriété depuis la page de détail"""
        try:
            # Recherche dans les meta tags
            meta_id = soup.find('meta', {'property': 'og:url'})
            if meta_id:
                url = meta_id.get('content', '')
                if '/property/' in url:
                    return url.split('/property/')[-1].split('/')[0]
            
            # Recherche dans les scripts
            scripts = soup.find_all('script')
            for script in scripts:
                script_text = script.string or ''
                if 'propertyId' in script_text:
                    # Extraction de l'ID depuis le script
                    import re
                    match = re.search(r'propertyId["\']?\s*:\s*["\']?([^"\']+)', script_text)
                    if match:
                        return match.group(1)
            
            # Fallback: extraction depuis l'URL
            return "temp_id"
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction ID: {str(e)}")
            return None
    
    def _extract_address(self, soup: BeautifulSoup) -> Address:
        """Extrait l'adresse détaillée depuis la page de détail"""
        try:
            # Extraction de l'adresse (à implémenter selon la structure HTML réelle)
            address_element = soup.find('span', {'data-id': 'PageTitle'}) or \
                            soup.find('h1', {'class': 'property-title'})
            
            if address_element:
                full_address = address_element.get_text(strip=True)
                # Parse l'adresse pour extraire les composants
                city, region = self._parse_address_text(full_address)
                
                return Address(
                    street=full_address,
                    city=city,
                    region=region,
                    country="Canada"
                )
            
            return Address()
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction de l'adresse: {str(e)}")
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
    
    def _extract_financial(self, soup: BeautifulSoup) -> FinancialInfo:
        """Extrait les informations financières depuis la page de détail"""
        try:
            # Recherche du prix
            price_element = soup.find('span', {'class': 'price'}) or \
                          soup.find('div', {'class': 'price'})
            
            price = None
            if price_element:
                price_text = price_element.get_text(strip=True)
                price_clean = ''.join(filter(str.isdigit, price_text))
                if price_clean:
                    price = float(price_clean)
            
            return FinancialInfo(price=price)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction financier: {str(e)}")
            return FinancialInfo()
    
    def _extract_features(self, soup: BeautifulSoup) -> PropertyFeatures:
        """Extrait les caractéristiques physiques depuis la page de détail"""
        try:
            # Recherche des caractéristiques
            features = {}
            
            # Exemple: extraction du nombre de chambres
            bedrooms_element = soup.find('span', {'class': 'bedrooms'})
            if bedrooms_element:
                bedrooms_text = bedrooms_element.get_text(strip=True)
                try:
                    features['bedrooms'] = int(''.join(filter(str.isdigit, bedrooms_text)))
                except ValueError:
                    pass
            
            # Exemple: extraction du nombre de salles de bain
            bathrooms_element = soup.find('span', {'class': 'bathrooms'})
            if bathrooms_element:
                bathrooms_text = bathrooms_element.get_text(strip=True)
                try:
                    features['bathrooms'] = int(''.join(filter(str.isdigit, bathrooms_text)))
                except ValueError:
                    pass
            
            return PropertyFeatures(**features)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction caractéristiques: {str(e)}")
            return PropertyFeatures()
    
    def _extract_dimensions(self, soup: BeautifulSoup) -> PropertyDimensions:
        """Extrait les dimensions depuis la page de détail"""
        try:
            # Recherche des dimensions
            dimensions = {}
            
            # Exemple: extraction de la superficie
            area_element = soup.find('span', {'class': 'area'})
            if area_element:
                area_text = area_element.get_text(strip=True)
                try:
                    # Extraire les chiffres
                    area_clean = ''.join(filter(str.isdigit, area_text))
                    if area_clean:
                        dimensions['area'] = int(area_clean)
                except ValueError:
                    pass
            
            return PropertyDimensions(**dimensions)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction dimensions: {str(e)}")
            return PropertyDimensions()
    
    def _extract_media(self, soup: BeautifulSoup) -> PropertyMedia:
        """Extrait les médias depuis la page de détail"""
        try:
            # Recherche des images
            images = []
            img_elements = soup.find_all('img', {'class': 'property-image'})
            
            for img in img_elements:
                src = img.get('src')
                if src:
                    images.append(src)
            
            return PropertyMedia(images=images)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction médias: {str(e)}")
            return PropertyMedia()
    
    def _extract_description(self, soup: BeautifulSoup) -> PropertyDescription:
        """Extrait les descriptions depuis la page de détail"""
        try:
            # Recherche de la description
            desc_element = soup.find('div', {'class': 'description'}) or \
                          soup.find('p', {'class': 'description'})
            
            description = ""
            if desc_element:
                description = desc_element.get_text(strip=True)
            
            return PropertyDescription(description=description)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction description: {str(e)}")
            return PropertyDescription()
    
    def _validate_and_clean_property(self, property_data: Property) -> Property:
        """
        Valide et nettoie les données d'une propriété
        
        Args:
            property_data: Propriété à valider
            
        Returns:
            Property: Propriété validée et nettoyée
        """
        try:
            # Validation et nettoyage de l'adresse
            if property_data.address:
                # Validation de la région
                if property_data.address.region:
                    if not self.validators['region'].is_valid_region(property_data.address.region):
                        logger.warning(f"⚠️ Région invalide détectée: {property_data.address.region}")
                        # Essayer de normaliser la région
                        normalized_region = self.validators['region'].normalize_region(property_data.address.region)
                        if normalized_region:
                            property_data.address.region = normalized_region
                            logger.info(f"✅ Région normalisée: {property_data.address.region}")
                        else:
                            logger.warning(f"⚠️ Impossible de normaliser la région: {property_data.address.region}")
                
                # Validation du code postal
                if property_data.address.postal_code:
                    if not self.validators['property'].is_valid_postal_code(property_data.address.postal_code):
                        logger.warning(f"⚠️ Code postal invalide: {property_data.address.postal_code}")
                
                # Nettoyage des textes d'adresse
                if property_data.address.street:
                    property_data.address.street = self.validators['data'].clean_text(property_data.address.street)
                if property_data.address.city:
                    property_data.address.city = self.validators['data'].clean_text(property_data.address.city)
            
            # Validation des informations financières
            if property_data.financial and property_data.financial.price:
                if not self.validators['property'].is_valid_price(property_data.financial.price):
                    logger.warning(f"⚠️ Prix invalide détecté: {property_data.financial.price}")
            
            # Validation des coordonnées géographiques
            if (property_data.address and 
                hasattr(property_data.address, 'latitude') and 
                hasattr(property_data.address, 'longitude')):
                
                if not self.validators['data'].is_valid_coordinates(
                    property_data.address.latitude, 
                    property_data.address.longitude
                ):
                    logger.warning(f"⚠️ Coordonnées géographiques invalides: {property_data.address.latitude}, {property_data.address.longitude}")
            
            # Validation de l'ID
            if not self.validators['property'].is_valid_property_id(property_data.id):
                logger.warning(f"⚠️ ID de propriété invalide: {property_data.id}")
            
            logger.debug(f"✅ Propriété {property_data.id} validée et nettoyée")
            return property_data
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation: {str(e)}")
            return property_data

