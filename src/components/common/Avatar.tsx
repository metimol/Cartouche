import React from 'react';
import styled from 'styled-components';

interface AvatarProps {
  src: string;
  size?: 'small' | 'medium' | 'large';
  verified?: boolean;
}

const AvatarContainer = styled.div<{ size: string }>`
  position: relative;
  width: ${props => {
    switch (props.size) {
      case 'small': return '32px';
      case 'large': return '80px';
      default: return '48px';
    }
  }};
  height: ${props => {
    switch (props.size) {
      case 'small': return '32px';
      case 'large': return '80px';
      default: return '48px';
    }
  }};
  border-radius: 50%;
  overflow: hidden;
`;

const AvatarImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: cover;
`;

const VerifiedBadge = styled.img<{ size: string }>`
  position: absolute;
  bottom: 0;
  right: 0;
  width: ${props => props.size === 'small' ? '12px' : props.size === 'large' ? '24px' : '16px'};
  height: ${props => props.size === 'small' ? '12px' : props.size === 'large' ? '24px' : '16px'};
`;

const Avatar: React.FC<AvatarProps> = ({
  src,
  size = 'medium',
  verified = false
}) => {
  return (
    <AvatarContainer size={size}>
      <AvatarImage src={src} alt="User avatar" />
      {verified && (
        <VerifiedBadge 
          src="/src/assets/images/verified.png" 
          alt="Verified" 
          size={size}
        />
      )}
    </AvatarContainer>
  );
};

export default Avatar;
