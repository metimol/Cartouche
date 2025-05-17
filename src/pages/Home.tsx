import React from "react";
import styled from "styled-components";
import posts from "../assets/json/posts.json";

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
const Divider = styled.div`
  width: 100%;
  height: 1px;
  background: #323232;
  margin: 24px 0;
`;
const ThreadCard = styled.div`
  background: #181818;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
`;
const Username = styled.div`
  font-weight: 600;
  font-size: 1.1rem;
`;
const Post = styled.div`
  margin: 12px 0;
`;
const Avatar = styled.img`
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 16px;
`;
const Row = styled.div`
  display: flex;
  align-items: center;
`;

const Home = () => (
  <Container>
    <List>
      {posts.map((item, idx) => (
        <React.Fragment key={item.id}>
          <ThreadCard>
            <Row>
              <Avatar src={item.avatar_uri} alt={item.username} />
              <Username>@{item.username}</Username>
            </Row>
            <Post>{item.post}</Post>
            {item.postImage && (
              <img
                src={item.postImage}
                alt="post"
                style={{ width: "100%", borderRadius: 8, marginTop: 8 }}
              />
            )}
            <div style={{ color: "#616161", marginTop: 12 }}>
              {item.answers.length} answers - {item.likes} likes
            </div>
          </ThreadCard>
          {idx < posts.length - 1 && <Divider />}
        </React.Fragment>
      ))}
    </List>
  </Container>
);

export default Home;
