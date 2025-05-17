import styled from "styled-components/native";
import { dark } from "../../themes/dark";
import { IBtnStyles } from "./types";

export const Btn = styled.TouchableOpacity<IBtnStyles>`
  background-color: ${({ inverted }) =>
    inverted ? "transparent" : dark.colors.white};
  border: ${({ inverted }) => (inverted ? `1px ${dark.colors.gray}` : null)};
  border-radius: 8px;
  padding-top: 8px;
  padding-bottom: 8px;
  flex: 1;
  align-items: center;
  justify-content: center;
`;

export const BtnText = styled.Text<IBtnStyles>`
  font-family: "Inter_600SemiBold";
  font-size: 12px;
  color: ${({ inverted }) => inverted ? dark.colors.white : dark.colors.gray};
`;
