#!/usr/bin/env python3
"""
Exemple d'utilisation du pipeline avec des noms de table/collection personnalisés
"""

import sys
import asyncio
from pathlib import Path

# Ajout des chemins au PYTHONPATH
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir / "src"))
sys.path.insert(0, str(current_dir / "config"))

from src.core.pipeline import main

async def run_examples():
    """Exécute des exemples avec différents noms de table"""
    
    print("🚀 Exemples d'utilisation avec des tables personnalisées")
    print("=" * 60)
    
    examples = [
        {
            "name": "Extraction 2024",
            "args": ["--table-name", "properties_2024", "--database-name", "real_estate_analytics"],
            "description": "Extraction dans la collection 'properties_2024' de la base 'real_estate_analytics'"
        },
        {
            "name": "Condos Montréal",
            "args": ["--location", "Montréal", "--property-type", "Condo", "--table-name", "montreal_condos"],
            "description": "Extraction des condos de Montréal dans la collection 'montreal_condos'"
        },
        {
            "name": "Maisons Montérégie",
            "args": ["--location", "Montérégie", "--property-type", "SingleFamilyHome", "--table-name", "monteregie_houses"],
            "description": "Extraction des maisons de Montérégie dans la collection 'monteregie_houses'"
        },
        {
            "name": "Plex Laval",
            "args": ["--location", "Laval", "--property-type", "Plex", "--table-name", "laval_plex", "--debug"],
            "description": "Extraction des plex de Laval en mode debug dans la collection 'laval_plex'"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Description: {example['description']}")
        print(f"   Commande: python run.py {' '.join(example['args'])}")
        print("-" * 60)
    
    print("\n🎯 Pour exécuter un exemple, utilisez la commande correspondante.")
    print("💡 Vous pouvez combiner ces paramètres selon vos besoins!")

if __name__ == "__main__":
    try:
        asyncio.run(run_examples())
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
