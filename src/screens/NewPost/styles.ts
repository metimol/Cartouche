import styled from "styled-components/native";
import { dark } from "../../themes/dark";
import { BottomSheetModal } from "@gorhom/bottom-sheet";

export const Container = styled.View`
  flex: 1;
  align-items: center;
  top: -2px;
`;

export const BottomModal = styled(BottomSheetModal).attrs({
  handleStyle: {
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  handleIndicatorStyle: { backgroundColor: "transparent" },
  backgroundStyle: { backgroundColor: dark.colors.gray_mid },
})``;

export const CancelButton = styled.TouchableOpacity`
  margin-left: 16px;
`;

export const Cancel = styled.Text`
  font-family: "Inter_500Medium";
  font-size: 12px;
  color: ${dark.colors.white};
`;

export const Heading = styled.Text`
  font-family: "Inter_700Bold";
  font-size: 16px;
  color: ${dark.colors.white};
  position: absolute;
  align-self: center;
  top: -2px;
`;

export const Icon = styled.Image`
  top: 0;
`;

export const Button = styled.TouchableOpacity``;

export const Divider = styled.View`
  width: 100%;
  height: 1px;
  background-color: ${dark.colors.gray_light};
  margin-top: 16px;
`;

export const Avatar = styled.Image`
  width: 36px;
  height: 36px;
  border-radius: 18px;
`;

export const AvatarSmall = styled.Image`
  width: 16px;
  height: 16px;
  border-radius: 8px;
`;

export const Line = styled.View`
  background-color: ${dark.colors.gray};
  width: 1.5px;
  margin: 16px 0;
  height: 80px;
`;

export const Content = styled.View`
  padding: 16px;
  align-items: flex-start;
`;

export const AlignCenter = styled.View`
  align-items: center;
  margin-right: 8px;
`;

export const Row = styled.View`
  flex-direction: row;
`;

export const Column = styled.View`
  flex: 1;
`;

export const Username = styled.Text`
  font-family: "Inter_500Medium";
  font-size: 14px;
  color: ${dark.colors.white};
`;

export const Input = styled.TextInput.attrs({
  keyboardAppearance: "dark",
  autoFocus: true,
})`
  font-family: "Inter_400Regular";
  font-size: 14px;
  color: ${dark.colors.white};
  margin-top: 8px;
  margin-right: 16px;
`;

export const ButtonAttach = styled.TouchableOpacity`
  margin-top: 16px;
`;
