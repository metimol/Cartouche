import styled from "styled-components/native";
import { dark } from "../../themes/dark";

export const Container = styled.View`
  margin-top: 32px;
  padding: 0 16px;
`;

export const Name = styled.Text`
  font-family: "Inter_700Bold";
  font-size: 20px;
  color: ${dark.colors.white};
`;

export const Username = styled.Text`
  font-family: "Inter_500Medium";
  font-size: 12px;
  color: ${dark.colors.white};
  margin-right: 8px;
`;

export const Bio = styled.Text`
  font-family: "Inter_500Medium";
  font-size: 12px;
  color: ${dark.colors.white};
  margin-top: 16px;
`;

export const Followers = styled.Text`
  font-family: "Inter_500Medium";
  font-size: 12px;
  color: ${dark.colors.gray};
  margin-left: 8px;
`;

export const TagContainer = styled.View`
  background-color: ${dark.colors.gray_dark};
  border-radius: 50px;
  padding: 8px 16px;
`;

export const Tag = styled.Text`
  font-family: "Inter_500Medium";
  font-size: 10px;
  color: ${dark.colors.gray};
`;

export const ContainerUsername = styled.View`
  flex-direction: row;
  align-items: center;
  margin-top: 8px;
`;

export const Row = styled.View`
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
`;

export const Column = styled.View``;

export const Avatar = styled.Image`
  height: 64px;
  width: 64px;
  border-radius: 32px;
`;

export const Verified = styled.Image`
  top: -16px;
`;

export const AvatarGroup = styled.Image<{ ml?: string }>`
  height: 22px;
  width: 22px;
  border-radius: 11px;
  margin-left: ${({ ml }) => (ml ? ml : 0)};
  border: 2px ${dark.colors.background};
`;

export const AvatarGroupContainer = styled.View`
  flex-direction: row;
  align-items: center;
  margin-top: 16px;
`;
