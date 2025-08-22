# 🏗️ Architecture Modulaire du Pipeline

## 📋 Vue d'Ensemble

Le pipeline utilise une architecture modulaire moderne basée sur des composants spécialisés, chacun ayant une responsabilité unique et bien définie. Cette approche facilite la maintenance, les tests et l'évolution du code.

## 🎯 **Améliorations Récentes**

- ✅ **Structure nettoyée** : Suppression des fichiers redondants et temporaires
- ✅ **Architecture modulaire** : Composants spécialisés et réutilisables
- ✅ **Validation centralisée** : `TypeCategoryValidator` pour la cohérence type/catégorie
- ✅ **Test intégré** : Validation Chambly Plex fonctionnelle à 100%
- ✅ **Code organisé** : Structure claire et maintenable

## 🎯 Principes de Conception

### **1. Responsabilité Unique (Single Responsibility)**

Chaque composant a une seule responsabilité clairement définie.

### **2. Séparation des Préoccupations (Separation of Concerns)**

Les différentes préoccupations (HTTP, parsing, validation, etc.) sont séparées dans des composants distincts.

### **3. Inversion de Dépendance (Dependency Inversion)**

Les composants dépendent d'abstractions, pas de détails d'implémentation.

### **4. Composition sur l'Héritage (Composition over Inheritance)**

L'architecture privilégie la composition de composants spécialisés.

## 🏗️ Structure Modulaire

```
📦 CentrisExtractor (Orchestrateur Principal)
├── 🔌 CentrisSessionManager     # Gestion des sessions HTTP
├── 🔍 CentrisSearchManager      # Recherche et pagination
├── 📋 CentrisSummaryExtractor   # Extraction des résumés
├── 🔎 CentrisDetailExtractor    # Extraction des détails
├── ✅ CentrisDataValidator      # Validation des données
└── 🚀 CentrisExtractor         # Orchestrateur principal
```

## 🔌 CentrisSessionManager

### **Responsabilité**

Gestion des sessions HTTP avec gestion des erreurs, retry automatique et configuration des timeouts.

### **Fonctionnalités**

- Configuration des sessions HTTP
- Gestion des headers et User-Agents
- Retry automatique avec backoff
- Gestion des timeouts
- Rotation des sessions

### **Interface**

```python
class CentrisSessionManager:
    async def get_session(self) -> aiohttp.ClientSession
    async def close(self)
    async def _setup_session(self) -> aiohttp.ClientSession
```

### **Avantages**

- **Réutilisabilité** : Session partagée entre composants
- **Gestion d'erreurs** : Retry automatique centralisé
- **Performance** : Réutilisation des connexions HTTP

## 🔍 CentrisSearchManager

### **Responsabilité**

Construction des requêtes de recherche, gestion de la pagination et communication avec l'API Centris.

### **Fonctionnalités**

- Construction des requêtes de recherche
- Gestion de la pagination
- Appel à l'API Centris
- Gestion des réponses et erreurs

### **Interface**

```python
class CentrisSearchManager:
    async def initialize_search(self, search_query: SearchQuery) -> bool
    async def search_with_pagination(self, search_query: SearchQuery, max_pages: int) -> List[str]
    def _build_search_request(self, search_query: SearchQuery) -> dict
```

### **Avantages**

- **Flexibilité** : Support de différents types de recherche
- **Robustesse** : Gestion de la pagination et des erreurs
- **Maintenabilité** : Logique de recherche centralisée

## 📋 CentrisSummaryExtractor

### **Responsabilité**

Extraction des résumés de propriétés depuis les pages HTML de résultats de recherche.

### **Fonctionnalités**

- Parsing HTML des pages de résultats
- Extraction des informations de base (ID, prix, adresse, type)
- Validation des données extraites
- Gestion des erreurs de parsing

### **Interface**

```python
class CentrisSummaryExtractor:
    def extract_summaries_from_html(self, html_content: str) -> List[PropertySummary]
    def _parse_summaries_from_soup(self, soup: BeautifulSoup) -> List[PropertySummary]
    def _extract_single_summary(self, container: BeautifulSoup) -> Optional[PropertySummary]
```

### **Avantages**

- **Spécialisation** : Focus uniquement sur l'extraction des résumés
- **Testabilité** : Tests unitaires indépendants
- **Évolutivité** : Facile d'ajouter de nouveaux sélecteurs

## 🔎 CentrisDetailExtractor

### **Responsabilité**

Extraction des détails complets des propriétés depuis les pages individuelles.

### **Fonctionnalités**

- Extraction des détails complets
- Parsing des informations détaillées
- Gestion des images et médias
- Validation des données détaillées

### **Interface**

```python
class CentrisDetailExtractor:
    async def extract_details(self, property_id: str) -> Optional[Property]
    def _parse_property_details(self, html_content: str) -> Optional[Property]
```

### **Avantages**

- **Séparation** : Extraction des résumés et détails séparée
- **Performance** : Extraction des détails à la demande
- **Flexibilité** : Support de différents formats de pages

## ✅ CentrisDataValidator

### **Responsabilité**

Validation et nettoyage des données extraites selon des règles métier définies.

### **Fonctionnalités**

- Validation des localisations
- Validation des types de propriétés
- Validation des prix et coordonnées
- Nettoyage des données

### **Interface**

