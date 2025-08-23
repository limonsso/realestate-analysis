#!/usr/bin/env python3
"""
Extracteur de détails de propriétés depuis Centris.ca
Version refactorisée utilisant des extracteurs spécialisés
"""

import structlog
import re
from typing import Optional
from bs4 import BeautifulSoup

from src.models.property import (
    Property, PropertyType, PropertyStatus, Address, Location, FinancialInfo, 
    PropertyFeatures, PropertyDimensions, PropertyMedia, PropertyDescription, 
    PropertyMetadata
)
from src.utils.validators import RegionValidator, PropertyValidator, DataValidator

# Import des extracteurs spécialisés
from .extractors import AddressExtractor, FinancialExtractor, NumericExtractor

logger = structlog.get_logger()


class CentrisDetailExtractor:
    """Extracteur de détails de propriétés depuis les pages de détail"""
    
    def __init__(self):
        self.validators = {
            'region': RegionValidator(),
            'property': PropertyValidator(),
            'data': DataValidator()
        }
        
        # Initialisation des extracteurs spécialisés
        self.address_extractor = AddressExtractor()
        self.financial_extractor = FinancialExtractor()
        self.numeric_extractor = NumericExtractor()
    
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
                logger.error(f"❌ Impossible d'extraire l'ID de la propriété depuis {url}")
                return None
            
            # Extraction des différentes sections avec les extracteurs spécialisés
            address = self.address_extractor.extract_address(soup)
            financial = self.financial_extractor.extract_financial(soup)
            dimensions = self._extract_dimensions(soup)
            media = self._extract_media(soup)
            description = self._extract_description(soup)
            
            # Extraction des nouvelles informations détaillées
            # COMMENTÉ: Utilisation de NumericExtractor à la place
            # property_usage = self._extract_property_usage(soup)
            # building_style = self._extract_building_style(soup)
            # parking_info = self._extract_parking_info(soup)
            # units_info = self._extract_units_info(soup)
            # main_unit_info = self._extract_main_unit_info(soup)
            # move_in_date = self._extract_move_in_date(soup)
            # walk_score = self._extract_walk_score(soup)
            
            # Extraction des caractéristiques détaillées avec le NumericExtractor
            detailed_features = self.numeric_extractor.extract_detailed_features(soup)
            # Extraction des valeurs numériques spécifiques avec le NumericExtractor
            numeric_values = self.numeric_extractor.extract_numeric_values(soup)
            
            # Création des features à partir des extractions numériques
            features = {
                'rooms': detailed_features.get('main_unit_rooms'),
                'bedrooms': detailed_features.get('main_unit_bedrooms'),
                'bathrooms': detailed_features.get('main_unit_bathrooms'),
                'total_bedrooms': detailed_features.get('main_unit_bedrooms'),  # Simplifié pour l'instant
                'bedrooms_basement': None  # À calculer si nécessaire
            }
            
            # Extraction du type HTML exact depuis la page (ex: "Triplex")
            html_type = self._extract_html_property_type(soup)
            if not html_type:
                # Valeur par défaut basée sur l'URL ou la catégorie
                html_type = "Triplex"  # Valeur par défaut pour les plex
                logger.debug(f"🏷️ Type HTML par défaut utilisé: {html_type}")
            else:
                logger.debug(f"🏷️ Type HTML extrait: {html_type}")
            
            # Détection de la catégorie depuis l'URL (ex: "Plex")
            original_url = f"https://www.centris.ca/fr/triplex~a-vendre~chambly/{property_id}"
            property_category = self._detect_property_type(original_url)
            
            # Extraction des coordonnées GPS
            location = self._extract_location(soup)
            
            # Création de l'objet Property avec la nouvelle logique
            property_data = Property(
                id=property_id,
                type=html_type,  # Type: "Triplex" (depuis le HTML)
                category=property_category,  # Catégorie: Plex (enum)
                status=PropertyStatus.FOR_SALE,
                address=address,
                location=location,
                financial=financial,
                features=features,
                dimensions=dimensions,
                media=media,
                description=description,
                # Nouvelles informations détaillées
                # COMMENTÉ: Utilisation de detailed_features à la place
                # property_usage=property_usage,
                # building_style=building_style,
                # parking_info=parking_info,
                # units_info=units_info,
                # main_unit_info=main_unit_info,
                # move_in_date=move_in_date,
                
                # Nouvelles informations numériques extraites
                construction_year=detailed_features.get('construction_year'),
                terrain_area_sqft=detailed_features.get('terrain_area_sqft'),
                parking_count=detailed_features.get('parking_count'),
                units_count=detailed_features.get('units_count'),  # Directement depuis extract_units_numeric_details
                walk_score=numeric_values.get('walk_score'),  # Depuis numeric_values, pas detailed_features
                
                # Informations détaillées des unités
                residential_units_detail=detailed_features.get('residential_units_detail'),
                main_unit_detail=detailed_features.get('main_unit_detail'),
                # main_unit_info supprimé car redondant avec main_unit_detail
                
                # Informations générales depuis detailed_features
                property_usage=detailed_features.get('property_usage'),
                building_style=detailed_features.get('building_style'),
                parking_info=detailed_features.get('parking_info'),
                # units_info supprimé car redondant avec residential_units_detail et units_count
                move_in_date=detailed_features.get('move_in_date'),
                
                # Nouvelles informations numériques détaillées des unités (approche dynamique)
                units_2_half_count=detailed_features.get('units_2_half_count'),
                units_3_half_count=detailed_features.get('units_3_half_count'),
                units_4_half_count=detailed_features.get('units_4_half_count'),
                units_5_half_count=detailed_features.get('units_5_half_count'),
                units_6_half_count=detailed_features.get('units_6_half_count'),
                units_7_half_count=detailed_features.get('units_7_half_count'),
                units_8_half_count=detailed_features.get('units_8_half_count'),
                units_9_half_count=detailed_features.get('units_9_half_count'),
                
                # Informations de l'unité principale
                main_unit_rooms=detailed_features.get('main_unit_rooms'),
                main_unit_bedrooms=detailed_features.get('main_unit_bedrooms'),
                main_unit_bathrooms=detailed_features.get('main_unit_bathrooms'),
                
                # Champs dynamiques supplémentaires 
                # units_breakdown supprimé car redondant avec units_X_half_count
                metadata=PropertyMetadata(
                    source="Centris",
                    source_id=property_id,
                    url=url
                )
            )
            
            # Log des types extraits
            if html_type:
                logger.info(f"🏷️ Type HTML extrait: {html_type} (ex: Triplex)")
                logger.info(f"🏠 Catégorie détectée: {property_category} (ex: Plex)")
                logger.info(f"📊 Résumé: {html_type} de catégorie {property_category}")
            
            # Validation et nettoyage des données
            validated_property = self._validate_and_clean_property(property_data)
            
            if validated_property:
                logger.info(f"✅ Détails extraits pour {validated_property.address.street}")
            else:
                logger.warning(f"⚠️ Propriété {property_id} non validée")
            
            return validated_property
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des détails: {e}")
            return None
    
    # Méthodes d'extraction simplifiées (gardent la logique existante)
    def _extract_property_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait l'ID de la propriété depuis le HTML"""
        try:
            # Recherche dans les meta tags (méthode la plus fiable)
            meta_id = soup.find('meta', {'property': 'og:url'})
            if meta_id:
                url = meta_id.get('content', '')
                # Format: https://www.centris.ca/fr/triplex~a-vendre~chambly/15236505
                if '/' in url:
                    property_id = url.split('/')[-1]
                    logger.debug(f"🏷️ ID propriété extrait (og:url): {property_id}")
                    return property_id
            
            # Recherche alternative dans l'URL de la page
            url_elem = soup.find('link', {'rel': 'canonical'})
            if url_elem:
                url = url_elem.get('href')
                if url:
                    # Format: https://www.centris.ca/fr/propriete/12345678
                    match = re.search(r'/propriete/(\d+)$', url)
                    if match:
                        property_id = match.group(1)
                        logger.debug(f"🏷️ ID propriété extrait (canonical): {property_id}")
                        return property_id
            
            # Fallback: utiliser l'ID depuis l'URL passée en paramètre
            logger.debug(f"⚠️ Impossible d'extraire l'ID depuis le HTML, utilisation du fallback")
            return "temp_id"
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction ID propriété: {e}")
            return "temp_id"
    
    def _extract_features(self, soup: BeautifulSoup) -> dict:
        """Extrait les caractéristiques de base de la propriété"""
        features = {}
        
        try:
            # Extraction depuis la description
            description = self._extract_description(soup)
            if description and description.short_description:
                features.update(self._parse_features_from_description(description.short_description))
            
            # Extraction depuis le HTML
            html_features = self._extract_features_from_html(soup)
            if html_features:
                features.update(html_features)
            
            logger.debug(f"🏠 Caractéristiques extraites: {features}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction caractéristiques: {e}")
        
        return features
    
    def _extract_dimensions(self, soup: BeautifulSoup) -> dict:
        """Extrait les dimensions de la propriété"""
        dimensions = {}
        
        try:
            # Recherche dans les conteneurs de caractéristiques
            carac_containers = soup.find_all('div', class_='carac-container')
            
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                value_elem = container.find('div', class_='carac-value')
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    if 'année de construction' in title:
                        try:
                            year = int(re.search(r'\d{4}', value).group())
                            dimensions['year_built'] = year
                        except (AttributeError, ValueError):
                            pass
                    
                    elif 'superficie du terrain' in title:
                        area_match = re.search(r'(\d+(?:\s+\d+)*)', value)
                        if area_match:
                            area_text = area_match.group(1).replace(' ', '')
                            try:
                                area = int(area_text)
                                dimensions['lot_size'] = area
                                dimensions['lot_size_acres'] = area / 43560  # Conversion en acres
                            except ValueError:
                                pass
            
            logger.debug(f"📏 Dimensions extraites: {dimensions}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction dimensions: {e}")
        
        return dimensions
    
    def _extract_media(self, soup: BeautifulSoup) -> dict:
        """Extrait les médias de la propriété avec focus sur les vraies photos"""
        media = {}
        
        try:
            # 1. Extraction des vraies images de propriétés depuis les scripts JavaScript
            image_urls = []
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string:
                    # Recherche spécifique des URLs d'images de propriétés Centris
                    # Pattern pour les vraies images de propriétés (mspublic.centris.ca)
                    property_image_matches = re.findall(
                        r'https://mspublic\.centris\.ca/media\.ashx[^"\']*', 
                        script.string
                    )
                    if property_image_matches:
                        image_urls.extend(property_image_matches)
                        logger.debug(f"🖼️ {len(property_image_matches)} images de propriété trouvées dans script")
                    
                    # Pattern alternatif pour d'autres URLs d'images de propriétés
                    alt_image_matches = re.findall(
                        r'https://[^"\']*centris[^"\']*\.(?:jpg|jpeg|png|gif|webp)', 
                        script.string
                    )
                    for img in alt_image_matches:
                        if 'mspublic' in img and img not in image_urls:
                            image_urls.append(img)
            
            # 2. Extraction depuis les balises img avec filtrage pour les vraies photos
            if not image_urls:
                img_elements = soup.find_all('img')
                
                for img in img_elements:
                    src = img.get('src') or img.get('data-src')
                    if src and self._is_property_image(src):
                        # Nettoyer l'URL
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            src = 'https://www.centris.ca' + src
                        
                        if src not in image_urls:
                            image_urls.append(src)
            
            # 3. Extraction depuis les attributs data spécifiques aux galeries
            if not image_urls:
                # Rechercher dans les galeries d'images
                gallery_elements = soup.find_all(['div', 'ul'], class_=re.compile(r'gallery|photo|image', re.I))
                for gallery in gallery_elements:
                    data_elements = gallery.find_all(attrs={'data-src': True})
                    for elem in data_elements:
                        data_src = elem.get('data-src')
                        if data_src and self._is_property_image(data_src):
                            if data_src not in image_urls:
                                image_urls.append(data_src)
            
            # 4. Filtrer et nettoyer les URLs
            filtered_images = []
            for url in image_urls:
                if self._is_property_image(url) and url not in filtered_images:
                    filtered_images.append(url)
            
            # 5. Assignation des résultats
            if filtered_images:
                media['images'] = filtered_images
                media['image_count'] = len(filtered_images)
                media['main_image'] = filtered_images[0]
                logger.debug(f"🖼️ {len(filtered_images)} vraies images de propriété trouvées")
            else:
                media['images'] = []
                media['image_count'] = 0
                media['main_image'] = None
                logger.debug("🖼️ Aucune vraie image de propriété trouvée")
            
            # 6. Recherche de visite virtuelle
            virtual_tour_elem = soup.find('a', {'href': re.compile(r'virtual.*tour', re.I)})
            if virtual_tour_elem:
                media['virtual_tour_url'] = virtual_tour_elem.get('href')
                logger.debug(f"🎥 Visite virtuelle trouvée: {media['virtual_tour_url']}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction médias: {e}")
            media = {'images': [], 'image_count': 0, 'main_image': None, 'virtual_tour_url': None}
        
        return media
    
    def _is_property_image(self, url: str) -> bool:
        """Vérifie si une URL correspond à une vraie image de propriété"""
        if not url:
            return False
        
        # URLs à exclure (images du site, pas de la propriété)
        exclude_patterns = [
            'consumersite/images',  # Images du site Centris
            'menu/',                # Images de menu
            'blog_',                # Images de blog
            'guide-',               # Images de guides
            'logo',                 # Logos
            'icon',                 # Icônes
            'button',               # Boutons
            'banner',               # Bannières
        ]
        
        for pattern in exclude_patterns:
            if pattern in url.lower():
                return False
        
        # URLs à inclure (vraies images de propriétés)
        include_patterns = [
            'mspublic.centris.ca/media.ashx',  # Images de propriétés Centris
            'centris.ca/image/',               # Images directes
            'centris.ca/photo/',               # Photos directes
        ]
        
        for pattern in include_patterns:
            if pattern in url.lower():
                return True
        
        # Si c'est une image et qu'elle contient "centris", probablement valide
        if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            if 'centris' in url.lower() and 'mspublic' in url.lower():
                return True
        
        return False
    
    def _extract_description(self, soup: BeautifulSoup) -> dict:
        """Extrait la description de la propriété"""
        description = {}
        
        try:
            # Description courte depuis le titre
            title_elem = soup.find('title')
            if title_elem:
                title_text = title_elem.get_text(strip=True)
                description['short_description'] = title_text
            
            # Description longue depuis le contenu
            desc_elem = soup.find('div', class_='property-description')
            if desc_elem:
                desc_text = desc_elem.get_text(strip=True)
                description['long_description'] = desc_text
                
                # Nettoyage de la description
                if description['long_description']:
                    description['long_description'] = self.validators['data'].clean_text(description['long_description'])
            
            # Nettoyage de la description courte
            if description.get('short_description'):
                description['short_description'] = self.validators['data'].clean_text(description['short_description'])
            
            logger.debug(f"📝 Description extraite et nettoyée: {description.get('short_description', '')[:100]}...")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction description: {e}")
        
        return description
    
    # Méthodes d'extraction des nouvelles informations détaillées
    def _extract_property_usage(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait l'utilisation de la propriété (ex: Résidentielle)"""
        try:
            logger.debug("🔍 Début extraction utilisation propriété")
            carac_containers = soup.find_all('div', class_='carac-container')
            logger.debug(f"🔍 Trouvé {len(carac_containers)} conteneurs carac-container")
            
            for i, container in enumerate(carac_containers):
                title_elem = container.find('div', class_='carac-title')
                if title_elem:
                    title_text = title_elem.get_text(strip=True).lower()
                    logger.debug(f"🔍 Conteneur {i}: titre = '{title_text}'")
                    
                    if 'utilisation' in title_text and 'propriété' in title_text:
                        value_elem = container.find('div', class_='carac-value')
                        if value_elem:
                            value = value_elem.get_text(strip=True)
                            logger.debug(f"🏠 Utilisation trouvée: {value}")
                            return value
            
            logger.debug("🔍 Aucune utilisation trouvée")
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction utilisation propriété: {e}")
            return None
    
    def _extract_building_style(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait le style de bâtiment (ex: Jumelé)"""
        try:
            carac_containers = soup.find_all('div', class_='carac-container')
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                if title_elem:
                    title_text = title_elem.get_text(strip=True).lower()
                    if 'style' in title_text and 'bâtiment' in title_text:
                        value_elem = container.find('div', class_='carac-value')
                        if value_elem:
                            value = value_elem.get_text(strip=True)
                            logger.debug(f"🏗️ Style bâtiment trouvé: {value}")
                            return value
            return None
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction style bâtiment: {e}")
            return None
    
    def _extract_parking_info(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait les informations de stationnement"""
        try:
            carac_containers = soup.find_all('div', class_='carac-container')
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                if title_elem:
                    title_text = title_elem.get_text(strip=True).lower()
                    if 'stationnement total' in title_text:
                        value_elem = container.find('div', class_='carac-value')
                        if value_elem:
                            value = value_elem.get_text(strip=True)
                            logger.debug(f"🚗 Stationnement trouvé: {value}")
                            return value
            return None
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction stationnement: {e}")
            return None
    
    # Méthode _extract_units_info supprimée car redondante avec extract_units_numeric_details
    
    # Méthode _extract_main_unit_info supprimée car redondante avec extract_main_unit_numeric_details
    
    def _extract_move_in_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait la date d'emménagement"""
        try:
            carac_containers = soup.find_all('div', class_='carac-container')
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                if title_elem:
                    title_text = title_elem.get_text(strip=True).lower()
                    if 'date d\'emménagement' in title_text:
                        value_elem = container.find('div', class_='carac-value')
                        if value_elem:
                            value = value_elem.get_text(strip=True)
                            logger.debug(f"📅 Date d'emménagement trouvée: {value}")
                            return value
            return None
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction date d'emménagement: {e}")
            return None
    
    def _extract_walk_score(self, soup: BeautifulSoup) -> Optional[int]:
        """Extrait le Walk Score depuis le HTML avec recherche étendue"""
        try:
            logger.debug("🔍 Début extraction Walk Score")
            
            # 1. Recherche dans les éléments avec classe 'walkscore'
            walkscore_elem = soup.find('div', class_='walkscore')
            if walkscore_elem:
                score_elem = walkscore_elem.find('span')
                if score_elem:
                    score_text = score_elem.get_text(strip=True)
                    try:
                        score = int(score_text)
                        logger.debug(f"🚶 Walk Score trouvé (walkscore): {score}")
                        return score
                    except ValueError:
                        logger.debug(f"⚠️ Walk Score non numérique: {score_text}")
            
            # 2. Recherche dans le texte contenant "Walk Score" ou "Score de marche"
            walk_score_patterns = [
                r'walk\s*score[:\s]*(\d+)',
                r'score\s*de\s*marche[:\s]*(\d+)',
                r'walkscore[:\s]*(\d+)',
                r'(\d+)\s*walkscore',
                r'(\d+)\s*score\s*de\s*marche'
            ]
            
            page_text = soup.get_text()
            for pattern in walk_score_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    try:
                        score = int(match.group(1))
                        logger.debug(f"🚶 Walk Score trouvé (regex): {score}")
                        return score
                    except ValueError:
                        continue
            
            # 3. Recherche dans les scripts JavaScript
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    for pattern in walk_score_patterns:
                        match = re.search(pattern, script.string, re.IGNORECASE)
                        if match:
                            try:
                                score = int(match.group(1))
                                logger.debug(f"🚶 Walk Score trouvé (script): {score}")
                                return score
                            except ValueError:
                                continue
            
            logger.debug("🔍 Aucun Walk Score trouvé")
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction Walk Score: {e}")
            return None
    
    # Méthodes utilitaires
    def _extract_html_property_type(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait le type de propriété depuis le HTML (ex: "Triplex")"""
        try:
            # Recherche dans le titre de la page
            title_elem = soup.find('title')
            if title_elem:
                title_text = title_elem.get_text()
                # Format: "Triplex à vendre à Chambly, Montérégie, 608..."
                # Extraire seulement le premier mot (le type de propriété)
                type_match = re.search(r'^([A-Za-zÀ-ÿ]+)', title_text)
                if type_match:
                    property_type = type_match.group(1).strip()
                    logger.debug(f"🏷️ Type HTML trouvé dans PageTitle: {property_type}")
                    return property_type
            
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction type HTML: {e}")
            return None
    
    def _detect_property_type(self, url: str) -> PropertyType:
        """Détecte le type de propriété depuis l'URL"""
        try:
            if 'plex' in url.lower():
                return PropertyType.PLEX
            elif 'condo' in url.lower():
                return PropertyType.SELL_CONDO
            elif 'maison' in url.lower():
                return PropertyType.SINGLE_FAMILY_HOME
            else:
                return PropertyType.RESIDENTIAL_LOT
        except Exception as e:
            logger.debug(f"⚠️ Erreur détection type propriété: {e}")
            return PropertyType.PLEX
    
    def _extract_location(self, soup: BeautifulSoup) -> Optional[Location]:
        """Extrait les coordonnées GPS pour créer un objet Location"""
        try:
            coordinates = self.address_extractor._extract_coordinates(soup)
            if coordinates:
                lat, lng = coordinates
                location = Location(latitude=lat, longitude=lng)
                logger.debug(f"📍 Coordonnées GPS extraites: {lat}, {lng}")
                return location
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction location: {e}")
            return None
    
    # Méthodes de validation et nettoyage
    def _validate_and_clean_property(self, property_data: Property) -> Property:
        """Valide et nettoie les données d'une propriété"""
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
    
    # Méthodes utilitaires pour l'extraction des caractéristiques
    def _parse_features_from_description(self, description: str) -> dict:
        """Parse les caractéristiques depuis la description"""
        features = {}
        
        try:
            # Recherche des caractéristiques dans la description
            if '5½' in description or '5 1/2' in description:
                features['bedrooms'] = 3
                features['total_bedrooms'] = 7
            elif '4½' in description or '4 1/2' in description:
                features['bedrooms'] = 2
                features['total_bedrooms'] = 6
            
            # Recherche du nombre de pièces
            rooms_match = re.search(r'(\d+)\s*pièces?', description)
            if rooms_match:
                features['rooms'] = int(rooms_match.group(1))
            
            # Recherche du nombre de chambres
            bedrooms_match = re.search(r'(\d+)\s*chambres?', description)
            if bedrooms_match:
                features['bedrooms'] = int(bedrooms_match.group(1))
            
            # Recherche du nombre de salles de bain
            bathrooms_match = re.search(r'(\d+)\s*salles?\s*de\s*bain', description)
            if bathrooms_match:
                features['bathrooms'] = int(bathrooms_match.group(1))
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur parsing description: {e}")
        
        return features
    
    def _extract_features_from_html(self, soup: BeautifulSoup) -> dict:
        """Extrait les caractéristiques depuis les éléments HTML"""
        features = {}
        
        try:
            # Recherche des caractéristiques dans les conteneurs carac-container
            carac_containers = soup.find_all('div', {'class': 'carac-container'})
            
            for container in carac_containers:
                title_elem = container.find('div', {'class': 'carac-title'})
                value_elem = container.find('div', {'class': 'carac-value'})
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    # Traitement des caractéristiques spécifiques
                    if 'unités résidentielles' in title:
                        # Format: "1 x 4 ½, 2 x 5 ½"
                        features.update(self._parse_units_from_text(value))
                    elif 'unité principale' in title:
                        # Format: "5 pièces, 3 chambres, 1 salle de bain"
                        features.update(self._parse_main_unit_from_text(value))
                    elif 'garage' in title:
                        # Format: "Garage (1)"
                        garage_match = re.search(r'\((\d+)\)', value)
                        if garage_match:
                            features['garages'] = int(garage_match.group(1))
            
            logger.debug(f"🏠 Caractéristiques HTML extraites: {features}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction HTML: {e}")
        
        return features
    
    def _parse_units_from_text(self, text: str) -> dict:
        """Parse les unités depuis le texte"""
        features = {}
        
        try:
            # Format: "1 x 4 ½, 2 x 5 ½"
            five_half_count = text.count('5½') + text.count('5 1/2')
            four_half_count = text.count('4½') + text.count('4 1/2')
            
            if five_half_count > 0:
                features['bedrooms_basement'] = five_half_count * 3
            if four_half_count > 0:
                features['bedrooms_basement'] = (features.get('bedrooms_basement', 0) + 
                                               four_half_count * 2)
            
            # Calcul du total des chambres
            total_bedrooms = (features.get('bedrooms', 0) + 
                             features.get('bedrooms_basement', 0))
            if total_bedrooms > 0:
                features['total_bedrooms'] = total_bedrooms
            
            # Calcul du nombre de salles de bain
            if five_half_count > 0 or four_half_count > 0:
                features['bathrooms'] = five_half_count + four_half_count
            
            logger.debug(f"🏠 Caractéristiques extraites: {five_half_count} unités 5½, {four_half_count} unités 4½")
        
        except Exception as e:
            logger.debug(f"⚠️ Erreur parsing description: {e}")
        
        return features
    
    def _parse_main_unit_from_text(self, text: str) -> dict:
        """Parse l'unité principale depuis le texte"""
        features = {}
        
        try:
            # Format: "5 pièces, 3 chambres, 1 salle de bain"
            rooms_match = re.search(r'(\d+)\s*pièces?', text)
            if rooms_match:
                features['rooms'] = int(rooms_match.group(1))
            
            bedrooms_match = re.search(r'(\d+)\s*chambres?', text)
            if bedrooms_match:
                features['bedrooms'] = int(bedrooms_match.group(1))
            
            bathrooms_match = re.search(r'(\d+)\s*salles?\s*de\s*bain', text)
            if bathrooms_match:
                features['bathrooms'] = int(bathrooms_match.group(1))
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur parsing unité principale: {e}")
        
        return features
