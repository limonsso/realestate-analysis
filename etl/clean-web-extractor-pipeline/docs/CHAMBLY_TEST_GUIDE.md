# 🏠 Guide du Test d'Extraction Chambly Plex

## 📋 Vue d'Ensemble

Ce guide vous accompagne dans l'exécution du test d'extraction réelle de données de plex à Chambly depuis Centris.ca avec stockage en base MongoDB.

## 🎯 **Statut : 100% Fonctionnel ✅**

Le test Chambly Plex est maintenant **entièrement opérationnel** avec :

- ✅ Extraction complète des résumés et détails
- ✅ Sauvegarde MongoDB réussie
- ✅ Validation de la cohérence type/catégorie
- ✅ Structure nettoyée et optimisée

## 🎯 Objectifs du Test

### **Ce que fait le test :**

1. **🔍 Recherche** : Trouve des plex à Chambly sur Centris.ca
2. **📊 Extraction** : Extrait les résumés et détails des propriétés
3. **💾 Stockage** : Sauvegarde les données en base MongoDB
4. **✅ Validation** : Vérifie la qualité des données extraites

### **Données ciblées :**

- **Localisation** : Chambly (CityDistrict ID: 730)
- **Type de propriété** : Plex uniquement
- **Fourchette de prix** : 200,000$ - 600,000$
- **Source** : Centris.ca

## 🚀 Préparation du Test

### **1. Prérequis**

```bash
# Vérifier Python 3.8+
python3 --version

# Vérifier MongoDB
mongod --version

# Vérifier les dépendances
pip list | grep -E "(aiohttp|pymongo|pydantic|structlog)"
```

### **2. Configuration de l'Environnement**

```bash
# Copier le fichier d'environnement
cp env.chambly_test .env.chambly_test

# Éditer selon votre environnement
nano .env.chambly_test

# Charger les variables
source .env.chambly_test
```

### **3. Vérification de la Configuration**

```bash
# Vérifier la configuration MongoDB
mongosh mongodb://localhost:27017/real_estate_test

# Vérifier la connectivité Centris
curl -I "https://www.centris.ca"
```

## 🧪 Exécution du Test

### **Méthode 1 : Script Interactif (Recommandé)**

```bash
# Lancer le test interactif
python run_chambly_test.py

# Le script demandera confirmation avant de lancer
# Répondre 'o' ou 'oui' pour continuer
```

### **Méthode 2 : Test Direct**

```bash
# Exécuter directement le test
python tests/test_chambly_plex_extraction.py
```

### **Méthode 3 : Avec Variables d'Environnement**

```bash
# Charger l'environnement et lancer
source .env.chambly_test
python tests/test_chambly_plex_extraction.py
```

## 📊 Suivi du Test

### **Logs en Temps Réel**

```bash
# Suivre les logs du test
tail -f logs/chambly_test.log

# Ou avec structlog en mode console
export LOG_LEVEL=DEBUG
python tests/test_chambly_plex_extraction.py
```

### **Indicateurs de Progression**

- 🔧 **Configuration** : Initialisation des composants
- 🔍 **Recherche** : Construction des requêtes Centris
- 📊 **Extraction** : Récupération des données
- 💾 **Sauvegarde** : Stockage en base MongoDB
- ✅ **Validation** : Vérification de la qualité

## 📈 Résultats Attendus

### **Métriques de Succès**

- **Résumés extraits** : 5-20 propriétés
- **Détails extraits** : 3-10 propriétés complètes
- **Collection créée** : `chambly_plex_test_YYYYMMDD_HHMMSS`
- **Validation** : 4-5 critères sur 5 validés

### **Exemple de Sortie Réussie**

```
🎉 RÉSULTATS DU TEST CHAMBLY PLEX
============================================================
🏠 Résumés extraits: 12
🔍 Détails extraits: 8
💾 Collection créée: chambly_plex_test_20250822_143022

📋 Validation des données:
   ✅ adresses_complètes: True
   ✅ prix_valides: True
   ✅ types_corrects: True
   ✅ ids_uniques: True
   ✅ localisation_chambly: True
```

## 🔍 Analyse des Résultats

### **1. Vérification en Base MongoDB**

```bash
# Se connecter à MongoDB
mongosh mongodb://localhost:27017/real_estate_test

# Lister les collections
show collections

# Compter les propriétés
db.chambly_plex_test_YYYYMMDD_HHMMSS.countDocuments()

# Voir un exemple de propriété
db.chambly_plex_test_YYYYMMDD_HHMMSS.findOne()
```

### **2. Requêtes d'Analyse**

```javascript
// Propriétés par prix
db.chambly_plex_test_YYYYMMDD_HHMMSS.aggregate([
  {
    $group: {
      _id: null,
      count: { $sum: 1 },
      avgPrice: { $avg: "$financial.price" },
      minPrice: { $min: "$financial.price" },
      maxPrice: { $max: "$financial.price" },
    },
  },
]);

// Adresses à Chambly
db.chambly_plex_test_YYYYMMDD_HHMMSS.find({
  "address.city": { $regex: /chambly/i },
});
```

