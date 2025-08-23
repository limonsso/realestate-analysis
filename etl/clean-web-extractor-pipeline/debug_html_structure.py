#!/usr/bin/env python3
"""
Debug de la structure HTML réelle d'une propriété Centris
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import structlog

# Configuration du logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

async def debug_html_structure():
    """Analyse la structure HTML réelle d'une propriété Centris"""
    
    print("🔍 Debug de la structure HTML réelle d'une propriété Centris")
    print("=" * 70)
    
    # URL d'une propriété Chambly réelle
    property_url = "https://www.centris.ca/fr/propriete/21002530"
    
    print(f"🌐 URL analysée: {property_url}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(property_url) as response:
                if response.status == 200:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    print(f"✅ HTML récupéré: {len(html_content)} caractères")
                    
                    # 1. Recherche des conteneurs carac-container
                    print("\n🔍 1. Recherche des conteneurs carac-container:")
                    carac_containers = soup.find_all('div', class_='carac-container')
                    print(f"   📊 Trouvé {len(carac_containers)} conteneurs carac-container")
                    
                    if carac_containers:
                        for i, container in enumerate(carac_containers[:5]):  # Afficher les 5 premiers
                            title_elem = container.find('div', class_='carac-title')
                            value_elem = container.find('div', class_='carac-value')
                            
                            title = title_elem.get_text(strip=True) if title_elem else "N/A"
                            value = value_elem.get_text(strip=True) if value_elem else "N/A"
                            
                            print(f"   📋 Conteneur {i+1}:")
                            print(f"      🏷️ Titre: {title}")
                            print(f"      💎 Valeur: {value}")
                    else:
                        print("   ❌ Aucun conteneur carac-container trouvé!")
                    
                    # 2. Recherche alternative - tous les div avec des classes
                    print("\n🔍 2. Recherche alternative - tous les div avec des classes:")
                    all_divs = soup.find_all('div', class_=True)
                    class_counts = {}
                    
                    for div in all_divs:
                        classes = div.get('class', [])
                        for cls in classes:
                            class_counts[cls] = class_counts.get(cls, 0) + 1
                    
                    # Afficher les classes les plus communes
                    sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
                    print("   📊 Classes CSS les plus communes:")
                    for cls, count in sorted_classes[:10]:
                        print(f"      🏷️ {cls}: {count} occurrences")
                    
                    # 3. Recherche des informations spécifiques
                    print("\n🔍 3. Recherche des informations spécifiques:")
                    
                    # Recherche des unités résidentielles
                    units_patterns = [
                        'unités résidentielles',
                        'unités',
                        'résidentielles',
                        'nombre d\'unités'
                    ]
                    
                    for pattern in units_patterns:
                        elements = soup.find_all(text=lambda text: text and pattern.lower() in text.lower())
                        if elements:
                            print(f"   🏘️ Pattern '{pattern}' trouvé dans:")
                            for elem in elements[:3]:  # Afficher les 3 premiers
                                parent = elem.parent
                                if parent:
                                    print(f"      📍 {elem.strip()}")
                                    print(f"      🏷️ Classe parent: {parent.get('class', 'N/A')}")
                    
                    # 4. Recherche de la structure générale
                    print("\n🔍 4. Structure générale de la page:")
                    
                    # Titre de la page
                    title = soup.find('title')
                    if title:
                        print(f"   📄 Titre de la page: {title.get_text(strip=True)}")
                    
                    # Meta tags
                    meta_tags = soup.find_all('meta')
                    print(f"   🏷️ Nombre de meta tags: {len(meta_tags)}")
                    
                    # Scripts
                    scripts = soup.find_all('script')
                    print(f"   📜 Nombre de scripts: {len(scripts)}")
                    
                    # 5. Sauvegarde du HTML pour analyse
                    print("\n💾 5. Sauvegarde du HTML pour analyse:")
                    debug_file = "debug_centris_html.html"
                    with open(debug_file, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print(f"   📁 HTML sauvegardé dans: {debug_file}")
                    
                    # 6. Recommandations
                    print("\n💡 6. Recommandations:")
                    if not carac_containers:
                        print("   ⚠️ La classe 'carac-container' n'existe pas dans le HTML réel")
                        print("   🔧 Il faut adapter l'extraction à la vraie structure HTML")
                    else:
                        print("   ✅ La classe 'carac-container' existe - vérifier la logique d'extraction")
                    
                    print("\n🎯 Debug terminé !")
                    
                else:
                    print(f"❌ Erreur HTTP: {response.status}")
                    
    except Exception as e:
        print(f"❌ Erreur lors du debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_html_structure())
