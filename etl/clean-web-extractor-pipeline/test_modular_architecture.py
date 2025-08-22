"""
Test de la nouvelle architecture modulaire du CentrisExtractor
"""

import asyncio
import structlog
from src.extractors.centris_extractor import CentrisExtractor
from src.models.property import SearchQuery, PropertyType
from config.settings import config

logger = structlog.get_logger()


async def test_modular_architecture():
    """Test de l'architecture modulaire"""
    print("🧪 Test de l'architecture modulaire...")
    
    try:
        # Création de l'extracteur
        extractor = CentrisExtractor(config.centris)
        print("✅ CentrisExtractor créé avec succès")
        
        # Test des composants
        print("  🔧 Test des composants...")
        
        # Session Manager
        assert extractor.session_manager is not None
        assert extractor.session_manager.session is not None
        print("    ✅ Session Manager")
        
        # Search Manager
        assert extractor.search_manager is not None
        assert extractor.search_manager.session_manager == extractor.session_manager
        print("    ✅ Search Manager")
        
        # Summary Extractor
        assert extractor.summary_extractor is not None
        print("    ✅ Summary Extractor")
        
        # Detail Extractor
        assert extractor.detail_extractor is not None
        print("    ✅ Detail Extractor")
        
        # Data Validator
        assert extractor.data_validator is not None
        print("    ✅ Data Validator")
        
        # Test du seuil de validation
        extractor.set_validation_threshold(0.8)
        assert extractor.get_validation_threshold() == 0.8
        print("    ✅ Configuration du seuil de validation")
        
        # Test de fermeture
        await extractor.close()
        print("    ✅ Fermeture propre")
        
        print("✅ Architecture modulaire testée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur du test: {e}")
        return False


async def test_component_initialization():
    """Test de l'initialisation des composants"""
    print("🔧 Test de l'initialisation des composants...")
    
    try:
        from src.extractors.centris.session_manager import CentrisSessionManager
        from src.extractors.centris.search_manager import CentrisSearchManager
        from src.extractors.centris.summary_extractor import CentrisSummaryExtractor
        from src.extractors.centris.detail_extractor import CentrisDetailExtractor
        from src.extractors.centris.data_validator import CentrisDataValidator
        
        # Test Session Manager
        session_manager = CentrisSessionManager(config.centris)
        assert session_manager.session is not None
        await session_manager.close()
        print("    ✅ Session Manager")
        
        # Test Data Validator
        validator = CentrisDataValidator()
        assert validator.validation_threshold == 0.7
        validator.set_validation_threshold(0.9)
        assert validator.validation_threshold == 0.9
        print("    ✅ Data Validator")
        
        # Test Detail Extractor
        detail_extractor = CentrisDetailExtractor()
        assert detail_extractor.validators is not None
        print("    ✅ Detail Extractor")
        
        print("✅ Initialisation des composants testée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur du test d'initialisation: {e}")
        return False


async def main():
    """Fonction principale de test"""
    print("🚀 Test de l'architecture modulaire du CentrisExtractor")
    print("=" * 60)
    
    # Test de l'architecture
    arch_test = await test_modular_architecture()
    
    # Test des composants
    comp_test = await test_component_initialization()
    
    # Résumé
    print("\n" + "=" * 60)
    if arch_test and comp_test:
        print("🎉 Tous les tests de l'architecture modulaire ont réussi !")
        print("✅ Le CentrisExtractor est maintenant modulaire et maintenable")
    else:
        print("❌ Certains tests ont échoué")
    
    return arch_test and comp_test


if __name__ == "__main__":
    asyncio.run(main())

