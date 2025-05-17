import React from "react";
import styled from "styled-components";
import users from "../assets/json/users.json";

const user = users[0];

const Container = styled.div`
  min-height: 100vh;
  background: #101010;
  color: #fff;
  padding: 32px 0;
`;
const Card = styled.div`
  max-width: 600px;
  margin: 0 auto;
  background: #181818;
  border-radius: 12px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;
const Avatar = styled.img`
  width: 96px;
  height: 96px;
  border-radius: 50%;
  margin-bottom: 16px;
`;
const Username = styled.div`
  font-weight: 600;
  font-size: 1.3rem;
`;
const Name = styled.div`
  color: #616161;
  margin-bottom: 8px;
`;
const Followers = styled.div`
  color: #616161;
  margin-top: 8px;
`;

const Profile = () => (
  <Container>
    <Card>
      <Avatar src={user.avatar_uri} alt={user.username} />
      <Username>@{user.username}</Username>
      <Name>{user.name}</Name>
      <Followers>{user.followers} followers</Followers>
    </Card>
  </Container>
);

export default Profile;
