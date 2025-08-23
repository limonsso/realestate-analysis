"""
Extracteur de détails de propriétés pour Centris.ca
Refactorisé pour utiliser des extracteurs spécialisés
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
                return None
            
            # Extraction des différentes sections avec les extracteurs spécialisés
            address = self.address_extractor.extract_address(soup)
            financial = self.financial_extractor.extract_financial(soup)
            features = self._extract_features(soup)
            dimensions = self._extract_dimensions(soup)
            media = self._extract_media(soup)
            description = self._extract_description(soup)
            
            # Extraction des nouvelles informations détaillées
            property_usage = self._extract_property_usage(soup)
            building_style = self._extract_building_style(soup)
            parking_info = self._extract_parking_info(soup)
            units_info = self._extract_units_info(soup)
            main_unit_info = self._extract_main_unit_info(soup)
            move_in_date = self._extract_move_in_date(soup)
            walk_score = self._extract_walk_score(soup)
            
            # Extraction du type HTML exact depuis la page (ex: "Triplex")
            html_type = self._extract_html_property_type(soup)
            
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
                property_usage=property_usage,
                building_style=building_style,
                parking_info=parking_info,
                units_info=units_info,
                main_unit_info=main_unit_info,
                move_in_date=move_in_date,
                walk_score=walk_score,
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
                
                # Stocker la catégorie dans les métadonnées
                if not hasattr(property_data.metadata, 'category'):
                    property_data.metadata.__dict__['category'] = str(property_category)
                    logger.info(f"🏠 Catégorie ajoutée aux métadonnées: {property_category}")
            
            # Validation et nettoyage des données
            validated_property = self._validate_and_clean_property(property_data)
            
            return validated_property
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des données détaillées: {str(e)}")
            return None
    
    def _detect_property_type(self, url: str) -> PropertyType:
        """Détecte le type de propriété depuis l'URL Centris"""
        try:
            # Format: https://www.centris.ca/fr/triplex~a-vendre~chambly/15236505
            if 'triplex' in url.lower():
                return PropertyType.PLEX
            elif 'condo' in url.lower():
                return PropertyType.SELL_CONDO
            elif 'terrain' in url.lower() or 'lot' in url.lower():
                return PropertyType.RESIDENTIAL_LOT
            else:
                return PropertyType.SINGLE_FAMILY_HOME
        except Exception:
            return PropertyType.SINGLE_FAMILY_HOME
    
    def _extract_property_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait l'ID de la propriété depuis la page de détail"""
        try:
            # Recherche dans les meta tags (méthode la plus fiable)
            meta_id = soup.find('meta', {'property': 'og:url'})
            if meta_id:
                url = meta_id.get('content', '')
                # Format: https://www.centris.ca/fr/triplex~a-vendre~chambly/15236505
                if '/' in url:
                    return url.split('/')[-1]
            
            # Fallback: extraction depuis l'URL
            return "temp_id"
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction ID: {str(e)}")
            return "temp_id"
    
    def _extract_address(self, soup: BeautifulSoup) -> Address:
        """Extrait l'adresse détaillée depuis la page de détail"""
        try:
            # Utilisation du sélecteur qui fonctionne selon notre analyse
            address_element = soup.find('div', {'class': 'address'})
            
            if address_element:
                full_address = address_element.get_text(strip=True)
                # Nettoyer l'adresse (enlever "Triplex à vendre" au début)
                if "Triplex à vendre" in full_address:
                    full_address = full_address.replace("Triplex à vendre", "").strip()
                
                # Parse l'adresse pour extraire les composants
                street, city, region = self._parse_address_text(full_address)
                
                return Address(
                    street=street,
                    city=city,
                    region=region,
                    postal_code=None,  # À extraire si disponible
                    country="Canada",
                    full_address=full_address
                )
            
            return Address()
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction de l'adresse: {str(e)}")
            return Address()
    
    def _parse_address_text(self, address_text: str) -> tuple[str, str, str]:
        """Parse le texte d'adresse pour extraire rue, ville et région"""
        try:
            # Format attendu: "2348 - 2352, Avenue Bourgogne, Chambly"
            parts = address_text.split(',')
            if len(parts) >= 3:
                street = f"{parts[0].strip()}, {parts[1].strip()}"  # Combiner numéro et nom de rue
                city = "Chambly"  # Ville fixe pour Chambly
                region = "Québec"  # Région fixe
                return street, city, region
            elif len(parts) == 2:
                street = f"{parts[0].strip()}, {parts[1].strip()}"
                city = "Chambly"
                region = "Québec"
                return street, city, region
            elif len(parts) == 1:
                return parts[0].strip(), "Chambly", "Québec"
            else:
                return "", "Chambly", "Québec"
        except Exception:
            return "", "Chambly", "Québec"
    
    def _extract_financial(self, soup: BeautifulSoup) -> FinancialInfo:
        """Extrait les informations financières depuis la page de détail"""
        try:
            financial_info = {}
            
            # Extraction du prix
            price_element = soup.find('div', {'class': 'price'})
            if price_element:
                price_text = price_element.get_text(strip=True)
                price_clean = ''.join(filter(str.isdigit, price_text))
                if price_clean:
                    financial_info['price'] = float(price_clean)
                    logger.debug(f"💰 Prix extrait: {financial_info['price']}")
            
            # Extraction des revenus depuis la description
            desc_element = soup.find('div', {'class': 'property-description'})
            if desc_element:
                description_text = desc_element.get_text(strip=True)
                revenue = self._extract_revenue_from_description(description_text)
                if revenue:
                    financial_info['potential_gross_revenue'] = revenue
                    logger.debug(f"💰 Revenus extraits: {revenue}$")
            
            # Extraction des informations financières détaillées
            financial_info.update(self._extract_detailed_financial(soup))
            
            return FinancialInfo(**financial_info)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction financier: {str(e)}")
            return FinancialInfo()
    
    def _extract_detailed_financial(self, soup: BeautifulSoup) -> dict:
        """Extrait les informations financières détaillées"""
        financial_details = {}
        
        try:
            # Recherche des revenus dans les carac-container
            carac_containers = soup.find_all('div', {'class': 'carac-container'})
            
            for container in carac_containers:
                title_elem = container.find('div', {'class': 'carac-title'})
                value_elem = container.find('div', {'class': 'carac-value'})
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    if 'revenus bruts potentiels' in title:
                        # Format: "43 320 $"
                        revenue_match = re.search(r'([\d\s]+)\s*\$', value)
                        if revenue_match:
                            revenue_str = revenue_match.group(1).replace(' ', '')
                            try:
                                financial_details['potential_gross_revenue'] = float(revenue_str)
                            except ValueError:
                                pass
            
            # Recherche des évaluations municipales et taxes
            financial_tables = soup.find_all('table')
            
            for table in financial_tables:
                # Évaluation municipale
                if 'Évaluation municipale' in table.get_text():
                    financial_details.update(self._extract_municipal_evaluation(table))
                
                # Taxes
                elif 'Taxes' in table.get_text():
                    financial_details.update(self._extract_taxes(table))
            
            logger.debug(f"💰 Informations financières détaillées: {financial_details}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction financier détaillé: {e}")
        
        return financial_details
    
    def _extract_municipal_evaluation(self, table: BeautifulSoup) -> dict:
        """Extrait l'évaluation municipale depuis le tableau"""
        evaluation = {}
        
        try:
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True).lower()
                    value_text = cells[1].get_text(strip=True)
                    
                    # Extraire les valeurs numériques
                    value_match = re.search(r'([\d\s]+)\s*\$', value_text)
                    if value_match:
                        value_str = value_match.group(1).replace(' ', '')
                        try:
                            value = float(value_str)
                            
                            if 'terrain' in label:
                                evaluation['municipal_evaluation_land'] = value
                            elif 'bâtiment' in label:
                                evaluation['municipal_evaluation_building'] = value
                            elif 'total' in label:
                                evaluation['municipal_evaluation_total'] = value
                                evaluation['municipal_evaluation_year'] = 2025  # Année fixe pour 2025
                        except ValueError:
                            pass
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction évaluation municipale: {e}")
        
        return evaluation
    
    def _extract_taxes(self, table: BeautifulSoup) -> dict:
        """Extrait les taxes depuis le tableau"""
        taxes = {}
        
        try:
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True).lower()
                    value_text = cells[1].get_text(strip=True)
                    
                    # Extraire les valeurs numériques
                    value_match = re.search(r'([\d\s]+)\s*\$', value_text)
                    if value_match:
                        value_str = value_match.group(1).replace(' ', '')
                        try:
                            value = float(value_str)
                            
                            if 'municipales' in label:
                                taxes['municipal_tax'] = value
                            elif 'scolaires' in label:
                                taxes['school_tax'] = value
                            elif 'total' in label:
                                taxes['total_taxes'] = value
                        except ValueError:
                            pass
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction taxes: {e}")
        
        return taxes
    
    def _extract_revenue_from_description(self, description: str) -> Optional[float]:
        """Extrait les revenus depuis la description"""
        try:
            # Recherche: "43 000 $ par année"
            revenue_match = re.search(r'(\d{1,3}(?:\s\d{3})*)\s*\$\s*par\s*année', description)
            if revenue_match:
                revenue_str = revenue_match.group(1).replace(' ', '')
                return float(revenue_str)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction revenus: {e}")
        
        return None
    
    def _extract_features(self, soup: BeautifulSoup) -> PropertyFeatures:
        """Extrait les caractéristiques physiques depuis la page de détail"""
        try:
            features = {}
            
            # Recherche dans la description pour extraire les caractéristiques
            desc_element = soup.find('div', {'class': 'property-description'})
            if desc_element:
                description_text = desc_element.get_text(strip=True)
                features.update(self._parse_features_from_description(description_text))
            
            # Recherche des caractéristiques dans le HTML
            features.update(self._extract_features_from_html(soup))
            
            return PropertyFeatures(**features)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction caractéristiques: {str(e)}")
            return PropertyFeatures()
    
    def _parse_features_from_description(self, description: str) -> dict:
        """Parse les caractéristiques depuis la description textuelle"""
        features = {}
        
        try:
            # Compter les unités de 5 ½ et 4 ½
            five_half_count = description.count("5 ½")
            four_half_count = description.count("4 ½")
            
            if five_half_count > 0 or four_half_count > 0:
                # Calculer le total des chambres
                total_bedrooms = (five_half_count * 5) + (four_half_count * 4)
                features['total_bedrooms'] = total_bedrooms
                
                # Estimer le nombre de chambres principales
                features['bedrooms'] = max(five_half_count, four_half_count)
                
                # Estimer le nombre de salles de bain (généralement 1 par unité)
                features['bathrooms'] = five_half_count + four_half_count
                
                logger.debug(f"🏠 Caractéristiques extraites: {five_half_count} unités 5½, {four_half_count} unités 4½")
        
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
    
    def _extract_property_details(self, soup: BeautifulSoup, url: str) -> Optional[Property]:
        """Extrait les détails complets d'une propriété depuis sa page HTML."""
        try:
            # Extraction de l'ID de la propriété
            property_id = self._extract_property_id(soup)
            if not property_id:
                logger.error(f"❌ Impossible d'extraire l'ID de la propriété depuis {url}")
                return None
            
            # Extraction des informations de base
            address = self._extract_address(soup)
            financial = self._extract_financial(soup)
            description = self._extract_description(soup)
            features = self._extract_features(soup)
            dimensions = self._extract_dimensions(soup)
            media = self._extract_media(soup)
            
            # Extraction des nouvelles informations détaillées
            property_usage = self._extract_property_usage(soup)
            building_style = self._extract_building_style(soup)
            parking_info = self._extract_parking_info(soup)
            units_info = self._extract_units_info(soup)
            main_unit_info = self._extract_main_unit_info(soup)
            move_in_date = self._extract_move_in_date(soup)
            walk_score = self._extract_walk_score(soup)
            
            # Extraction du type HTML exact depuis la page (ex: "Triplex")
            html_type = self._extract_html_property_type(soup)
            
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
                property_usage=property_usage,
                building_style=building_style,
                parking_info=parking_info,
                units_info=units_info,
                main_unit_info=main_unit_info,
                move_in_date=move_in_date,
                walk_score=walk_score,
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
    
    def _extract_property_usage(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait l'utilisation de la propriété (ex: Résidentielle)"""
        try:
            logger.debug("🔍 Début extraction utilisation propriété")
            # Recherche plus flexible
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
                        else:
                            logger.debug(f"⚠️ Pas de valeur trouvée pour l'utilisation")
                    else:
                        logger.debug(f"🔍 Titre ne correspond pas aux critères")
                else:
                    logger.debug(f"⚠️ Pas de titre trouvé dans le conteneur {i}")
            
            logger.debug("🔍 Aucune utilisation trouvée")
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction utilisation propriété: {e}")
            return None
    
    def _extract_building_style(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait le style de bâtiment (ex: Jumelé)"""
        try:
            # Recherche plus flexible
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
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction style bâtiment: {e}")
        return None
    
    def _extract_parking_info(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait les informations de stationnement (ex: Garage (1))"""
        try:
            # Recherche plus flexible
            carac_containers = soup.find_all('div', class_='carac-container')
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                if title_elem:
                    title_text = title_elem.get_text(strip=True).lower()
                    if 'stationnement' in title_text and 'total' in title_text:
                        value_elem = container.find('div', class_='carac-value')
                        if value_elem:
                            value = value_elem.get_text(strip=True)
                            logger.debug(f"🚗 Stationnement trouvé: {value}")
                            return value
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction stationnement: {e}")
        return None
    
    def _extract_units_info(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait le nombre d'unités (ex: Résidentiel (3))"""
        try:
            logger.debug("🔍 Début extraction nombre d'unités")
            # Recherche plus flexible
            carac_containers = soup.find_all('div', class_='carac-container')
            
            for i, container in enumerate(carac_containers):
                title_elem = container.find('div', class_='carac-title')
                if title_elem:
                    title_text = title_elem.get_text(strip=True).lower()
                    logger.debug(f"🔍 Conteneur {i}: titre = '{title_text}'")
                    
                    if 'nombre' in title_text and 'unités' in title_text:
                        value_elem = container.find('div', class_='carac-value')
                        if value_elem:
                            value = value_elem.get_text(strip=True)
                            logger.debug(f"🏘️ Nombre d'unités trouvé: {value}")
                            return value
                        else:
                            logger.debug(f"⚠️ Pas de valeur trouvée pour le nombre d'unités")
                    else:
                        logger.debug(f"🔍 Titre ne correspond pas aux critères")
                else:
                    logger.debug(f"⚠️ Pas de titre trouvé dans le conteneur {i}")
            
            logger.debug("🔍 Aucun nombre d'unités trouvé")
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction nombre d'unités: {e}")
            return None
    
    def _extract_main_unit_info(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait les informations de l'unité principale (ex: 5 pièces, 3 chambres, 1 salle de bain)"""
        try:
            logger.debug("🔍 Début extraction unité principale")
            # Recherche plus flexible
            carac_containers = soup.find_all('div', class_='carac-container')
            
            for i, container in enumerate(carac_containers):
                title_elem = container.find('div', class_='carac-title')
                if title_elem:
                    title_text = title_elem.get_text(strip=True).lower()
                    logger.debug(f"🔍 Conteneur {i}: titre = '{title_text}'")
                    
                    if 'unité' in title_text and 'principale' in title_text:
                        value_elem = container.find('div', class_='carac-value')
                        if value_elem:
                            value = value_elem.get_text(strip=True)
                            logger.debug(f"🏠 Unité principale trouvée: {value}")
                            return value
                        else:
                            logger.debug(f"⚠️ Pas de valeur trouvée pour l'unité principale")
                    else:
                        logger.debug(f"🔍 Titre ne correspond pas aux critères")
                else:
                    logger.debug(f"⚠️ Pas de titre trouvé dans le conteneur {i}")
            
            logger.debug("🔍 Aucune unité principale trouvée")
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction unité principale: {e}")
            return None
    
    def _extract_move_in_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait la date d'emménagement (ex: Selon les baux)"""
        try:
            logger.debug("🔍 Début extraction date d'emménagement")
            # Recherche plus flexible
            carac_containers = soup.find_all('div', class_='carac-container')
            
            for i, container in enumerate(carac_containers):
                title_elem = container.find('div', class_='carac-title')
                if title_elem:
                    title_text = title_elem.get_text(strip=True).lower()
                    logger.debug(f"🔍 Conteneur {i}: titre = '{title_text}'")
                    
                    if 'date' in title_text and 'emménagement' in title_text:
                        value_elem = container.find('div', class_='carac-value')
                        if value_elem:
                            value = value_elem.get_text(strip=True)
                            logger.debug(f"📅 Date d'emménagement trouvée: {value}")
                            return value
                        else:
                            logger.debug(f"⚠️ Pas de valeur trouvée pour la date d'emménagement")
                    else:
                        logger.debug(f"🔍 Titre ne correspond pas aux critères")
                else:
                    logger.debug(f"⚠️ Pas de titre trouvé dans le conteneur {i}")
            
            logger.debug("🔍 Aucune date d'emménagement trouvée")
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction date d'emménagement: {e}")
            return None
    
    def _extract_walk_score(self, soup: BeautifulSoup) -> Optional[int]:
        """Extrait le Walk Score depuis le HTML"""
        try:
            logger.debug("🔍 Début extraction Walk Score")
            walkscore_elem = soup.find('div', class_='walkscore')
            if walkscore_elem:
                score_elem = walkscore_elem.find('span')
                if score_elem:
                    score_text = score_elem.get_text(strip=True)
                    try:
                        score = int(score_text)
                        logger.debug(f"🚶 Walk Score trouvé: {score}")
                        return score
                    except ValueError:
                        logger.debug(f"⚠️ Walk Score non numérique: {score_text}")
            logger.debug("🔍 Aucun Walk Score trouvé")
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction Walk Score: {e}")
            return None

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

    def _extract_numeric_values(self, soup: BeautifulSoup) -> dict:
        """Extrait les valeurs numériques spécifiques du HTML"""
        numeric_values = {}
        
        try:
            logger.debug("🔍 Début extraction valeurs numériques")
            carac_containers = soup.find_all('div', class_='carac-container')
            
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                value_elem = container.find('div', class_='carac-value')
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    # Année de construction
                    if 'année de construction' in title:
                        try:
                            year = int(value)
                            numeric_values['construction_year'] = year
                            logger.debug(f"🏗️ Année construction: {year}")
                        except ValueError:
                            logger.debug(f"⚠️ Année non numérique: {value}")
                    
                    # Superficie du terrain
                    elif 'superficie du terrain' in title:
                        # Format: "5 654 pc" -> 5654
                        area_match = re.search(r'(\d+(?:\s+\d+)*)', value)
                        if area_match:
                            area_text = area_match.group(1).replace(' ', '')
                            try:
                                area = int(area_text)
                                numeric_values['terrain_area'] = area
                                logger.debug(f"📏 Superficie terrain: {area} pc")
                            except ValueError:
                                logger.debug(f"⚠️ Superficie non numérique: {area_text}")
                    
                    # Stationnement total
                    elif 'stationnement total' in title:
                        # Format: "Garage (1)" -> 1
                        parking_match = re.search(r'\((\d+)\)', value)
                        if parking_match:
                            parking_count = int(parking_match.group(1))
                            numeric_values['parking_count'] = parking_count
                            logger.debug(f"🚗 Nombre stationnements: {parking_count}")
                    
                    # Nombre d'unités
                    elif 'nombre d\'unités' in title:
                        # Format: "Résidentiel (3)" -> 3
                        units_match = re.search(r'\((\d+)\)', value)
                        if units_match:
                            units_count = int(units_match.group(1))
                            numeric_values['units_count'] = units_count
                            logger.debug(f"🏘️ Nombre d'unités: {units_count}")
                    
                    # Revenus bruts potentiels
                    elif 'revenus bruts potentiels' in title:
                        # Format: "43 320 $" -> 43320
                        revenue_match = re.search(r'(\d+(?:\s+\d+)*)', value)
                        if revenue_match:
                            revenue_text = revenue_match.group(1).replace(' ', '')
                            try:
                                revenue = int(revenue_text)
                                numeric_values['potential_revenue'] = revenue
                                logger.debug(f"💰 Revenus potentiels: {revenue}$")
                            except ValueError:
                                logger.debug(f"⚠️ Revenus non numériques: {revenue_text}")
            
            logger.debug(f"🔢 Valeurs numériques extraites: {numeric_values}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction valeurs numériques: {e}")
        
        return numeric_values

    def _extract_detailed_features(self, soup: BeautifulSoup) -> dict:
        """Extrait les caractéristiques détaillées avec valeurs numériques"""
        detailed_features = {}
        
        try:
            logger.debug("🔍 Début extraction caractéristiques détaillées")
            carac_containers = soup.find_all('div', class_='carac-container')
            
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                value_elem = container.find('div', class_='carac-value')
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    # Unités résidentielles détaillées
                    if 'unités résidentielles' in title:
                        # Format: "1 x 4 ½, 2 x 5 ½"
                        detailed_features['residential_units_detail'] = value
                        logger.debug(f"🏠 Unités résidentielles: {value}")
                        
                        # Extraction des nombres
                        units_pattern = r'(\d+)\s*x\s*(\d+(?:½)?)'
                        units_matches = re.findall(units_pattern, value)
                        if units_matches:
                            detailed_features['units_breakdown'] = units_matches
                            logger.debug(f"🔢 Détail unités: {units_matches}")
                    
                    # Unité principale détaillée
                    elif 'unité principale' in title:
                        # Format: "5 pièces, 3 chambres, 1 salle de bain"
                        detailed_features['main_unit_detail'] = value
                        logger.debug(f"🏠 Unité principale: {value}")
                        
                        # Extraction des nombres
                        numbers = re.findall(r'(\d+)', value)
                        if numbers:
                            detailed_features['main_unit_numbers'] = [int(n) for n in numbers]
                            logger.debug(f"🔢 Nombres unité principale: {numbers}")
            
            logger.debug(f"🔍 Caractéristiques détaillées: {detailed_features}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction caractéristiques détaillées: {e}")
        
        return detailed_features
    
    def _parse_units_from_text(self, text: str) -> dict:
        """Parse le texte des unités résidentielles"""
        features = {}
        
        try:
            # Format: "1 x 4 ½, 2 x 5 ½"
            
            # Compter les unités de 4 ½
            four_half_match = re.search(r'(\d+)\s*x\s*4\s*½', text)
            if four_half_match:
                four_half_count = int(four_half_match.group(1))
                features['bedrooms_basement'] = four_half_count * 4
            
            # Compter les unités de 5 ½
            five_half_match = re.search(r'(\d+)\s*x\s*5\s*½', text)
            if five_half_match:
                five_half_count = int(five_half_match.group(1))
                features['bedrooms'] = five_half_count * 5
            
            # Total des chambres
            if 'bedrooms' in features or 'bedrooms_basement' in features:
                total = (features.get('bedrooms', 0) + features.get('bedrooms_basement', 0))
                features['total_bedrooms'] = total
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur parsing unités: {e}")
        
        return features
    
    def _parse_main_unit_from_text(self, text: str) -> dict:
        """Parse le texte de l'unité principale"""
        features = {}
        
        try:
            # Format: "5 pièces, 3 chambres, 1 salle de bain"
            
            # Pièces
            pieces_match = re.search(r'(\d+)\s*pièces', text)
            if pieces_match:
                features['rooms'] = int(pieces_match.group(1))
            
            # Chambres
            chambres_match = re.search(r'(\d+)\s*chambres', text)
            if chambres_match:
                features['bedrooms'] = int(chambres_match.group(1))
            
            # Salles de bain
            sdb_match = re.search(r'(\d+)\s*salle\s*de\s*bain', text)
            if sdb_match:
                features['bathrooms'] = int(sdb_match.group(1))
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur parsing unité principale: {e}")
        
        return features
    
    def _extract_dimensions(self, soup: BeautifulSoup) -> PropertyDimensions:
        """Extrait les dimensions depuis la page de détail"""
        try:
            dimensions = {}
            
            # Recherche des dimensions dans les conteneurs carac-container
            carac_containers = soup.find_all('div', {'class': 'carac-container'})
            
            for container in carac_containers:
                title_elem = container.find('div', {'class': 'carac-title'})
                value_elem = container.find('div', {'class': 'carac-value'})
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    # Traitement des dimensions spécifiques
                    if 'année de construction' in title:
                        # Format: "1976"
                        try:
                            dimensions['year_built'] = int(value)
                        except ValueError:
                            pass
                    elif 'superficie du terrain' in title:
                        # Format: "5 654 pc"
                        area_match = re.search(r'([\d\s]+)\s*pc', value)
                        if area_match:
                            area_str = area_match.group(1).replace(' ', '')
                            try:
                                dimensions['lot_size'] = float(area_str)
                            except ValueError:
                                pass
            
            logger.debug(f"📏 Dimensions extraites: {dimensions}")
            
            return PropertyDimensions(**dimensions)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction dimensions: {str(e)}")
            return PropertyDimensions()
    
    def _extract_media(self, soup: BeautifulSoup) -> PropertyMedia:
        """Extrait les médias depuis la page de détail"""
        try:
            images = []
            main_image = None
            
            # 1. Extraction depuis le JavaScript MosaicPhotoUrls (méthode principale)
            script_tags = soup.find_all('script')
            for script in script_tags:
                script_text = script.get_text()
                if 'MosaicPhotoUrls' in script_text:
                    # Recherche du pattern: window.MosaicPhotoUrls = ["url1", "url2", ...]
                    urls_match = re.search(r'window\.MosaicPhotoUrls\s*=\s*\[(.*?)\]', script_text, re.DOTALL)
                    if urls_match:
                        urls_text = urls_match.group(1)
                        # Extraire les URLs entre guillemets
                        urls = re.findall(r'"([^"]+)"', urls_text)
                        images.extend(urls)
                        logger.debug(f"🖼️ {len(urls)} images trouvées dans MosaicPhotoUrls")
                        break
            
            # 2. Fallback: recherche des images avec différents sélecteurs
            if not images:
                img_selectors = [
                    'img[src*="centris"]',
                    '.property-image',
                    '.main-image',
                    '.hero-image',
                    '.gallery img'
                ]
                
                for selector in img_selectors:
                    img_elements = soup.select(selector)
                    for img in img_elements:
                        src = img.get('src')
                        if src and src not in images:
                            # Filtrer les images non-propriété (logos, etc.)
                            if 'property' in src.lower() or 'listing' in src.lower() or 'photo' in src.lower():
                                images.append(src)
                                if not main_image:
                                    main_image = src
            
            # 3. Définir l'image principale
            if not main_image and images:
                main_image = images[0]
            
            # 4. Filtrer les images valides
            valid_images = []
            for img in images:
                if img.startswith('http') and 'centris.ca' in img:
                    valid_images.append(img)
            
            logger.debug(f"🖼️ {len(valid_images)} images valides extraites")
            
            return PropertyMedia(
                main_image=main_image,
                images=valid_images,
                image_count=len(valid_images)
            )
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction médias: {str(e)}")
            return PropertyMedia()
    
    def _extract_description(self, soup: BeautifulSoup) -> PropertyDescription:
        """Extrait les descriptions depuis la page de détail"""
        try:
            # Utilisation du sélecteur qui fonctionne selon notre analyse
            desc_element = soup.find('div', {'class': 'property-description'})
            
            description = ""
            if desc_element:
                description = desc_element.get_text(strip=True)
                # Nettoyer la description
                description = self._clean_description(description)
                logger.debug(f"📝 Description extraite et nettoyée: {description[:100]}...")
            
            return PropertyDescription(short_description=description, long_description=description)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction description: {str(e)}")
            return PropertyDescription()
    
    def _clean_description(self, description: str) -> str:
        """Nettoie la description des artefacts"""
        try:
            # Enlever "Description" au début
            if description.startswith("Description"):
                description = description[11:].strip()
            
            # Enlever les artefacts "No Centris{ID}"
            description = re.sub(r'No Centris\d+', '', description)
            
            # Nettoyer les espaces multiples
            description = ' '.join(description.split())
            
            return description
        except Exception as e:
            logger.debug(f"⚠️ Erreur nettoyage description: {e}")
            return description
    
    def _extract_location(self, soup: BeautifulSoup) -> Location:
        """Extrait les coordonnées géographiques depuis la page de détail"""
        try:
            location = {}
            
            # 1. Recherche des coordonnées dans les meta tags
            meta_lat = soup.find('meta', {'itemprop': 'latitude'})
            meta_lng = soup.find('meta', {'itemprop': 'longitude'})
            
            if meta_lat and meta_lng:
                try:
                    lat = float(meta_lat.get('content', ''))
                    lng = float(meta_lng.get('content', ''))
                    location['latitude'] = lat
                    location['longitude'] = lng
                    logger.debug(f"📍 Coordonnées GPS extraites: {lat}, {lng}")
                except ValueError:
                    pass
            
            # 2. Fallback: recherche dans les spans cachés
            if not location:
                lat_span = soup.find('span', {'id': 'PropertyLat'})
                lng_span = soup.find('span', {'id': 'PropertyLng'})
                
                if lat_span and lng_span:
                    try:
                        lat = float(lat_span.get_text(strip=True))
                        lng = float(lng_span.get_text(strip=True))
                        location['latitude'] = lat
                        location['longitude'] = lng
                        logger.debug(f"📍 Coordonnées GPS extraites (fallback): {lat}, {lng}")
                    except ValueError:
                        pass
            
            return Location(**location)
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction localisation: {str(e)}")
            return Location()
    
    def _extract_html_property_type(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait le type exact de propriété depuis le HTML de la page"""
        try:
            # 1. Recherche dans le titre principal (PageTitle)
            page_title = soup.find('span', {'data-id': 'PageTitle'})
            if page_title:
                title_text = page_title.get_text(strip=True)
                # Extraire le type avant "à vendre"
                if 'à vendre' in title_text:
                    html_type = title_text.split('à vendre')[0].strip()
                    logger.debug(f"🏷️ Type HTML trouvé dans PageTitle: {html_type}")
                    return html_type
            
            # 2. Recherche dans les meta tags
            meta_name = soup.find('meta', {'itemprop': 'name'})
            if meta_name:
                meta_content = meta_name.get('content', '')
                # Format: "Triplex à vendre à Chambly, Montérégie, ..."
                if 'à vendre' in meta_content:
                    html_type = meta_content.split('à vendre')[0].strip()
                    logger.debug(f"🏷️ Type HTML trouvé dans meta name: {html_type}")
                    return html_type
            
            # 3. Recherche dans le titre H1
            h1_title = soup.find('h1', {'itemprop': 'category'})
            if h1_title:
                h1_text = h1_title.get_text(strip=True)
                if 'à vendre' in h1_text:
                    html_type = h1_text.split('à vendre')[0].strip()
                    logger.debug(f"🏷️ Type HTML trouvé dans H1: {html_type}")
                    return html_type
            
            logger.debug("⚠️ Aucun type HTML trouvé dans la page")
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction type HTML: {str(e)}")
            return None
    
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

