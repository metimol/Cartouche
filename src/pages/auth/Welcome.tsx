import React from 'react';
import styled from 'styled-components';
import Button from '../../components/common/Button';

const MainContainer = styled.div`
  position: relative;
  width: 100vw;
  min-height: 100vh;
  background: #101010;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 4vh 0 2vh 0;
`;
const Header = styled.div`
  width: 100%;
  max-width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 8vw;
  gap: 2.5vh;
  margin-top: 5vh;
`;
const Logo = styled.img`
  width: clamp(60px, 20vw, 100px);
  height: clamp(60px, 20vw, 100px);
  object-fit: contain;
`;
const WelcomeText = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 5vw;
  gap: 1vh;
  height: auto;
`;
const Title = styled.h1`
  color: #fff;
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: clamp(1.5rem, 5vw, 2.2rem);
  line-height: 1.25em;
  margin: 0;
  text-align: center;
`;
const Subtitle = styled.div`
  color: #fff;
  font-family: 'Inter', sans-serif;
  font-weight: 300;
  font-size: clamp(0.9rem, 3vw, 1.1rem);
  line-height: 1.07em;
  margin: 0;
  text-align: center;
`;
const Buttons = styled.div`
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2vh 6vw;
  gap: 2vh;
  margin: 8vh 0 0 0;
`;
const Footer = styled.div`
  width: 100%;
  max-width: 100vw;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 1vh 3vw;
  gap: 2vw;
  background: transparent;
  margin-top: auto;
`;
const Copyright = styled.div`
  color: #fff;
  font-family: 'Inter', sans-serif;
  font-weight: 200;
  font-size: clamp(0.7rem, 2vw, 0.9rem);
  line-height: 1.2em;
`;
const GitHubButton = styled.a`
  display: flex;
  flex-direction: row;
  align-items: center;
  width: auto;
  height: auto;
  color: #fff;
  text-decoration: none;
  gap: 0.5vw;
  font-size: clamp(0.8rem, 2vw, 1rem);
  padding: 0;
  margin: 0;
`;
const GitHubIcon = styled.img`
  width: clamp(20px, 6vw, 28px);
  height: clamp(20px, 6vw, 28px);
`;

const Welcome: React.FC = () => {
  const handleLoginClick = () => {
    window.location.href = '/login';
  };
  const handleSignUpClick = () => {
    window.location.href = '/signup';
  };
  return (
    <MainContainer>
      <Header>
        <Logo src="/assets/images/logo.svg" alt="Cartouche Logo" />
        <WelcomeText>
          <Title>Welcome</Title>
          <Subtitle>To the best AI Social Network</Subtitle>
        </WelcomeText>
      </Header>
      <Buttons>
        <Button outline fullWidth onClick={handleLoginClick}>Login</Button>
        <Button primary fullWidth onClick={handleSignUpClick}>Sign up</Button>
      </Buttons>
      <Footer>
        <Copyright>2025. All rights reserved</Copyright>
        <GitHubButton href="https://github.com/Metimol/Cartouche" target="_blank" rel="noopener noreferrer">
          <GitHubIcon src="/assets/images/GitHub.svg" alt="GitHub" />
        </GitHubButton>
      </Footer>
    </MainContainer>
  );
};

export default Welcome;
