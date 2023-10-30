import React, { useState } from 'react';
import { toast } from 'react-toastify';

function Login(props) {
  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      backgroundColor: '#f2f2f2'
    },
    input: {
      margin: '10px',
      padding: '10px',
      fontSize: '16px', 
      width: '200px'
    },
    button_login: {
      padding: '10px 20px',
      fontSize: '16px',
      cursor: 'pointer',
      backgroundColor: '#808080',
      color: 'white',
      border: 'none',
      borderRadius: '4px'
    },
    button_goback: {
        padding: '10px 20px',
        fontSize: '10px',
        cursor: 'pointer',
        color: '#808080',
        border: 'none',
        borderRadius: '4px'
      }
  };

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    const loginData = {
      username: username.toLowerCase(), 
      password: password.toLowerCase(), 
    };
  
    fetch('http://localhost:5000/authors/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(loginData),
    })
      .then(response => response.json())
      .then(data => {
        if (data.message === 'Login successful') {
          localStorage.setItem('isAuthenticated', 'true');
          const newUsername = username.toLowerCase();
          const newAuthorId = data.author_id;
          localStorage.setItem('username', newUsername);
          localStorage.setItem('authorId', newAuthorId); 
          props.updateAuthStatus(true);
          props.updateUserAndAuthorId(newUsername, newAuthorId);
          props.navigate('/homepage');
        } else if (data.message === 'Wrong Password') {
          toast.error('Wrong Password');
        } else if (data.message === 'User not found') {
          toast.error('User not found');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  return (
    <div style={styles.container}>
      <h2>Login</h2>
      <input
        style={styles.input}
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        style={styles.input}
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button style={styles.button_login} onClick={handleLogin}>
        Login
      </button>
      <button style={styles.button_goback} onClick={() => props.setCurrentPage(null)}>
        Go Back
      </button>
    </div>
  );
}

export default Login;