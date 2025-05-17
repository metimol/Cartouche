import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "../pages/Home";
import Search from "../pages/Search";
import Profile from "../pages/Profile";
import Activities from "../pages/Activities";
import Detail from "../pages/Detail";
import NewPost from "../pages/NewPost";

const Nav = () => (
  <nav style={{ background: "#181818", padding: 16, marginBottom: 32 }}>
    <Link to="/" style={{ color: "#fff", marginRight: 16 }}>
      Home
    </Link>
    <Link to="/search" style={{ color: "#fff", marginRight: 16 }}>
      Search
    </Link>
    <Link to="/activities" style={{ color: "#fff", marginRight: 16 }}>
      Activities
    </Link>
    <Link to="/profile" style={{ color: "#fff", marginRight: 16 }}>
      Profile
    </Link>
    <Link to="/new" style={{ color: "#fff" }}>
      New Post
    </Link>
  </nav>
);

const App = () => (
  <BrowserRouter>
    <Nav />
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/search" element={<Search />} />
      <Route path="/activities" element={<Activities />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/detail" element={<Detail />} />
      <Route path="/new" element={<NewPost />} />
    </Routes>
  </BrowserRouter>
);

export default App;
