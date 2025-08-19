#!/usr/bin/env python3
"""
Script de nettoyage et maintenance de la structure organisée
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
# Ajouter le dossier parent au path pour accéder aux modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.config import (
    INPUT_DIR, OUTPUT_DIR, CLEANED_DATA_DIR, 
    REPORTS_DIR, LOGS_DIR, ensure_directories
)

def cleanup_old_files(days_to_keep: int = 30):
    """Nettoie les anciens fichiers de sortie"""
    print(f"🧹 Nettoyage des fichiers de plus de {days_to_keep} jours...")
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    cleaned_count = 0
    
    # Nettoyer les dossiers de sortie
    output_dirs = [CLEANED_DATA_DIR, REPORTS_DIR, LOGS_DIR]
    
    for output_dir in output_dirs:
        if output_dir.exists():
            for file_path in output_dir.glob("*"):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_date:
                        try:
                            file_path.unlink()
                            print(f"  🗑️ Supprimé: {file_path.name}")
                            cleaned_count += 1
                        except Exception as e:
                            print(f"  ⚠️ Erreur suppression {file_path.name}: {e}")
    
    print(f"✅ Nettoyage terminé: {cleaned_count} fichiers supprimés")

def organize_files():
    """Organise les fichiers dans la structure appropriée"""
    print("📁 Organisation des fichiers...")
    
    # S'assurer que les dossiers existent
    ensure_directories()
    
    # Déplacer les fichiers CSV du dossier racine vers inputs
    current_dir = Path(".")
    csv_files = list(current_dir.glob("*.csv"))
    
    for csv_file in csv_files:
        if csv_file.name != "sample_real_estate_data.csv":  # Ne pas déplacer le fichier principal
            try:
                # Vérifier si c'est un fichier de données
                if "real_estate" in csv_file.name.lower() or "property" in csv_file.name.lower():
                    target_path = INPUT_DIR / csv_file.name
                    if not target_path.exists():
                        shutil.move(str(csv_file), str(target_path))
                        print(f"  📥 Déplacé vers inputs: {csv_file.name}")
                    else:
                        print(f"  ⚠️ Fichier déjà dans inputs: {csv_file.name}")
            except Exception as e:
                print(f"  ❌ Erreur déplacement {csv_file.name}: {e}")
    
    # Déplacer les fichiers de sortie vers les bons dossiers
    output_files = {
        "*.parquet": CLEANED_DATA_DIR,
        "*.json": CLEANED_DATA_DIR,
        "*.geojson": CLEANED_DATA_DIR,
        "quality_report_*.json": REPORTS_DIR,
        "cleaning_log_*.log": LOGS_DIR
    }
    
    for pattern, target_dir in output_files.items():
        for file_path in current_dir.glob(pattern):
            if file_path.is_file():
                try:
                    target_path = target_dir / file_path.name
                    if not target_path.exists():
                        shutil.move(str(file_path), str(target_path))
                        print(f"  📤 Déplacé vers {target_dir.name}: {file_path.name}")
                    else:
                        print(f"  ⚠️ Fichier déjà dans {target_dir.name}: {file_path.name}")
                except Exception as e:
                    print(f"  ❌ Erreur déplacement {file_path.name}: {e}")
    
    print("✅ Organisation terminée")

def show_structure_status():
    """Affiche le statut de la structure"""
    print("\n📊 STATUT DE LA STRUCTURE")
    print("=" * 50)
    
    # Vérifier les dossiers
    directories = [INPUT_DIR, OUTPUT_DIR, CLEANED_DATA_DIR, REPORTS_DIR, LOGS_DIR]
    for directory in directories:
        if directory.exists():
            file_count = len(list(directory.glob("*")))
            size_mb = sum(f.stat().st_size for f in directory.glob("*") if f.is_file()) / (1024 * 1024)
            print(f"📁 {directory.name}: {file_count} fichiers ({size_mb:.1f} MB)")
        else:
            print(f"❌ {directory.name}: N'existe pas")
    
    # Afficher les fichiers récents
    print(f"\n🕒 FICHIERS RÉCENTS (dernières 24h):")
    recent_files = []
    
    for output_dir in [CLEANED_DATA_DIR, REPORTS_DIR, LOGS_DIR]:
        if output_dir.exists():
            for file_path in output_dir.glob("*"):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time > datetime.now() - timedelta(hours=24):
                        recent_files.append((file_path, file_time))
    
    if recent_files:
        recent_files.sort(key=lambda x: x[1], reverse=True)
        for file_path, file_time in recent_files[:5]:  # Top 5
            time_str = file_time.strftime("%H:%M")
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"  📄 {file_path.name} ({time_str}, {size_mb:.1f} MB)")
    else:
        print("  📭 Aucun fichier récent")

def main():
    """Fonction principale"""
    print("🏗️ MAINTENANCE DE LA STRUCTURE ORGANISÉE")
    print("=" * 60)
    
    # 1. Organiser les fichiers
    organize_files()
    
    # 2. Nettoyer les anciens fichiers (optionnel)
    cleanup_choice = input("\n🧹 Voulez-vous nettoyer les anciens fichiers ? (y/N): ").strip().lower()
    if cleanup_choice in ['y', 'yes', 'o', 'oui']:
        try:
            days = int(input("  📅 Nombre de jours à conserver (défaut: 30): ") or "30")
            cleanup_old_files(days)
        except ValueError:
            print("  ⚠️ Valeur invalide, utilisation de 30 jours par défaut")
            cleanup_old_files()
    
    # 3. Afficher le statut
    show_structure_status()
    
    print("\n✅ Maintenance terminée!")

if __name__ == "__main__":
    main()
