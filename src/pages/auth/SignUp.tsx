import React, { useState } from 'react';
import styled from 'styled-components';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';

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
const SignUpText = styled.div`
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
const WarningBox = styled.div`
  background-color: rgba(255, 59, 48, 0.1);
  border: 1px solid #FF3B30;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 24px;
  width: 100%;
  max-width: 320px;
  text-align: center;
`;
const WarningText = styled.p`
  color: #fff;
  font-size: 13px;
  margin: 0;
`;
const Form = styled.form`
  width: 100%;
  max-width: 320px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-top: 40px;
  padding: 0 30px;
`;
const Buttons = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 24px;
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

const SignUp: React.FC = () => {
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [confirmPassword, setConfirmPassword] = React.useState('');

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
  };
  const handleBackClick = () => {
    window.location.href = '/';
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
        <Logo src="/src/images/registration_page.png" alt="Cartouche Logo" />
        <SignUpText>
          <Title>Sign Up</Title>
          <Subtitle>Create your account to get started</Subtitle>
        </SignUpText>
      </Header>
      <Form onSubmit={handleSubmit}>
        <WarningBox>
          <WarningText>Warning! Only first user can create posts</WarningText>
        </WarningBox>
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
        <Buttons>
          <Button primary fullWidth type="submit">Sign up</Button>
          <Button outline fullWidth type="button" onClick={handleBackClick}>← Back</Button>
        </Buttons>
      </Form>
      <Footer>
        <Copyright>2025. All rights reserved</Copyright>
        <GitHubButton href="https://github.com/Metimol/Cartouche" target="_blank" rel="noopener noreferrer">
          <GitHubIcon src="/src/assets/images/github.svg" alt="GitHub" />
        </GitHubButton>
      </Footer>
    </MainContainer>
  );
};

export default SignUp;
