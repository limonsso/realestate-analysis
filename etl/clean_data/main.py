#!/usr/bin/env python3
"""
Script principal pour le nettoyage immobilier
Utilise la nouvelle architecture modulaire
"""

import sys
from pathlib import Path

# Ajouter le dossier src au path Python
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from core.cleaner import RealEstateDataCleaner
from core.simple_cleaner import SimpleRealEstateCleaner
from core.config import ensure_directories

# Définir les chemins relatifs au script principal
INPUT_DIR = Path("inputs")
OUTPUT_DIR = Path("outputs")
CLEANED_DATA_DIR = OUTPUT_DIR / "cleaned_data"
REPORTS_DIR = OUTPUT_DIR / "reports"
LOGS_DIR = OUTPUT_DIR / "logs"
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Fonction principale"""
    import argparse
    
    # S'assurer que les dossiers existent
    ensure_directories()
    
    parser = argparse.ArgumentParser(description='Nettoyage expert du dataset immobilier')
    parser.add_argument('--input', '-i', help='Fichier d\'entrée (CSV, Excel, JSON)')
    parser.add_argument('--mongodb', help='Chaîne de connexion MongoDB')
    parser.add_argument('--output-dir', '-o', default='.', help='Répertoire de sortie')
    parser.add_argument('--mode', choices=['full', 'simple'], default='full', 
                       help='Mode de nettoyage: full (complet) ou simple')
    
    args = parser.parse_args()
    
    # Utiliser le fichier par défaut si aucun n'est spécifié
    if not args.input:
        default_input = INPUT_DIR / "sample_real_estate_data.csv"
        if default_input.exists():
            args.input = str(default_input)
            logger.info(f"📁 Utilisation du fichier par défaut: {args.input}")
        else:
            logger.error(f"❌ Aucun fichier d'entrée spécifié et fichier par défaut non trouvé: {default_input}")
            logger.info(f"💡 Placez votre fichier CSV dans le dossier: {INPUT_DIR}")
            return 1
    
    try:
        if args.mode == 'full':
            # Mode complet avec toutes les phases
            logger.info("🚀 Mode de nettoyage COMPLET sélectionné")
            cleaner = RealEstateDataCleaner(
                input_file=args.input,
                mongodb_connection=args.mongodb
            )
            
            # Exécuter le pipeline complet
            success = cleaner.run_complete_cleaning_pipeline()
            
            if success:
                logger.info("✅ Nettoyage COMPLET terminé avec succès!")
                logger.info(f"📊 Données nettoyées: {len(cleaner.get_cleaned_data())} propriétés")
                
                # Afficher le rapport de qualité
                quality_report = cleaner.get_quality_report()
                if quality_report:
                    logger.info("📋 Rapport de qualité généré")
            else:
                logger.error("❌ Échec du nettoyage COMPLET")
                return 1
                
        else:
            # Mode simple
            logger.info("🚀 Mode de nettoyage SIMPLE sélectionné")
            cleaner = SimpleRealEstateCleaner(args.input)
            
            # Exécuter le nettoyage simple
            success = cleaner.clean_data()
            
            if success:
                logger.info("✅ Nettoyage SIMPLE terminé avec succès!")
                logger.info(f"📊 Données nettoyées: {len(cleaner.df_cleaned)} propriétés")
                
                # Sauvegarder les données
                cleaner.save_cleaned_data()
                
                # Afficher le résumé
                summary = cleaner.get_summary()
                logger.info(f"📋 Résumé: {summary['cleaned_shape']}")
            else:
                logger.error("❌ Échec du nettoyage SIMPLE")
                return 1
        
        logger.info("🎉 Traitement terminé avec succès!")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
