import styled from "styled-components/native";
import { dark } from "../../themes/dark";

export const Container = styled.View`
  flex: 1;
  background-color: ${dark.colors.background};
`;

export const List = styled.ScrollView``;

export const Header = styled.View`
  margin-bottom: 8px;
`;

export const SafeArea = styled.SafeAreaView``;

export const Heading = styled.Text`
  font-family: "Inter_700Bold";
  font-size: 16px;
  color: ${dark.colors.white};
  align-self: center;
`;

export const BackButton = styled.TouchableOpacity`
  margin-left: 16px;
  top: 16px;
`;

export const Back = styled.Text`
  font-family: "Inter_500Medium";
  font-size: 12px;
  color: ${dark.colors.white};
`;
