#!/usr/bin/env python3
"""
Configuration des chemins et dossiers pour le projet de nettoyage immobilier
"""

import os
from pathlib import Path

# Chemin racine du projet
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Dossiers d'entrée et de sortie
INPUT_DIR = PROJECT_ROOT / "etl" / "clean_data" / "inputs"
OUTPUT_DIR = PROJECT_ROOT / "etl" / "clean_data" / "outputs"
CLEANED_DATA_DIR = OUTPUT_DIR / "cleaned_data"
REPORTS_DIR = OUTPUT_DIR / "reports"
LOGS_DIR = OUTPUT_DIR / "logs"

# Créer les dossiers s'ils n'existent pas
def ensure_directories():
    """Crée tous les dossiers nécessaires"""
    directories = [INPUT_DIR, OUTPUT_DIR, CLEANED_DATA_DIR, REPORTS_DIR, LOGS_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Dossier créé/vérifié: {directory}")

# Noms de fichiers par défaut
DEFAULT_INPUT_FILE = INPUT_DIR / "sample_real_estate_data.csv"

# Formats de sortie supportés
SUPPORTED_OUTPUT_FORMATS = {
    'csv': '.csv',
    'parquet': '.parquet',
    'json': '.json',
    'geojson': '.geojson'
}

# Configuration des logs
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': LOGS_DIR / f"cleaning_log_{os.getenv('USER', 'user')}.log"
}

# Configuration des rapports
REPORT_CONFIG = {
    'quality_report': REPORTS_DIR / "quality_report.json",
    'cleaning_summary': REPORTS_DIR / "cleaning_summary.txt",
    'data_profile': REPORTS_DIR / "data_profile.html"
}

if __name__ == "__main__":
    print("🏗️ Configuration des dossiers du projet...")
    ensure_directories()
    print("\n📁 Structure des dossiers:")
    print(f"  📥 Entrées: {INPUT_DIR}")
    print(f"  📤 Sorties: {OUTPUT_DIR}")
    print(f"  🗂️ Données nettoyées: {CLEANED_DATA_DIR}")
    print(f"  📊 Rapports: {REPORTS_DIR}")
    print(f"  📝 Logs: {LOGS_DIR}")
    print("\n✅ Configuration terminée!")