```python
class CentrisDataValidator:
    def validate_search_results(self, summaries: List[PropertySummary], search_query: SearchQuery) -> bool
    def validate_property_data(self, property_data: Property) -> bool
    def _validate_locations(self, summaries: List[PropertySummary], search_query: SearchQuery) -> bool
```

### **Avantages**

- **Qualité** : Assurance de la qualité des données
- **Cohérence** : Validation centralisée des règles métier
- **Maintenabilité** : Règles de validation centralisées

## 🚀 CentrisExtractor (Orchestrateur)

### **Responsabilité**

Coordination de tous les composants et orchestration du processus d'extraction complet.

### **Fonctionnalités**

- Initialisation des composants
- Orchestration du workflow d'extraction
- Gestion des erreurs globales
- Logging et monitoring

### **Interface**

```python
class CentrisExtractor:
    async def extract_summaries(self, search_query: SearchQuery) -> List[PropertySummary]
    async def extract_details(self, property_id: str) -> Optional[Property]
    async def close(self)
```

### **Avantages**

- **Coordination** : Orchestration centralisée du processus
- **Simplicité** : Interface simple pour les utilisateurs
- **Gestion d'erreurs** : Gestion globale des erreurs

## 🔄 Flux de Données

### **1. Initialisation**

```
CentrisExtractor → CentrisSessionManager → Configuration des sessions
```

### **2. Recherche**

```
SearchQuery → CentrisSearchManager → API Centris → Pages HTML
```

### **3. Extraction des Résumés**

```
Pages HTML → CentrisSummaryExtractor → List[PropertySummary]
```

### **4. Validation**

```
List[PropertySummary] → CentrisDataValidator → Résultats validés
```

### **5. Extraction des Détails (Optionnel)**

```
PropertySummary → CentrisDetailExtractor → Property complète
```

## 🧪 Testabilité

### **Tests Unitaires**

Chaque composant peut être testé indépendamment avec des mocks des autres composants.

### **Tests d'Intégration**

Les composants peuvent être testés ensemble pour valider leur interaction.

### **Tests de Performance**

Chaque composant peut être testé individuellement pour identifier les goulots d'étranglement.

## 🔧 Extensibilité

### **Ajout de Nouveaux Extracteurs**

```python
class NewExtractor:
    async def extract_data(self, content: str) -> List[Data]:
        # Implémentation spécifique
        pass

# Intégration dans CentrisExtractor
self.new_extractor = NewExtractor()
```

### **Ajout de Nouvelles Validations**

```python
class CentrisDataValidator:
    def _validate_new_field(self, data: Any) -> bool:
        # Nouvelle règle de validation
        pass
```

### **Ajout de Nouveaux Types de Recherche**

```python
class CentrisSearchManager:
    def _build_new_search_request(self, query: NewQuery) -> dict:
        # Nouveau type de requête
        pass
```

## 📊 Métriques et Monitoring

### **Métriques par Composant**

- **CentrisSessionManager** : Nombre de sessions, taux de succès
- **CentrisSearchManager** : Temps de réponse, nombre de pages
- **CentrisSummaryExtractor** : Taux d'extraction, temps de parsing
- **CentrisDataValidator** : Taux de validation, types d'erreurs

### **Logging Structuré**

```json
{
  "component": "CentrisSummaryExtractor",
  "operation": "extract_summaries",
  "input_size": "27991",
  "output_count": 8,
  "duration_ms": 1250,
  "success": true
}
```

## 🚨 Gestion des Erreurs

### **Stratégies par Composant**

- **CentrisSessionManager** : Retry automatique, rotation des sessions
- **CentrisSearchManager** : Fallback sur des requêtes alternatives
- **CentrisSummaryExtractor** : Sélecteurs alternatifs, validation des données
- **CentrisDataValidator** : Règles de validation flexibles, logging détaillé

### **Propagation des Erreurs**

Les erreurs sont propagées de manière appropriée à travers les composants, permettant une gestion centralisée dans l'orchestrateur.

## 🎯 Avantages de l'Architecture

### **1. Maintenabilité**

- Code organisé et facile à comprendre
- Modifications localisées dans des composants spécifiques
- Documentation claire de chaque composant

### **2. Testabilité**

- Tests unitaires indépendants
- Mocks faciles à créer
- Couverture de code élevée

### **3. Extensibilité**

- Ajout facile de nouvelles fonctionnalités
- Réutilisation des composants existants
- Architecture évolutive

### **4. Performance**

- Optimisation possible par composant
- Parallélisation des opérations
- Gestion efficace des ressources

### **5. Robustesse**

- Gestion d'erreurs localisée
- Fallback et retry automatique
- Validation des données à chaque étape

## 🔮 Évolutions Futures

### **1. Support Multi-Sources**

- Ajout d'extracteurs pour d'autres sites
- Interface commune pour tous les extracteurs
- Comparaison des données entre sources

### **2. Pipeline de Données**

- Intégration avec Apache Kafka
- Traitement en temps réel
- Stockage distribué

### **3. Interface Web**

- Dashboard de monitoring
- Configuration via interface graphique
- Visualisation des données extraites

---

## 🎉 Conclusion

L'architecture modulaire du pipeline offre une base solide pour l'extraction de données immobilières. Elle combine flexibilité, maintenabilité et performance, tout en facilitant l'évolution future du système.

**🚀 Architecture prête pour la production et l'évolution !**
