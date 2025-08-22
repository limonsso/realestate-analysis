#!/usr/bin/env python3
"""
🚀 Lanceur du Test d'Extraction Chambly Plex

Script simplifié pour lancer le test d'extraction de plex à Chambly.
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from tests.test_chambly_plex_extraction import ChamblyPlexExtractionTest
import structlog

# Configuration du logging
logger = structlog.get_logger()

async def main():
    """Fonction principale du lanceur."""
    logger.info("🚀 Lancement du Test d'Extraction Chambly Plex")
    logger.info("=" * 60)
    
    try:
        # Créer et exécuter le test
        test = ChamblyPlexExtractionTest()
        results = await test.run_test()
        
        # Affichage des résultats
        if results["success"]:
            logger.info("🎉 Test réussi!")
            logger.info(f"📊 Résultats: {results}")
            
            # Afficher un résumé détaillé
            print("\n" + "="*60)
            print("🎉 RÉSULTATS DU TEST CHAMBLY PLEX")
            print("="*60)
            print(f"🏠 Résumés extraits: {results['summaries_count']}")
            print(f"🔍 Détails extraits: {results['details_count']}")
            print(f"💾 Collection créée: {results['collection_name']}")
            
            if 'validation_results' in results:
                print(f"\n📋 Validation des données:")
                for field, result in results['validation_results'].items():
                    status = "✅" if result else "❌"
                    print(f"   {status} {field}: {result}")
            
            print(f"\n💡 Prochaines étapes:")
            print(f"   1. Vérifier la collection MongoDB: {results['collection_name']}")
            print(f"   2. Analyser les données extraites")
            print(f"   3. Valider la qualité des informations")
            
        else:
            logger.error("❌ Test échoué!")
            logger.error(f"🚨 Erreur: {results.get('error', 'Erreur inconnue')}")
            
            print("\n" + "="*60)
            print("❌ TEST ÉCHOUÉ")
            print("="*60)
            print(f"🚨 Erreur: {results.get('error', 'Erreur inconnue')}")
            print(f"\n💡 Solutions possibles:")
            print(f"   1. Vérifier la connexion MongoDB")
            print(f"   2. Vérifier la configuration Centris")
            print(f"   3. Vérifier la connectivité réseau")
            print(f"   4. Consulter les logs pour plus de détails")
        
        return results
        
    except KeyboardInterrupt:
        logger.info("⏹️ Test interrompu par l'utilisateur")
        print("\n⏹️ Test interrompu par l'utilisateur")
        return {"success": False, "error": "Interruption utilisateur"}
        
    except Exception as e:
        logger.error(f"❌ Erreur inattendue: {e}")
        print(f"\n❌ Erreur inattendue: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("🏠 Test d'Extraction Réelle: Plex à Chambly")
    print("=" * 60)
    print("Ce test va:")
    print("1. 🔍 Rechercher des plex à Chambly sur Centris.ca")
    print("2. 📊 Extraire les résumés et détails des propriétés")
    print("3. 💾 Sauvegarder les données en base MongoDB")
    print("4. ✅ Valider la qualité des données extraites")
    print("=" * 60)
    
    # Demander confirmation
    response = input("\n🚀 Lancer le test? (o/N): ").strip().lower()
    
    if response in ['o', 'oui', 'y', 'yes']:
        print("\n🚀 Lancement du test...")
        try:
            results = asyncio.run(main())
            
            # Code de sortie approprié
            sys.exit(0 if results.get("success", False) else 1)
        except Exception as e:
            print(f"\n❌ Erreur lors de l'exécution: {e}")
            sys.exit(1)
    else:
        print("❌ Test annulé")
        sys.exit(0)
