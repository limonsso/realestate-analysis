import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { Toaster } from 'react-hot-toast';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import KPICards from './components/KPICards';
import Filters from './components/Filters';
import Map from './components/Map';
import Charts from './components/Charts';
import PropertyTable from './components/PropertyTable';
import DealHunter from './components/DealHunter';
import TopPerformers from './components/TopPerformers';
import QuickActions from './components/QuickActions';
import { calculateMetrics, calculateOpportunityScore } from './utils/calculations';
import { mockData } from './data/mockData';

const AppContainer = styled(motion.div)`
  min-height: 100vh;
  background: var(--gradient-dark);
  position: relative;
  overflow-x: hidden;
`;

const BackgroundPattern = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 80%, rgba(251, 191, 36, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(16, 185, 129, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(59, 130, 246, 0.05) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
`;

const MainContent = styled.main`
  padding: 0;
  position: relative;
  z-index: 1;
`;

const DashboardGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  margin-top: 2rem;
`;

const MapSection = styled.div`
  grid-column: 1 / -1;
`;

const ChartsSection = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
`;

const TableSection = styled.div`
  grid-column: 1 / -1;
`;

const PremiumFeatures = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
`;

const LoadingContainer = styled(motion.div)`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: var(--gradient-dark);
  color: var(--text-gold);
`;

const LoadingSpinner = styled.div`
  width: 60px;
  height: 60px;
  border: 4px solid var(--bg-secondary);
  border-top: 4px solid var(--gold-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 2rem;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const LoadingText = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  background: var(--gradient-gold);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const LoadingSubtext = styled.p`
  color: var(--text-secondary);
  font-size: 1rem;
  margin-top: 0.5rem;
`;

function App() {
  const [properties, setProperties] = useState([]);
  const [filteredProperties, setFilteredProperties] = useState([]);
  const [filters, setFilters] = useState({
    priceRange: [0, 2000000],
    minYield: 0,
    bedrooms: [],
    bathrooms: [],
    maxAge: 100,
    minSurface: 0,
    cities: [],
    propertyTypes: [],
    minScore: 0,
    maxRisk: 10
  });
  const [loading, setLoading] = useState(true);
  const [userLevel, setUserLevel] = useState('Expert'); // Novice, Expert, Maître, Légende
  const [darkMode, setDarkMode] = useState(true);
  const [selectedProperties, setSelectedProperties] = useState([]);

  useEffect(() => {
    // Simuler le chargement des données
    const loadData = async () => {
      try {
        setLoading(true);
        
        // Simuler un délai de chargement premium
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Traitement des données avec calculs premium
        const processedData = mockData.map(property => {
          const metrics = calculateMetrics(property);
          const opportunityScore = calculateOpportunityScore(property);
          
          // Calculs premium supplémentaires
          const riskScore = calculateRiskScore(property, metrics);
          const potentialValue = calculatePotentialValue(property, metrics);
          const marketTrend = calculateMarketTrend(property);
          
          return {
            ...property,
            ...metrics,
            opportunityScore,
            riskScore,
            potentialValue,
            marketTrend,
            dealType: getDealType(opportunityScore, metrics.netYield, riskScore)
          };
        });
        
        setProperties(processedData);
        setFilteredProperties(processedData);
      } catch (error) {
        console.error('Erreur lors du chargement des données:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  useEffect(() => {
    // Appliquer les filtres premium
    const applyFilters = () => {
      let filtered = properties;

      // Filtres de base
      filtered = filtered.filter(property => 
        property.price >= filters.priceRange[0] && 
        property.price <= filters.priceRange[1]
      );

      if (filters.minYield > 0) {
        filtered = filtered.filter(property => 
          property.netYield >= filters.minYield
        );
      }

      if (filters.minScore > 0) {
        filtered = filtered.filter(property => 
          property.opportunityScore >= filters.minScore
        );
      }

      if (filters.maxRisk < 10) {
        filtered = filtered.filter(property => 
          property.riskScore <= filters.maxRisk
        );
      }

      // Filtres avancés
      if (filters.bedrooms.length > 0) {
        filtered = filtered.filter(property => 
          filters.bedrooms.includes(property.bedrooms)
        );
      }

      if (filters.bathrooms.length > 0) {
        filtered = filtered.filter(property => 
          filters.bathrooms.includes(property.bathrooms)
        );
      }

      if (filters.maxAge < 100) {
        filtered = filtered.filter(property => 
          property.buildingAge <= filters.maxAge
        );
      }

      if (filters.minSurface > 0) {
        filtered = filtered.filter(property => 
          property.surface >= filters.minSurface
        );
      }

      if (filters.cities.length > 0) {
        filtered = filtered.filter(property => 
          filters.cities.includes(property.city)
        );
      }

      if (filters.propertyTypes.length > 0) {
        filtered = filtered.filter(property => 
          filters.propertyTypes.includes(property.type)
        );
      }

      setFilteredProperties(filtered);
    };

    applyFilters();
  }, [properties, filters]);

  const handleFilterChange = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handlePropertySelection = (property) => {
    setSelectedProperties(prev => {
      if (prev.find(p => p.id === property.id)) {
        return prev.filter(p => p.id !== property.id);
      } else {
        return [...prev, property].slice(0, 5); // Max 5 propriétés sélectionnées
      }
    });
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle('dark-mode');
  };

  if (loading) {
    return (
      <LoadingContainer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <LoadingSpinner />
        <LoadingText>Chargement de l'Intelligence Immobilière</LoadingText>
        <LoadingSubtext>Analyse des opportunités en cours...</LoadingSubtext>
      </LoadingContainer>
    );
  }

  return (
    <AppContainer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
      className={darkMode ? 'dark-mode' : ''}
    >
      <BackgroundPattern />
      <Toaster 
        position="top-right"
        toastOptions={{
          style: {
            background: 'var(--bg-secondary)',
            color: 'var(--text-primary)',
            border: '1px solid var(--border-gold)',
          },
        }}
      />
      
      <Header 
        darkMode={darkMode} 
        onToggleDarkMode={toggleDarkMode}
        userLevel={userLevel}
      />
      
      <div className="container">
        <MainContent>
          <HeroSection 
            properties={filteredProperties}
            userLevel={userLevel}
          />
          
          <KPICards properties={filteredProperties} />
          
          <PremiumFeatures>
            <DealHunter 
              properties={filteredProperties}
              onPropertySelect={handlePropertySelection}
            />
            <TopPerformers properties={filteredProperties} />
          </PremiumFeatures>
          
          <Filters 
            filters={filters} 
            onFilterChange={handleFilterChange}
            properties={properties}
          />

          <DashboardGrid>
            <MapSection>
              <Map 
                properties={filteredProperties}
                selectedProperties={selectedProperties}
                onPropertySelect={handlePropertySelection}
              />
            </MapSection>

            <ChartsSection>
              <Charts properties={filteredProperties} />
            </ChartsSection>

            <TableSection>
              <PropertyTable 
                properties={filteredProperties}
                selectedProperties={selectedProperties}
                onPropertySelect={handlePropertySelection}
              />
            </TableSection>
          </DashboardGrid>

          <QuickActions 
            selectedProperties={selectedProperties}
            onClearSelection={() => setSelectedProperties([])}
          />
        </MainContent>
      </div>
    </AppContainer>
  );
}

// Fonctions utilitaires premium
const calculateRiskScore = (property, metrics) => {
  let risk = 0;
  
  // Âge du bâtiment
  if (property.buildingAge > 50) risk += 3;
  else if (property.buildingAge > 30) risk += 2;
  else if (property.buildingAge > 20) risk += 1;
  
  // Ratio prix/évaluation
  if (metrics.priceToAssessmentRatio > 1.3) risk += 2;
  else if (metrics.priceToAssessmentRatio > 1.1) risk += 1;
  
  // Cash-flow négatif
  if (metrics.monthlyCashFlow < 0) risk += 2;
  
  // Rendement faible
  if (metrics.netYield < 4) risk += 1;
  
  return Math.min(risk, 10);
};

const calculatePotentialValue = (property, metrics) => {
  let potential = 0;
  
  // Plus-value potentielle
  if (metrics.priceToAssessmentRatio < 0.9) potential += 3;
  else if (metrics.priceToAssessmentRatio < 1.0) potential += 2;
  
  // Zone en développement
  if (property.city === 'Montréal' || property.city === 'Québec') potential += 1;
  
  // Bâtiment récent
  if (property.buildingAge < 20) potential += 1;
  
  return Math.min(potential, 10);
};

const calculateMarketTrend = (property) => {
  // Simulation de tendance de marché
  const baseTrend = 0.5;
  const cityMultiplier = {
    'Montréal': 1.2,
    'Québec': 1.1,
    'Trois-Rivières': 0.9,
    'Sherbrooke': 0.8
  };
  
  return baseTrend * (cityMultiplier[property.city] || 1.0);
};

const getDealType = (score, yieldValue, risk) => {
  if (score >= 8.5 && yieldValue >= 8 && risk <= 3) return 'DEAL DU SIÈCLE';
  if (score >= 7.5 && yieldValue >= 6 && risk <= 4) return 'OPPORTUNITÉ HOT';
  if (score >= 6.5 && yieldValue >= 5 && risk <= 5) return 'DIAMANT BRUT';
  if (score >= 5.5 && yieldValue >= 4 && risk <= 6) return 'CASH MACHINE';
  if (score >= 4.5) return 'SOLIDE';
  return 'RISQUÉ';
};

export default App;
