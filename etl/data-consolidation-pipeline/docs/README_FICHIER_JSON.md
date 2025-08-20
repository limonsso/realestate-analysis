# 📁 GUIDE D'UTILISATION - REQUÊTES MONGODB VIA FICHIER JSON

## 🎯 Objectif

Permettre d'utiliser des requêtes MongoDB complexes sans problèmes d'échappement du shell en passant par un fichier JSON.

## 🚀 Utilisation

### 1. Créer un fichier JSON de requête

Créez un fichier JSON avec votre requête MongoDB :

```json
{
  "city": "Trois-Rivières",
  "type": {
    "$regex": "triplex",
    "$options": "i"
  }
}
```

### 2. Lancer le pipeline avec le fichier

```bash
python3 main_ultra_intelligent.py \
  --source mongodb \
  --mongodb-db real_estate_db \
  --mongodb-collection properties \
  --mongodb-query-file query_trois_rivieres.json \
  --limit 100 \
  --output exports/ \
  --formats csv \
  --optimization medium
```

## ✅ Avantages

- **Pas de problèmes d'échappement** du shell bash
- **Requêtes complexes** supportées (regex, opérateurs MongoDB)
- **Lisibilité** : requêtes claires et structurées
- **Réutilisabilité** : même fichier pour plusieurs exécutions
- **Versioning** : peut être commité dans Git

## 🔧 Exemples de requêtes

### Requête simple

```json
{
  "city": "Montréal"
}
```

### Requête avec regex

```json
{
  "type": {
    "$regex": "duplex|triplex",
    "$options": "i"
  }
}
```

### Requête avec conditions multiples

```json
{
  "city": "Trois-Rivières",
  "type": {
    "$regex": "triplex",
    "$options": "i"
  },
  "price": {
    "$gte": 500000,
    "$lte": 1000000
  }
}
```

### Requête avec opérateurs logiques

```json
{
  "$or": [{ "city": "Montréal" }, { "city": "Trois-Rivières" }],
  "type": "triplex"
}
```

## 📋 Priorité des arguments

1. **`--mongodb-query-file`** : Priorité haute (fichier JSON)
2. **`--mongodb-query`** : Priorité basse (argument en ligne de commande)

Si les deux sont fournis, le fichier JSON sera utilisé.

## 🐛 Dépannage

### Fichier introuvable

```
⚠️ Fichier de requête introuvable: query.json
```

- Vérifiez le chemin du fichier
- Vérifiez les permissions

### Erreur de parsing JSON

```
⚠️ Erreur lecture fichier de requête: Expecting property name
```

- Vérifiez la syntaxe JSON
- Utilisez un validateur JSON en ligne

### Requête non appliquée

```
ℹ️ Aucune requête MongoDB spécifiée, extraction de tous les documents
```

- Vérifiez que le fichier JSON est valide
- Vérifiez que l'argument `--mongodb-query-file` est correct

## 🔍 Vérification

Pour vérifier que votre requête est appliquée, regardez les logs :

```
📁 Lecture de la requête depuis le fichier: query.json
✅ Requête MongoDB chargée depuis le fichier: {'city': 'Trois-Rivières', ...}
```

## 📚 Cas d'usage recommandés

- **Requêtes complexes** avec opérateurs MongoDB
- **Requêtes longues** difficiles à taper en ligne de commande
- **Environnements de production** où la robustesse est importante
- **Scripts automatisés** et CI/CD
- **Documentation** des requêtes fréquemment utilisées
