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

    const handleFollowRequest = async (receiveAuthorId, displayName, host) => {
      try {
        if (host === 'local') {
          const response = await fetch('http://localhost:5000/api/follow/follow_request', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              author_send: authorId,
              author_receive: receiveAuthorId,
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
            console.error('Local follow request failed');
          }
        } else {
          let apiUrl;
          let object;
          let creds;
          if (host === 'https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/') {
            apiUrl = `https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/authors/${receiveAuthorId}/inbox`;
            creds = 'Basic ' + btoa('cross-server:password');
            object = {
              type: 'Follow',
              summary: 'Follow Request',
              actor: {
                type: 'author',
                id: `https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/authors/${authorId}`,
                url: `https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/authors/${authorId}`,
                host: 'https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/',
                displayName: username,
                github: null,
                profileImage: null
              },
              object: {
                type: 'author',
                id: `${host}authors/${receiveAuthorId}`,
                host: host,
                displayName: displayName,
                url: `${host}authors/${receiveAuthorId}`,
                github: null,
                profileImage: null
              }
            };
          } else if (host === 'https://cmput-average-21-b54788720538.herokuapp.com/api') {
            apiUrl = `https://cmput-average-21-b54788720538.herokuapp.com/api/authors/${receiveAuthorId}/inbox/`;
            creds = 'Basic ' + btoa('CtrlAltDefeat:string');
            object = {
              items: {              
                type: 'Follow',
                summary: 'Follow Request',
                actor: {
                  type: 'author',
                  id: `https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/authors/${authorId}`,
                  url: `https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/authors/${authorId}`,
                  host: 'https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/',
                  displayName: username,
                  github: null,
                  profileImage: null
                },
                object: {
                  type: 'author',
                  id: `${host}/authors/${receiveAuthorId}`,
                  host: host,
                  displayName: displayName,
                  url: `${host}/authors/${receiveAuthorId}`,
                  github: null,
                  profileImage: null
                }
              }
            };
          } else if (host === 'https://chimp-chat-1e0cca1cc8ce.herokuapp.com/') {
            apiUrl = `https://chimp-chat-1e0cca1cc8ce.herokuapp.com/authors/${receiveAuthorId}/inbox/`;
            creds = 'Basic ' + btoa('node-ctrl-alt-defeat:chimpchatapi');
            object = {
              type: 'Follow',
              summary: 'Follow Request',
              actor: {
                type: 'author',
                id: `https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/authors/${authorId}`,
                url: `https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/authors/${authorId}`,
                host: 'https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/',
                displayName: username,
                github: null,
                profileImage: null
              },
              object: {
                type: 'author',
                id: `${host}authors/${receiveAuthorId}`,
                host: host,
                displayName: displayName,
                url: `${host}authors/${receiveAuthorId}`,
                github: null,
                profileImage: null
              }
            };
          } else {
            console.error('Invalid host:', host);
            return;
          }
      
          const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': creds,
            },
            body: JSON.stringify(object),
          });
          
          console.log(JSON.stringify(object))

          if (!response.ok) {
            if (host === 'https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/') {
              if (response.status === 400) {
                console.log('400');
                toast.error('Follow request already sent')
                return;
              }
              console.log('not 400');
            }
            console.error('Remote follow request failed:', response.statusText);
            console.log('Response body:', await response.text());
            return;
          } else {
            if (host === 'https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/') {
              toast.success('Follow Request Sent');
              return;
            }
            const data = await response.json();
            if (data) {
              toast.success('Follow Request Sent');
              console.log('Remote follow working');
              console.log(data);
            } else {
                console.error('Response does not contain valid JSON');
            }
          }    
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
                <button onClick={() => handleFollowRequest(user.id, user.username, user.host)} type="button" class="btn btn-primary">Follow</button>    
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