import React from "react";
import styled from "styled-components";
import posts from "../assets/json/posts.json";

const post = posts[0];

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
`;
const Avatar = styled.img`
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-bottom: 16px;
`;
const Username = styled.div`
  font-weight: 600;
  font-size: 1.1rem;
`;
const Post = styled.div`
  margin: 12px 0;
`;

const Detail = () => (
  <Container>
    <Card>
      <Avatar src={post.avatar_uri} alt={post.username} />
      <Username>@{post.username}</Username>
      <Post>{post.post}</Post>
      {post.postImage && (
        <img
          src={post.postImage}
          alt="post"
          style={{ width: "100%", borderRadius: 8, marginTop: 8 }}
        />
      )}
      <div style={{ color: "#616161", marginTop: 12 }}>
        {post.answers.length} answers - {post.likes} likes
      </div>
    </Card>
  </Container>
);

export default Detail;
