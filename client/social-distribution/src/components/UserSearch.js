import React, { useState } from 'react';

function UserSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  
  const handleSearch = () => {
    // Send a request to your Flask API to search for users based on the searchQuery
    // Update the searchResults state with the API response
    // You can use the `fetch` function or Axios to make the API call
    
    // Example using fetch:
    fetch(`API_URL_HERE?query=${searchQuery}`)
      .then((response) => response.json())
      .then((data) => setSearchResults(data))
      .catch((error) => console.error('Error:', error));
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
          <h2>Search Results:</h2>
          <ul>
            {searchResults.map((user) => (
              <li key={user.id}>
                {user.username}
                <button onClick={() => handleFollow(user.id)}>Follow</button>
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
