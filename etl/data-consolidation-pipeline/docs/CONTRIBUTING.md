# 🤝 GUIDE DE CONTRIBUTION - Pipeline ETL Modulaire

## 🎯 Vue d'ensemble

Ce guide explique comment contribuer au pipeline ETL modulaire de consolidation de données immobilières.

## 🚀 Démarrage Rapide

### **1. Fork et Clone**

```bash
# Fork le projet sur GitHub
# Puis clonez votre fork
git clone https://github.com/votre-username/realestate-analysis.git
cd realestate-analysis/etl/data-consolidation-pipeline
```

### **2. Installation de l'environnement**

```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# ou
venv\Scripts\activate     # Sur Windows

# Installer les dépendances
pip install -r requirements.txt

# Installation des dépendances de développement
pip install pytest pytest-cov black flake8 mypy
```

### **3. Vérification de l'installation**

```bash
# Tests de base
python3 tests/test_mongodb_connection.py
python3 tests/test_complete_pipeline.py

# Test du pipeline complet
python3 main_modular_pipeline.py --source test --output exports/test
```

## 🏗️ Architecture du Projet

### **Structure des Composants**

```
core/
├── pipeline_manager.py      ← Orchestrateur principal
├── data_processor.py        ← Traitement des données
├── export_manager.py        ← Gestion des exports
├── report_generator.py      ← Génération des rapports
├── config_manager.py        ← Gestion de la configuration
└── components/              ← Composants spécialisés
    ├── data_extractor.py    ← Extraction des données
    ├── data_consolidator.py ← Consolidation intelligente
    ├── data_cleaner.py      ← Nettoyage des données
    ├── data_enricher.py     ← Enrichissement des données
    └── data_validator.py    ← Validation des données
```

### **Ajout d'un Nouveau Composant**

1. **Créer le composant** dans `core/components/`
2. **Implémenter l'interface** standard
3. **Ajouter les tests** dans `tests/`
4. **Mettre à jour** `core/__init__.py`
5. **Documenter** le composant

## 📝 Standards de Code

### **Style Python (PEP 8)**

```bash
# Vérification automatique
black --check .
flake8 .
mypy core/
```

### **Formatage Automatique**

```bash
# Formater le code
black .

# Organiser les imports
isort .
```

### **Annotations de Types**

```python
from typing import Dict, List, Optional, Union
import pandas as pd

def process_data(
    df: pd.DataFrame,
    config: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Union[pd.DataFrame, str]]:
    """Traite les données selon la configuration.

    Args:
        df: DataFrame à traiter
        config: Configuration du traitement
        options: Options optionnelles

    Returns:
        Dictionnaire contenant le DataFrame traité et le statut
    """
    pass
```

### **Docstrings**

```python
def consolidate_columns(df: pd.DataFrame, rules: List[Dict]) -> pd.DataFrame:
    """Consolide les colonnes selon les règles définies.

    Cette fonction applique une stratégie de consolidation intelligente
    pour fusionner les colonnes similaires en une seule colonne.

    Args:
        df: DataFrame contenant les données à consolider
        rules: Liste des règles de consolidation

    Returns:
        DataFrame avec les colonnes consolidées

    Raises:
        ValueError: Si les règles sont invalides
        KeyError: Si une colonne source n'existe pas

    Example:
        >>> rules = [{'source': ['price', 'prix'], 'target': 'price_final'}]
        >>> df_consolidated = consolidate_columns(df, rules)
    """
    pass
```

## 🧪 Tests

### **Structure des Tests**

```
tests/
├── test_mongodb_connection.py    ← Tests de connexion
├── test_complete_pipeline.py     ← Tests end-to-end
├── test_consolidation_strategy.py ← Tests de consolidation
├── test_custom_config_integration.py ← Tests d'intégration
├── test_new_features.py          ← Tests des nouvelles fonctionnalités
├── test_pipeline_complet.py      ← Tests du pipeline complet
└── test_pipeline_simplifie.py    ← Tests du pipeline simplifié
```

### **Exécution des Tests**

```bash
# Tous les tests
python -m pytest tests/

# Test spécifique
python -m pytest tests/test_mongodb_connection.py

# Avec couverture
python -m pytest --cov=core tests/

# Tests avec verbosité
python -m pytest -v tests/

# Tests en parallèle
python -m pytest -n auto tests/
```

### **Écriture de Tests**

```python
import pytest
import pandas as pd
from core.data_processor import DataProcessor

class TestDataProcessor:
    """Tests pour la classe DataProcessor."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.processor = DataProcessor()
        self.sample_df = pd.DataFrame({
            'price': [100000, 200000, 300000],
            'prix': [100000, 200000, 300000]
        })

    def test_consolidate_columns(self):
        """Test de consolidation des colonnes."""
        result = self.processor.consolidate_columns(self.sample_df)
        assert 'price_final' in result.columns
        assert 'price' not in result.columns
        assert 'prix' not in result.columns

    def test_consolidate_columns_empty_df(self):
        """Test avec DataFrame vide."""
        empty_df = pd.DataFrame()
        result = self.processor.consolidate_columns(empty_df)
        assert result.empty

    @pytest.mark.parametrize("invalid_rules", [
        None,
        [],
        [{"invalid": "rule"}]
    ])
    def test_consolidate_columns_invalid_rules(self, invalid_rules):
        """Test avec règles invalides."""
        with pytest.raises(ValueError):
            self.processor.consolidate_columns(self.sample_df, invalid_rules)
```

