import React, { useEffect, useRef, useState } from 'react'
import PostsList from '../components/PostsList'
import UserSearch from '../components/UserSearch';
import Profile from '../components/Profile';
import FollowRequests from '../components/followRequests';
import axios from 'axios';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';

const postsUrl = 'http://127.0.0.1:5000/posts/';


export default function Stream({ username, authorId, setUsername }) {;
    const navigate = useNavigate();
    
    const likedPostsUrl = 'http://127.0.0.1:5000/authors/' + authorId + '/liked';
    const githubIdLink = 'http://127.0.0.1:5000/authors/github/' + authorId;     
    
    const [likedPostIds, setLikedPostIds] = useState({});
    const [responseData, setResponseData] = useState([]);
    
    const [postsLists, setPostsLists] = useState([]);
    const [activityList, setActivityList] = useState([]);
    const [showProfile, setShowProfile] = useState(false);     

    const styles = {
        container: {
            margin: "20px"
        }
    }

    const fetchGithubActivity = async () => {        
        try {
            // Make the GET request using Axios
                axios.get(githubIdLink)
                .then(response => {
                    try {
                            if (response.data !== "") {
                                // Make the GET request using Axios
                                    axios.get('https://api.github.com/users/' + response.data + '/events')
                                    .then(response => {
                                    // Handle the successful response here                
                                    setActivityList(response.data.slice(0, 5));         
                                    console.log(response.data);   
                                    })
                                    .catch(error => {
                                    // Handle any errors that occur during the request                                    

                                    console.error('Error:', error);
                                    });                                
                            }
                      } catch (error) {
                        console.error('Error:', error);
                      }                                
                })
                .catch(error => {
                // Handle any errors that occur during the request
                console.error('Error:', error);
                });
          } catch (error) {
            console.error('Error:', error);
          }
    }

    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.get(postsUrl + `?author_id=${authorId}`)
                .then(response => {
                // Handle the successful response here
                //console.log('Response data:', response.data);
                
                setResponseData(response.data);      
                console.log(response.data)          
                setPostsLists(response.data);                
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
        fetchLikedPosts();
        if (username !== null) {
            fetchGithubActivity();
        }
    }, []);

    useEffect(() => {
        labelLikedPosts();
    }, [likedPostIds]);

    const labelLikedPosts = () => {
        // Label (on front-end) which posts have been liked by the logged in author
        let posts = responseData.map((item, index) => {
            let liked = false;
            for (let i = 0; i < likedPostIds.length; i++) {
                //console.log("check post id in likedPostIds", likedPostIds[i].post_id);
                if (likedPostIds[i].post_id === item.post_id) {
                    liked = true;
                }
            }

            return {...item, liked: liked}; 
        });
        
        //console.log("posts passed:", posts);
        // Pass the posts to setPostsLists
        setPostsLists(posts);
    };

     // Check `likes` table (back-end) for all posts that logged in author has liked
     async function fetchLikedPosts() {
        try {
            axios.get(likedPostsUrl)
            .then(response => {
                //console.log('liked ids:', response.data);
                setLikedPostIds(response.data);
                console.log(response.data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
            } catch (error) {
                console.error('Error:', error);
            }
    }

    const toggleProfile = () => {
        setShowProfile(!showProfile);
      };

    const closeProfile = () => {
    setShowProfile(false);
    };
      
    function goToManagePosts() {
        navigate("/manageposts")
    }

    function goToNewPost() {
        navigate("/newpost")
    }

    return (
        <div style={styles.container}>
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
          <h1>My Github Activity</h1>          
          {activityList.length ? <div>
            {activityList.map(e => {
                return <div>
                    <h3>{e.repo.name}</h3>
                        <p>{e.created_at.split("T")[0]}</p>
                        <ul>
                            {e.payload.commits ? e.payload.commits.map(i => {
                                return <div>{i.message}</div>
                            }) : null}
                        </ul>
                    </div>
            })}
            
          </div> : "You have no commits"}
          
          <h1>Streams</h1>
          <button onClick={goToNewPost}>New post</button>
          <button onClick={goToManagePosts}>Manage my posts</button>
          <div>
            {postsLists.length !== 0 ? <PostsList postsLists={postsLists} setPostsLists={setPostsLists} authorId={authorId} /> : <div>There are no posts</div>}
          </div>
          <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
        </div>
    );
}
