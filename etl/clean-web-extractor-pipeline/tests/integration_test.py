"""
Tests d'intégration pour l'architecture modulaire du CentrisExtractor
"""

import asyncio
import structlog
from unittest.mock import Mock, patch, AsyncMock
from bs4 import BeautifulSoup

from src.extractors.centris_extractor import CentrisExtractor
from src.models.property import SearchQuery, PropertyType, PropertySummary, Address
from config.settings import config

logger = structlog.get_logger()


class MockCentrisConfig:
    """Configuration mock pour les tests"""
    def __init__(self):
        self.base_url = "https://www.centris.ca"
        self.timeout = 30


class IntegrationTestSuite:
    """Suite de tests d'intégration complète"""
    
    def __init__(self):
        self.mock_config = MockCentrisConfig()
        self.extractor = None
    
    async def setup(self):
        """Configuration initiale pour les tests"""
        logger.info("🔧 Configuration des tests d'intégration...")
        
        # Mock de la configuration
        with patch('config.settings.config') as mock_config:
            mock_config.centris = self.mock_config
            self.extractor = CentrisExtractor(self.mock_config)
        
        logger.info("✅ Configuration terminée")
    
    async def teardown(self):
        """Nettoyage après les tests"""
        if self.extractor:
            await self.extractor.close()
        logger.info("🧹 Nettoyage terminé")
    
    async def test_full_extraction_workflow(self):
        """Test du workflow complet d'extraction"""
        logger.info("🔄 Test du workflow complet d'extraction...")
        
        try:
            # Création d'une requête de recherche
            search_query = SearchQuery(
                locations=["Montréal"],
                property_types=[PropertyType.SELL_CONDO],
                price_min=200000,
                price_max=500000
            )
            
            # Mock des composants internes
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                with patch.object(self.extractor.summary_extractor, 'extract_summaries_from_html') as mock_extract:
                    with patch.object(self.extractor.data_validator, 'validate_search_results') as mock_validate:
                        
                        # Configuration des mocks
                        mock_search.return_value = ["<html>page1</html>", "<html>page2</html>"]
                        mock_extract.return_value = [
                            PropertySummary(
                                id="test1",
                                address=Address(city="Montréal", region="Québec"),
                                type=PropertyType.SELL_CONDO,
                                price=250000,
                                source="centris",
                                last_updated="2024-01-01T00:00:00Z",
                                main_image="https://example.com/image1.jpg",
                                url="https://example.com/property1"
                            ),
                            PropertySummary(
                                id="test2",
                                address=Address(city="Montréal", region="Québec"),
                                type=PropertyType.SELL_CONDO,
                                price=300000,
                                source="centris",
                                last_updated="2024-01-01T00:00:00Z",
                                main_image="https://example.com/image2.jpg",
                                url="https://example.com/property2"
                            )
                        ]
                        mock_validate.return_value = True
                        
                        # Exécution du workflow
                        result = await self.extractor.extract_summaries(search_query)
                        
                        # Vérifications
                        assert len(result) == 4  # 2 propriétés × 2 pages
                        assert all(isinstance(prop, PropertySummary) for prop in result)
                        assert all(prop.address.city == "Montréal" for prop in result)
                        
                        # Vérification des appels aux composants
                        mock_search.assert_called_once_with(search_query)
                        assert mock_extract.call_count == 2  # Une fois par page
                        mock_validate.assert_called_once()
                        
                        logger.info("✅ Workflow complet testé avec succès")
                        return True
                        
        except Exception as e:
            logger.error(f"❌ Erreur du test de workflow: {e}")
            return False
    
    async def test_component_interaction(self):
        """Test des interactions entre composants"""
        logger.info("🔗 Test des interactions entre composants...")
        
        try:
            # Vérification des références entre composants
            assert self.extractor.session_manager is not None
            assert self.extractor.search_manager.session_manager == self.extractor.session_manager
            assert self.extractor.summary_extractor.session_manager == self.extractor.session_manager
            
            # Vérification de la configuration partagée
            assert self.extractor.search_manager.base_url == self.mock_config.base_url
            assert self.extractor.summary_extractor.base_url == self.mock_config.base_url
            
            logger.info("✅ Interactions entre composants validées")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test d'interactions: {e}")
            return False
    
    async def test_error_handling_integration(self):
        """Test de la gestion d'erreurs en intégration"""
        logger.info("⚠️ Test de la gestion d'erreurs en intégration...")
        
        try:
            search_query = SearchQuery(
                locations=["Montréal"],
                property_types=[PropertyType.SELL_CONDO]
            )
            
            # Test avec échec de la recherche
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                mock_search.return_value = []  # Aucune page trouvée
                
                result = await self.extractor.extract_summaries(search_query)
                assert result == []
                
                logger.info("✅ Gestion d'erreur de recherche testée")
            
            # Test avec validation échouée
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                with patch.object(self.extractor.data_validator, 'validate_search_results') as mock_validate:
                    
                    mock_search.return_value = ["<html>page1</html>"]
                    mock_validate.return_value = False  # Validation échouée
                    
                    result = await self.extractor.extract_summaries(search_query)
                    assert result == []
                    
                    logger.info("✅ Gestion d'erreur de validation testée")
            
            logger.info("✅ Gestion d'erreurs en intégration testée avec succès")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test de gestion d'erreurs: {e}")
            return False
    
    async def test_validation_threshold_integration(self):
        """Test de l'intégration du seuil de validation"""
        logger.info("🎯 Test de l'intégration du seuil de validation...")
        
        try:
            # Test du seuil par défaut
            default_threshold = self.extractor.get_validation_threshold()
            assert default_threshold == 0.7
            
            # Modification du seuil
            self.extractor.set_validation_threshold(0.9)
            new_threshold = self.extractor.get_validation_threshold()
            assert new_threshold == 0.9
            
            # Vérification que le composant interne est mis à jour
            assert self.extractor.data_validator.validation_threshold == 0.9
            
            logger.info("✅ Intégration du seuil de validation testée avec succès")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test de seuil de validation: {e}")
            return False
    
    async def test_session_management_integration(self):
        """Test de la gestion des sessions en intégration"""
        logger.info("🔌 Test de la gestion des sessions en intégration...")
        
        try:
            # Vérification de l'initialisation de la session
            assert self.extractor.session_manager.session is not None
            
            # Test de la fermeture propre
            await self.extractor.close()
            assert self.extractor.session_manager.session is None
            
            logger.info("✅ Gestion des sessions en intégration testée avec succès")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test de gestion des sessions: {e}")
            return False


