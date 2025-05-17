import styled from "styled-components/native";
import { dark } from "../../themes/dark";
import { IAvatarGroupStyle } from "./types";

export const Container = styled.View`
  padding: 16px;
`;

export const Avatar = styled.Image`
  height: 36px;
  width: 36px;
  border-radius: 18px;
`;

export const Line = styled.View`
  flex: 1;
  background-color: ${dark.colors.gray};
  width: 1.5px;
  margin: 16px 0 8px 0;
`;

export const AlignCenter = styled.View`
  align-items: center;
`;

export const Column = styled.View`
  flex: 1;
  margin-right: 16px;
`;

export const AvatarGroupContent = styled.View`
  align-items: center;
  margin-top: 8px;
`;

export const AvatarGroup = styled.Image<IAvatarGroupStyle>`
  height: ${({ h }) => (h ? h : 20)}px;
  width: ${({ w }) => (w ? w : 20)}px;
  top: ${({ top }) => (top ? top : 0)}px;
  border-radius: 10px;
  margin-right: 4px;
`;

export const Row = styled.View`
  flex-direction: row;
  align-items: center;
`;

export const ContainerInteractions = styled.View`
  flex-direction: row;
  align-items: center;
  margin-top: 8px;
`;

export const Username = styled.Text`
  font-family: "Inter_500Medium";
  font-size: 14px;
  color: ${dark.colors.white};
`;

export const Post = styled.Text`
  font-family: "Inter_400Regular";
  font-size: 14px;
  color: ${dark.colors.white};
  margin-top: 8px;
  margin-right: 48px;
`;

export const ContainerPost = styled.TouchableOpacity`
  margin: 0 8px 0 8px;
  width: 100%;
`;

export const ContainerActions = styled.View`
  flex-direction: row;
  margin: 16px 8px 8px 8px;
`;

export const Action = styled.TouchableOpacity`
  margin-right: 16px;
`;

export const Icon = styled.Image.attrs({
  resizeMode: "contain",
})`
  width: 24px;
  height: 24px;
`;

export const Likes = styled.Text`
  font-family: "Inter_400Regular";
  font-size: 14px;
  color: ${dark.colors.gray};
  margin-left: 8px;
`;

export const PostImage = styled.Image.attrs({
  resizeMode: "cover",
})`
  margin-top: 8px;
  border-radius: 8px;
  width: 100%;
  height: 300px;
  margin-right: 32px;
`;

export const Verified = styled.Image`
  width: 16px;
  height: 16px;
`;
