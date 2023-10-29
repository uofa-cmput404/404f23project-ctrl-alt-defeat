import React, { createContext, useState, useEffect, useContext } from 'react';
import LoginPage from './pages/LoginPage';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Stream from './pages/Stream';
import ManagePosts from './pages/ManagePosts';
import Restrictions from './pages/Restrictions';
import { Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const UserContext = createContext();

function App() {

  // Have the username and authorId state here and pass it down to pages and components
  // const [username, setUsername] = useState('philiponins')
  // const [authorId, setAuthorId] = useState('1')
  // const [isAuthenticated, setIsAuthenticated] = useState(false);
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
    <UserContext.Provider value={{ username, authorId, setUsername, setAuthorId }}>
      <BrowserRouter>
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
            element={isAuthenticated ? <Stream /> : <Navigate to="/" />}
          />
          <Route path="/manageposts" element={<ManagePosts/>}/> /* Merge with /posts? */
          <Route path="/manageposts/restrictions" element={<Restrictions/>}/> /* Merge with /posts? */
        </Routes>
        <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
      </BrowserRouter>
    </UserContext.Provider>
  );
}

export default App;