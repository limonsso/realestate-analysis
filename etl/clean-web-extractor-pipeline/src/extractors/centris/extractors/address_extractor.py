#!/usr/bin/env python3
"""
Extracteur spécialisé pour les adresses et coordonnées GPS
"""

import re
from typing import Optional, Tuple
from bs4 import BeautifulSoup
import structlog

logger = structlog.get_logger()

class AddressExtractor:
    """Extracteur spécialisé pour les adresses et coordonnées GPS"""
    
    def __init__(self, config=None):
        self.logger = logger
        self.config = config
    
    def extract_address(self, soup: BeautifulSoup) -> dict:
        """Extrait l'adresse complète d'une propriété"""
        try:
            address_data = {}
            
            # Extraction de la rue
            street = self._extract_street(soup)
            if street:
                address_data['street'] = street
            
            # Extraction de la ville
            city = self._extract_city(soup)
            if city:
                address_data['city'] = city
            
            # Extraction de la région
            region = self._extract_region(soup)
            if region:
                address_data['region'] = region
            
            # Extraction du code postal
            postal_code = self._extract_postal_code(soup)
            if postal_code:
                address_data['postal_code'] = postal_code
            
            # Extraction du pays
            country = self._extract_country(soup)
            if country:
                address_data['country'] = country
            
            # Construction de l'adresse complète
            if address_data:
                address_data['full_address'] = self._build_full_address(address_data)
            
            # Extraction des coordonnées GPS
            coordinates = self._extract_coordinates(soup)
            if coordinates:
                address_data['latitude'] = coordinates[0]
                address_data['longitude'] = coordinates[1]
            
            logger.debug(f"📍 Adresse extraite: {address_data}")
            return address_data
            
        except Exception as e:
            logger.error(f"❌ Erreur extraction adresse: {e}")
            return {}
    
    def _extract_street(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait la rue depuis le HTML"""
        try:
            # 1. Recherche dans les éléments d'adresse schema.org (priorité haute)
            address_elem = soup.find('h2', {'itemprop': 'address'})
            if address_elem:
                address_text = address_elem.get_text(strip=True)
                # Format: "608 - 612, boulevard Brassard, Chambly"
                street = self._extract_street_from_address(address_text)
                if street:
                    logger.debug(f"🏠 Rue trouvée (schema.org): {street}")
                    return street
            
            # 2. Recherche dans les éléments d'adresse spécifiques
            address_elem = soup.find('span', {'data-id': 'Address'})
            if address_elem:
                street = address_elem.get_text(strip=True)
                logger.debug(f"🏠 Rue trouvée (data-id): {street}")
                return street
            
            # 3. Recherche alternative
            address_elem = soup.find('h1', class_='property-title')
            if address_elem:
                street = address_elem.get_text(strip=True)
                logger.debug(f"🏠 Rue trouvée (titre): {street}")
                return street
            
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction rue: {e}")
            return None
    
    def _extract_city(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait la ville depuis le HTML"""
        try:
            # 1. Recherche dans les éléments d'adresse spécifiques
            city_elem = soup.find('span', {'data-id': 'City'})
            if city_elem:
                city = city_elem.get_text(strip=True)
                logger.debug(f"🏙️ Ville trouvée (data-id): {city}")
                return city
            
            # 2. Recherche dans les éléments d'adresse génériques
            address_selectors = [
                'span[data-id="Address"]',
                'div.address',
                'span.address',
                '.property-address',
                '[data-id="PropertyAddress"]'
            ]
            
            for selector in address_selectors:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(strip=True)
                    # Extraire la ville depuis l'adresse complète
                    city = self._extract_city_from_address(text)
                    if city:
                        logger.debug(f"🏙️ Ville trouvée (sélecteur {selector}): {city}")
                        return city
            
            # 3. Recherche dans le contenu de la page selon la configuration
            page_text = soup.get_text()
            
            if self.config and hasattr(self.config, 'locations_searched'):
                # Utiliser les localisations de la configuration
                city_keywords = []
                for location in self.config.locations_searched:
                    if hasattr(location, 'value'):
                        city_keywords.append(location.value)
                    elif isinstance(location, dict) and 'value' in location:
                        city_keywords.append(location['value'])
                
                if city_keywords:
                    logger.debug(f"🏙️ Villes de la config: {city_keywords}")
                    for keyword in city_keywords:
                        if keyword in page_text:
                            logger.debug(f"🏙️ Ville trouvée (config): {keyword}")
                            return keyword
            
            # Fallback intelligent si pas de config
            logger.debug("🏙️ Pas de config, recherche intelligente dans le texte")
            # Chercher des mots qui ressemblent à des villes (commençant par majuscule, longueur > 3)
            words = page_text.split()
            for word in words:
                word = word.strip('.,!?;:')
                if len(word) > 3 and word[0].isupper() and word.isalpha():
                    logger.debug(f"🏙️ Ville candidate trouvée: {word}")
                    return word
            
            # 4. Recherche alternative dans l'URL ou le titre
            title_elem = soup.find('title')
            if title_elem:
                title_text = title_elem.get_text()
                # Format: "Triplex à vendre - Chambly"
                city_match = re.search(r'-\s*([^-]+)\s*$', title_text)
                if city_match:
                    city = city_match.group(1).strip()
                    logger.debug(f"🏙️ Ville trouvée (titre): {city}")
                    return city
            
            logger.warning("⚠️ Aucune ville trouvée dans la page")
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction ville: {e}")
            return None
    
    def _extract_street_from_address(self, address_text: str) -> Optional[str]:
        """Extrait la rue depuis un texte d'adresse complète"""
        try:
            # Format: "608 - 612, boulevard Brassard, Chambly"
            # Extraire la partie avant la ville (numéro + nom de rue)
            parts = address_text.split(',')
            if len(parts) >= 3:
                # Prendre les 2 premières parties : "608 - 612" + "boulevard Brassard"
                street_part = f"{parts[0].strip()}, {parts[1].strip()}"
                logger.debug(f"🏠 Rue complète extraite: {street_part}")
                return street_part
            elif len(parts) >= 2:
                # Fallback : juste la première partie si pas assez de parties
                street_part = parts[0].strip()
                logger.debug(f"🏠 Partie rue extraite (fallback): {street_part}")
                return street_part
            
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction rue depuis adresse: {e}")
            return None
    
    def _extract_city_from_address(self, address_text: str) -> Optional[str]:
        """Extrait la ville depuis un texte d'adresse"""
        try:
            # Patterns courants pour les adresses canadiennes
            patterns = [
                r'([A-Za-zÀ-ÿ]+),\s*QC?\s*[A-Z]\d[A-Z]\s*\d[A-Z]\d',  # Ville, QC A1A 1A1
                r'([A-Za-zÀ-ÿ]+),\s*Québec',  # Ville, Québec
                r'([A-Za-zÀ-ÿ]+),\s*Canada',  # Ville, Canada
                r'([A-Za-zÀ-ÿ]+)\s*\(QC\)',  # Ville (QC)
            ]
            
            for pattern in patterns:
                match = re.search(pattern, address_text)
                if match:
                    city = match.group(1).strip()
                    logger.debug(f"🏙️ Ville extraite du pattern: {city}")
                    return city
            
            # Si pas de pattern, chercher des mots qui ressemblent à des villes
            words = address_text.split(',')
            for word in words:
                word = word.strip()
                if len(word) > 2 and word[0].isupper() and word.isalpha():
                    logger.debug(f"🏙️ Ville candidate trouvée: {word}")
                    return word
            
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction ville depuis adresse: {e}")
            return None
    
    def _extract_region(self, soup: BeautifulSoup) -> str:
        """Extrait la région depuis le HTML"""
        try:
            # 1. Recherche dans le meta tag avec itemprop="name"
            meta_name = soup.find('meta', {'itemprop': 'name'})
            if meta_name:
                content = meta_name.get('content', '')
                # Format: "Triplex à vendre à Chambly, Montérégie, 608 - 612, boulevard Brassard, 10001989 - Centris.ca"
                region_match = re.search(r'à\s+([^,]+),\s+([^,]+),', content)
                if region_match:
                    region = region_match.group(2).strip()
                    logger.debug(f"🏛️ Région trouvée (meta name): {region}")
                    return region
            
            # 2. Recherche dans le titre de la page
            title_elem = soup.find('title')
            if title_elem:
                title_text = title_elem.get_text()
                # Format: "Triplex à vendre - Chambly, Montérégie"
                region_match = re.search(r'([^,]+),\s*([^,\s-]+)\s*$', title_text)
                if region_match:
                    region = region_match.group(2).strip()
                    logger.debug(f"🏛️ Région trouvée (titre): {region}")
                    return region
            
            # 3. Recherche dans le contenu de la page selon la configuration
            page_text = soup.get_text()
            
            if self.config and hasattr(self.config, 'locations_searched'):
                # Utiliser les régions de la configuration si disponibles
                region_keywords = []
                for location in self.config.locations_searched:
                    if hasattr(location, 'region'):
                        region_keywords.append(location.region)
                    elif isinstance(location, dict) and 'region' in location:
                        region_keywords.append(location['region'])
                
                if region_keywords:
                    logger.debug(f"🏛️ Régions de la config: {region_keywords}")
                    for keyword in region_keywords:
                        if keyword in page_text:
                            logger.debug(f"🏛️ Région trouvée (config): {keyword}")
                            return keyword
            
            # Fallback intelligent si pas de config
            logger.debug("🏛️ Pas de config, recherche intelligente dans le texte")
            # Chercher des mots qui ressemblent à des régions
            words = page_text.split()
            for word in words:
                word = word.strip('.,!?;:')
                if len(word) > 3 and word[0].isupper() and word.isalpha():
                    logger.debug(f"🏛️ Région candidate trouvée: {word}")
                    return word
            
            # 4. Fallback par défaut
            logger.debug("🏛️ Région non trouvée, utilisation du défaut: Québec")
            return "Québec"
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction région: {e}")
            return "Québec"
    
    def _extract_postal_code(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait le code postal depuis le HTML"""
        try:
            # Recherche dans les éléments d'adresse
            postal_elem = soup.find('span', {'data-id': 'PostalCode'})
            if postal_elem:
                postal_code = postal_elem.get_text(strip=True)
                logger.debug(f"📮 Code postal trouvé: {postal_code}")
                return postal_code
            
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction code postal: {e}")
            return None
    
    def _extract_country(self, soup: BeautifulSoup) -> str:
        """Extrait le pays (par défaut Canada)"""
        return "Canada"
    
    def _extract_coordinates(self, soup: BeautifulSoup) -> Optional[Tuple[float, float]]:
        """Extrait les coordonnées GPS depuis le HTML"""
        try:
            # Recherche dans les scripts JavaScript
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # Recherche des coordonnées dans le JavaScript
                    lat_match = re.search(r'var\s+lat\s*=\s*([-\d.]+)', script.string)
                    lng_match = re.search(r'var\s+lng\s*=\s*([-\d.]+)', script.string)
                    
                    if lat_match and lng_match:
                        try:
                            lat = float(lat_match.group(1))
                            lng = float(lng_match.group(1))
                            logger.debug(f"📍 Coordonnées GPS extraites: {lat}, {lng}")
                            return (lat, lng)
                        except ValueError:
                            logger.debug(f"⚠️ Coordonnées non numériques: {lat_match.group(1)}, {lng_match.group(1)}")
            
            # Recherche alternative dans les métadonnées
            meta_lat = soup.find('meta', {'name': 'latitude'})
            meta_lng = soup.find('meta', {'name': 'longitude'})
            
            if meta_lat and meta_lng:
                try:
                    lat = float(meta_lat.get('content'))
                    lng = float(meta_lng.get('content'))
                    logger.debug(f"📍 Coordonnées GPS (meta): {lat}, {lng}")
                    return (lat, lng)
                except ValueError:
                    logger.debug(f"⚠️ Coordonnées meta non numériques")
            
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction coordonnées: {e}")
            return None
    
    def _build_full_address(self, address_data: dict) -> str:
        """Construit l'adresse complète à partir des composants"""
        try:
            parts = []
            
            if address_data.get('street'):
                parts.append(address_data['street'])
            
            if address_data.get('city'):
                parts.append(address_data['city'])
            
            if address_data.get('region'):
                parts.append(address_data['region'])
            
            if address_data.get('postal_code'):
                parts.append(address_data['postal_code'])
            
            if address_data.get('country'):
                parts.append(address_data['country'])
            
            full_address = ', '.join(parts)
            logger.debug(f"📍 Adresse complète construite: {full_address}")
            return full_address
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur construction adresse complète: {e}")
            return ""
