#!/usr/bin/env python3
"""
Script de debug pour l'extraction des valeurs numériques
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from src.extractors.centris.extractors.numeric_extractor import NumericExtractor
from src.extractors.centris.session_manager import CentrisSessionManager

async def debug_numeric_extraction():
    """Debug de l'extraction des valeurs numériques"""
    
    # URL d'une propriété de test
    test_url = "https://www.centris.ca/fr/propriete/10001989"
    
    # Initialiser les composants
    session_manager = CentrisSessionManager()
    numeric_extractor = NumericExtractor()
    
    try:
        # Récupérer la page
        await session_manager.start()
        html_content = await session_manager.get_property_details(test_url)
        
        if not html_content:
            print("❌ Impossible de récupérer le contenu HTML")
            return
            
        print(f"✅ Contenu HTML récupéré: {len(html_content)} caractères")
        
        # Parser avec BeautifulSoup
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Trouver tous les carac-container
        carac_containers = soup.find_all('div', class_='carac-container')
        print(f"🔍 Trouvé {len(carac_containers)} conteneurs carac-container")
        
        # Analyser chaque conteneur
        for i, container in enumerate(carac_containers):
            title_elem = container.find('div', class_='carac-title')
            value_elem = container.find('div', class_='carac-value')
            
            if title_elem and value_elem:
                title = title_elem.get_text(strip=True).lower()
                value = value_elem.get_text(strip=True)
                
                print(f"  📋 Conteneur {i+1}: '{title}' = '{value}'")
                
                # Tester les conditions de matching
                if 'année de construction' in title:
                    print(f"    ✅ MATCH: Année de construction")
                elif 'superficie du terrain' in title:
                    print(f"    ✅ MATCH: Superficie du terrain")
                elif 'stationnement total' in title:
                    print(f"    ✅ MATCH: Stationnement total")
                elif 'nombre d\'unités' in title:
                    print(f"    ✅ MATCH: Nombre d'unités")
                elif 'revenus bruts potentiels' in title:
                    print(f"    ✅ MATCH: Revenus bruts potentiels")
                elif 'walkscore' in title.lower() or 'walk score' in title.lower():
                    print(f"    ✅ MATCH: Walk Score")
                else:
                    print(f"    ❌ NO MATCH")
            else:
                print(f"  ❌ Conteneur {i+1}: Éléments manquants")
        
        # Tester l'extraction avec NumericExtractor
        print(f"\n🔧 Test avec NumericExtractor:")
        numeric_values = numeric_extractor.extract_numeric_values(soup)
        
        print(f"📊 Résultats de extract_numeric_values:")
        for key, value in numeric_values.items():
            print(f"  ✅ {key}: {value}")
            
        if not numeric_values:
            print(f"  ❌ Aucune valeur numérique extraite")
            
        # Tester extract_detailed_features aussi
        print(f"\n🔧 Test avec extract_detailed_features:")
        detailed_features = numeric_extractor.extract_detailed_features(soup)
        
        print(f"📊 Résultats de extract_detailed_features:")
        for key, value in detailed_features.items():
            print(f"  ✅ {key}: {value}")
            
        if not detailed_features:
            print(f"  ❌ Aucune caractéristique détaillée extraite")
        
    except Exception as e:
        print(f"❌ Erreur lors du debug: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Fermer la session
        await session_manager.close()

if __name__ == "__main__":
    asyncio.run(debug_numeric_extraction())
