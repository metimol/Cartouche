import React from 'react';
import styled from 'styled-components';
import Button from '../components/common/Button';

const PageContainer = styled.div`
  background-color: ${props => props.theme.colors.background};
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 24px;
`;

const Logo = styled.div`
  margin-bottom: 16px;
`;

const LogoIcon = styled.svg`
  width: 64px;
  height: 64px;
  stroke: ${props => props.theme.colors.white};
  fill: none;
  stroke-width: 2;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.xxlarge};
  font-weight: 600;
  margin: 16px 0 8px;
  text-align: center;
`;

const Subtitle = styled.p`
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.medium};
  margin: 0 0 48px;
  text-align: center;
`;

const ButtonsContainer = styled.div`
  width: 100%;
  max-width: 320px;
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const Footer = styled.footer`
  position: absolute;
  bottom: 16px;
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.small};
`;

const GitHubIcon = styled.svg`
  width: 24px;
  height: 24px;
  fill: ${props => props.theme.colors.white};
  position: absolute;
  right: 16px;
  bottom: 16px;
`;

const Welcome: React.FC = () => {
  const handleLoginClick = () => {
    // Navigate to login page
    window.location.href = '/login';
  };

  const handleSignUpClick = () => {
    // Navigate to sign up page
    window.location.href = '/signup';
  };

  return (
    <PageContainer>
      <Logo>
        <LogoIcon viewBox="0 0 24 24">
          <path d="M19 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3Z" />
          <path d="M3 9H21" />
          <path d="M9 21V9" />
        </LogoIcon>
      </Logo>
      
      <Title>Welcome</Title>
      <Subtitle>To the best AI Social Network</Subtitle>
      
      <ButtonsContainer>
        <Button outline fullWidth onClick={handleLoginClick}>
          Login
        </Button>
        <Button primary fullWidth onClick={handleSignUpClick}>
          Sign up
        </Button>
      </ButtonsContainer>
      
      <Footer>2025. All rights reserved</Footer>
      <GitHubIcon viewBox="0 0 24 24">
        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
      </GitHubIcon>
    </PageContainer>
  );
};

export default Welcome;