async def run_integration_tests():
    """Exécution de tous les tests d'intégration"""
    logger.info("🚀 Démarrage des tests d'intégration...")
    
    test_suite = IntegrationTestSuite()
    
    try:
        # Configuration
        await test_suite.setup()
        
        # Exécution des tests
        tests = [
            test_suite.test_full_extraction_workflow(),
            test_suite.test_component_interaction(),
            test_suite.test_error_handling_integration(),
            test_suite.test_validation_threshold_integration(),
            test_suite.test_session_management_integration()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Analyse des résultats
        passed = 0
        failed = 0
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"❌ Test {i+1} a levé une exception: {result}")
                failed += 1
            elif result:
                logger.info(f"✅ Test {i+1} réussi")
                passed += 1
            else:
                logger.error(f"❌ Test {i+1} a échoué")
                failed += 1
        
        # Résumé
        logger.info(f"\n📊 Résumé des tests d'intégration:")
        logger.info(f"✅ Réussis: {passed}")
        logger.info(f"❌ Échoués: {failed}")
        logger.info(f"📈 Taux de réussite: {(passed/(passed+failed)*100):.1f}%")
        
        return passed, failed
        
    finally:
        await test_suite.teardown()


if __name__ == "__main__":
    asyncio.run(run_integration_tests())
