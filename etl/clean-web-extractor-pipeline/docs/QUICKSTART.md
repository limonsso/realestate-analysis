# 🚀 Guide de Démarrage Rapide

## ⚡ Installation Express

## 🎯 **Pipeline Nettoyé et Optimisé**

Le pipeline a été **entièrement refactorisé** pour :

- ✅ **Structure claire** : Architecture modulaire et maintenable
- ✅ **Validation robuste** : Cohérence type/catégorie automatique
- ✅ **Test intégré** : Validation Chambly Plex fonctionnelle
- ✅ **Code organisé** : Suppression des fichiers redondants

### **1. Prérequis**

```bash
# Python 3.8+
python3 --version

# Git
git --version

# MongoDB (optionnel pour les tests)
mongod --version
```

### **2. Installation**

```bash
# Cloner le repository
git clone <repository-url>
cd clean-web-extractor-pipeline

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### **3. Configuration Rapide**

```bash
# Copier et configurer l'environnement
cp env.example .env
# Éditer .env avec vos paramètres MongoDB

# Copier et configurer Centris
cp config/centris_ids.example.yml config/centris_ids.yml
# Éditer centris_ids.yml avec vos IDs de localisation
```

## 🎯 Première Exécution

### **Test Principal : Chambly Plex**

```bash
# Test complet d'extraction de plex à Chambly
python run_chambly_test.py

# Ce test valide l'ensemble du pipeline :
# ✅ Recherche de propriétés à Chambly
# ✅ Extraction des résumés et détails
# ✅ Sauvegarde en base MongoDB
# ✅ Validation de la cohérence type/catégorie
```

### **Exécution Complète**

```python
# run.py
from src.extractors.centris_extractor import CentrisExtractor
from config.settings import config
from src.models.property import SearchQuery, LocationConfig

async def main():
    # Initialisation
    extractor = CentrisExtractor(config.centris)

    # Recherche simple
    search_query = SearchQuery(
        locations=[
            LocationConfig(
                type="GeographicArea",
                value="Montérégie",
                type_id="RARA16"
            )
        ],
        property_types=["Plex"],
        price_min=200000,
        price_max=260000
    )

    # Extraction
    summaries = await extractor.extract_summaries(search_query)
    print(f"✅ {len(summaries)} propriétés trouvées")

    # Fermeture
    await extractor.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## 🔧 Configuration Essentielle

### **Variables d'Environnement Minimales**

```bash
# .env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=real_estate
MONGODB_COLLECTION=properties
CENTRIS_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

### **Configuration YAML Minimale**

```yaml
# config/config.yml
database:
  uri: ${MONGODB_URI}
  database: ${MONGODB_DATABASE}
  collection: ${MONGODB_COLLECTION}

centris:
  base_url: https://www.centris.ca
  user_agent: ${CENTRIS_USER_AGENT}
  locations_searched:
    - type: "GeographicArea"
      value: "Montérégie"
      type_id: "RARA16"
  property_types: ["Plex"]
  sale_price_min: 200000
  sale_price_max: 260000

pipeline:
  max_workers: 2
  batch_size: 5
  request_timeout: 30
  max_retries: 3
  log_level: "INFO"
```

## 🧪 Tests Essentiels

### **1. Test de Structure** ✅

```bash
python tests/test_centris_structure.py
```

**Résultat attendu** : Structure des requêtes validée

### **2. Test d'Intégration** 🔗

```bash
python tests/updated_integration_test.py
```

**Résultat attendu** : Composants modulaires validés

### **3. Test d'Extraction Réelle** 🏠

```bash
python tests/real_extraction_test.py
```

**Résultat attendu** : Données extraites de Centris

## 📊 Premiers Résultats

### **Exemple de Sortie**

```json
{
  "timestamp": "2025-08-22T04:40:41.517661Z",
  "level": "info",
  "event": "🏠 Extraction réussie: 8 propriétés",
  "search_query": "Montérégie - Plex",
  "pages_processed": 1,
  "properties_found": 8
}
```

### **Données Extraites**

```python
# Exemple de PropertySummary
PropertySummary(
    id="16871982",
    address=Address(
        street="123 Rue Principale",
        city="Saint-Hyacinthe",
        region="Montérégie"
    ),
    price=245000.0,
    type=PropertyType.PLEX,
    source="Centris"
)
```

## 🚨 Dépannage Rapide

### **Erreurs Courantes**

#### **1. ModuleNotFoundError**

```bash
# Solution
export PYTHONPATH="."
python tests/test_name.py
```

#### **2. Erreur de Configuration**

```bash
# Vérifier
ls -la config/
cat config/config.yml
```

#### **3. Erreur MongoDB**

```bash
# Vérifier la connexion
mongosh mongodb://localhost:27017
```

### **Logs de Débogage**

```bash
# Activer les logs détaillés
export LOG_LEVEL="DEBUG"
python tests/real_extraction_test.py
```

## 📈 Prochaines Étapes

### **1. Personnalisation**

- Modifier les localisations dans `config/config.yml`
- Ajuster les fourchettes de prix
- Configurer les types de propriétés

### **2. Production**

- Configurer MongoDB de production
- Ajuster les timeouts et retry
- Configurer le logging avancé

### **3. Monitoring**

- Surveiller les logs dans `logs/`
- Analyser les métriques de performance
- Configurer les alertes

## 🎯 Checklist de Démarrage

- [ ] **Environnement Python** : Python 3.8+ installé
- [ ] **Dépendances** : `pip install -r requirements.txt` ✅
- [ ] **Configuration** : `.env` et `config.yml` configurés
- [ ] **Test Structure** : `test_centris_structure.py` ✅
- [ ] **Test Intégration** : `updated_integration_test.py` ✅
- [ ] **Test Extraction** : `real_extraction_test.py` ✅
- [ ] **Première Exécution** : Pipeline fonctionnel ✅

## 🔗 Ressources Utiles

- **Documentation complète** : [README.md](README.md)
- **Architecture** : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Tests** : [docs/TESTING.md](docs/TESTING.md)
- **Configuration** : [config/](config/)

---

## 🎉 Félicitations !

Votre pipeline est maintenant opérationnel et prêt à extraire des données immobilières depuis Centris.ca !

**🚀 Prêt pour l'extraction de données à grande échelle !**
