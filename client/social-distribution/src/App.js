import React, { createContext, useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Stream from './pages/Stream';
import { Navigate } from 'react-router-dom';
import Profile from './pages/Profile';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const UserContext = createContext();

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem('isAuthenticated') === 'true');
  const [username, setUsername] = useState(localStorage.getItem('username') || '');
  const [authorId, setAuthorId] = useState(localStorage.getItem('author_id') || '');

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
    <UserContext.Provider value={{ username, authorId, setUsername, setAuthorId}}>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              <LoginPage
                isAuthenticated={isAuthenticated}
                updateAuthStatus={updateAuthStatus}
              />
            }
          />
          <Route
            path="/homepage"
            element={isAuthenticated ? <Stream/> : <Navigate to="/" />}
          />
          <Route
            path="/profile"
            element={isAuthenticated ? <Profile /> : <Navigate to="/" />}
          />
        </Routes>
        <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
      </BrowserRouter>
    </UserContext.Provider>
  );
}

export default App;