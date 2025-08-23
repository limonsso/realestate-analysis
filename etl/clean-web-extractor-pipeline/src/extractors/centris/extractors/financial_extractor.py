#!/usr/bin/env python3
"""
Extracteur spécialisé pour les informations financières
"""

import re
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
import structlog

logger = structlog.get_logger()

class FinancialExtractor:
    """Extracteur spécialisé pour les informations financières"""
    
    def __init__(self):
        self.logger = logger
    
    def extract_financial(self, soup: BeautifulSoup) -> dict:
        """Extrait les informations financières d'une propriété"""
        try:
            financial_data = {}
            
            # Extraction du prix
            price = self._extract_price(soup)
            if price:
                financial_data['price'] = price
            
            # Extraction des évaluations municipales
            municipal_eval = self._extract_municipal_evaluation(soup)
            if municipal_eval:
                financial_data.update(municipal_eval)
            
            # Extraction des taxes
            taxes = self._extract_taxes(soup)
            if taxes:
                financial_data.update(taxes)
            
            # Extraction des revenus potentiels
            potential_revenue = self._extract_potential_revenue(soup)
            if potential_revenue:
                financial_data['potential_gross_revenue'] = potential_revenue
            
            # Calcul du prix au pied carré
            if financial_data.get('price') and financial_data.get('living_area'):
                price_per_sqft = financial_data['price'] / financial_data['living_area']
                financial_data['price_per_sqft'] = round(price_per_sqft, 2)
            
            logger.debug(f"💰 Informations financières extraites: {financial_data}")
            return financial_data
            
        except Exception as e:
            logger.error(f"❌ Erreur extraction financier: {e}")
            return {}
    
    def _extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        """Extrait le prix depuis le HTML"""
        try:
            # 1. Recherche dans les métadonnées schema.org (priorité haute)
            meta_price = soup.find('meta', {'itemprop': 'price'})
            if meta_price:
                price_text = meta_price.get('content')
                price = self._parse_price(price_text)
                if price:
                    logger.debug(f"💰 Prix trouvé (schema.org meta): {price}")
                    return price
            
            # 2. Recherche dans l'élément BuyPrice (Centris spécifique)
            buy_price_elem = soup.find('span', {'id': 'BuyPrice'})
            if buy_price_elem:
                price_text = buy_price_elem.get_text(strip=True)
                price = self._parse_price(price_text)
                if price:
                    logger.debug(f"💰 Prix trouvé (BuyPrice): {price}")
                    return price
            
            # 3. Recherche dans les éléments de prix spécifiques
            price_elem = soup.find('span', {'data-id': 'Price'})
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price = self._parse_price(price_text)
                if price:
                    logger.debug(f"💰 Prix trouvé (data-id): {price}")
                    return price
            
            # 4. Recherche dans les conteneurs de caractéristiques
            carac_containers = soup.find_all('div', class_='carac-container')
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                value_elem = container.find('div', class_='carac-value')
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    # Recherche de prix dans différents formats
                    if any(keyword in title for keyword in ['prix', 'valeur', 'coût', 'montant']):
                        price = self._parse_price(value)
                        if price:
                            logger.debug(f"💰 Prix trouvé (carac-container): {price}")
                            return price
            
            # 5. Recherche dans les scripts JavaScript
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # Patterns pour les prix dans le JavaScript
                    price_patterns = [
                        r'price["\']?\s*:\s*([\d,]+)',
                        r'prix["\']?\s*:\s*([\d,]+)',
                        r'value["\']?\s*:\s*([\d,]+)',
                        r'amount["\']?\s*:\s*([\d,]+)',
                        r'var\s+price\s*=\s*([\d,]+)',
                        r'var\s+prix\s*=\s*([\d,]+)'
                    ]
                    
                    for pattern in price_patterns:
                        price_match = re.search(pattern, script.string)
                        if price_match:
                            price_text = price_match.group(1)
                            price = self._parse_price(price_text)
                            if price:
                                logger.debug(f"💰 Prix trouvé (script {pattern}): {price}")
                                return price
            
            # 6. Recherche dans les métadonnées génériques
            meta_price = soup.find('meta', {'name': 'price'})
            if meta_price:
                price_text = meta_price.get('content')
                price = self._parse_price(price_text)
                if price:
                    logger.debug(f"💰 Prix trouvé (meta name): {price}")
                    return price
            
            # 7. Recherche dans le texte de la page pour des patterns de prix
            page_text = soup.get_text()
            price_patterns = [
                r'Prix\s*:\s*([\d\s,]+)\s*\$',
                r'Valeur\s*:\s*([\d\s,]+)\s*\$',
                r'Coût\s*:\s*([\d\s,]+)\s*\$',
                r'Montant\s*:\s*([\d\s,]+)\s*\$'
            ]
            
            for pattern in price_patterns:
                price_match = re.search(pattern, page_text)
                if price_match:
                    price_text = price_match.group(1)
                    price = self._parse_price(price_text)
                    if price:
                        logger.debug(f"💰 Prix trouvé (pattern {pattern}): {price}")
                        return price
            
            logger.warning("⚠️ Aucun prix trouvé dans la page")
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction prix: {e}")
            return None
    
    def _parse_price(self, price_text: str) -> Optional[float]:
        """Parse le texte du prix en nombre"""
        try:
            # Suppression des caractères non numériques sauf virgule et point
            clean_price = re.sub(r'[^\d,.]', '', price_text)
            
            # Remplacement de la virgule par un point pour la conversion
            clean_price = clean_price.replace(',', '.')
            
            # Conversion en float
            price = float(clean_price)
            return price
            
        except (ValueError, TypeError):
            logger.debug(f"⚠️ Impossible de parser le prix: {price_text}")
            return None
    
    def _extract_municipal_evaluation(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extrait les évaluations municipales"""
        try:
            municipal_data = {}
            
            # 1. Recherche dans les conteneurs de caractéristiques
            carac_containers = soup.find_all('div', class_='carac-container')
            
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                value_elem = container.find('div', class_='carac-value')
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    if 'évaluation municipale' in title:
                        if 'terrain' in title:
                            municipal_data['municipal_evaluation_land'] = self._parse_price(value)
                        elif 'bâtiment' in title:
                            municipal_data['municipal_evaluation_building'] = self._parse_price(value)
                        elif 'totale' in title or 'total' in title:
                            municipal_data['municipal_evaluation_total'] = self._parse_price(value)
                        elif 'année' in title:
                            try:
                                year = int(re.search(r'\d{4}', value).group())
                                municipal_data['municipal_evaluation_year'] = year
                            except (AttributeError, ValueError):
                                pass
            
            # 2. Recherche dans les tableaux financiers (Centris spécifique)
            financial_tables = soup.find_all('table', class_='table')
            
            for table in financial_tables:
                # Vérifier si c'est un tableau d'évaluation municipale
                header = table.find('thead')
                if header and 'évaluation municipale' in header.get_text().lower():
                    rows = table.find_all('tr')
                    
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) == 2:
                            label = cells[0].get_text(strip=True).lower()
                            value = cells[1].get_text(strip=True)
                            
                            if 'terrain' in label:
                                municipal_data['municipal_evaluation_land'] = self._parse_price(value)
                            elif 'bâtiment' in label:
                                municipal_data['municipal_evaluation_building'] = self._parse_price(value)
                            elif 'total' in label:
                                municipal_data['municipal_evaluation_total'] = self._parse_price(value)
                    
                    # Extraire l'année depuis le titre du tableau
                    header_text = header.get_text()
                    year_match = re.search(r'\((\d{4})\)', header_text)
                    if year_match:
                        try:
                            year = int(year_match.group(1))
                            municipal_data['municipal_evaluation_year'] = year
                        except ValueError:
                            pass
            
            # 3. Recherche dans les métadonnées schema.org
            meta_eval = soup.find_all('meta', {'itemprop': 'value'})
            for meta in meta_eval:
                eval_type = meta.get('itemprop', '').lower()
                eval_value = meta.get('content', '')
                
                if 'land' in eval_type or 'terrain' in eval_type:
                    municipal_data['municipal_evaluation_land'] = self._parse_price(eval_value)
                elif 'building' in eval_type or 'bâtiment' in eval_type:
                    municipal_data['municipal_evaluation_building'] = self._parse_price(eval_value)
            
            logger.debug(f"💰 Évaluations municipales extraites: {municipal_data}")
            return municipal_data
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction évaluation municipale: {e}")
            return {}
    
    def _extract_taxes(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extrait les informations de taxes"""
        try:
            taxes_data = {}
            
            # 1. Recherche dans les conteneurs de caractéristiques
            carac_containers = soup.find_all('div', class_='carac-container')
            
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                value_elem = container.find('div', class_='carac-value')
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    if 'taxe municipale' in title:
                        taxes_data['municipal_tax'] = self._parse_price(value)
                    elif 'taxe scolaire' in title:
                        taxes_data['school_tax'] = self._parse_price(value)
                    elif 'taxes totales' in title:
                        taxes_data['total_taxes'] = self._parse_price(value)
            
            # 2. Recherche dans les tableaux financiers (Centris spécifique)
            financial_tables = soup.find_all('table', class_='table')
            
            for table in financial_tables:
                # Vérifier si c'est un tableau de taxes
                header = table.find('thead')
                if header and 'taxes' in header.get_text().lower():
                    rows = table.find_all('tr')
                    
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) == 2:
                            label = cells[0].get_text(strip=True).lower()
                            value = cells[1].get_text(strip=True)
                            
                            if 'municipales' in label:
                                taxes_data['municipal_tax'] = self._parse_price(value)
                            elif 'scolaires' in label:
                                taxes_data['school_tax'] = self._parse_price(value)
                            elif 'total' in label:
                                taxes_data['total_taxes'] = self._parse_price(value)
            
            # 3. Recherche dans les métadonnées schema.org
            meta_taxes = soup.find_all('meta', {'itemprop': 'tax'})
            for meta in meta_taxes:
                tax_type = meta.get('itemprop', '').lower()
                tax_value = meta.get('content', '')
                
                if 'municipal' in tax_type:
                    taxes_data['municipal_tax'] = self._parse_price(tax_value)
                elif 'school' in tax_type or 'scolaire' in tax_type:
                    taxes_data['school_tax'] = self._parse_price(tax_value)
            
            logger.debug(f"💰 Taxes extraites: {taxes_data}")
            return taxes_data
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction taxes: {e}")
            return {}
    
    def _extract_potential_revenue(self, soup: BeautifulSoup) -> Optional[float]:
        """Extrait les revenus potentiels"""
        try:
            # Recherche dans les conteneurs de caractéristiques
            carac_containers = soup.find_all('div', class_='carac-container')
            
            for container in carac_containers:
                title_elem = container.find('div', class_='carac-title')
                value_elem = container.find('div', class_='carac-value')
                
                if title_elem and value_elem:
                    title = title_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)
                    
                    if 'revenus bruts potentiels' in title:
                        revenue = self._parse_price(value)
                        if revenue:
                            logger.debug(f"💰 Revenus potentiels trouvés: {revenue}")
                            return revenue
            
            return None
            
        except Exception as e:
            logger.debug(f"⚠️ Erreur extraction revenus potentiels: {e}")
            return None
