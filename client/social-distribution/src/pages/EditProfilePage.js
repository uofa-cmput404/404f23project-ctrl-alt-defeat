import React, { useContext, useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import { UserContext } from '../App';

function EditProfilePage() {
    const [newUsername, setNewUsername] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const {username, authorId} = useContext(UserContext);    

    const styles = {
        container: {
            margin: 20
        },

        box: {
            width: "30%"
        }
    }
    
    const handleUsernameUpdate = async (e) => {
        e.preventDefault();
        if (!newUsername) {
          toast.error('Username cannot be empty');
          return;
        }
        console.log(authorId);
        const response = await fetch('http://localhost:5000/authors/update_username', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ new_username: newUsername, authorId }),
        });
    
        const data = await response.json();
    
        if (data.error) {
          toast.error(data.error);
        } else {          
          localStorage.setItem('username', newUsername);
          toast.success(data.message);
        }
        setNewUsername('');
      };
    
      const handlePasswordUpdate = async (e) => {
        e.preventDefault();
        if (!newPassword) {
          toast.error('Password cannot be empty');
          return;
        }
    
        const response = await fetch('http://localhost:5000/authors/update_password', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
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

    useEffect(() => {
        console.log(authorId);
    }, [])
    
  return (
    <div style={styles.container}> 

            <h2>Edit Profile</h2>
            <form style={styles.box}>
                <div class="form-group">
                    <label for="exampleInputUsername1">Username</label>
                    <input type="username" class="form-control" id="exampleInputUsername1" aria-describedby="emailHelp" placeholder="Username" value={newUsername}
                    onChange={(e) => setNewUsername(e.target.value)}/>                    
                </div>
                <button style={{marginTop: 3.5}} type="submit" class="btn btn-primary" onClick={(e) => handleUsernameUpdate(e)}>Update Username</button>
                <div class="form-group">
                    <label for="exampleInputPassword1">Password</label>
                    <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password" value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}/>
                </div>                
                <button style={{marginTop: 1.25}} type="submit" class="btn btn-primary" onClick={(e) => handlePasswordUpdate(e)}>Update password</button>
            </form>
        <div/>
    </div>
  )
}

export default EditProfilePage