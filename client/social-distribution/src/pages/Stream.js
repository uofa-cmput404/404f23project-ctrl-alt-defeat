import React, { useEffect, useRef, useState } from 'react'
import PostsList from '../components/PostsList'
import UserSearch from '../components/UserSearch';
import Profile from '../components/Profile';
import FollowRequests from '../components/followRequests';
import axios from 'axios';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';
import './global.css';

import Navbar from '../components/Navbar';

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

    const styles = {
        container: {
            margin: 20,
            display: "flex",
            marginLeft: 300,
            padding: 10   
        },
        followContainer: {            
            marginTop: 10,
            padding: 10           
        },
        contentContainer: {
            display: "flex",            
        },
        postsContainer: {
            marginTop: 20
        },
        card: {
            padding: 10
        },        
        sidebar: {            
            position: "fixed",
            zIndex: 1,            
            left: 10,            
            overflowX: "hidden",            
            overflowY:"scroll",
            height: "90%",
            paddingBottom: 10
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
        <div>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"/>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

            {showProfile && <Profile username={username} authorId={authorId} setUsername={setUsername} onClose={closeProfile} />}          
        <div style={styles.container}>       
        <div style={styles.sidebar}>
            <div class="card" style={styles.card}>                                  
                    <h3>My Github Activity</h3>                          
                    {activityList.length ? <div>
                        {activityList.map(e => {
                            return <div>
                                <b>{e.repo.name}</b>
                                    <p>{e.created_at.split("T")[0]}</p>                                
                                </div>
                        })}
                    
            </div> : "You have no commits"}
            
            </div>                
            <div class="card" style={styles.followContainer}>
                <h3>Follow Requests</h3>
                <FollowRequests authorId={authorId} />
            </div>
            </div>        
            <div style={styles.posts}>
                <h1>Streams</h1>
                <button onClick={goToNewPost} type="button" class="btn btn-primary"><i class="fa fa-comment"></i> New Post</button>                      
                <div style={styles.postsContainer}>
                    {postsLists.length !== 0 ? <PostsList postsLists={postsLists} setPostsLists={setPostsLists} authorId={authorId} /> : <div>There are no posts</div>}
                </div>
            </div>
            <div></div>         
            </div>
            <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
        </div>
    );
}
