import React, { useContext, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { toast } from 'react-toastify';
import { UserContext } from '../App';

function SearchPage() {
    const location = useLocation();
    const searchResults = location.state;
    const {username, authorId} = useContext(UserContext);    

    const styles = {
        container: {
            margin: 10
        }
    }

    const handleFollowRequest = async (recieveAuthorId) => {
      try {
        const response = await fetch('http://localhost:5000/api/follow/follow_request', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            author_send: authorId,
            author_receive: recieveAuthorId, 
          }),
        });
  
        const data = await response.json();
  
        if (response.ok) {
          if (data.message === 'Already following') {
            toast.error('Already following');
          } else if (data.message === 'Follow request already sent') {
            toast.error('Follow request already sent');
          } else {
            toast.success('Follow Request Sent');
          }
        } else {
          console.error('Follow request failed');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };
  
    const handleUnfollow = async (unfollowUserId) => {
      try {
        const response = await fetch('http://localhost:5000/api/follow/unfollow', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            author_unfollow: unfollowUserId,
            author_unfollower: authorId,
          }),
        });
  
        const data = await response.json();
  
        if (response.ok) {
          toast.success('Unfollowed');
        } else {
          console.error('Unfollow failed');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };
    
  
    return (
    <div style={styles.container}>
        <h1>Users found</h1>
         {searchResults !== null && searchResults.length > 0 ? (
        <div>          
          <ul>
            {searchResults.map((user) => (
              <li key={user.id} style={{display: "flex", alignItems: "center", marginTop: 10}}>
                <div style={{minWidth: 200}}>
                  {user.username}
                </div>
                <button onClick={() => handleFollowRequest(user.id)} type="button" class="btn btn-primary">Follow</button>    
                <div style={{marginRight: 10}}/>
                <button onClick={() => handleUnfollow(user.id)} type="button" class="btn btn-warning">Unfollow</button>                
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>No results found</p>
      )}
    </div>
  )
}

export default SearchPage