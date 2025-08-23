#!/usr/bin/env python3
"""
🚀 Lanceur du Test d'Extraction Corrigé - Trois-Rivières Plex

Version corrigée qui force l'utilisation de la configuration Trois-Rivières
et évite les conflits avec la configuration par défaut (Chambly).
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from tests.test_trois_rivieres_plex_extraction_fixed import TroisRivieresPlexExtractionTestFixed
import structlog

# Configuration du logging
logger = structlog.get_logger()

async def main():
    """Fonction principale du lanceur corrigé."""
    logger.info("🚀 Lancement du Test d'Extraction Trois-Rivières Plex (Version Corrigée)")
    logger.info("🔒 Configuration Trois-Rivières forcée (évite Chambly)")
    logger.info("=" * 60)
    
    try:
        # Créer et exécuter le test corrigé
        test = TroisRivieresPlexExtractionTestFixed()
        results = await test.run_test()
        
        # Affichage des résultats
        if results["success"]:
            logger.info("🎉 Test réussi!")
            logger.info(f"📊 Résultats: {results}")
            
            # Affichage d'un résumé détaillé
            print("\n" + "="*60)
            print("🎉 RÉSULTATS DU TEST TROIS-RIVIÈRES PLEX (CORRIGÉ)")
            print("="*60)
            print(f"🏠 Résumés extraits: {results['summaries_count']}")
            print(f"🔍 Détails extraits: {results['details_count']}")
            print(f"💾 Collection créée: {results['collection_name']}")
            print(f"🔒 Configuration Trois-Rivières forcée: ✅")
            print(f"🚫 Chambly évité: ✅")
            
            if 'validation_results' in results:
                print(f"\n📋 Validation des données:")
                for field, result in results['validation_results'].items():
                    status = "✅" if result else "❌"
                    print(f"   {status} {field}: {result}")
            
            print(f"\n💡 Prochaines étapes:")
            print(f"   1. Vérifier la collection MongoDB: {results['collection_name']}")
            print(f"   2. Analyser les données extraites (Trois-Rivières uniquement)")
            print(f"   3. Valider la qualité des informations")
            print(f"   4. Vérifier qu'aucune donnée Chambly n'est présente")
            
        else:
            logger.error("❌ Test échoué!")
            logger.error(f"🚨 Erreur: {results.get('error', 'Erreur inconnue')}")
            
            print("\n" + "="*60)
            print("❌ TEST ÉCHOUÉ")
            print("="*60)
            print(f"🚨 Erreur: {results.get('error', 'Erreur inconnue')}")
            print(f"\n💡 Solutions possibles:")
            print(f"   1. Vérifier la connexion MongoDB")
            print(f"   2. Vérifier la configuration Trois-Rivières")
            print(f"   3. Vérifier la connectivité réseau")
            print(f"   4. Consulter les logs pour plus de détails")
            print(f"   5. Vérifier que la configuration évite Chambly")
        
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
    print("🏠 Test d'Extraction Corrigé: Plex à Trois-Rivières")
    print("🔒 Configuration Trois-Rivières forcée (évite Chambly)")
    print("=" * 60)
    print("Ce test va:")
    print("1. 🔍 Rechercher des plex à Trois-Rivières sur Centris.ca")
    print("2. 📊 Extraire les résumés et détails des propriétés")
    print("3. 💾 Sauvegarder les données en base MongoDB (collection temporaire)")
    print("4. ✅ Valider la qualité des données extraites")
    print("5. 🔒 FORCER la configuration Trois-Rivières")
    print("6. 🚫 ÉVITER complètement les données Chambly")
    print("=" * 60)
    
    # Demander confirmation
    response = input("\n🚀 Lancer le test corrigé? (o/N): ").strip().lower()
    
    if response in ['o', 'oui', 'y', 'yes']:
        print("\n🚀 Lancement du test corrigé...")
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
