/**
 * Calcule toutes les métriques financières pour une propriété
 * @param {Object} property - Objet propriété avec les données de base
 * @returns {Object} - Objet contenant toutes les métriques calculées
 */
export const calculateMetrics = (property) => {
  const {
    price = 0,
    annualRevenue = 0,
    municipalTaxes = 0,
    schoolTaxes = 0,
    depenses = 0,
    surface = 0,
    constructionYear = 0,
    priceAssessment = 0,
  } = property;

  // Calculs de base
  const totalExpenses = municipalTaxes + schoolTaxes + depenses;
  const annualExpenses = totalExpenses * 12; // Convertir en annuel si mensuel

  // Rendements
  const grossYield = annualRevenue > 0 ? (annualRevenue / price) * 100 : 0;
  const netYield =
    annualRevenue > 0 ? ((annualRevenue - annualExpenses) / price) * 100 : 0;

  // Ratios
  const priceToAssessmentRatio =
    priceAssessment > 0 ? price / priceAssessment : 0;
  const pricePerSqft = surface > 0 ? price / surface : 0;
  const revenuePerSqft = surface > 0 ? annualRevenue / surface : 0;

  // Âge du bâtiment
  const buildingAge = constructionYear > 0 ? 2025 - constructionYear : 0;

  // Charges totales
  const totalCharges = totalExpenses;

  // Cash-flow
  const monthlyCashFlow =
    annualRevenue > 0 ? (annualRevenue - annualExpenses) / 12 : 0;
  const annualCashFlow = annualRevenue > 0 ? annualRevenue - annualExpenses : 0;

  return {
    grossYield: Number(grossYield.toFixed(2)),
    netYield: Number(netYield.toFixed(2)),
    priceToAssessmentRatio: Number(priceToAssessmentRatio.toFixed(2)),
    pricePerSqft: Number(pricePerSqft.toFixed(0)),
    revenuePerSqft: Number(revenuePerSqft.toFixed(0)),
    buildingAge: Number(buildingAge),
    totalCharges: Number(totalCharges),
    monthlyCashFlow: Number(monthlyCashFlow.toFixed(0)),
    annualCashFlow: Number(annualCashFlow.toFixed(0)),
    annualRevenue: Number(annualRevenue),
    annualExpenses: Number(annualExpenses),
  };
};

/**
 * Calcule le score d'opportunité basé sur une formule pondérée
 * @param {Object} property - Objet propriété avec les métriques calculées
 * @returns {number} - Score entre 0 et 10
 */
export const calculateOpportunityScore = (property) => {
  const {
    netYield = 0,
    priceToAssessmentRatio = 0,
    buildingAge = 0,
    monthlyCashFlow = 0,
    price = 0,
  } = property;

  // Normaliser les valeurs entre 0 et 1
  const normalizeYield = Math.min(netYield / 10, 1); // 10% = 1.0
  const normalizeRatio = Math.min(priceToAssessmentRatio / 1.2, 1); // 1.2 = 1.0
  const normalizeAge = Math.max(0, 1 - buildingAge / 100); // 0 ans = 1.0, 100+ ans = 0.0
  const normalizeCashFlow = Math.min(Math.max(monthlyCashFlow / 2000, 0), 1); // $2000 = 1.0

  // Pondérations selon les spécifications
  const weights = {
    netYield: 0.4, // 40%
    priceToAssessment: 0.3, // 30%
    buildingAge: 0.2, // 20%
    cashFlow: 0.1, // 10%
  };

  // Calcul du score pondéré
  const score =
    (normalizeYield * weights.netYield +
      normalizeRatio * weights.priceToAssessment +
      normalizeAge * weights.buildingAge +
      normalizeCashFlow * weights.cashFlow) *
    10; // Convertir en échelle 0-10

  return Number(score.toFixed(1));
};

/**
 * Calcule les statistiques agrégées pour un ensemble de propriétés
 * @param {Array} properties - Tableau de propriétés
 * @returns {Object} - Statistiques agrégées
 */
