#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 ALIAS DE COMPATIBILITÉ - UltraIntelligentCleaner
====================================================

Ce fichier maintient la compatibilité avec l'ancien nom
en important et exposant la nouvelle classe ModularPipeline

⚠️  ATTENTION: Ce fichier est maintenant un alias vers main_modular_pipeline.py
    Pour de nouveaux projets, utilisez directement main_modular_pipeline.py
"""

# Import de la nouvelle classe principale
from main_modular_pipeline import ModularPipeline

# Alias pour maintenir la compatibilité
UltraIntelligentPipeline = ModularPipeline

# Export de la classe pour la compatibilité
__all__ = ['UltraIntelligentPipeline', 'ModularPipeline']

# Message de dépréciation
import warnings
warnings.warn(
    "⚠️  Le fichier main_ultra_intelligent.py est déprécié. "
    "Utilisez main_modular_pipeline.py pour de nouveaux projets.",
    DeprecationWarning,
    stacklevel=2
)

# Exécution directe
if __name__ == "__main__":
    # Rediriger vers le nouveau fichier principal
    import subprocess
    import sys
    
    print("🔄 Redirection vers main_modular_pipeline.py...")
    result = subprocess.run([sys.executable, "main_modular_pipeline.py"] + sys.argv[1:])
    sys.exit(result.returncode)
