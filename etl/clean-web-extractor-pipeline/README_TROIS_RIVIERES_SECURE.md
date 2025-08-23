# 🏠 Test d'Extraction Sécurisé - Trois-Rivières Plex

## 🔒 **Protection de la Collection `properties_2024`**

Ce test utilise une configuration sécurisée qui **évite complètement** l'utilisation de la collection principale `properties_2024`.

## 📁 **Fichiers de Configuration**

### 1. **Configuration Principale**

- **Fichier** : `config/config.trois_rivieres_test.yml`
- **Objectif** : Configuration spécifique pour Trois-Rivières avec collections temporaires

### 2. **Variables d'Environnement**

- **Fichier** : `env.trois_rivieres_test`
- **Objectif** : Variables d'environnement spécifiques au test

### 3. **Script de Lancement Sécurisé**

- **Fichier** : `run_trois_rivieres_test_safe.py`
- **Objectif** : Lancement sécurisé qui protège `properties_2024`

## 🚀 **Utilisation**

### **Lancement du Test Sécurisé**

```bash
cd etl/clean-web-extractor-pipeline
python3 run_trois_rivieres_test_safe.py
```

### **Lancement du Test Original (Non Sécurisé)**

```bash
cd etl/clean-web-extractor-pipeline
python3 run_trois_rivieres_test.py
```

## 🔍 **Vérification de Sécurité**

### **Script de Vérification**

```bash
cd etl
python3 verify_collections.py
```

Ce script vérifie que :

- ✅ `properties_2024` n'est pas affectée
- ✅ Les tests utilisent des collections temporaires
- ✅ Aucun document de test n'est dans `properties_2024`

## 📊 **Collections Créées**

### **Collections Temporaires (Sécurisées)**

- `trois_rivieres_plex_test_YYYYMMDD_HHMMSS`
- `trois_rivieres_summaries_YYYYMMDD_HHMMSS`
- `trois_rivieres_logs_YYYYMMDD_HHMMSS`

### **Collection Principale (Protégée)**

- `properties_2024` ← **Jamais modifiée par les tests**

## 🛡️ **Mécanismes de Protection**

### 1. **Configuration Dédiée**

- Collections temporaires spécifiées dans `config.trois_rivieres_test.yml`
- Évite l'utilisation de `properties_2024`

### 2. **Forçage des Collections**

- `DatabaseService.set_collection_names()` force l'utilisation des collections temporaires
- Timestamp unique pour éviter les conflits

### 3. **Validation Post-Test**

- Vérification que `properties_2024` n'a pas été modifiée
- Logs détaillés des opérations

## 🔧 **Configuration Technique**

### **Collections MongoDB**

```yaml
database:
  properties_collection: "trois_rivieres_plex_test_temp"
  summaries_collection: "trois_rivieres_summaries_test_temp"
  logs_collection: "trois_rivieres_logs_test_temp"
```

### **Paramètres de Test**

```yaml
test_config:
  max_test_properties: 10
  max_test_pages: 3
  test_timeout: 300
  use_temporary_collections: true
  cleanup_after_test: false
```

## 📋 **Résultats Attendus**

### **Test Réussi**

- ✅ Collections temporaires créées
- ✅ Données extraites et sauvegardées
- ✅ `properties_2024` non affectée
- ✅ Validation des données réussie

### **Test Échoué**

- ❌ Erreur d'extraction ou de sauvegarde
- ✅ `properties_2024` reste intacte
- 🔍 Logs détaillés disponibles

## 🚨 **Dépannage**

### **Problème : Test utilise encore `properties_2024`**

**Solution** : Vérifier que `config.trois_rivieres_test.yml` est bien chargé

### **Problème : Collections temporaires non créées**

**Solution** : Vérifier les permissions MongoDB et la configuration

### **Problème : Validation échoue**

**Solution** : Consulter les logs et vérifier la connectivité Centris

## 📝 **Notes Importantes**

1. **Toujours utiliser** `run_trois_rivieres_test_safe.py` pour les tests
2. **Vérifier** avec `verify_collections.py` après chaque test
3. **Ne jamais** modifier `properties_2024` directement
4. **Conserver** les collections de test pour inspection

## 🔗 **Fichiers Associés**

- `config/config.trois_rivieres_test.yml` - Configuration sécurisée
- `env.trois_rivieres_test` - Variables d'environnement
- `run_trois_rivieres_test_safe.py` - Lanceur sécurisé
- `verify_collections.py` - Vérificateur de sécurité
- `tests/test_trois_rivieres_plex_extraction.py` - Test principal modifié
