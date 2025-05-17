import { ImageSourcePropType } from "react-native";

export interface ITabIcon {
  imageName: ImageSourcePropType;
  imageFocusedName: ImageSourcePropType;
  focused: boolean;
}
