import React from 'react';
import styled from 'styled-components';

interface InputProps {
  placeholder?: string;
  type?: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  fullWidth?: boolean;
  name?: string;
  required?: boolean;
  showPasswordToggle?: boolean;
}

const InputContainer = styled.div<{ fullWidth?: boolean }>`
  position: relative;
  width: ${props => props.fullWidth ? '100%' : 'auto'};
`;

const StyledInput = styled.input`
  width: 100%;
  padding: 12px 0;
  background-color: transparent;
  border: none;
  border-bottom: 1px solid ${props => props.theme.colors.gray};
  color: ${props => props.theme.colors.white};
  font-family: ${props => props.theme.fonts.primary};
  font-size: ${props => props.theme.fontSizes.medium};
  outline: none;
  
  &::placeholder {
    color: ${props => props.theme.colors.gray};
  }
  
  &:focus {
    border-bottom: 1px solid ${props => props.theme.colors.white};
  }
`;

const PasswordToggle = styled.span`
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.medium};
  display: flex;
  align-items: center;
`;

const EyeIcon = styled.img`
  width: 24px;
  height: 24px;
`;

const Input: React.FC<InputProps> = ({
  placeholder,
  type = 'text',
  value,
  onChange,
  fullWidth = false,
  name,
  required = false,
  showPasswordToggle = false
}) => {
  const [showPassword, setShowPassword] = React.useState(false);
  const inputType = type === 'password' && showPassword ? 'text' : type;

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <InputContainer fullWidth={fullWidth}>
      <StyledInput
        placeholder={placeholder}
        type={inputType}
        value={value}
        onChange={onChange}
        name={name}
        required={required}
      />
      {type === 'password' && showPasswordToggle && (
        <PasswordToggle onClick={togglePasswordVisibility}>
          <EyeIcon
            src={showPassword ? '/assets/images/eye_open.svg' : '/assets/images/eye_closed.svg'}
            alt={showPassword ? 'Hide password' : 'Show password'}
          />
        </PasswordToggle>
      )}
    </InputContainer>
  );
};

export default Input;
