import React, { useContext, useEffect, useState } from 'react'
import PostsList from '../components/PostsList'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../App';

const postsUrl = 'http://127.0.0.1:5000/posts/'

export default function Stream() {

    // const username = "philiponions" // temporary username
    const navigate = useNavigate();
    const {username, authorId} = useContext(UserContext);   

    const likedPostsUrl = 'http://127.0.0.1:5000/authors/' + authorId + '/liked'
    const [likedPostIds, setLikedPostIds] = useState({});
    const [responseData, setResponseData] = useState([]);
    

    const [postsLists, setPostsLists] = useState([])
    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.post(postsUrl, {
                    author_id: authorId
                })
                .then(response => {
                // Handle the successful response here
                //console.log('Response data:', response.data);

                // Check if each post if it has been liked or not
                fetchLikedPosts()
                
                setResponseData(response.data);

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
    }, []);

    useEffect(() => {
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
    }, [postsLists]);


     // Check `likes` table (back-end) for all posts that logged in author has liked
     async function fetchLikedPosts() {
        try {
            axios.get(likedPostsUrl)
            .then(response => {
                //console.log('liked ids:', response.data);
                setLikedPostIds(response.data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
            } catch (error) {
                console.error('Error:', error);
            }
    }

    function goToManagePosts() {
        navigate("/manageposts")
    }

    function goToNewPost() {
        navigate("/newpost")
    }

  return (
    <div>
        <h1>Streams</h1>
        <button onClick={goToNewPost}>New post</button>
        <button onClick={goToManagePosts}>Manage my posts</button>
        <div>
            {
                postsLists.length !== 0 ? <PostsList postsLists={postsLists}
                setPostsLists={setPostsLists}/> : <div>There are no posts</div>
            }
        </div>
    </div>
  )
}
