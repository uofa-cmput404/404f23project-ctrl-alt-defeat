import React, { useContext, useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import { UserContext } from '../App';
import axios from 'axios';

function EditProfilePage() {
  const [newPassword, setNewPassword] = useState('');
  const [GithubName, setGithubName] = useState('');
  const {username, authorId} = useContext(UserContext);    
  const [newUsername, setNewUsername] = useState(username);
  const githubIdLink = `${process.env.REACT_APP_API_HOSTNAME}/api/authors/github/` + authorId;     

  const fetchGithubUsername = async () => {        
    try {
        // Make the GET request using Axios
            axios.get(githubIdLink)
            .then(response => {
              try {
                if (response.data !== "" && response.data.github !== null) {
                  setGithubName(response.data.github);
                }
              }
              catch (error) {
                console.error('Error', error)
              }}).catch(error => {
                // Handle any errors that occur during the request
                console.error('Error:', error);
                });
          } catch (error) {
            console.error('Error:', error);
          }
    }

    const styles = {
        container: {
            margin: 20
        },

        box: {
            width: "30%"
        }
    }


    const handleGithubUpdate = async () => {
      axios.post(`${process.env.REACT_APP_API_HOSTNAME}/api/authors/github`, {
        
          author_id: authorId,
          github: GithubName
        
      }).then((response) => {
        toast.success(response.data);
      })
    }

      
    const handleUsernameUpdate = async (e) => {
        e.preventDefault();
        if (!newUsername) {
        toast.error('Username cannot be empty');
        return;
      }

      const response = await fetch(`${process.env.REACT_APP_API_HOSTNAME}/api/authors/update_username`, {
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
    
        const response = await fetch(`${process.env.REACT_APP_API_HOSTNAME}/api/authors/update_password`, {
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
        fetchGithubUsername();
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
                <div class="form-group">
                    <label for="exampleInputUsername1">Github</label>
                    <input type="username" class="form-control" id="exampleInputUsername1" aria-describedby="emailHelp" placeholder="Link your github" value={GithubName}
                    onChange={(e) => setGithubName(e.target.value)}/>                    
                </div>
                <button style={{marginTop: 1.25}} type="submit" class="btn btn-primary" onClick={(e) => handleGithubUpdate(e)}>Link Github</button>
            </form>
        <div/>
    </div>
  )
}

export default EditProfilePage