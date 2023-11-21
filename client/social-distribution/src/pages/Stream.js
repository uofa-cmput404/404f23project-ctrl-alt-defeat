import React, { useEffect, useState } from 'react'
import PostsList from '../components/PostsList'
import UserSearch from '../components/UserSearch';
import Profile from '../components/Profile';
import FollowRequests from '../components/followRequests';
import axios from 'axios';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';

import Navbar from '../components/Navbar';

const postsUrl = 'http://127.0.0.1:5000/posts/'

export default function Stream({ username, authorId, setUsername }) {;
    const navigate = useNavigate();

    const likedPostsUrl = 'http://127.0.0.1:5000/authors/' + authorId + '/liked'
    const [likedPostIds, setLikedPostIds] = useState({});
    const [responseData, setResponseData] = useState([]);
    

    const [postsLists, setPostsLists] = useState([])
    const [showProfile, setShowProfile] = useState(false); 

    const styles = {
        container: {
            margin: 20,
            display: "flex",
            justifyContent: "space-between",                        
        },
        followContainer: {
            position: "sticky",            
        },
        contentContainer: {
            display: "flex",            
        },
        postsContainer: {
            marginTop: 20
        }
    }

    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.post(postsUrl, {
                    author_id: authorId
                })
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

        <div style={styles.container}>               
            {showProfile && <Profile username={username} authorId={authorId} setUsername={setUsername} onClose={closeProfile} />}          
            <div>
                <h1>Streams</h1>
                <button onClick={goToNewPost} type="button" class="btn btn-primary"><i class="fa fa-comment"></i> New Post</button>                      
                <div style={styles.postsContainer}>
                    {postsLists.length !== 0 ? <PostsList postsLists={postsLists} setPostsLists={setPostsLists} authorId={authorId} /> : <div>There are no posts</div>}
                </div>
            </div>         
            <div>
                <div className="search-container">
                {/* <h1>Search:</h1> */}
                {/* <UserSearch username={username} authorId={authorId} /> */}
                </div>
                <div style={styles.followContainer}>
                    <FollowRequests authorId={authorId} />
                </div>                
            </div>
            </div>
            <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
        </div>
    );
}
