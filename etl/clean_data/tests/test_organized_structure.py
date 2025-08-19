#!/usr/bin/env python3
"""
Test de la nouvelle structure organisée des dossiers
"""

import os
from pathlib import Path
from config import ensure_directories, INPUT_DIR, OUTPUT_DIR, CLEANED_DATA_DIR, REPORTS_DIR, LOGS_DIR

def test_directory_structure():
    """Teste la structure des dossiers"""
    print("🧪 TEST DE LA STRUCTURE ORGANISÉE")
    print("=" * 50)
    
    # 1. Créer les dossiers
    print("📁 Création des dossiers...")
    ensure_directories()
    
    # 2. Vérifier que les dossiers existent
    directories = [INPUT_DIR, OUTPUT_DIR, CLEANED_DATA_DIR, REPORTS_DIR, LOGS_DIR]
    for directory in directories:
        if directory.exists():
            print(f"✅ {directory.name}: {directory}")
        else:
            print(f"❌ {directory.name}: N'existe pas")
    
    # 3. Vérifier le contenu du dossier inputs
    print(f"\n📥 Contenu du dossier inputs ({INPUT_DIR}):")
    if INPUT_DIR.exists():
        input_files = list(INPUT_DIR.glob("*"))
        if input_files:
            for file in input_files:
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"  📄 {file.name} ({size_mb:.1f} MB)")
        else:
            print("  📭 Aucun fichier trouvé")
    else:
        print("  ❌ Dossier inputs n'existe pas")
    
    # 4. Vérifier le contenu du dossier outputs
    print(f"\n📤 Contenu du dossier outputs ({OUTPUT_DIR}):")
    if OUTPUT_DIR.exists():
        for subdir in [CLEANED_DATA_DIR, REPORTS_DIR, LOGS_DIR]:
            if subdir.exists():
                files = list(subdir.glob("*"))
                print(f"  📁 {subdir.name}: {len(files)} fichiers")
                for file in files[:3]:  # Afficher les 3 premiers fichiers
                    print(f"    📄 {file.name}")
                if len(files) > 3:
                    print(f"    ... et {len(files) - 3} autres fichiers")
            else:
                print(f"  ❌ Sous-dossier {subdir.name} n'existe pas")
    else:
        print("  ❌ Dossier outputs n'existe pas")
    
    # 5. Test de la configuration
    print(f"\n⚙️ Configuration:")
    print(f"  📥 Dossier d'entrée: {INPUT_DIR}")
    print(f"  📤 Dossier de sortie: {OUTPUT_DIR}")
    print(f"  🗂️ Données nettoyées: {CLEANED_DATA_DIR}")
    print(f"  📊 Rapports: {REPORTS_DIR}")
    print(f"  📝 Logs: {LOGS_DIR}")
    
    print("\n✅ Test de la structure terminé!")

def test_file_operations():
    """Teste les opérations de fichiers"""
    print("\n🧪 TEST DES OPÉRATIONS DE FICHIERS")
    print("=" * 50)
    
    # 1. Créer un fichier de test dans inputs
    test_file = INPUT_DIR / "test_file.txt"
    try:
        with open(test_file, 'w') as f:
            f.write("Fichier de test pour la structure organisée")
        print(f"✅ Fichier de test créé: {test_file}")
    except Exception as e:
        print(f"❌ Erreur création fichier test: {e}")
    
    # 2. Créer un fichier de test dans cleaned_data
    test_output = CLEANED_DATA_DIR / "test_output.txt"
    try:
        with open(test_output, 'w') as f:
            f.write("Fichier de sortie de test")
        print(f"✅ Fichier de sortie créé: {test_output}")
    except Exception as e:
        print(f"❌ Erreur création fichier sortie: {e}")
    
    # 3. Nettoyer les fichiers de test
    try:
        if test_file.exists():
            test_file.unlink()
            print(f"🧹 Fichier de test supprimé: {test_file}")
        if test_output.exists():
            test_output.unlink()
            print(f"🧹 Fichier de sortie supprimé: {test_output}")
    except Exception as e:
        print(f"⚠️ Erreur suppression fichiers test: {e}")
    
    print("✅ Test des opérations de fichiers terminé!")

if __name__ == "__main__":
    test_directory_structure()
    test_file_operations()
