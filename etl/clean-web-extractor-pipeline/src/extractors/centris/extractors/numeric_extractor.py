#!/usr/bin/env python3
"""
Extracteur spécialisé pour les valeurs numériques spécifiques
"""

import re
from typing import Optional, Dict, Any, List
from bs4 import BeautifulSoup
import structlog

logger = structlog.get_logger()

class NumericExtractor:
    """Extracteur spécialisé pour les valeurs numériques spécifiques"""
    
    def __init__(self):
        self.logger = logger
    
    def extract_numeric_values(self, soup: BeautifulSoup) -> dict:
        """Extrait les valeurs numériques spécifiques du HTML"""
        numeric_values = {}
        
        try:
            logger.debug("🔍 Début extraction valeurs numériques")
            carac_containers = soup.find_all('div', class_='carac-container')
            logger.debug(f"🔍 Trouvé {len(carac_containers)} conteneurs carac-container dans extract_numeric_values")
            
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                value_elem = container.find('div', class_='carac-value')
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    logger.debug(f"🔍 Traitement numérique: '{title}' = '{value}'")
                    
                    # Année de construction
                    if 'année de construction' in title:
                        year = self._extract_year(value)
                        if year:
                            numeric_values['construction_year'] = year
                    
                    # Superficie du terrain
                    if 'superficie du terrain' in title:
                        area = self._extract_terrain_area(value)
                        if area:
                            numeric_values['terrain_area_sqft'] = area
                    
                    # Stationnement total
                    if 'stationnement total' in title:
                        parking_count = self._extract_parking_count(value)
                        if parking_count:
                            numeric_values['parking_count'] = parking_count
                    
                    # Nombre d'unités - COMMENTÉ car traité dans extract_detailed_features
                    # if 'nombre d\'unités' in title:
                    #     logger.debug(f"🔍 Extraction units_count pour titre: '{title}' et valeur: '{value}'")
                    #     units_count = self._extract_units_count(value)
                    #     if units_count:
                    #         numeric_values['units_count'] = units_count
                    #             logger.debug(f"✅ units_count extrait et assigné: {units_count}")
                    #         else:
                    #             logger.debug(f"❌ units_count non extrait de: '{value}'")
                    
                    # Revenus bruts potentiels
                    if 'revenus bruts potentiels' in title:
                        revenue = self._extract_revenue(value)
                        if revenue:
                            numeric_values['potential_gross_revenue'] = revenue
                    
                    # Walk Score
                    if 'walkscore' in title.lower() or 'walk score' in title.lower():
                        walk_score = self._extract_walk_score(value)
                        if walk_score:
                            numeric_values['walk_score'] = walk_score
            
            logger.debug(f"🔢 Valeurs numériques extraites: {numeric_values}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction valeurs numériques: {e}")
        
        return numeric_values
    
    def extract_detailed_features(self, soup: BeautifulSoup) -> dict:
        """Extrait les caractéristiques détaillées avec valeurs numériques"""
        detailed_features = {}
        
        try:
            logger.debug("🔍 Début extraction caractéristiques détaillées")
            carac_containers = soup.find_all('div', class_='carac-container')
            logger.debug(f"🔍 Trouvé {len(carac_containers)} conteneurs carac-container")
            
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                value_elem = container.find('div', class_='carac-value')
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    logger.debug(f"🔍 Traitement: '{title}' = '{value}'")
                    
                    # Unités résidentielles détaillées
                    if 'unités résidentielles' in title:
                        detailed_features['residential_units_detail'] = value
                        # units_breakdown supprimé car redondant avec units_X_half_count
                        
                        # Extraction des détails numériques des unités
                        units_numeric_details = self.extract_units_numeric_details(value)
                        detailed_features.update(units_numeric_details)
                        
                        # units_count est maintenant directement extrait dans extract_units_numeric_details
                        # Plus besoin d'assignation depuis total_units
                    
                    # Unité principale détaillée
                    if 'unité principale' in title:
                        detailed_features['main_unit_detail'] = value
                        main_unit_numbers = self._extract_main_unit_numbers(value)
                        if main_unit_numbers:
                            detailed_features['main_unit_numbers'] = main_unit_numbers
                        
                        # Extraction des détails numériques de l'unité principale
                        main_unit_numeric_details = self.extract_main_unit_numeric_details(value)
                        detailed_features.update(main_unit_numeric_details)
                    
                    # Année de construction
                    if 'année de construction' in title:
                        year = self._extract_year(value)
                        if year:
                            detailed_features['construction_year'] = year
                    
                    # Superficie du terrain
                    if 'superficie du terrain' in title:
                        area = self._extract_terrain_area(value)
                        if area:
                            detailed_features['terrain_area_sqft'] = area
                    
                    # Stationnement total
                    if 'stationnement total' in title:
                        detailed_features['parking_info'] = value
                        parking_count = self._extract_parking_count(value)
                        if parking_count:
                            detailed_features['parking_count'] = parking_count
                    
                    # Nombre d'unités
                    if 'nombre d\'unités' in title:
                        detailed_features['units_info'] = value
                        units_count = self._extract_units_count(value)
                        if units_count:
                            detailed_features['units_count'] = units_count
                    
                    # Revenus bruts potentiels
                    if 'revenus bruts potentiels' in title:
                        revenue = self._extract_revenue(value)
                        if revenue:
                            detailed_features['potential_gross_revenue'] = revenue
                    
                    # Utilisation de la propriété
                    if 'utilisation de la propriété' in title:
                        detailed_features['property_usage'] = value
                    
                    # Style de bâtiment
                    if 'style de bâtiment' in title:
                        detailed_features['building_style'] = value
                    
                    # Caractéristiques additionnelles
                    if 'caractéristiques additionnelles' in title:
                        detailed_features['additional_features'] = value
                    
                    # Date d'emménagement
                    if 'date d\'emménagement' in title:
                        detailed_features['move_in_date'] = value
                    
                    # Walk Score
                    if 'walkscore' in title or 'walk score' in title:
                        walk_score = self._extract_walk_score(value)
                        if walk_score:
                            detailed_features['walk_score'] = walk_score
            
            # Parser les détails de l'unité principale si disponible
            main_unit_info = detailed_features.get('main_unit_info')
            if main_unit_info:
                logger.debug(f"🏠 Parsing main_unit_info: {main_unit_info}")
                
                # Parser les détails de l'unité principale
                main_unit_details = self.extract_main_unit_numeric_details(main_unit_info)
                detailed_features.update(main_unit_details)
                
            # Parser les détails des unités résidentielles si disponible
            residential_units = detailed_features.get('residential_units_detail')
            if residential_units:
                logger.debug(f"🏠 Parsing residential_units_detail: {residential_units}")
                
                # Parser les détails des unités
                units_details = self.extract_units_numeric_details(residential_units)
                detailed_features.update(units_details)
            
            logger.debug(f"🔍 Caractéristiques détaillées extraites: {detailed_features}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction caractéristiques détaillées: {e}")
            import traceback
            logger.debug(f"⚠️ Traceback: {traceback.format_exc()}")
        
        return detailed_features
    
    def _extract_year(self, value: str) -> Optional[int]:
        """Extrait l'année depuis le texte"""
        try:
            year_match = re.search(r'\b(19|20)\d{2}\b', value)
            if year_match:
                year = int(year_match.group())
                logger.debug(f"🏗️ Année construction: {year}")
                return year
            return None
        except (ValueError, AttributeError):
            logger.debug(f"⚠️ Année non numérique: {value}")
            return None
    
    def _extract_terrain_area(self, value: str) -> Optional[int]:
        """Extrait la superficie du terrain depuis le texte"""
        try:
            # Format: "5 654 pc" -> 5654
            area_match = re.search(r'(\d+(?:\s+\d+)*)', value)
            if area_match:
                area_text = area_match.group(1).replace(' ', '')
                area = int(area_text)
                logger.debug(f"📏 Superficie terrain: {area} pc")
                return area
            return None
        except (ValueError, AttributeError):
            logger.debug(f"⚠️ Superficie non numérique: {value}")
            return None
    
    def _extract_parking_count(self, value: str) -> Optional[int]:
        """Extrait le nombre total de stationnements depuis le texte"""
        try:
            # Format: "Allée (3), Garage (1)" -> 4 (total)
            parking_matches = re.findall(r'\((\d+)\)', value)
            if parking_matches:
                total_parking = sum(int(count) for count in parking_matches)
                logger.debug(f"🚗 Nombre total stationnements: {total_parking} (détail: {parking_matches})")
                return total_parking
            return None
        except (ValueError, AttributeError):
            logger.debug(f"⚠️ Nombre stationnements non numérique: {value}")
            return None
    
    def _extract_units_count(self, value: str) -> Optional[int]:
        """Extrait le nombre d'unités depuis le texte"""
        try:
            logger.debug(f"🔍 Début extraction units_count depuis: '{value}'")
            logger.debug(f"🔍 Type de valeur: {type(value)}")
            logger.debug(f"🔍 Longueur de valeur: {len(value)}")
            logger.debug(f"🔍 Caractères ASCII: {[ord(c) for c in value]}")
            
            # Format: "Résidentiel (3)" -> 3
            # Essayer plusieurs patterns de parenthèses
            patterns = [
                r'\((\d+)\)',      # Parenthèses simples (3)
                r'（(\d+)）',      # Parenthèses japonaises （3）
                r'\[(\d+)\]',      # Crochets [3]
                r'\{(\d+)\}',      # Accolades {3}
                r'(\d+)',          # Juste le nombre
            ]
            
            for i, pattern in enumerate(patterns):
                logger.debug(f"🔍 Test pattern {i+1}: {pattern}")
                units_match = re.search(pattern, value)
                if units_match:
                    units_count = int(units_match.group(1))
                    logger.debug(f"🏘️ Nombre d'unités trouvé avec pattern {i+1}: {units_count}")
                    return units_count
                else:
                    logger.debug(f"🔍 Pattern {i+1} n'a pas trouvé de correspondance")
            
            logger.debug(f"⚠️ Aucun pattern n'a trouvé de correspondance pour: '{value}'")
            return None
            
        except (ValueError, AttributeError) as e:
            logger.debug(f"⚠️ Erreur extraction units_count: {e} pour valeur: '{value}'")
            return None
        except Exception as e:
            logger.debug(f"⚠️ Erreur inattendue dans _extract_units_count: {e} pour valeur: '{value}'")
            return None
    
    def _extract_revenue(self, value: str) -> Optional[int]:
        """Extrait les revenus depuis le texte"""
        try:
            # Format: "36 960 $" -> 36960
            # Recherche de tous les nombres dans la valeur
            revenue_matches = re.findall(r'(\d+)', value)
            if revenue_matches:
                # Concatène tous les nombres trouvés
                revenue_text = ''.join(revenue_matches)
                revenue = int(revenue_text)
                logger.debug(f"💰 Revenus potentiels: {revenue}$ (extrait de: {value})")
                return revenue
            return None
        except (ValueError, AttributeError):
            logger.debug(f"⚠️ Revenus non numériques: {value}")
            return None
    
    # _extract_units_breakdown supprimée car redondante avec extract_units_numeric_details
    
    def extract_units_numeric_details(self, value: str) -> dict:
        """Extrait les détails numériques des unités résidentielles de manière dynamique"""
        units_details = {}
        
        try:
            # Format: "1 x 2 ½, 2 x 3 ½, 1 x 4 ½, 2 x 5 ½, 1 x 9 ½"
            units_pattern = r'(\d+)\s*x\s*(\d+(?:\s*½)?)'
            units_matches = re.findall(units_pattern, value)
            
            if units_matches:
                # Créer un dictionnaire dynamique pour toutes les tailles d'unités
                for count, unit_type in units_matches:
                    count_int = int(count)
                    unit_type_clean = unit_type.replace('½', '').strip()
                    
                    # Créer la clé dynamiquement
                    key = f"units_{unit_type_clean}_half_count"
                    units_details[key] = count_int
                    
                    logger.debug(f"🏘️ {count_int} unité(s) {unit_type_clean} ½")
                
                # Ajouter un résumé global
                units_count = sum(units_details.values())
                units_details['units_count'] = units_count
                
                # units_breakdown supprimé car redondant avec units_X_half_count
                
                logger.debug(f"🔢 Détails numériques des unités: {units_details}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction détails numériques des unités: {e}")
        
        return units_details
    
    def _extract_main_unit_numbers(self, value: str) -> Optional[List[int]]:
        """Extrait les nombres de l'unité principale depuis le texte"""
        try:
            # Format: "5 pièces, 3 chambres, 1 salle de bain"
            numbers = re.findall(r'(\d+)', value)
            if numbers:
                main_unit_numbers = [int(n) for n in numbers]
                logger.debug(f"🔢 Nombres unité principale: {main_unit_numbers}")
                return main_unit_numbers
            return None
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction nombres unité principale: {e}")
            return None
    
    def extract_main_unit_numeric_details(self, value: str) -> dict:
        """Extrait les détails numériques de l'unité principale"""
        main_unit_details = {}
        
        try:
            # Format: "5 pièces, 3 chambres, 1 salle de bain"
            if 'pièces' in value:
                rooms_match = re.search(r'(\d+)\s*pièces?', value)
                if rooms_match:
                    main_unit_details['main_unit_rooms'] = int(rooms_match.group(1))
                    logger.debug(f"🏠 {main_unit_details['main_unit_rooms']} pièces dans l'unité principale")
            
            if 'chambres' in value:
                bedrooms_match = re.search(r'(\d+)\s*chambres?', value)
                if bedrooms_match:
                    main_unit_details['main_unit_bedrooms'] = int(bedrooms_match.group(1))
                    logger.debug(f"🛏️ {main_unit_details['main_unit_bedrooms']} chambres dans l'unité principale")
            
            if 'salle' in value and 'bain' in value:
                bathrooms_match = re.search(r'(\d+)\s*salle[s]?\s*de\s*bain', value)
                if bathrooms_match:
                    main_unit_details['main_unit_bathrooms'] = int(bathrooms_match.group(1))
                    logger.debug(f"🚿 {main_unit_details['main_unit_bathrooms']} salle(s) de bain dans l'unité principale")
            
            logger.debug(f"🔢 Détails numériques de l'unité principale: {main_unit_details}")
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction détails numériques de l'unité principale: {e}")
        
        return main_unit_details
    
    def _extract_walk_score(self, value: str) -> Optional[int]:
        """Extrait le Walk Score depuis le texte"""
        try:
            # Format: "71" (dans le span du walkscore)
            walk_score_match = re.search(r'(\d+)', value)
            if walk_score_match:
                walk_score = int(walk_score_match.group(1))
                logger.debug(f"🚶 Walk Score: {walk_score}")
                return walk_score
            return None
        except (ValueError, AttributeError):
            logger.debug(f"⚠️ Walk Score non numérique: {value}")
            return None
