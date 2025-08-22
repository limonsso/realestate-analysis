#!/usr/bin/env python3
"""
Script de test simple pour vérifier le pipeline
Teste les composants principaux sans exécuter l'extraction complète
"""

import sys
import asyncio
from pathlib import Path

# Ajout des chemins au PYTHONPATH
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "src"))
sys.path.insert(0, str(current_dir / "config"))

def test_imports():
    """Teste l'import des modules principaux"""
    print("🔍 Test des imports...")
    
    try:
        from src.models.property import Property, PropertyType, PropertyStatus
        from src.extractors.centris_extractor import CentrisExtractor
        from src.services.database_service import DatabaseService
        from src.utils.logging import setup_logging, get_logger
        from config.settings import config
        print("✅ Tous les imports réussis")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_config():
    """Teste la configuration"""
    print("🔧 Test de la configuration...")
    
    try:
        from config.settings import config
        
        # Vérification des éléments de base
        assert hasattr(config, 'centris'), "Configuration Centris manquante"
        assert hasattr(config, 'database'), "Configuration base de données manquante"
        assert len(config.centris.locations_searched) > 0, "Aucune localisation configurée"
        assert len(config.centris.property_types) > 0, "Aucun type de propriété configuré"
        
        print(f"✅ Configuration valide:")
        print(f"   - {len(config.centris.locations_searched)} localisations")
        print(f"   - {len(config.centris.property_types)} types de propriétés")
        print(f"   - Base de données: {config.database.server_url}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

def test_models():
    """Teste les modèles de données"""
    print("📊 Test des modèles...")
    
    try:
        from src.models.property import Property, PropertyType, PropertyStatus, Address, FinancialInfo
        
        # Création d'une propriété de test
        test_property = Property(
            id="TEST123",
            type=PropertyType.SINGLE_FAMILY_HOME,
            status=PropertyStatus.FOR_SALE,
            address=Address(
                street="123 Test St",
                city="Test City",
                region="Test Region"
            ),
            financial=FinancialInfo(
                price=500000
            )
        )
        
        # Vérification des propriétés calculées
        assert test_property.id == "TEST123", "ID incorrect"
        assert test_property.type == PropertyType.SINGLE_FAMILY_HOME, "Type incorrect"
        assert test_property.financial.price == 500000, "Prix incorrect"
        
        print("✅ Modèles de données valides")
        return True
    except Exception as e:
        print(f"❌ Erreur des modèles: {e}")
        return False

def test_logging():
    """Teste le système de logging"""
    print("📝 Test du logging...")
    
    try:
        from src.utils.logging import setup_logging, get_logger
        
        # Configuration du logging
        setup_logging(log_level="INFO", log_format="console")
        
        # Test du logger
        logger = get_logger("test")
        logger.info("Test de logging réussi")
        
        print("✅ Système de logging fonctionnel")
        return True
    except Exception as e:
        print(f"❌ Erreur du logging: {e}")
        return False

async def test_extractor():
    """Teste l'extracteur (sans connexion réseau)"""
    print("🔍 Test de l'extracteur...")
    
    try:
        from src.extractors.centris_extractor import CentrisExtractor
        from config.settings import config
        
        # Création de l'extracteur
        extractor = CentrisExtractor(config.centris)
        
        # Test de la configuration
        assert extractor.base_url == "https://www.centris.ca", "URL de base incorrecte"
        assert extractor.config == config.centris, "Configuration incorrecte"
        
        print("✅ Extracteur configuré correctement")
        return True
    except Exception as e:
        print(f"❌ Erreur de l'extracteur: {e}")
        return False

def test_database_service():
    """Teste le service de base de données (sans connexion)"""
    print("🗄️ Test du service de base de données...")
    
    try:
        from src.services.database_service import DatabaseService
        from config.settings import config
        
        # Création du service (sans connexion)
        db_service = DatabaseService(config.database)
        
        # Vérification de la configuration
        assert db_service.config == config.database, "Configuration incorrecte"
        assert db_service.config.server_url == config.database.server_url, "URL serveur incorrecte"
        
        # Test de la configuration des noms de collections
        db_service.set_collection_names(
            properties_collection="test_properties",
            summaries_collection="test_summaries",
            logs_collection="test_logs"
        )
        
        assert db_service.collection_names['properties'] == "test_properties", "Nom de collection propriétés incorrect"
        assert db_service.collection_names['summaries'] == "test_summaries", "Nom de collection résumés incorrect"
        assert db_service.collection_names['logs'] == "test_logs", "Nom de collection logs incorrect"
        
        print("✅ Service de base de données configuré")
        return True
    except Exception as e:
        print(f"❌ Erreur du service de base de données: {e}")
        return False

async def test_validation_functionality():
    """Teste la fonctionnalité de validation des résultats"""
    print("🔍 Test de la fonctionnalité de validation...")
    
    try:
        from src.extractors.centris_extractor import CentrisExtractor
        from src.models.property import PropertySummary, Address, PropertyType, SearchQuery
        from src.utils.validators import RegionValidator, PropertyValidator
        from config.settings import config
        
        # Test des validateurs de base
        print("  🔍 Test des validateurs de base...")
        
        # Test validation des régions
        assert RegionValidator.is_valid_region("Montréal") == True
        assert RegionValidator.is_valid_region("InvalidRegion") == False
        print("    ✅ Validation des régions")
        
        # Test validation des prix
        assert PropertyValidator.is_valid_price(250000) == True
        assert PropertyValidator.is_valid_price(-1000) == False
        print("    ✅ Validation des prix")
        
        # Test validation des codes postaux
        assert PropertyValidator.is_valid_postal_code("H1A 1A1") == True
        assert PropertyValidator.is_valid_postal_code("12345") == False
        print("    ✅ Validation des codes postaux")
        
        # Création d'un extracteur de test
        extractor = CentrisExtractor(config.centris)
        
        # Création de données de test
        test_properties = [
            PropertySummary(
                id="test1",
                address=Address(city="Montréal", region="Québec"),
                type=PropertyType.CONDO,
                price=250000
            ),
            PropertySummary(
                id="test2", 
                address=Address(city="Montréal", region="Québec"),
                type=PropertyType.CONDO,
                price=300000
            ),
            PropertySummary(
                id="test3",
                address=Address(city="Laval", region="Québec"), 
                type=PropertyType.CONDO,
                price=275000
            )
        ]
        
        # Test de validation avec critères correspondants
        search_query = SearchQuery(
            locations=["Montréal"],
            property_types=[PropertyType.CONDO]
        )
        
        # Test de la validation des localisations
        location_valid = extractor._validate_locations_searched(test_properties, ["Montréal"])
        print(f"✅ Validation des localisations: {location_valid}")
        
        # Test de la validation des types
        type_valid = extractor._validate_property_types(test_properties, [PropertyType.CONDO])
        print(f"✅ Validation des types: {type_valid}")
        
        # Test de la validation globale
        is_valid = extractor._validate_search_results(test_properties, search_query)
        print(f"✅ Validation globale: {is_valid}")
        
        if is_valid:
            print("✅ Toutes les validations fonctionnent correctement")
            return True
        else:
            print("❌ Validation des résultats échoue")
            return False
            
    except Exception as e:
        print(f"❌ Erreur du test de validation: {e}")
        return False

async def main():
    """Fonction principale de test"""
    print("🧪 Démarrage des tests du pipeline...")
    print("=" * 50)
    
    # Liste des tests à exécuter
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Modèles", test_models),
        ("Logging", test_logging),
        ("Extracteur", test_extractor),
        ("Base de données", test_database_service),
        ("Validation", test_validation_functionality),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Test: {test_name}")
        print("-" * 30)
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📊 Résumé des tests:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés! Le pipeline est prêt à être utilisé.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrompus par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Erreur fatale lors des tests: {e}")
        sys.exit(1)
