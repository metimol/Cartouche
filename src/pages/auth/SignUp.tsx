import React, { useState } from 'react';
import styled from 'styled-components';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';

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
  margin: 16px 0 24px;
  text-align: center;
`;

const WarningBox = styled.div`
  background-color: rgba(255, 59, 48, 0.1);
  border: 1px solid ${props => props.theme.colors.red};
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 24px;
  width: 100%;
  max-width: 320px;
  text-align: center;
`;

const WarningText = styled.p`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.small};
  margin: 0;
`;

const Form = styled.form`
  width: 100%;
  max-width: 320px;
  display: flex;
  flex-direction: column;
  gap: 24px;
`;

const ButtonsContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 24px;
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

const SignUp: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handleConfirmPasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmPassword(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle sign up logic here
    console.log('Sign up with:', { username, password, confirmPassword });
  };

  const handleBackClick = () => {
    // Navigate back to welcome page
    window.location.href = '/';
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
      
      <Title>Sign Up</Title>
      
      <WarningBox>
        <WarningText>Warning!</WarningText>
        <WarningText>Only first user can create posts</WarningText>
      </WarningBox>
      
      <Form onSubmit={handleSubmit}>
        <Input 
          placeholder="Your username..." 
          value={username}
          onChange={handleUsernameChange}
          fullWidth
          required
        />
        
        <Input 
          placeholder="Your password..." 
          type="password"
          value={password}
          onChange={handlePasswordChange}
          fullWidth
          required
          showPasswordToggle
        />
        
        <Input 
          placeholder="Repeat password..." 
          type="password"
          value={confirmPassword}
          onChange={handleConfirmPasswordChange}
          fullWidth
          required
          showPasswordToggle
        />
        
        <ButtonsContainer>
          <Button primary fullWidth type="submit">
            Sign up
          </Button>
          
          <Button outline fullWidth type="button" onClick={handleBackClick}>
            ← Back
          </Button>
        </ButtonsContainer>
      </Form>
      
      <Footer>2025. All rights reserved</Footer>
      <GitHubIcon viewBox="0 0 24 24">
        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
      </GitHubIcon>
    </PageContainer>
  );
};

export default SignUp;
