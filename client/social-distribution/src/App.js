import React, { useState } from 'react';
import LoginPage from './pages/LoginPage';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Stream from './pages/Stream';
import ManagePosts from './pages/ManagePosts';
import Restrictions from './pages/Restrictions';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage/>}/>
        <Route path="/homepage" element={<Stream/>}/>
        <Route path="/manageposts" element={<ManagePosts/>}/> /* Merge with /posts? */
        <Route path="/manageposts/restrictions" element={<Restrictions/>}/> /* Merge with /posts? */
      </Routes>
    </BrowserRouter>

  );
}


export default App;
