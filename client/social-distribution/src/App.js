import React, { useState } from 'react';
import Login from './components/login';
import Register from './components/register';

function App() {
  const [currentPage, setCurrentPage] = useState(null); // null | 'login' | 'register'

  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
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
      
      {currentPage === 'login' && <Login setCurrentPage={setCurrentPage} />}
      {currentPage === 'register' && <Register setCurrentPage={setCurrentPage} />}
    </div>
  );
}


export default App;
