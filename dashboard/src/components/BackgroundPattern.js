import React from "react";
import styled from "styled-components";

const PatternContainer = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  overflow: hidden;
`;

const GridPattern = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: linear-gradient(
      rgba(59, 130, 246, 0.03) 1px,
      transparent 1px
    ),
    linear-gradient(90deg, rgba(59, 130, 246, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
`;

const FloatingOrbs = styled.div`
  position: absolute;
  width: 100%;
  height: 100%;
`;

const Orb = styled.div`
  position: absolute;
  border-radius: 50%;
  background: ${(props) => props.gradient};
  opacity: 0.1;
  filter: blur(40px);
  animation: ${(props) => props.animation} ${(props) => props.duration}s
    ease-in-out infinite;
  animation-delay: ${(props) => props.delay}s;
`;

const GradientOrb1 = styled(Orb)`
  width: 300px;
  height: 300px;
  top: 10%;
  left: 5%;
  background: var(--gradient-gold);
  animation: float1 15s ease-in-out infinite;
`;

const GradientOrb2 = styled(Orb)`
  width: 400px;
  height: 400px;
  top: 60%;
  right: 10%;
  background: var(--gradient-emerald);
  animation: float2 20s ease-in-out infinite;
`;

const GradientOrb3 = styled(Orb)`
  width: 250px;
  height: 250px;
  bottom: 20%;
  left: 20%;
  background: var(--gradient-royal);
  animation: float3 18s ease-in-out infinite;
`;

const NoiseOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.015'/%3E%3C/svg%3E");
  opacity: 0.3;
`;

const BackgroundPattern = () => {
  return (
    <PatternContainer>
      <GridPattern />
      <FloatingOrbs>
        <GradientOrb1 />
        <GradientOrb2 />
        <GradientOrb3 />
      </FloatingOrbs>
      <NoiseOverlay />

      <style jsx>{`
        @keyframes gridMove {
          0% {
            transform: translate(0, 0);
          }
          100% {
            transform: translate(50px, 50px);
          }
        }

        @keyframes float1 {
          0%,
          100% {
            transform: translate(0, 0) scale(1);
          }
          33% {
            transform: translate(30px, -30px) scale(1.1);
          }
          66% {
            transform: translate(-20px, 20px) scale(0.9);
          }
        }

        @keyframes float2 {
          0%,
          100% {
            transform: translate(0, 0) scale(1);
          }
          50% {
            transform: translate(-40px, -20px) scale(1.2);
          }
        }

        @keyframes float3 {
          0%,
          100% {
            transform: translate(0, 0) scale(1);
          }
          25% {
            transform: translate(25px, 25px) scale(0.8);
          }
          75% {
            transform: translate(-15px, -15px) scale(1.1);
          }
        }
      `}</style>
    </PatternContainer>
  );
};

export default BackgroundPattern;

