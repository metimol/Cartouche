import React, { useState } from 'react';
import styled from 'styled-components';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';

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
const LoginText = styled.div`
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
const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 500px;
  padding: 0 6vw;
  margin-top: 8vh;
  gap: 0;
`;
const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 2vh;
`;
const StyledInput = styled(Input)`
  width: 100%;
  background: transparent;
  color: #fff;
  font-family: 'Inter', sans-serif;
  font-weight: 200;
  font-size: 14px;
  line-height: 16px;
  border: none;
  border-bottom: 0.5px solid #fff;
  padding: 3px 0;
  margin-bottom: 0;
  &::placeholder {
    color: #fff;
    opacity: 0.7;
    font-weight: 200;
  }
`;
const Buttons = styled.div`
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0;
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

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle login logic here
  };
  const handleBackClick = () => {
    window.location.href = '/';
  };
  return (
    <MainContainer>
      <Header>
        <Logo src="/assets/images/logo.svg" alt="Cartouche Logo" />
        <LoginText>
          <Title>Log In</Title>
          <Subtitle>Enter your credentials to continue</Subtitle>
        </LoginText>
      </Header>
      <Form onSubmit={handleSubmit}>
        <InputGroup>
          <StyledInput 
            placeholder="Your username..." 
            value={username}
            onChange={handleUsernameChange}
            fullWidth
            required
          />
          <StyledInput 
            placeholder="Your password..." 
            type="password"
            value={password}
            onChange={handlePasswordChange}
            fullWidth
            required
            showPasswordToggle
          />
        </InputGroup>
        <Buttons>
          <Button primary fullWidth type="submit">Login</Button>
          <Button outline fullWidth type="button" onClick={handleBackClick}>
            <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '100%' }}>
              <img src="/assets/images/arrow_back.svg" alt="Back" style={{ width: 20, height: 20, marginRight: 8 }} />
              <span style={{ fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: 16, lineHeight: '16px', color: '#FFFFFF' }}>Back</span>
            </span>
          </Button>
        </Buttons>
      </Form>
      <Footer>
        <Copyright>2025. All rights reserved</Copyright>
        <GitHubButton href="https://github.com/Metimol/Cartouche" target="_blank" rel="noopener noreferrer">
          <GitHubIcon src="/assets/images/GitHub.svg" alt="GitHub" />
        </GitHubButton>
      </Footer>
    </MainContainer>
  );
};

export default Login;