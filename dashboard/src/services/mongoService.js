/**
 * Service pour l'intégration avec MongoDB
 * Utilise les fonctions de votre projet principal lib/db.py
 */

import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:3001/api";

class MongoService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Récupère toutes les propriétés depuis MongoDB
   * @param {Object} filters - Filtres optionnels
   * @returns {Promise<Array>} - Tableau des propriétés
   */
  async getAllProperties(filters = {}) {
    try {
      const response = await axios.get(`${this.baseURL}/properties`, {
        params: filters,
      });
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la récupération des propriétés:", error);
      throw error;
    }
  }

  /**
   * Récupère un échantillon de propriétés
   * @param {number} limit - Nombre maximum de propriétés
   * @param {Object} filters - Filtres optionnels
   * @returns {Promise<Array>} - Tableau des propriétés
   */
  async getSampleProperties(limit = 1000, filters = {}) {
    try {
      const response = await axios.get(`${this.baseURL}/properties/sample`, {
        params: { limit, ...filters },
      });
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la récupération de l'échantillon:", error);
      throw error;
    }
  }

  /**
   * Récupère les propriétés par ville
   * @param {string} city - Nom de la ville
   * @returns {Promise<Array>} - Tableau des propriétés
   */
  async getPropertiesByCity(city) {
    try {
      const response = await axios.get(
        `${this.baseURL}/properties/city/${encodeURIComponent(city)}`
      );
      return response.data;
    } catch (error) {
      console.error(
        `Erreur lors de la récupération des propriétés de ${city}:`,
        error
      );
      throw error;
    }
  }

  /**
   * Récupère les propriétés par type
   * @param {string} type - Type de propriété
   * @returns {Promise<Array>} - Tableau des propriétés
   */
  async getPropertiesByType(type) {
    try {
      const response = await axios.get(
        `${this.baseURL}/properties/type/${encodeURIComponent(type)}`
      );
      return response.data;
    } catch (error) {
      console.error(
        `Erreur lors de la récupération des propriétés de type ${type}:`,
        error
      );
      throw error;
      throw error;
    }
  }

  /**
   * Recherche de propriétés avec critères multiples
   * @param {Object} searchCriteria - Critères de recherche
   * @returns {Promise<Array>} - Tableau des propriétés
   */
  async searchProperties(searchCriteria) {
    try {
      const response = await axios.post(
        `${this.baseURL}/properties/search`,
        searchCriteria
      );
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la recherche:", error);
      throw error;
    }
  }

  /**
   * Récupère les statistiques agrégées
   * @returns {Promise<Object>} - Statistiques des propriétés
   */
  async getAggregateStats() {
    try {
      const response = await axios.get(`${this.baseURL}/properties/stats`);
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la récupération des statistiques:", error);
      throw error;
    }
  }

  /**
   * Récupère les propriétés dans une zone géographique
   * @param {Object} bounds - Limites géographiques {north, south, east, west}
   * @returns {Promise<Array>} - Tableau des propriétés
   */
  async getPropertiesInBounds(bounds) {
    try {
      const response = await axios.get(`${this.baseURL}/properties/bounds`, {
        params: bounds,
      });
      return response.data;
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des propriétés dans la zone:",
        error
      );
      throw error;
    }
  }

  /**
   * Récupère les propriétés avec un rendement minimum
   * @param {number} minYield - Rendement minimum en pourcentage
   * @returns {Promise<Array>} - Tableau des propriétés
   */
  async getPropertiesByMinYield(minYield) {
    try {
      const response = await axios.get(`${this.baseURL}/properties/yield`, {
        params: { min: minYield },
      });
      return response.data;
    } catch (error) {
      console.error(
        `Erreur lors de la récupération des propriétés avec rendement >= ${minYield}%:`,
        error
      );
      throw error;
    }
  }

  /**
   * Récupère les propriétés dans une plage de prix
   * @param {number} minPrice - Prix minimum
   * @param {number} maxPrice - Prix maximum
   * @returns {Promise<Array>} - Tableau des propriétés
   */
  async getPropertiesByPriceRange(minPrice, maxPrice) {
    try {
      const response = await axios.get(
        `${this.baseURL}/properties/price-range`,
        {
          params: { min: minPrice, max: maxPrice },
        }
      );
      return response.data;
    } catch (error) {
      console.error(
        `Erreur lors de la récupération des propriétés entre $${minPrice} et $${maxPrice}:`,
        error
      );
      throw error;
    }
  }

  /**
   * Récupère les meilleures opportunités (score élevé)
   * @param {number} limit - Nombre maximum de propriétés
   * @returns {Promise<Array>} - Tableau des propriétés
   */
  async getTopOpportunities(limit = 10) {
    try {
      const response = await axios.get(
        `${this.baseURL}/properties/top-opportunities`,
        {
          params: { limit },
        }
      );
      return response.data;
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des meilleures opportunités:",
        error
      );
      throw error;
    }
  }

  /**
   * Teste la connexion à l'API
   * @returns {Promise<boolean>} - True si la connexion réussit
   */
  async testConnection() {
    try {
      const response = await axios.get(`${this.baseURL}/health`);
      return response.status === 200;
    } catch (error) {
      console.error("Erreur de connexion à l'API:", error);
      return false;
    }
  }
}

// Instance singleton
const mongoService = new MongoService();

export default mongoService;

/**
 * Hook personnalisé pour utiliser le service MongoDB
 * Utilisez ce hook dans vos composants React
 */
export const useMongoService = () => {
  return mongoService;
};

/**
 * Fonction utilitaire pour convertir les données MongoDB en format compatible
 * @param {Object} mongoData - Données brutes de MongoDB
 * @returns {Object} - Données formatées pour le tableau de bord
 */
export const formatMongoData = (mongoData) => {
  if (!mongoData) return null;

  // Si c'est un tableau, formater chaque élément
  if (Array.isArray(mongoData)) {
    return mongoData.map(formatMongoData);
  }

  // Si c'est un objet unique, le formater
  return {
    id: mongoData._id || mongoData.id,
    address: mongoData.address || mongoData.adresse || "N/A",
    city: mongoData.city || mongoData.ville || "N/A",
    type: mongoData.type || mongoData.type_propriete || "N/A",
    price: mongoData.price || mongoData.prix || 0,
    annualRevenue:
      mongoData.annualRevenue ||
      mongoData.revenu_annuel ||
      mongoData.revenue ||
      0,
    municipalTaxes:
      mongoData.municipalTaxes || mongoData.taxes_municipales || 0,
    schoolTaxes: mongoData.schoolTaxes || mongoData.taxes_scolaires || 0,
    depenses: mongoData.depenses || mongoData.expenses || 0,
    surface: mongoData.surface || mongoData.superficie || 0,
    constructionYear:
      mongoData.constructionYear || mongoData.annee_construction || 0,
    priceAssessment: mongoData.priceAssessment || mongoData.evaluation || 0,
    bedrooms: mongoData.bedrooms || mongoData.chambres || 0,
    bathrooms: mongoData.bathrooms || mongoData.salles_bain || 0,
    latitude: mongoData.latitude || mongoData.lat || 0,
    longitude: mongoData.longitude || mongoData.lng || 0,
  };
};
