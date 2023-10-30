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
    

    const [postsLists, setPostsLists] = useState([])
    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.post(postsUrl, {
                    author_id: authorId
                })
                .then(response => {
                // Handle the successful response here
                console.log('Response data:', response.data);
                
                const likedPostIds = fetchLikedPosts();
                // Check if each post if it has been liked or not
                const posts = response.data.map( (data, index) => ({...data, liked: false}) );
                
                console.log("Posts:", posts)

                // Pass the posts to setPostsLists
                setPostsLists(posts);
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

    async function fetchLikedPosts() {
        try {
            // Check `likes` table for all posts that logged in author has liked
            axios.get(likedPostsUrl)
            .then(response => {
                console.log('liked ids:', response.data);
                return response.data;
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
