import React, { useState } from 'react';
import { toast } from 'react-toastify';

function Profile() {
  const [newUsername, setNewUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');

  const handleUsernameUpdate = async () => {
    if (!newUsername) {
      toast.error('Username cannot be empty');
      return;
    }

    const response = await fetch('http://localhost:5000/authors/update_username', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ new_username: newUsername }),
    });

    const data = await response.json();

    if (data.error) {
      toast.error(data.error);
    } else {
      toast.success(data.message);
    }
    setNewUsername('');
  };

  const handlePasswordUpdate = async () => {
    if (!newPassword) {
      toast.error('Password cannot be empty');
      return;
    }

    const response = await fetch('http://localhost:5000/authors/update_password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ new_password: newPassword }),
    });

    const data = await response.json();

    if (data.error) {
      toast.error(data.error);
    } else {
      toast.success(data.message);
    }
    setNewPassword('');
  };


  const styles = `
    .profile-container {
      max-width: 400px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f5f5f5;
      border: 1px solid #ccc;
      border-radius: 5px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    h2 {
      font-size: 24px;
      margin-bottom: 20px;
      color: #333;
    }

    .input-container {
      margin-bottom: 20px;
    }

    label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
      color: #333;
    }

    input[type="text"],
    input[type="password"] {
      width: 100%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
      font-size: 16px;
    }

    button.save-button {
      display: block;
      width: 100%;
      padding: 10px;
      background-color: #007bff;
      color: #fff;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    button.save-button:hover {
      background-color: #0056b3;
    }
  `;

  return (
    <div className="profile-container" style={{ display: 'block' }}>
      <h2>Edit Profile</h2>
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
      <style>{styles}</style>
    </div>
  );
}

export default Profile;
