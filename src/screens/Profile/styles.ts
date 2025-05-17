import styled from "styled-components/native";
import { dark } from "../../themes/dark";
import { MaterialTabBar } from "react-native-collapsible-tab-view";

export const Container = styled.View`
  flex: 1;
  background-color: ${dark.colors.background};
`;

export const Header = styled.View`
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
`;

export const Icon = styled.Image``;

export const ButtonIcon = styled.TouchableOpacity<{ mr?: string }>`
  margin-right: ${({ mr }) => (mr ? mr : 0)}px;
`;

export const SafeArea = styled.SafeAreaView``;

export const List = styled.ScrollView``;

export const ContainerButtons = styled.View`
  flex-direction: row;
  padding: 0 16px;
  margin: 16px 0 16px 0;
`;

export const Spacing = styled.View`
  width: 8px;
`;

export const TabLabel = styled.Text`
  font-family: "Inter_600SemiBold";
  font-size: 12px;
  color: ${dark.colors.white};
`;

export const CustomTabBar = styled(MaterialTabBar).attrs({
  indicatorStyle: {
    backgroundColor: dark.colors.white,
  },
})``;

export const Divider = styled.View`
  width: 100%;
  height: 1px;
  background-color: ${dark.colors.gray_light};
`;
