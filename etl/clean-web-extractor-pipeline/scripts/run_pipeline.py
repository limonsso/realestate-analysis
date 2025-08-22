#!/usr/bin/env python3
"""
Script principal pour exécuter le pipeline d'extraction immobilière
Pipeline autonome sans dépendances externes
"""

import sys
import asyncio
from pathlib import Path

# Ajout du répertoire src au path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.core.pipeline import main


def run_sync():
    """Version synchrone pour compatibilité"""
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_sync()
