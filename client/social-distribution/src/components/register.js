import React from 'react';

function Register(props) {
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
        button_register: {
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
    
      return (
        <div style={styles.container}>
          <h2>Register</h2>
          <input style={styles.input} type="text" placeholder="Enter your Username" />
          <input style={styles.input} type="password" placeholder="Creating Password" />
          <button style={styles.button_register}>Register</button>
          <button style={styles.button_goback} onClick={() => props.setCurrentPage(null)}>Go Back</button>
    
        </div>
      );
}

export default Register;
