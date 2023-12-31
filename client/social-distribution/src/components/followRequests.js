import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';

function FollowRequests({ authorId }) {
  const [followRequests, setFollowRequests] = useState([]);

  const styles = {
    container: {
      padding: 20,
      minHeight: 300
    },
    follow: {
      display: "flex",
      alignItems: "center",

    },
    username: {
      width: 100
    },
    box: {
      padding: 10
    }
  }

  useEffect(() => {
    // Fetch follow requests for the current user (authorId)
    const fetchFollowRequests = async () => {
      try {
        const response = await fetch(process.env.REACT_APP_API_HOSTNAME + `/api/follow/show_requests?authorId=${authorId}`, {
          headers: {
            'Authorization' : process.env.REACT_APP_AUTHORIZATION
          }
        });
        if (response.ok) {
          const data = await response.json();
          setFollowRequests(data.followRequests);
        } else {
          console.error('Failed to fetch follow requests');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchFollowRequests();
  }, [authorId]);

  const acceptFollowRequest = (requestId) => {
    fetch(process.env.REACT_APP_API_HOSTNAME + '/api/follow/accept_request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization' : process.env.REACT_APP_AUTHORIZATION
      },
      body: JSON.stringify({
        author_followee: authorId, // The current user
        author_following: requestId, // The user who sent the request
      }),
    })
      .then((response) => {
        if (response.ok) {
          setFollowRequests((prevRequests) => prevRequests.filter((request) => request.id !== requestId));
          toast.success('Accepted follow request!');
        } else {
          toast.error('Accepted follow request!');
          console.error('Failed to accept follow request');
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  const rejectFollowRequest = (requestId) => {
    const data = {
      author_followee: authorId,        
      author_following: requestId,      
    };
  
    fetch(process.env.REACT_APP_API_HOSTNAME + '/api/follow/reject_request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization' : process.env.REACT_APP_AUTHORIZATION
      },
      body: JSON.stringify(data),
    })
      .then(response => {
        if (response.ok) {
          setFollowRequests((prevRequests) => prevRequests.filter((request) => request.id !== requestId));
        } else {
          console.error('Failed to reject follow request');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };
  

  return (
    <div style={styles.box}>
    {followRequests.length > 0 ?
       <ul>
       {followRequests.map((request) => (
         <li key={request.id}>
           <div style={styles.follow}>
            <p style={styles.username}>{request.username}</p>
            <div>
              <button onClick={() => acceptFollowRequest(request.id)} class="btn"><i style={{color: "green"}} class="fa fa-check"></i></button>
              <button onClick={() => rejectFollowRequest(request.id)} class="btn"><i style={{color: "red"}} class="fa fa-close"></i></button>
            </div>
           </div>
         </li>
        ))}
      </ul>
      : <li>Empty! 😅</li>
    }

    </div>
  );
}

export default FollowRequests;
