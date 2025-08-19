# 🛠️ Scripts Utilitaires

Ce dossier contient les scripts utilitaires pour le projet de nettoyage immobilier.

## 📁 Contenu

- **`validate_specifications.py`** : Validation complète des spécifications du projet
- **`cleanup_structure.py`** : Nettoyage et maintenance de la structure organisée
- **`run_scripts.py`** : Script principal pour exécuter les différents utilitaires
- **`__init__.py`** : Initialisation du package scripts

## 🚀 Utilisation

### 📋 **Script Principal (Recommandé)**
```bash
# Validation des spécifications
python scripts/run_scripts.py validate

# Nettoyage de la structure
python scripts/run_scripts.py cleanup

# Affichage du statut
python scripts/run_scripts.py status
```

### 🔧 **Scripts Individuels**
```bash
# Validation des spécifications
python scripts/validate_specifications.py

# Nettoyage de la structure
python scripts/cleanup_structure.py
```

## 📊 **Scripts Disponibles**

### 🔍 **Validation des Spécifications**
```bash
python scripts/run_scripts.py validate
```
- ✅ Vérifie la structure du projet
- ✅ Valide la stack technologique
- ✅ Contrôle les phases de nettoyage
- ✅ Vérifie les fonctionnalités
- ✅ Valide les livrables

### 🧹 **Nettoyage de la Structure**
```bash
python scripts/run_scripts.py cleanup
```
- 📁 Organise les fichiers dans les bons dossiers
- 🗑️ Nettoie les anciens fichiers (optionnel)
- 📊 Affiche le statut de la structure

### 📊 **Statut de la Structure**
```bash
python scripts/run_scripts.py status
```
- 📁 Affiche l'état des dossiers
- 📄 Compte les fichiers par dossier
- 🕒 Montre les fichiers récents

## 🎯 **Avantages de cette Organisation**

1. **📁 Structure Claire** : Scripts séparés du code principal
2. **🔄 Réutilisabilité** : Scripts modulaires et indépendants
3. **📋 Interface Unifiée** : Un seul point d'entrée pour tous les utilitaires
4. **🧪 Maintenance Facile** : Chaque script a sa responsabilité
5. **📚 Documentation** : Chaque script est documenté

## 🔧 **Personnalisation**

### ⚙️ **Ajouter un Nouveau Script**
1. Créer le fichier dans le dossier `scripts/`
2. L'ajouter dans `__init__.py`
3. L'intégrer dans `run_scripts.py`

### 🎨 **Modifier un Script Existant**
- Chaque script est indépendant
- Modifications sans impact sur les autres
- Tests isolés possibles

---

*Scripts créés le 19 août 2025 - Projet de nettoyage immobilier québécois* 🏠✨
