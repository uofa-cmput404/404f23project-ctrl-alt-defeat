import React, { useState } from 'react';
import { toast } from 'react-toastify';
import axios from 'axios';
function Profile({ username, authorId, setUsername, onClose }) {
  const [newUsername, setNewUsername] = useState('');
  const [GithubName, setGithubName] = useState('');
  const [newPassword, setNewPassword] = useState('');

  const handleGithubUpdate = async () => {
    axios.post(process.env.REACT_APP_API_HOSTNAME + '/api/authors/github', {
      
        author_id: authorId,
        github: GithubName
      
    },{headers: {'Authorization' : process.env.REACT_APP_AUTHORIZATION}})
        .then((response) => {
      toast.success(response.data);
    })
  }

  const handleUsernameUpdate = async () => {
    if (!newUsername) {
      toast.error('Username cannot be empty');
      return;
    }

    const response = await fetch(process.env.REACT_APP_API_HOSTNAME + '/authors/update_username', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization' : process.env.REACT_APP_AUTHORIZATION
      },
      body: JSON.stringify({ new_username: newUsername, authorId }),
    });

    const data = await response.json();

    if (data.error) {
      toast.error(data.error);
    } else {
      setUsername(newUsername);
      localStorage.setItem('username', newUsername);
      toast.success(data.message);
    }
    setNewUsername('');
  };

  const handlePasswordUpdate = async () => {
    if (!newPassword) {
      toast.error('Password cannot be empty');
      return;
    }

    const response = await fetch(process.env.REACT_APP_API_HOSTNAME + '/authors/update_password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization' : process.env.REACT_APP_AUTHORIZATION
      },
      body: JSON.stringify({ new_password: newPassword, authorId }),
    });

    const data = await response.json();

    if (data.error) {
      toast.error(data.error);
    } else {
      toast.success(data.message);
    }
    setNewPassword('');
  };

  const modalStyles = {
    display: 'block',
    position: 'fixed',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    zIndex: '9999',
    backgroundColor: '#f5f5f5',
    borderRadius: '5px',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    width: '400px',
  };

  const overlayStyles = {
    position: 'fixed',
    top: '0',
    left: '0',
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: '9998',
  };

  return (
    <>
      <div style={overlayStyles}></div>
      <div style={modalStyles}>
        <button className="close-button" onClick={onClose}>
          x
        </button>
        <h2>Edit Profile</h2>
        <p>Current Username: {username}</p>
        <div className="input-container">
          <label>Enter New Username:</label>
          <input
            type="text"
            value={newUsername}
            onChange={(e) => setNewUsername(e.target.value)}
          />
          <button className="save-button" onClick={handleUsernameUpdate}>
            Save Username
          </button>
        </div>
        <div className="input-container">
          <label>Enter New Password:</label>
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <button className="save-button" onClick={handlePasswordUpdate}>
            Save Password
          </button>
        </div>
        <div className="input-container">
          <label>Enter Github Username:</label>
          <input            
            onChange={(e) => setGithubName(e.target.value)}
          />
          <button className="save-button" onClick={handleGithubUpdate}>
            Save Github Name
          </button>
        </div>
      </div>
    </>
  );
}

export default Profile;
