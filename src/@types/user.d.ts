declare interface IUser {
  id: number;
  name: string;
  username: string;
  avatar_uri: string;
  followers: string;
  verified: boolean;
}

declare interface IUserRequest extends IUser {
  message?: string;
}
