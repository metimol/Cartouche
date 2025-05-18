import React from 'react';
import styled from 'styled-components';

// Responsive container that adapts to different screen sizes
const ResponsiveContainer = styled.div`
  width: 100%;
  margin: 0 auto;
  
  @media (min-width: 768px) {
    max-width: 720px;
  }
  
  @media (min-width: 992px) {
    max-width: 960px;
  }
  
  @media (min-width: 1200px) {
    max-width: 1140px;
  }
`;

// Flex container with responsive behavior
const FlexContainer = styled.div<{
  direction?: 'row' | 'column';
  justify?: string;
  align?: string;
  wrap?: string;
  gap?: string;
}>`
  display: flex;
  flex-direction: ${props => props.direction || 'row'};
  justify-content: ${props => props.justify || 'flex-start'};
  align-items: ${props => props.align || 'stretch'};
  flex-wrap: ${props => props.wrap || 'nowrap'};
  gap: ${props => props.gap || '0'};
  
  @media (min-width: 768px) {
    flex-direction: ${props => props.direction === 'column' ? 'row' : props.direction};
  }
`;

// Grid container with responsive columns
const GridContainer = styled.div<{
  columns?: number;
  gap?: string;
}>`
  display: grid;
  grid-template-columns: 1fr;
  gap: ${props => props.gap || '16px'};
  
  @media (min-width: 768px) {
    grid-template-columns: repeat(${props => props.columns || 2}, 1fr);
  }
  
  @media (min-width: 992px) {
    grid-template-columns: repeat(${props => props.columns || 3}, 1fr);
  }
`;

// Responsive padding that adjusts based on screen size
const ResponsivePadding = styled.div<{
  p?: string;
  px?: string;
  py?: string;
}>`
  padding: ${props => props.p || '16px'};
  padding-left: ${props => props.px || props.p || '16px'};
  padding-right: ${props => props.px || props.p || '16px'};
  padding-top: ${props => props.py || props.p || '16px'};
  padding-bottom: ${props => props.py || props.p || '16px'};
  
  @media (min-width: 768px) {
    padding: ${props => props.p ? `calc(${props.p} * 1.5)` : '24px'};
    padding-left: ${props => props.px ? `calc(${props.px} * 1.5)` : props.p ? `calc(${props.p} * 1.5)` : '24px'};
    padding-right: ${props => props.px ? `calc(${props.px} * 1.5)` : props.p ? `calc(${props.p} * 1.5)` : '24px'};
    padding-top: ${props => props.py ? `calc(${props.py} * 1.5)` : props.p ? `calc(${props.p} * 1.5)` : '24px'};
    padding-bottom: ${props => props.py ? `calc(${props.py} * 1.5)` : props.p ? `calc(${props.p} * 1.5)` : '24px'};
  }
`;

// Hide element on mobile or desktop
const Responsive = styled.div<{
  hideOnMobile?: boolean;
  hideOnDesktop?: boolean;
}>`
  display: ${props => props.hideOnMobile ? 'none' : 'block'};
  
  @media (min-width: 768px) {
    display: ${props => props.hideOnDesktop ? 'none' : 'block'};
  }
`;

export {
  ResponsiveContainer,
  FlexContainer,
  GridContainer,
  ResponsivePadding,
  Responsive
};
