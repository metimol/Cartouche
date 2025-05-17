export interface ICardUser {
  name: string;
  username: string;
  bio: string;
  followers: string;
  avatar_uri: string;
}

export interface IUser {
  user?: ICardUser;
}
