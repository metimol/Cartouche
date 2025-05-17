import { TouchableOpacityProps } from "react-native";

export interface IAvatarGroupStyle {
  h?: string;
  w?: string;
  top?: string;
}

export interface IPost {
  id: number;
  name: string;
  username: string;
  avatar_uri: string;
  post: string;
  postImage: string;
  likes: string;
  answers: IAnswer[];
}

export interface IThread extends TouchableOpacityProps {
  post: IPost;
}

export interface IAnswer {
  id: number;
  name: string;
  username: string;
  avatar_uri: string;
  likes: string;
  answers: string;
}
