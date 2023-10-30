import React, { useEffect, useState } from 'react'
import PostsList from '../components/PostsList'
import UserSearch from '../components/UserSearch';
import Profile from '../components/Profile';
import FollowRequests from '../components/followRequests';
import axios from 'axios';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';

const postsUrl = 'http://127.0.0.1:5000/posts/'

export default function Stream({ username, authorId, setUsername }) {;
    const navigate = useNavigate();
    const [postsLists, setPostsLists] = useState([])
    const [showProfile, setShowProfile] = useState(false); 

    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.post(postsUrl, {
                    author_id: authorId
                })
                .then(response => {
                // Handle the successful response here
                console.log('Response data:', response.data);
                    setPostsLists(response.data)
                })
                .catch(error => {
                // Handle any errors that occur during the request
                console.error('Error:', error);
                });
          } catch (error) {
            console.error('Error:', error);
          }
    }
    useEffect(() => {
        fetchData();
    }, [])

    const toggleProfile = () => {
        setShowProfile(!showProfile);
      };

    const closeProfile = () => {
    setShowProfile(false);
    };
      
    function goToManagePosts() {
        navigate("/manageposts")
    }

    return (
        <div>
          <div className="flex-container">
            <div className="search-container">
              <h1>Search:</h1>
              <UserSearch username={username} authorId={authorId} />
            </div>
            <div className="follow-requests-container">
              <FollowRequests authorId={authorId} />
            </div>
          </div>
          {showProfile && <Profile username={username} authorId={authorId} setUsername={setUsername} onClose={closeProfile} />}
          <button onClick={toggleProfile}>Edit Profile</button>
          <h1>Stream</h1>
          <button onClick={goToManagePosts}>Manage my posts</button>
          <div>
            {postsLists.length !== 0 ? <PostsList postsLists={postsLists} /> : <div>There are no posts</div>}
          </div>
          <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
        </div>
      );
}
