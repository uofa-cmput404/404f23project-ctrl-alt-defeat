import React, { useState, useEffect } from 'react';

function FollowRequests({ authorId }) {
  const [followRequests, setFollowRequests] = useState([]);

  useEffect(() => {
    // Fetch follow requests for the current user (authorId)
    const fetchFollowRequests = async () => {
      try {
        const response = await fetch(process.env.API_HOSTNAME + `/api/follow/show_requests?authorId=${authorId}`, {
          headers: {
            'Authorization' : 'Basic ' + process.env.USERPASSBASE64
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
    fetch(process.env.API_HOSTNAME + '/api/follow/accept_request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization' : 'Basic ' + process.env.USERPASSBASE64
      },
      body: JSON.stringify({
        author_followee: authorId, // The current user
        author_following: requestId, // The user who sent the request
      }),
    })
      .then((response) => {
        if (response.ok) {
          setFollowRequests((prevRequests) => prevRequests.filter((request) => request.id !== requestId));
        } else {
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
  
    fetch(process.env.API_HOSTNAME + '/api/follow/reject_request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization' : 'Basic ' + process.env.USERPASSBASE64
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
    <div>
      <h1>Follow Requests:</h1>
      <ul>
        {followRequests.map((request) => (
          <li key={request.id}>
            {request.username}
            <button onClick={() => acceptFollowRequest(request.id)}>Accept</button>
            <button onClick={() => rejectFollowRequest(request.id)}>Reject</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FollowRequests;
