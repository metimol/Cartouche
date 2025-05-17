import React, { useState } from "react";
import styled from "styled-components";

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
`;
const Input = styled.textarea`
  width: 100%;
  min-height: 80px;
  border-radius: 8px;
  border: none;
  padding: 12px;
  font-size: 1rem;
  margin-bottom: 16px;
  resize: vertical;
`;
const Button = styled.button`
  background: #673fe6;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 1rem;
  cursor: pointer;
  align-self: flex-end;
`;

const NewPost = () => {
  const [text, setText] = useState("");
  return (
    <Container>
      <Card>
        <h2>New Post</h2>
        <Input
          placeholder="What's on your mind?"
          value={text}
          onChange={e => setText(e.target.value)}
        />
        <Button disabled={!text.trim()}>Post</Button>
      </Card>
    </Container>
  );
};

export default NewPost;
