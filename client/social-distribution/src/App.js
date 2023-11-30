import React, { createContext, useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Stream from './pages/Stream';
import NewPost from './pages/NewPost'
import ManagePosts from './pages/ManagePosts';
import Restrictions from './pages/Restrictions';
import { Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import IndividualPost from './pages/IndividualPost';
import Navbar from './components/Navbar';
import SearchPage from './pages/SearchPage';
import EditProfilePage from './pages/EditProfilePage';

export const UserContext = createContext();

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    localStorage.getItem('isAuthenticated') === 'true'
  );
  const [username, setUsername] = useState(
    localStorage.getItem('username') || ''
  );
  const [authorId, setAuthorId] = useState(
    localStorage.getItem('authorId') || ''
  );

  const updateUserAndAuthorId = (newUsername, newAuthorId) => {
    setUsername(newUsername);
    setAuthorId(newAuthorId);

    localStorage.setItem('username', newUsername);
    localStorage.setItem('authorId', newAuthorId);
  };

  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === 'isAuthenticated') {
        setIsAuthenticated(e.newValue === 'true');
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const updateAuthStatus = (newStatus) => {
    setIsAuthenticated(newStatus);
  };
  
  return (
    <UserContext.Provider value={{ username, authorId, setUsername, setAuthorId, updateAuthStatus, updateUserAndAuthorId }}>
      <BrowserRouter>          
      {isAuthenticated && <Navbar/>}
        <Routes>          
          <Route
            path="/"
            element={
              <LoginPage
                isAuthenticated={isAuthenticated}
                updateAuthStatus={updateAuthStatus}
                updateUserAndAuthorId={updateUserAndAuthorId}
              />
            }
          />
          <Route
            path="/homepage"
            element={isAuthenticated ? <Stream username={username} authorId={authorId} setUsername={setUsername} updateAuthStatus={updateAuthStatus} updateUserAndAuthorId={updateUserAndAuthorId}/> : <Navigate to="/" />}
          />          

          <Route path="/authors/:author_id/posts/:post_id" element={<IndividualPost/>}/>
          <Route path="/manageposts" element={<ManagePosts/>}/>
          <Route path="/manageposts/restrictions" element={<Restrictions/>}/> 
          <Route path="/newpost" element={<NewPost/>}/> 
          <Route path="/search" element={<SearchPage/>}/>
          <Route path="/edit" element={<EditProfilePage/>}/>
          
        </Routes>
        <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
      </BrowserRouter>
    </UserContext.Provider>
  );
}

export default App;