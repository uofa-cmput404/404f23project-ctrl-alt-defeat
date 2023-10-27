import React, { useState } from 'react';
import { toast } from 'react-toastify';

function UserSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`http://localhost:5000/follow/usersearch?query=${searchQuery}`);
      if (response.ok) {
        const data = await response.json();
        setSearchResults(data.users);
      } else {
        console.error('Search failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleFollowRequest = async (authorId) => {
    try {
      const response = await fetch('http://localhost:5000/follow/follow_request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          author_send: 2,  // Replace with the ID of the current user
          author_receive: authorId, 
        }),
      });

      const data = await response.json();

      if (response.ok) {
        if (data.message === 'Follow request already sent') {
          toast.error('Follow request already sent');
        } else {
          toast.success('Follow Request Sent');
          console.log('hereee',authorId)
        }
      } else {
        console.error('Follow request failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search users"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>

      {searchResults.length > 0 ? (
        <div>
          <h2>Users Found:</h2>
          <ul>
            {searchResults.map((user) => (
              <li key={user.id}>
                {user.username}
                <button onClick={() => handleFollowRequest(user.id)}>Follow Request</button>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>No users found</p>
      )}
    </div>
  );
}

export default UserSearch;
