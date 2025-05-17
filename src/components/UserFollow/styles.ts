import styled from "styled-components/native";
import { dark } from "../../themes/dark";

export const Container = styled.View`
  flex-direction: row;
  margin: 16px;
  justify-content: space-between;
`;

export const Row = styled.View`
  flex-direction: row;
`;

export const Column = styled.View``;

export const Avatar = styled.Image`
  height: 36px;
  width: 36px;
  border-radius: 18px;
  margin-right: 8px;
`;

export const Username = styled.Text`
  font-family: "Inter_500Medium";
  font-size: 14px;
  color: ${dark.colors.white};
`;

export const Name = styled.Text`
  font-family: "Inter_400Regular";
  font-size: 14px;
  color: ${dark.colors.gray};
  margin-top: 4px;
`;

export const Message = styled.Text`
  font-family: "Inter_400Regular";
  font-size: 14px;
  color: ${dark.colors.gray};
  margin-top: 4px;
`;

export const Followers = styled.Text`
  font-family: "Inter_400Regular";
  font-size: 14px;
  color: ${dark.colors.white};
  margin-top: 8px;
`;

export const ContainerButton = styled.View`
  width: 100px;
  height: 32px;
`;

export const UserContainerIcon = styled.View`
  height: 20px;
  width: 20px;
  border-radius: 10px;
  background-color: ${dark.colors.purple};
  align-items: center;
  justify-content: center;
  position: absolute;
  bottom: 0;
  right: 4px;
  border: 2px ${dark.colors.background};
`;

export const UserIcon = styled.Image`
  height: 8px;
  width: 8px;
`;

export const Verified = styled.Image`
  width: 16px;
  height: 16px;
`;
