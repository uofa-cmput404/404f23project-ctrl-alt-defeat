import React, { useState } from 'react';
import { toast } from 'react-toastify';

function Register(props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      backgroundColor: '#f2f2f2',
    },
    input: {
      margin: '10px',
      padding: '10px',
      fontSize: '16px',
      width: '200px',
    },
    button_register: {
      padding: '10px 20px',
      fontSize: '16px',
      cursor: 'pointer',
      backgroundColor: '#808080',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
    },
    button_goback: {
      padding: '10px 20px',
      fontSize: '10px',
      cursor: 'pointer',
      color: '#808080',
      border: 'none',
      borderRadius: '4px',
    },
  };

  const handleRegistration = async () => {
    if (!username || !password) {
      toast.error('Empty Fields!', {
        position: 'top-right',
        autoClose: 3000,
      });
      return;
    }

    const registrationData = { username, password };
    try {
      const response = await fetch('http://localhost:5000/requestors/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationData),
      });

      const data = await response.json();

      if (response.ok) {
        if (data.error === 'Username already exists') {
          console.log('Username taken');
          toast.error('Username already exists', {
              position: 'top-right',
              autoClose: 3000,
          });
        } else {
          console.log('Registration Successful');
          toast.success('Awaiting Approval!', {
            position: 'top-right',
            autoClose: 3000,
          });
        }
      } else {
        console.error('Registration failed');
        toast.error('Registration failed', {
          position: 'top-right',
          autoClose: 3000,
        });
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Register</h2>
      <input
        style={styles.input}
        type="text"
        placeholder="Choose a Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        style={styles.input}
        type="password"
        placeholder="Create a Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button style={styles.button_register} onClick={handleRegistration}>
        Register
      </button>
      <button
        style={styles.button_goback}
        onClick={() => props.setCurrentPage(null)}
      >
        Go Back
      </button>
    </div>
  );
}

export default Register;
