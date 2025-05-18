import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import styled, { ThemeProvider, createGlobalStyle } from 'styled-components';
import { dark } from "../themes/dark";
import Home from "../pages/Home";
import Activities from "../pages/Activities";
import Profile from "../pages/Profile";
import NewPost from "../pages/NewPost";
import Welcome from "../pages/auth/Welcome";
import Login from "../pages/auth/Login";
import SignUp from "../pages/auth/SignUp";

// Global styles
const GlobalStyle = createGlobalStyle`
  html, body {
    margin: 0;
    padding: 0;
    width: 100vw;
    min-height: 100vh;
    background: ${({ theme }) => theme.colors.background};
    color: ${({ theme }) => theme.colors.white};
    box-sizing: border-box;
    overflow-x: hidden;
  }
  *, *::before, *::after {
    box-sizing: inherit;
  }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }
`;

// Wrapper components for responsive design
const AuthPageWrapper = styled.div`
  @media (min-width: 768px) {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 0;
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