import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import styled, { ThemeProvider } from 'styled-components';
import { dark } from "../themes/dark";
import Home from "../pages/Home";
import Activities from "../pages/Activities";
import Profile from "../pages/Profile";
import NewPost from "../pages/NewPost";
import Welcome from "../pages/auth/Welcome";
import Login from "../pages/auth/Login";
import SignUp from "../pages/auth/SignUp";

// Global styles
const GlobalStyle = styled.div`
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }
  
  body {
    background-color: ${props => props.theme.colors.background};
    color: ${props => props.theme.colors.white};
  }
  
  /* Responsive styles */
  @media (min-width: 768px) {
    .auth-container {
      max-width: 480px;
      margin: 0 auto;
      border-radius: 16px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
      overflow: hidden;
    }
    
    .main-container {
      max-width: 768px;
      margin: 0 auto;
      border-radius: 16px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
      overflow: hidden;
    }
  }
  
  @media (min-width: 1200px) {
    .main-container {
      max-width: 1024px;
    }
  }
`;

// Wrapper components for responsive design
const AuthPageWrapper = styled.div`
  @media (min-width: 768px) {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 32px;
  }
`;

const MainPageWrapper = styled.div`
  @media (min-width: 768px) {
    padding: 32px;
  }
`;

// Auth route wrapper
const AuthRoute = ({ children }: { children: React.ReactNode }) => {
  return (
    <AuthPageWrapper>
      <div className="auth-container">
        {children}
      </div>
    </AuthPageWrapper>
  );
};

// Main app route wrapper
const MainRoute = ({ children }: { children: React.ReactNode }) => {
  return (
    <MainPageWrapper>
      <div className="main-container">
        {children}
      </div>
    </MainPageWrapper>
  );
};

const App = () => {
  // Mock authentication state
  const isAuthenticated = false;

  return (
    <ThemeProvider theme={dark}>
      <GlobalStyle />
      <BrowserRouter>
        <Routes>
          {/* Auth Routes */}
          <Route path="/" element={
            isAuthenticated ? 
            <Navigate to="/home" replace /> : 
            <AuthRoute><Welcome /></AuthRoute>
          } />
          <Route path="/login" element={<AuthRoute><Login /></AuthRoute>} />
          <Route path="/signup" element={<AuthRoute><SignUp /></AuthRoute>} />
          
          {/* Main App Routes */}
          <Route path="/home" element={<MainRoute><Home /></MainRoute>} />
          <Route path="/activities" element={<MainRoute><Activities /></MainRoute>} />
          <Route path="/profile" element={<MainRoute><Profile /></MainRoute>} />
          <Route path="/new" element={<MainRoute><NewPost /></MainRoute>} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
};

export default App;
