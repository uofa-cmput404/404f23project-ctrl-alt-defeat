import React, { useEffect, useState } from 'react'
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
import GithubIcon from '../components/GithubIcon';

const postsUrl = 'http://127.0.0.1:5000/api/posts';


export default function Stream({ username, authorId, setUsername, updateAuthStatus, updateUserAndAuthorId }) {;
    const navigate = useNavigate();
    const likedPostsUrl = 'http://127.0.0.1:5000/api/authors/' + authorId + '/liked';
    const githubIdLink = 'http://127.0.0.1:5000/api/authors/github/' + authorId;     
    
    const [likedPostIds, setLikedPostIds] = useState({});
    const [responseData, setResponseData] = useState([]);
    const [fetchDone, setFetchDone] = useState(false);
    const [fetchGithubDone, setFetchGithubDone] = useState(false);
    
    const [postsLists, setPostsLists] = useState([]);
    const [activityList, setActivityList] = useState([]);
    const [showProfile, setShowProfile] = useState(false);     


    const fetchGithubActivity = async () => {        
        try {
            // Make the GET request using Axios
                axios.get(githubIdLink)
                .then(response => {
                    try {
                            if (response.data !== "" && response.data.github !== null) {
                                
                                // Make the GET request using Axios
                                    axios.get('https://api.github.com/users/' + response.data.github + '/events')
                                    .then(response => {
                                    // Handle the successful response here                
                                    setActivityList(response.data.slice(0, 5));         
                                    //console.log(response.data);   
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
                }).finally(() => {
                    setFetchGithubDone(true);
                });
          } catch (error) {
            console.error('Error:', error);
          }
    }

    const styles = {
        posts: {
            width: "100%"
        },
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
            width: "100%",            
            marginTop: 20
        },
        card: {
            padding: 10,
            textOverflow: 'ellipsis',                        
        },        
        sidebar: {            
            position: "fixed",
            zIndex: 1,            
            left: 10,            
            overflowX: "hidden",            
            overflowY:"scroll",
            maxHeight: "90%",            
            textOverflow: 'ellipsis',
            paddingBottom: 10,   
            width: 280                     
        }
    }

    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.get(postsUrl + `?author_id=${authorId}`, {
                    headers: {
                        'Authorization': 'Basic Q3RybEFsdERlZmVhdDpmcm9udGVuZA=='
                    }
                })
                .then(response => {
                // Handle the successful response here
                //console.log('Response data:', response.data);
                
                setResponseData(response.data);    
                
                // We set postLists here, in case the post likes feature is not working
                setPostsLists(response.data);
                })
                .catch(error => {
                // Handle any errors that occur during the request
                console.error('Error:', error);
                })
                .finally(() => {
                    setFetchDone(true);
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
    }, [responseData]);

    
    const labelLikedPosts = () => {
        // Label (on front-end) which posts have been liked by the logged in author
        let posts = responseData.map((item, index) => {
            let liked = false;
            for (let i = 0; i < likedPostIds.length; i++) {
                //console.log('indiv like post id', likedPostIds[i])
                if (likedPostIds[i]=== item.post_id) {
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
    // Check `likes` table (back-end) for all posts that logged in author has liked
    async function fetchLikedPosts() {        
        try {
            axios.get(likedPostsUrl)
            .then(response => {
                    console.log("Fetched data");
                    console.log(response.data);
                // Parse the liked posts for the post IDs exclusively
                let fetchedLikedPostIds = [];
                for (let i = 0; i < response.data.items.length; i++) {
                    // Assuming each liked item has an 
                    // `object` that follows URL structure per spec,
                    // i.e. http://service/authors/<author_id>/posts/<post_id>
                    fetchedLikedPostIds.push(response.data.items[i].object.split('/')[6]);

                }

                setLikedPostIds(fetchedLikedPostIds);
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
                        <div style={{display: "flex", alignItems: "center"}}><GithubIcon/><h3 style={{marginLeft: 10, paddingTop: 10, alignSelf: "center" }}>Activity</h3></div>
                        <hr/>
                                                    
                        {
                            !fetchGithubDone ? <div class="spinner-border" role="status">
                                        <span class="sr-only"></span>
                                    </div>
                        : activityList.length ? <div>
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
                <b>Hi {username}! 😎</b>
                <h1>Streams</h1>
                    <div>
                        <button onClick={goToNewPost} type="button" class="btn btn-primary"><i class="fa fa-comment"></i> New Post</button>                                                              
                    </div>
                <div style={styles.postsContainer}>
                    {
                        !fetchDone ?
                        <div class="spinner-border" role="status">
                            <span class="sr-only">Loading...</span>
                        </div> :  (postsLists.length !== 0 ? <PostsList postsLists={postsLists} setPostsLists={setPostsLists} authorId={authorId} /> : <div>There are no posts</div>)
                    }
                </div>
            </div>
            <div></div>         
            </div>            
        </div>
    );
}
