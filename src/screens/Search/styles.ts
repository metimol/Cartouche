import styled from "styled-components/native";
import { dark } from "../../themes/dark";

export const Container = styled.View`
  flex: 1;
  background-color: ${dark.colors.background};
`;

export const Title = styled.Text`
  font-family: "Inter_700Bold";
  font-size: 32px;
  color: ${dark.colors.white};
  margin: 0 16px;
`;

export const ContainerInput = styled.View`
  background-color: ${dark.colors.gray_dark};
  padding: 8px;
  margin: 8px 16px 0 16px;
  border-radius: 8px;
  flex-direction: row;
`;

export const Input = styled.TextInput.attrs({
  keyboardAppearance: "dark",
})`
  font-family: "Inter_500Medium";
  margin-left: 8px;
  color: ${dark.colors.white};
  flex: 1;
`;

export const SafeArea = styled.SafeAreaView``;

export const List = styled.FlatList``;

export const Divider = styled.View`
  width: 100%;
  height: 1px;
  background-color: ${dark.colors.gray_light};
  margin-left: 60px;
`;

export const Header = styled.View`
  margin-top: ${Platform.OS === "android" ? 24 : 0}px;
`;
