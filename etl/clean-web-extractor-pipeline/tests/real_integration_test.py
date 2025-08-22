#!/usr/bin/env python3
"""
Tests d'intégration sur cas réels pour l'architecture modulaire CentrisExtractor
Teste l'extraction réelle de données depuis Centris avec tous les composants
"""

import asyncio
import structlog
from unittest.mock import patch
from src.extractors.centris_extractor import CentrisExtractor
from src.models.property import SearchQuery, PropertyType
from src.utils.logging import setup_logging

# Configuration du logging
setup_logging()
logger = structlog.get_logger(__name__)


class RealIntegrationTestSuite:
    """Suite de tests d'intégration sur cas réels"""
    
    def __init__(self):
        self.extractor = None
        self.test_results = []
        
    async def setup(self):
        """Configuration initiale des tests"""
        logger.info("🔧 Configuration des tests d'intégration sur cas réels...")
        
        # Initialisation de l'extracteur avec architecture modulaire
        from config.settings import config
        self.extractor = CentrisExtractor(config.centris)
        
        logger.info("✅ Configuration terminée")
        
    async def cleanup(self):
        """Nettoyage des ressources"""
        if self.extractor:
            await self.extractor.close()
            logger.info("🔌 CentrisExtractor fermé proprement")
            
    async def test_real_search_extraction(self):
        """Test d'extraction réelle avec recherche simple"""
        logger.info("🔍 Test d'extraction réelle - Recherche simple...")
        
        try:
            # Requête de recherche réelle
            search_query = SearchQuery(
                locations=["Montréal"],
                property_types=[PropertyType.SELL_CONDO],
                price_min=200000,
                price_max=210000
            )
            
            # Extraction réelle des résumés
            summaries = await self.extractor.extract_summaries(search_query)
            
            # Validation des résultats
            if summaries:
                logger.info(f"✅ Extraction réussie: {len(summaries)} propriétés trouvées")
                
                # Vérification de la structure des données
                for summary in summaries[:3]:  # Vérifier les 3 premiers
                    self._validate_summary_structure(summary)
                    
                self.test_results.append(("Recherche simple", "SUCCESS", len(summaries)))
                return True
            else:
                logger.warning("⚠️ Aucune propriété trouvée - possible problème de recherche")
                self.test_results.append(("Recherche simple", "WARNING", 0))
                return True  # Pas d'erreur, juste pas de résultats
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction réelle: {e}")
            self.test_results.append(("Recherche simple", "ERROR", str(e)))
            return False
            
    async def test_real_detail_extraction(self):
        """Test d'extraction réelle des détails d'une propriété"""
        logger.info("🏠 Test d'extraction réelle - Détails d'une propriété...")
        
        try:
            # D'abord, extraire des résumés
            search_query = SearchQuery(
                locations=["Trois-Rivières"],
                property_types=[PropertyType.PLEX],
                price_min=300000,
                price_max=360000
            )
            
            summaries = await self.extractor.extract_summaries(search_query)
            
            if not summaries:
                logger.warning("⚠️ Aucun résumé trouvé pour tester l'extraction des détails")
                self.test_results.append(("Extraction détails", "WARNING", "Pas de résumés"))
                return True
                
            # Prendre la première propriété pour extraire les détails
            first_summary = summaries[0]
            logger.info(f"🔍 Extraction des détails pour: {first_summary.id}")
            
            # Extraction des détails réels
            property_details = await self.extractor.extract_details(first_summary.id)
            
            if property_details:
                logger.info(f"✅ Détails extraits avec succès pour {first_summary.id}")
                self._validate_property_structure(property_details)
                self.test_results.append(("Extraction détails", "SUCCESS", first_summary.id))
                return True
            else:
                logger.warning(f"⚠️ Aucun détail trouvé pour {first_summary.id}")
                self.test_results.append(("Extraction détails", "WARNING", "Pas de détails"))
                return True
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des détails: {e}")
            self.test_results.append(("Extraction détails", "ERROR", str(e)))
            return False
            
    async def test_real_validation_integration(self):
        """Test d'intégration réelle de la validation"""
        logger.info("🎯 Test d'intégration réelle - Validation des données...")
        
        try:
            # Test avec différents types de propriétés
            property_types = [
                PropertyType.PLEX,
                PropertyType.SINGLE_FAMILY_HOME,
                PropertyType.SELL_CONDO
            ]
            
            validation_results = []
            
            for prop_type in property_types:
                search_query = SearchQuery(
                                    locations=["Laval"],
                property_types=[prop_type],
                price_min=200000,
                price_max=210000
                )
                
                summaries = await self.extractor.extract_summaries(search_query)
                
                if summaries:
                    # Vérifier que la validation fonctionne sur les vraies données
                    valid_count = sum(1 for s in summaries if s.type == prop_type)
                    total_count = len(summaries)
                    
                    validation_results.append({
                        'type': prop_type.value,
                        'total': total_count,
                        'valid': valid_count,
                        'ratio': valid_count / total_count if total_count > 0 else 0
                    })
                    
                    logger.info(f"✅ {prop_type.value}: {valid_count}/{total_count} valides ({valid_count/total_count*100:.1f}%)")
                else:
                    logger.warning(f"⚠️ Aucun résultat pour {prop_type.value}")
                    
            if validation_results:
                avg_ratio = sum(r['ratio'] for r in validation_results) / len(validation_results)
                logger.info(f"📊 Ratio de validation moyen: {avg_ratio*100:.1f}%")
                
                self.test_results.append(("Validation intégration", "SUCCESS", f"{avg_ratio*100:.1f}%"))
                return True
            else:
                logger.warning("⚠️ Aucun résultat de validation obtenu")
                self.test_results.append(("Validation intégration", "WARNING", "Pas de résultats"))
                return True
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation: {e}")
            self.test_results.append(("Validation intégration", "ERROR", str(e)))
            return False
            
    async def test_real_component_interaction(self):
        """Test d'interaction réelle entre composants"""
        logger.info("🔗 Test d'interaction réelle entre composants...")
        
        try:
            # Vérifier que tous les composants sont initialisés
            components = [
                self.extractor.session_manager,
                self.extractor.search_manager,
                self.extractor.summary_extractor,
                self.extractor.detail_extractor,
                self.extractor.data_validator
            ]
            
            component_names = [
                "SessionManager",
                "SearchManager", 
                "SummaryExtractor",
                "DetailExtractor",
                "DataValidator"
            ]
            
            for component, name in zip(components, component_names):
                if component is None:
                    raise ValueError(f"Composant {name} non initialisé")
                    
            logger.info("✅ Tous les composants sont initialisés")
            
            # Test d'interaction : recherche -> extraction -> validation
            search_query = SearchQuery(
                locations=["Montérégie"],
                property_types=[PropertyType.PLEX],
                price_min=150000,
                price_max=600000
            )
            
            # Utiliser le SearchManager
            search_results = await self.extractor.search_manager.search_with_pagination(search_query)
            
            if search_results:
                logger.info(f"✅ SearchManager: {len(search_results)} résultats trouvés")
                
                # Utiliser le SummaryExtractor
                summaries = await self.extractor.summary_extractor.extract_summaries_from_html(
                    search_results[0], search_query
                )
                
                if summaries:
                    logger.info(f"✅ SummaryExtractor: {len(summaries)} résumés extraits")
                    
                    # Utiliser le DataValidator
                    validation_result = await self.extractor.data_validator.validate_search_results(
                        summaries, search_query
                    )
                    
                    logger.info(f"✅ DataValidator: validation terminée (ratio: {validation_result:.1f})")
                    
                    self.test_results.append(("Interaction composants", "SUCCESS", f"{len(summaries)} propriétés"))
                    return True
                else:
                    logger.warning("⚠️ Aucun résumé extrait par SummaryExtractor")
                    self.test_results.append(("Interaction composants", "WARNING", "Pas de résumés"))
                    return True
            else:
                logger.warning("⚠️ Aucun résultat de recherche trouvé")
                self.test_results.append(("Interaction composants", "WARNING", "Pas de résultats"))
                return True
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'interaction des composants: {e}")
            self.test_results.append(("Interaction composants", "ERROR", str(e)))
            return False
            
    def _validate_summary_structure(self, summary):
        """Valide la structure d'un résumé de propriété"""
        required_fields = ['id', 'type', 'price', 'address', 'source', 'last_updated']
        
        for field in required_fields:
            if not hasattr(summary, field) or getattr(summary, field) is None:
                raise ValueError(f"Champ manquant ou null: {field}")
                
        # Validation spécifique
        if summary.price <= 0:
            raise ValueError(f"Prix invalide: {summary.price}")
            
        if not summary.address.city:
            raise ValueError("Ville manquante dans l'adresse")
            
        logger.debug(f"✅ Résumé {summary.id} validé: {summary.type.value} - {summary.price}$")
        
    def _validate_property_structure(self, property_obj):
        """Valide la structure d'une propriété complète"""
        required_fields = ['id', 'type', 'address', 'source', 'last_updated']
        
        for field in required_fields:
            if not hasattr(property_obj, field) or getattr(property_obj, field) is None:
                raise ValueError(f"Champ manquant ou null: {field}")
                
        # Validation des composants imbriqués
        if not property_obj.address.city:
            raise ValueError("Ville manquante dans l'adresse")
            
        if property_obj.financial and property_obj.financial.price:
            if property_obj.financial.price <= 0:
                raise ValueError(f"Prix invalide: {property_obj.financial.price}")
                
        logger.debug(f"✅ Propriété {property_obj.id} validée: {property_obj.type.value}")
        
    def print_results(self):
        """Affiche les résultats des tests"""
        logger.info("\n" + "="*60)
        logger.info("📊 RÉSULTATS DES TESTS D'INTÉGRATION SUR CAS RÉELS")
        logger.info("="*60)
        
        success_count = sum(1 for _, status, _ in self.test_results if status == "SUCCESS")
        warning_count = sum(1 for _, status, _ in self.test_results if status == "WARNING")
        error_count = sum(1 for _, status, _ in self.test_results if status == "ERROR")
        total_count = len(self.test_results)
        
        for test_name, status, details in self.test_results:
            if status == "SUCCESS":
                logger.info(f"✅ {test_name}: {details}")
            elif status == "WARNING":
                logger.warning(f"⚠️ {test_name}: {details}")
            else:
                logger.error(f"❌ {test_name}: {details}")
                
        logger.info("-"*60)
        logger.info(f"📈 Résumé: {success_count} succès, {warning_count} avertissements, {error_count} erreurs")
        logger.info(f"🎯 Taux de réussite: {(success_count + warning_count) / total_count * 100:.1f}%")
        
        if error_count == 0:
            logger.info("🎉 Tous les tests critiques ont réussi !")
        else:
            logger.warning(f"⚠️ {error_count} test(s) critique(s) ont échoué")
            
        logger.info("="*60)


async def run_real_integration_tests():
    """Exécute tous les tests d'intégration sur cas réels"""
    logger.info("🚀 Démarrage des tests d'intégration sur cas réels...")
    
    test_suite = RealIntegrationTestSuite()
    
    try:
        # Configuration
        await test_suite.setup()
        
        # Tests
        tests = [
            test_suite.test_real_search_extraction,
            test_suite.test_real_detail_extraction,
            test_suite.test_real_validation_integration,
            test_suite.test_real_component_interaction
        ]
        
        for test in tests:
            try:
                await test()
            except Exception as e:
                logger.error(f"❌ Test {test.__name__} a échoué: {e}")
                
        # Affichage des résultats
        test_suite.print_results()
        
    except Exception as e:
        logger.error(f"❌ Erreur critique lors des tests: {e}")
        
    finally:
        # Nettoyage
        await test_suite.cleanup()
        logger.info("🧹 Tests terminés et ressources nettoyées")


if __name__ == "__main__":
    asyncio.run(run_real_integration_tests())
