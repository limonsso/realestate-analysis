import React from "react";
import styled, { keyframes } from "styled-components";
import { motion } from "framer-motion";
import {
  TrendingUp,
  Target,
  DollarSign,
  BarChart3,
  Zap,
  Star,
} from "lucide-react";

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const pulse = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
`;

const shimmer = keyframes`
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
`;

const LoadingContainer = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    var(--bg-primary) 0%,
    var(--bg-secondary) 100%
  );
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  overflow: hidden;
`;

const LoadingContent = styled.div`
  text-align: center;
  position: relative;
  z-index: 2;
`;

const LogoContainer = styled.div`
  position: relative;
  margin-bottom: 2rem;
`;

const LogoIcon = styled(motion.div)`
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: var(--gradient-gold);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  position: relative;
  box-shadow: var(--shadow-gold);

  &::before {
    content: "";
    position: absolute;
    top: -4px;
    left: -4px;
    right: -4px;
    bottom: -4px;
    border-radius: 50%;
    background: var(--gradient-gold);
    opacity: 0.3;
    animation: ${pulse} 2s ease-in-out infinite;
  }
`;

const LogoText = styled(motion.h1)`
  font-size: 2.5rem;
  font-weight: 800;
  background: var(--gradient-gold);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 1rem 0;
  text-align: center;
`;

const LoadingSpinner = styled.div`
  width: 80px;
  height: 80px;
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--gold-primary);
  border-radius: 50%;
  animation: ${spin} 1s linear infinite;
  margin: 2rem auto;
  position: relative;

  &::after {
    content: "";
    position: absolute;
    top: -8px;
    left: -8px;
    right: -8px;
    bottom: -8px;
    border: 2px solid transparent;
    border-top: 2px solid var(--emerald-primary);
    border-radius: 50%;
    animation: ${spin} 1.5s linear infinite reverse;
  }
`;

const LoadingText = styled(motion.p)`
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin: 1rem 0;
  font-weight: 500;
`;

const LoadingSubtext = styled(motion.p)`
  font-size: 1rem;
  color: var(--text-muted);
  margin: 0.5rem 0;
  opacity: 0.8;
`;

const ProgressBar = styled.div`
  width: 300px;
  height: 6px;
  background: var(--bg-tertiary);
  border-radius: 3px;
  margin: 2rem auto;
  overflow: hidden;
  position: relative;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background: var(--gradient-gold);
    animation: ${shimmer} 2s ease-in-out infinite;
  }
`;

const FeatureIcons = styled.div`
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
  opacity: 0.6;
`;

const FeatureIcon = styled(motion.div)`
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  border: 2px solid var(--border-color);
`;

const BackgroundElements = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
`;

const FloatingElement = styled(motion.div)`
  position: absolute;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: var(--gradient-emerald);
  opacity: 0.1;
  filter: blur(60px);
`;

const LoadingContainer = ({ isLoading, progress = 0 }) => {
  const [loadingText, setLoadingText] = React.useState("Initialisation...");
  const [loadingSubtext, setLoadingSubtext] = React.useState(
    "Préparation de votre tableau de bord premium"
  );

  React.useEffect(() => {
    if (!isLoading) return;

    const texts = [
      "Initialisation...",
      "Chargement des données...",
      "Analyse des opportunités...",
      "Calcul des métriques...",
      "Préparation des visualisations...",
      "Finalisation...",
    ];

    const subtexts = [
      "Préparation de votre tableau de bord premium",
      "Connexion à la base de données",
      "Application de l'algorithme GOLDMINE",
      "Génération des rapports personnalisés",
      "Optimisation des performances",
      "Prêt à analyser vos investissements",
    ];

    let currentIndex = 0;
    const interval = setInterval(() => {
      if (currentIndex < texts.length) {
        setLoadingText(texts[currentIndex]);
        setLoadingSubtext(subtexts[currentIndex]);
        currentIndex++;
      }
    }, 800);

    return () => clearInterval(interval);
  }, [isLoading]);

  if (!isLoading) return null;

  return (
    <LoadingContainer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      <BackgroundElements>
        <FloatingElement
          style={{ top: "20%", left: "10%" }}
          animate={{
            y: [0, -20, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <FloatingElement
          style={{ top: "60%", right: "15%" }}
          animate={{
            y: [0, 20, 0],
            scale: [1, 0.9, 1],
          }}
          transition={{
            duration: 5,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1,
          }}
        />
        <FloatingElement
          style={{ bottom: "30%", left: "20%" }}
          animate={{
            x: [0, 15, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 6,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 2,
          }}
        />
      </BackgroundElements>

      <LoadingContent>
        <LogoContainer>
          <LogoIcon
            animate={{
              rotate: [0, 360],
              scale: [1, 1.1, 1],
            }}
            transition={{
              rotate: { duration: 3, repeat: Infinity, ease: "linear" },
              scale: { duration: 2, repeat: Infinity, ease: "easeInOut" },
            }}
          >
            <TrendingUp size={48} color="white" />
          </LogoIcon>
        </LogoContainer>

        <LogoText
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.8 }}
        >
          REAL ESTATE INTELLIGENCE
        </LogoText>

        <LoadingText
          key={loadingText}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {loadingText}
        </LoadingText>

        <LoadingSubtext
          key={loadingSubtext}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          {loadingSubtext}
        </LoadingSubtext>

        <ProgressBar />

        <FeatureIcons>
          <FeatureIcon
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
          >
            <Target size={24} />
          </FeatureIcon>
          <FeatureIcon
            animate={{ rotate: [0, -360] }}
            transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
          >
            <DollarSign size={24} />
          </FeatureIcon>
          <FeatureIcon
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 12, repeat: Infinity, ease: "linear" }}
          >
            <BarChart3 size={24} />
          </FeatureIcon>
          <FeatureIcon
            animate={{ rotate: [0, -360] }}
            transition={{ duration: 9, repeat: Infinity, ease: "linear" }}
          >
            <Zap size={24} />
          </FeatureIcon>
          <FeatureIcon
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 11, repeat: Infinity, ease: "linear" }}
          >
            <Star size={24} />
          </FeatureIcon>
        </FeatureIcons>
      </LoadingContent>
    </LoadingContainer>
  );
};

export default LoadingContainer;

