#!/usr/bin/env python3
"""
Script de démarrage simple pour le pipeline d'extraction immobilière
Exécution directe sans configuration complexe
"""

import sys
import asyncio
from pathlib import Path

# Ajout des chemins au PYTHONPATH
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "src"))
sys.path.insert(0, str(current_dir / "config"))

from src.core.pipeline import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Pipeline interrompu par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {str(e)}")
        sys.exit(1)
