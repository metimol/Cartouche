import styled from "styled-components/native";
import { dark } from "../../themes/dark";
import { Platform } from "react-native";

export const Container = styled.View`
  flex: 1;
  background-color: ${dark.colors.background};
`;

export const List = styled.FlatList``;

export const SafeArea = styled.SafeAreaView``;

export const Logo = styled.Image`
  align-self: center;
  margin-top: ${Platform.OS === "android" ? 24 : 0}px;
`;

export const Divider = styled.View`
  width: 100%;
  height: 1px;
  background-color: ${dark.colors.gray_light};
`;
