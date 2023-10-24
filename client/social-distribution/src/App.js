import React, { useState } from 'react';
import LoginPage from './pages/LoginPage';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Stream from './pages/Stream';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage/>}/>
        <Route path="/homepage" element={<Stream/>}/>
      </Routes>
    </BrowserRouter>

  );
}


export default App;