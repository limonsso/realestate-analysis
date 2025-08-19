#!/usr/bin/env python3
"""
Script principal pour exécuter les différents scripts utilitaires
"""

import sys
import argparse
from pathlib import Path

# Ajouter le dossier parent au path pour accéder aux modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from validate_specifications import SpecificationValidator
from cleanup_structure import cleanup_old_files, organize_files, show_structure_status

def run_validation():
    """Exécute la validation des spécifications"""
    print("🔍 VALIDATION DES SPÉCIFICATIONS")
    print("=" * 50)
    
    validator = SpecificationValidator()
    success = validator.validate_all_specifications()
    
    if success:
        print("\n🎉 VALIDATION RÉUSSIE - Toutes les spécifications sont respectées !")
        return 0
    else:
        print("\n❌ VALIDATION ÉCHOUÉE - Certaines spécifications ne sont pas respectées")
        return 1

def run_cleanup():
    """Exécute le nettoyage de la structure"""
    print("🧹 NETTOYAGE DE LA STRUCTURE")
    print("=" * 50)
    
    # Organiser les fichiers
    organize_files()
    
    # Afficher le statut
    show_structure_status()
    
    # Demander si l'utilisateur veut nettoyer les anciens fichiers
    choice = input("\n🧹 Voulez-vous nettoyer les anciens fichiers ? (y/N): ").strip().lower()
    if choice in ['y', 'yes', 'o', 'oui']:
        try:
            days = int(input("  📅 Nombre de jours à conserver (défaut: 30): ") or "30")
            cleanup_old_files(days)
        except ValueError:
            print("  ⚠️ Valeur invalide, utilisation de 30 jours par défaut")
            cleanup_old_files()
    
    print("\n✅ Nettoyage terminé!")
    return 0

def run_structure_status():
    """Affiche le statut de la structure"""
    print("📊 STATUT DE LA STRUCTURE")
    print("=" * 50)
    
    show_structure_status()
    return 0

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='Scripts utilitaires pour le projet de nettoyage immobilier')
    parser.add_argument('script', choices=['validate', 'cleanup', 'status'], 
                       help='Script à exécuter')
    
    args = parser.parse_args()
    
    if args.script == 'validate':
        return run_validation()
    elif args.script == 'cleanup':
        return run_cleanup()
    elif args.script == 'status':
        return run_structure_status()
    
    return 0

if __name__ == "__main__":
    exit(main())