### **3. Validation des Données**

```javascript
// Vérifier les types de propriétés
db.chambly_plex_test_YYYYMMDD_HHMMSS.distinct("type");

// Vérifier les villes
db.chambly_plex_test_YYYYMMDD_HHMMSS.distinct("address.city");

// Vérifier les prix
db.chambly_plex_test_YYYYMMDD_HHMMSS.find({
  "financial.price": { $exists: true, $gt: 0 },
});
```

## 🚨 Dépannage

### **Problèmes Courants**

#### **1. Erreur de Connexion MongoDB**

```bash
# Vérifier le service MongoDB
sudo systemctl status mongod

# Redémarrer si nécessaire
sudo systemctl restart mongod

# Vérifier la connexion
mongosh mongodb://localhost:27017
```

#### **2. Erreur de Configuration**

```bash
# Vérifier le fichier de configuration
cat config/chambly_test_config.yml

# Vérifier les variables d'environnement
env | grep -E "(MONGODB|CENTRIS|PIPELINE)"
```

#### **3. Erreur d'Extraction Centris**

```bash
# Vérifier la connectivité
curl -I "https://www.centris.ca"

# Vérifier le User-Agent
curl -H "User-Agent: Mozilla/5.0..." "https://www.centris.ca"

# Vérifier les logs détaillés
export LOG_LEVEL=DEBUG
python tests/test_chambly_plex_extraction.py
```

#### **4. Aucune Propriété Trouvée**

```bash
# Vérifier la configuration des prix
echo $SALE_PRICE_MIN
echo $SALE_PRICE_MAX

# Vérifier la localisation
cat config/chambly_test_config.yml | grep -A 5 "locations_searched"

# Tester avec une fourchette plus large
export SALE_PRICE_MIN=100000
export SALE_PRICE_MAX=1000000
```

### **Logs de Débogage**

```bash
# Activer les logs détaillés
export LOG_LEVEL=DEBUG
export LOG_FILE=logs/chambly_debug.log

# Lancer le test
python tests/test_chambly_plex_extraction.py

# Analyser les logs
tail -f logs/chambly_debug.log
```

## 🔧 Personnalisation

### **Modifier la Localisation**

```yaml
# config/chambly_test_config.yml
centris:
  locations_searched:
    - type: "GeographicArea"
      value: "Laurentides" # Changer pour une autre région
      type_id: "RARA15"
```

### **Modifier les Types de Propriétés**

```yaml
# config/chambly_test_config.yml
centris:
  property_types: ["Plex", "SingleFamilyHome"] # Ajouter d'autres types
```

### **Modifier les Fourchettes de Prix**

```bash
# .env.chambly_test
SALE_PRICE_MIN=150000
SALE_PRICE_MAX=800000
```

## 📊 Métriques et Performance

### **Temps d'Exécution Typiques**

- **Configuration** : 2-5 secondes
- **Recherche** : 10-30 secondes
- **Extraction des résumés** : 15-45 secondes
- **Extraction des détails** : 30-90 secondes
- **Sauvegarde** : 5-15 secondes
- **Validation** : 2-5 secondes

### **Utilisation des Ressources**

- **Mémoire** : 50-200 MB selon le nombre de propriétés
- **CPU** : 10-30% selon la configuration
- **Réseau** : 5-20 MB de données transférées
- **Base de données** : 1-10 MB de données stockées

## 🎯 Prochaines Étapes

### **Après un Test Réussi**

1. **Analyser les données** extraites en base
2. **Valider la qualité** des informations
3. **Comparer avec d'autres sources** si disponible
4. **Optimiser les paramètres** selon les besoins

### **Évolution du Test**

1. **Ajouter d'autres localisations** (Saint-Hyacinthe, Granby)
2. **Étendre les types de propriétés** (condos, maisons)
3. **Améliorer la validation** des données
4. **Ajouter des métriques** de performance

## 📞 Support

### **Ressources Utiles**

- **Logs détaillés** : `logs/chambly_test.log`
- **Configuration** : `config/chambly_test_config.yml`
- **Variables d'environnement** : `.env.chambly_test`
- **Documentation générale** : `docs/README.md`

### **En Cas de Problème**

1. **Vérifier les logs** pour identifier l'erreur
2. **Consulter la documentation** de dépannage
3. **Vérifier la configuration** et l'environnement
4. **Tester avec des paramètres simplifiés**

---

## 🎉 Conclusion

Ce test d'extraction Chambly Plex vous permet de valider le pipeline complet avec des données réelles. Il constitue une excellente base pour comprendre le fonctionnement du système et l'adapter à vos besoins spécifiques.

**🚀 Prêt à extraire des données immobilières réelles de Chambly !**