## 🔄 Workflow Git

### **Branches**

```bash
# Branche principale
main                    ← Code stable et testé

# Branches de développement
develop                ← Intégration des features
feature/nouveau-composant    ← Nouvelle fonctionnalité
bugfix/correction-bug        ← Correction de bug
hotfix/urgence-production    ← Correction urgente
```

### **Processus de Contribution**

#### **1. Créer une branche**

```bash
# Mettre à jour la branche principale
git checkout main
git pull origin main

# Créer une nouvelle branche
git checkout -b feature/nouveau-composant
```

#### **2. Développer et tester**

```bash
# Faire les modifications
# Ajouter les tests
# Vérifier le style de code

# Tests locaux
python -m pytest tests/
black --check .
flake8 .
```

#### **3. Commiter les changements**

```bash
# Ajouter les fichiers
git add .

# Commiter avec un message conventionnel
git commit -m "feat: ajouter nouveau composant de validation

- Implémentation de DataValidator
- Tests complets avec couverture 95%
- Documentation mise à jour
- Respect des standards PEP 8"
```

#### **4. Pousser et créer une Pull Request**

```bash
# Pousser la branche
git push origin feature/nouveau-composant

# Créer une Pull Request sur GitHub
# Titre : "feat: ajouter nouveau composant de validation"
# Description : Détail des changements et tests
```

### **Conventions de Commits**

Suivre [Conventional Commits](https://www.conventionalcommits.org/) :

```bash
# Types de commits
feat: nouvelle fonctionnalité
fix: correction de bug
docs: documentation
style: formatage du code
refactor: refactoring
test: ajout/modification de tests
chore: tâches de maintenance

# Exemples
feat: ajouter support export Parquet
fix: corriger gestion des erreurs MongoDB
docs: mettre à jour README avec exemples
style: formater code avec Black
refactor: simplifier PipelineManager
test: ajouter tests pour DataValidator
chore: mettre à jour requirements.txt
```

## 📚 Documentation

### **Mise à Jour de la Documentation**

1. **README.md** : Vue d'ensemble et exemples
2. **docs/INDEX.md** : Index de la documentation
3. **docs/ARCHITECTURE.md** : Architecture technique
4. **docs/STRUCTURE.md** : Structure du projet
5. **docs/CONFIGURATION.md** : Guide de configuration
6. **docs/USAGE_GUIDE.md** : Guide d'utilisation
7. **CHANGELOG.md** : Historique des versions

### **Standards de Documentation**

- **Clarté** : Explications simples et directes
- **Exemples** : Code fonctionnel et cas d'usage
- **Cohérence** : Style uniforme dans tous les documents
- **Mise à jour** : Documentation synchronisée avec le code

## 🚨 Gestion des Erreurs

### **Reporting de Bugs**

1. **Vérifier** que le bug n'est pas déjà reporté
2. **Créer une issue** avec :
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu vs observé
   - Version du code et environnement
   - Logs d'erreur complets

### **Demande de Fonctionnalité**

1. **Décrire** la fonctionnalité souhaitée
2. **Expliquer** le cas d'usage
3. **Proposer** une approche technique
4. **Discuter** avec l'équipe

## 🔧 Outils de Développement

### **IDE Recommandés**

- **VS Code** : Extensions Python, Git, Markdown
- **PyCharm** : IDE Python complet
- **Vim/Emacs** : Éditeurs avancés

### **Extensions Utiles**

```json
{
  "python.pythonPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true
}
```

### **Configuration Pre-commit**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
```

## 📊 Métriques de Qualité

### **Objectifs**

- **Couverture de tests** : ≥ 90%
- **Complexité cyclomatique** : ≤ 10
- **Maintenabilité** : A (CodeClimate)
- **Duplication** : ≤ 3%

### **Outils de Qualité**

```bash
# Couverture
pytest --cov=core --cov-report=html

# Complexité
radon cc core/ -a

# Maintenabilité
radon mi core/

# Duplication
radon raw core/
```

## 🎯 Checklist de Contribution

### **Avant de Soumettre**

- [ ] Code respecte PEP 8
- [ ] Tests passent (≥ 90% couverture)
- [ ] Documentation mise à jour
- [ ] Changelog mis à jour
- [ ] Commit message conventionnel
- [ ] Pull Request descriptive

### **Après Révision**

- [ ] Commentaires adressés
- [ ] Tests supplémentaires si nécessaire
- [ ] Documentation finale
- [ ] Merge dans develop/main

## 📞 Support et Contact

- **Issues** : [GitHub Issues](https://github.com/username/realestate-analysis/issues)
- **Discussions** : [GitHub Discussions](https://github.com/username/realestate-analysis/discussions)
- **Documentation** : Voir docs/INDEX.md
- **Wiki** : Documentation collaborative

---

## 🚀 Prochaines Étapes

1. **Forker le projet**
2. **Créer une branche** pour votre contribution
3. **Développer et tester** localement
4. **Soumettre une Pull Request**
5. **Collaborer** avec l'équipe

---

**🤝 Merci de contribuer au Pipeline ETL Modulaire !**

_Dernière mise à jour : Août 2025_
