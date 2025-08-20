# 📋 Exemples de Requêtes MongoDB

Ce répertoire contient des exemples de requêtes MongoDB au format JSON pour le pipeline ultra-intelligent.

## 🎯 Utilisation

### 1. **Requête Trois-Rivières + Triplex**

```bash
python3 main_ultra_intelligent.py \
  --source mongodb \
  --mongodb-db real_estate_db \
  --mongodb-collection properties \
  --mongodb-query-file examples/query_trois_rivieres_triplex.json \
  --limit 100 \
  --output exports/ \
  --formats csv
```

**Fichier** : `query_trois_rivieres_triplex.json`

```json
{
  "city": "Trois-Rivières",
  "type": {
    "$regex": "triplex",
    "$options": "i"
  }
}
```

### 2. **Requête Montréal + Triplex**

```bash
python3 main_ultra_intelligent.py \
  --source mongodb \
  --mongodb-db real_estate_db \
  --mongodb-collection properties \
  --mongodb-query-file examples/query_montreal_triplex.json \
  --limit 100 \
  --output exports/ \
  --formats csv
```

**Fichier** : `query_montreal_triplex.json`

```json
{
  "city": {
    "$regex": "Montréal",
    "$options": "i"
  },
  "type": {
    "$regex": "triplex",
    "$options": "i"
  }
}
```

## 🔧 Créer vos propres requêtes

### **Structure de base**

```json
{
  "field1": "value1",
  "field2": {
    "$regex": "pattern",
    "$options": "i"
  },
  "field3": {
    "$gte": 100000,
    "$lte": 500000
  }
}
```

### **Opérateurs MongoDB supportés**

- **Comparaison** : `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`
- **Logique** : `$and`, `$or`, `$not`, `$nor`
- **Regex** : `$regex`, `$options`
- **Existence** : `$exists`
- **Type** : `$type`

### **Exemples avancés**

#### **Requête avec conditions multiples**

```json
{
  "city": "Trois-Rivières",
  "type": {
    "$regex": "triplex|duplex",
    "$options": "i"
  },
  "price": {
    "$gte": 300000,
    "$lte": 800000
  },
  "surface": {
    "$gte": 1000
  }
}
```

#### **Requête avec opérateurs logiques**

```json
{
  "$or": [{ "city": "Montréal" }, { "city": "Trois-Rivières" }],
  "type": "triplex",
  "price": {
    "$gte": 400000
  }
}
```

#### **Requête avec dates**

```json
{
  "city": "Montréal",
  "type": "triplex",
  "date_created": {
    "$gte": "2024-01-01",
    "$lte": "2024-12-31"
  }
}
```

## 📁 Structure des fichiers

```
examples/
├── README.md                           ← Ce fichier
├── query_trois_rivieres_triplex.json  ← Exemple Trois-Rivières
└── query_montreal_triplex.json        ← Exemple Montréal
```

## ✅ Validation

Pour valider vos fichiers JSON :

1. **Vérifiez la syntaxe** avec un validateur JSON en ligne
2. **Testez la requête** directement dans MongoDB
3. **Utilisez le mode verbose** : `--verbose`
4. **Vérifiez les logs** pour confirmer le parsing

## 🚀 Bonnes pratiques

- **Nommage** : Utilisez des noms descriptifs
- **Versioning** : Commitez vos requêtes dans Git
- **Documentation** : Commentez les requêtes complexes
- **Tests** : Validez avec de petits datasets d'abord
- **Backup** : Gardez des versions de vos requêtes
