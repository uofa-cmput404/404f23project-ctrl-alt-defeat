import React, { useContext, useState } from 'react';
import { toast } from 'react-toastify';
import { UserContext } from '../App';

function UserSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const {username, authorId} = useContext(UserContext);    

  const handleSearch = async () => {
    try {
      const localResponse = await fetch(`http://localhost:5000/api/follow/usersearch?query=${searchQuery}`);
      if (!localResponse.ok) {
        console.error('Local search failed');
        return;
      }
      const localData = await localResponse.json();
      const localResults = localData.users.filter(user => user.id !== authorId);
  
      const externalResponse1 = await fetch('https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/authors/', {
        headers: {
          'accept': 'application/json',
          'Authorization': 'Basic Y3Jvc3Mtc2VydmVyOnBhc3N3b3Jk',
        },
      });
      if (!externalResponse1.ok) {
        console.error('External search 1 failed');
        return;
      }
      const externalData1 = await externalResponse1.json();
      const externalResults1 = externalData1.items.map(item => ({
        id: item.id.split('/').pop(),
        username: item.displayName,
      }));

      const externalResponse2 = await fetch('https://cmput-average-21-b54788720538.herokuapp.com/api/authors/?page=1&page_size=1000', {
        headers: {
          'accept': 'application/json',
          'Authorization': 'Basic Q3RybEFsdERlZmVhdDpzdHJpbmc=',
        },
      });
      if (!externalResponse2.ok) {
        console.error('External search 2 failed');
        return;
      }
      const externalData2 = await externalResponse2.json();
      const externalResults2 = externalData2.items.map(item => ({
        id: item.id.split('/').pop(),
        username: item.displayName,
      }));

      const filteredExternalResults1 = externalResults1.filter(user => user.username.toLowerCase().includes(searchQuery.toLowerCase()));
      const filteredExternalResults2 = externalResults2.filter(user => user.username.toLowerCase().includes(searchQuery.toLowerCase()));
      // const filteredExternalResults3 = externalResults3.filter(user => user.username.toLowerCase().includes(searchQuery.toLowerCase()));

      const combinedResults = [...localResults, ...filteredExternalResults1, ...filteredExternalResults2];
      setSearchResults(combinedResults);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  
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
                <button onClick={() => handleUnfollow(user.id)}>Unfollow</button>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p></p>
      )}
    </div>
  );
}

export default UserSearch;