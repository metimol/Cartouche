import React from 'react';
import styled from 'styled-components';
import Button from '../../components/common/Button';

// Status Bar (макет)
const StatusBar = styled.div`
  width: 100%;
  height: 44px;
  background: #101010;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 27px;
  box-sizing: border-box;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 2;
  filter: blur(0.5px);
`;
const StatusBarLeft = styled.div`
  color: #fff;
  font-family: 'SF Pro Text', 'Inter', sans-serif;
  font-weight: 600;
  font-size: 17px;
  letter-spacing: -0.024em;
`;
const StatusBarRight = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
`;
const StatusBarIcon = styled.img`
  height: 16px;
  margin-left: 4px;
`;

const MainContainer = styled.div`
  width: 390px;
  min-height: 844px;
  background: #101010;
  border-radius: 32px;
  margin: 48px auto;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const Header = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 44px 0 0 0;
`;
const Logo = styled.img`
  width: 64px;
  height: 64px;
`;
const WelcomeText = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
`;
const Title = styled.h1`
  color: #fff;
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 32px;
  line-height: 1.25em;
  margin: 0;
`;
const Subtitle = styled.div`
  color: #fff;
  font-family: 'Inter', sans-serif;
  font-weight: 300;
  font-size: 15px;
  line-height: 1.07em;
  margin: 0;
`;
const Buttons = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 15px 30px;
  margin-top: 40px;
`;
const Footer = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: absolute;
  bottom: 0;
  left: 0;
  padding: 5px 10px;
  background: transparent;
`;
const Copyright = styled.div`
  color: #fff;
  font-family: 'Inter', sans-serif;
  font-weight: 200;
  font-size: 13px;
`;
const GitHubButton = styled.a`
  display: flex;
  align-items: center;
  color: #fff;
  text-decoration: none;
  gap: 6px;
  font-size: 15px;
`;
const GitHubIcon = styled.img`
  width: 24px;
  height: 24px;
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
      <StatusBar>
        <StatusBarLeft>9:41</StatusBarLeft>
        <StatusBarRight>
          <StatusBarIcon src="/src/assets/images/status/wifi.svg" alt="wifi" />
          <StatusBarIcon src="/src/assets/images/status/signal.svg" alt="signal" />
          <StatusBarIcon src="/src/assets/images/status/battery.svg" alt="battery" />
        </StatusBarRight>
      </StatusBar>
      <Header>
        <Logo src="/src/images/main_page.png" alt="Cartouche Logo" />
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
          <GitHubIcon src="/src/assets/images/github.svg" alt="GitHub" />
        </GitHubButton>
      </Footer>
    </MainContainer>
  );
};

export default Welcome;
