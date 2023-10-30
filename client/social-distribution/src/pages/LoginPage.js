import React, { useState } from 'react';
import Login from '../components/login';
import Register from '../components/register';
import { useNavigate, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function LoginPage({ isAuthenticated, updateAuthStatus, updateUserAndAuthorId }) {
  const [currentPage, setCurrentPage] = useState(null); 
  const navigate = useNavigate(); 

  const styles = {
    container: {      
      justifyContent: 'center',
      height: '100vh',
      backgroundColor: '#f4f4f4',
    },
    buttonContainer: {
      display: 'flex',
      flexDirection: 'column',
      gap: '20px',  
    },
    button: {
      padding: '10px 20px',
      fontSize: '18px',
      cursor: 'pointer',
      backgroundColor: '#808080',  // Grey color
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      width: '150px',  // Fixed width for consistency
      textAlign: 'center',
      transition: 'background-color 0.3s',
    },
    buttonHover: {
      backgroundColor: '#666666',  // Slightly darker grey on hover
    }
  };

  if (isAuthenticated) {
    return <Navigate to="/homepage" />;
  }

  return (
    <div style={styles.container}>
      {currentPage === null && (
        <div style={styles.buttonContainer}>
          <button 
            style={styles.button} 
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = styles.buttonHover.backgroundColor}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = styles.button.backgroundColor}
            onClick={() => setCurrentPage('login')}
          >
            Login
          </button>
          <button 
            style={styles.button} 
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = styles.buttonHover.backgroundColor}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = styles.button.backgroundColor}
            onClick={() => setCurrentPage('register')}
          >
            Register
          </button>
        </div>
      )}
      
      {currentPage === 'login' && (
        <Login
          setCurrentPage={setCurrentPage}
          navigate={navigate}
          updateAuthStatus={updateAuthStatus}
          updateUserAndAuthorId={updateUserAndAuthorId}
        />
      )}
      {currentPage === 'register' && <Register setCurrentPage={setCurrentPage} />}

      <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
    </div>
  );
}


export default LoginPage;