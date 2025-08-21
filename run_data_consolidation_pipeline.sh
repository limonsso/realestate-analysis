#!/bin/bash

# 🚀 PIPELINE DE CONSOLIDATION DES DONNÉES IMMOBILIÈRES
# ======================================================
# Script bash pour exécuter le pipeline modulaire

# Configuration
PROJECT_ROOT="/Users/zecklimonsso/GitHub/realestate-analysis"
VENV_PATH="$PROJECT_ROOT/.venv"
PIPELINE_SCRIPT="$PROJECT_ROOT/etl/data-consolidation-pipeline/main_modular_pipeline.py"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérification de l'environnement
check_environment() {
    print_status "Vérification de l'environnement..."
    
    if [ ! -d "$PROJECT_ROOT" ]; then
        print_error "Répertoire projet non trouvé: $PROJECT_ROOT"
        exit 1
    fi
    
    if [ ! -d "$VENV_PATH" ]; then
        print_error "Environnement virtuel non trouvé: $VENV_PATH"
        exit 1
    fi
    
    if [ ! -f "$PIPELINE_SCRIPT" ]; then
        print_error "Script pipeline non trouvé: $PIPELINE_SCRIPT"
        exit 1
    fi
    
    print_success "Environnement vérifié"
}

# Exécution du pipeline
run_pipeline() {
    print_status "🚀 Démarrage du pipeline de consolidation..."
    print_status "📊 Source: MongoDB (real_estate_db.properties)"
    print_status "🎯 Requête: Trois-Rivières Plex"
    print_status "📁 Sortie: etl/data-consolidation-pipeline/exports/trois_rivieres_plex"
    
    cd "$PROJECT_ROOT"
    
    # Exécution avec l'environnement virtuel
    "$VENV_PATH/bin/python" "$PIPELINE_SCRIPT" \
        --source mongodb \
        --mongodb-db real_estate_db \
        --mongodb-collection properties \
        --mongodb-query-file etl/data-consolidation-pipeline/examples/query_trois_rivieres_plex.json \
        --limit 1 \
        --output etl/data-consolidation-pipeline/exports/trois_rivieres_plex \
        --formats csv \
        --optimization medium
    
    # Vérification du code de sortie
    if [ $? -eq 0 ]; then
        print_success "Pipeline exécuté avec succès !"
        print_status "📁 Fichiers générés dans: etl/data-consolidation-pipeline/exports/trois_rivieres_plex"
    else
        print_error "Erreur lors de l'exécution du pipeline"
        exit 1
    fi
}

# Fonction d'aide
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Afficher cette aide"
    echo "  -v, --verbose  Mode verbeux"
    echo "  -c, --check    Vérifier l'environnement uniquement"
    echo ""
    echo "Exemples:"
    echo "  $0                    # Exécuter le pipeline"
    echo "  $0 --check           # Vérifier l'environnement"
    echo "  $0 --help            # Afficher l'aide"
}

# Parsing des arguments
VERBOSE=false
CHECK_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--check)
            CHECK_ONLY=true
            shift
            ;;
        *)
            print_error "Option inconnue: $1"
            show_help
            exit 1
            ;;
    esac
done

# Mode verbeux
if [ "$VERBOSE" = true ]; then
    set -x
fi

# Vérification de l'environnement
check_environment

# Si seulement vérification demandée
if [ "$CHECK_ONLY" = true ]; then
    print_success "Vérification terminée - environnement prêt"
    exit 0
fi

# Exécution du pipeline
run_pipeline

print_success "🎉 Script terminé avec succès !"
