import React, { useState, createContext, useContext } from 'react';
import LoginPage from './pages/LoginPage';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Stream from './pages/Stream';
import ManagePosts from './pages/ManagePosts';
import Restrictions from './pages/Restrictions';
import { Navigate } from 'react-router-dom';

export const UserContext = createContext();
function App() {

  // Have the username and authorId state here and pass it down to pages and components
  const [username, setUsername] = useState('techgeek5000')
  const [authorId, setAuthorId] = useState('11')
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  return (
    <UserContext.Provider value = {{username, authorId}}>
      <BrowserRouter>
        <Routes>            
            <Route
              path="/"
              element={
                <LoginPage
                  setIsAuthenticated={setIsAuthenticated}
                  isAuthenticated={isAuthenticated}
                />
              }
            />
            <Route
              path="/homepage"
              element={
                isAuthenticated ? <Stream /> : <Navigate to="/" />
              }
            />
            <Route path="/manageposts" element={<ManagePosts/>}/> /* Merge with /posts? */
            <Route path="/manageposts/restrictions" element={<Restrictions/>}/> /* Merge with /posts? */
        </Routes>
      </BrowserRouter>
    </UserContext.Provider>
  );
}

export default App;