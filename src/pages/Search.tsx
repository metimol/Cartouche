import React from "react";
import styled from "styled-components";
import users from "../assets/json/users.json";

const Container = styled.div`
  min-height: 100vh;
  background: #101010;
  color: #fff;
  padding: 32px 0;
`;
const List = styled.div`
  max-width: 600px;
  margin: 0 auto;
`;
const UserCard = styled.div`
  background: #181818;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
`;
const Avatar = styled.img`
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 16px;
`;
const Username = styled.div`
  font-weight: 600;
  font-size: 1.1rem;
`;
const Name = styled.div`
  color: #616161;
`;

const Search = () => (
  <Container>
    <List>
      {users.map((user) => (
        <UserCard key={user.id}>
          <Avatar src={user.avatar_uri} alt={user.username} />
          <div>
            <Username>@{user.username}</Username>
            <Name>{user.name}</Name>
            <div style={{ color: "#616161", marginTop: 8 }}>{user.followers} followers</div>
          </div>
        </UserCard>
      ))}
    </List>
  </Container>
);

export default Search;
