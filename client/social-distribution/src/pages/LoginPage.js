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
    buttonSpace: {
      display: "flex",
      width: "100%",
      
      justifyContent: "center",
      height: "100%"
    },
    container: {      
      justifyContent: 'center',
      height: '100vh',
      backgroundColor: '#f4f4f4',      
    },
    buttonContainer: {
      display: 'flex',
      flexDirection: 'column',
      justifyContent: "center",            
      gap: '20px',        
      height: "100%"
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
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"/>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
      {currentPage === null && (
        <div style={styles.buttonSpace}>

        <div style={styles.buttonContainer}>
          <button  type="button"  class="btn btn-primary"            
            onClick={() => setCurrentPage('login')}
          >
            Login
          </button>
          <button type="button"     class="btn btn-secondary"                      
            onClick={() => setCurrentPage('register')}
          >
            Register
          </button>
          </div>
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