export const calculateAggregateStats = (properties) => {
  if (!properties || properties.length === 0) {
    return {
      totalProperties: 0,
      avgPrice: 0,
      avgYield: 0,
      avgCashFlow: 0,
      totalRevenue: 0,
      priceRanges: {},
      yieldDistribution: {},
      cityDistribution: {},
      typeDistribution: {},
    };
  }

  const stats = {
    totalProperties: properties.length,
    avgPrice: 0,
    avgYield: 0,
    avgCashFlow: 0,
    totalRevenue: 0,
    priceRanges: {},
    yieldDistribution: {},
    cityDistribution: {},
    typeDistribution: {},
  };

  // Calculs de base
  const totalPrice = properties.reduce((sum, p) => sum + (p.price || 0), 0);
  const totalYield = properties.reduce((sum, p) => sum + (p.netYield || 0), 0);
  const totalCashFlow = properties.reduce(
    (sum, p) => sum + (p.monthlyCashFlow || 0),
    0
  );
  const totalRev = properties.reduce(
    (sum, p) => sum + (p.annualRevenue || 0),
    0
  );

  stats.avgPrice = totalPrice / properties.length;
  stats.avgYield = totalYield / properties.length;
  stats.avgCashFlow = totalCashFlow / properties.length;
  stats.totalRevenue = totalRev;

  // Distribution des prix
  properties.forEach((p) => {
    if (p.price) {
      const range = Math.floor(p.price / 100000) * 100000;
      const key = `$${range.toLocaleString()}-${(
        range + 100000
      ).toLocaleString()}`;
      stats.priceRanges[key] = (stats.priceRanges[key] || 0) + 1;
    }
  });

  // Distribution des rendements
  properties.forEach((p) => {
    if (p.netYield) {
      const range = Math.floor(p.netYield / 2) * 2;
      const key = `${range}-${range + 2}%`;
      stats.yieldDistribution[key] = (stats.yieldDistribution[key] || 0) + 1;
    }
  });

  // Distribution par ville
  properties.forEach((p) => {
    if (p.city) {
      stats.cityDistribution[p.city] =
        (stats.cityDistribution[p.city] || 0) + 1;
    }
  });

  // Distribution par type
  properties.forEach((p) => {
    if (p.type) {
      stats.typeDistribution[p.type] =
        (stats.typeDistribution[p.type] || 0) + 1;
    }
  });

  return stats;
};

/**
 * Filtre les propriétés selon des critères spécifiques
 * @param {Array} properties - Tableau de propriétés
 * @param {Object} filters - Critères de filtrage
 * @returns {Array} - Propriétés filtrées
 */
export const filterProperties = (properties, filters) => {
  if (!properties || !filters) return properties;

  return properties.filter((property) => {
    // Filtre par plage de prix
    if (filters.priceRange && filters.priceRange.length === 2) {
      const [min, max] = filters.priceRange;
      if (property.price < min || property.price > max) return false;
    }

    // Filtre par rendement minimum
    if (filters.minYield && property.netYield < filters.minYield) {
      return false;
    }

    // Filtre par nombre de chambres
    if (filters.bedrooms && filters.bedrooms.length > 0) {
      if (!filters.bedrooms.includes(property.bedrooms)) return false;
    }

    // Filtre par nombre de salles de bain
    if (filters.bathrooms && filters.bathrooms.length > 0) {
      if (!filters.bathrooms.includes(property.bathrooms)) return false;
    }

    // Filtre par âge maximum
    if (filters.maxAge && property.buildingAge > filters.maxAge) {
      return false;
    }

    // Filtre par surface minimale
    if (filters.minSurface && property.surface < filters.minSurface) {
      return false;
    }

    // Filtre par villes
    if (filters.cities && filters.cities.length > 0) {
      if (!filters.cities.includes(property.city)) return false;
    }

    // Filtre par types de propriété
    if (filters.propertyTypes && filters.propertyTypes.length > 0) {
      if (!filters.propertyTypes.includes(property.type)) return false;
    }

    return true;
  });
};

/**
 * Trie les propriétés selon différents critères
 * @param {Array} properties - Tableau de propriétés
 * @param {string} sortBy - Critère de tri
 * @param {string} sortOrder - Ordre de tri (asc/desc)
 * @returns {Array} - Propriétés triées
 */
export const sortProperties = (
  properties,
  sortBy = "opportunityScore",
  sortOrder = "desc"
) => {
  if (!properties) return [];

  const sorted = [...properties].sort((a, b) => {
    let aValue = a[sortBy] || 0;
    let bValue = b[sortBy] || 0;

    // Gérer les chaînes de caractères
    if (typeof aValue === "string") {
      aValue = aValue.toLowerCase();
      bValue = bValue.toLowerCase();
    }

    if (sortOrder === "asc") {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });

  return sorted;
};
