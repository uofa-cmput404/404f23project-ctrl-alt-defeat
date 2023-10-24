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

    function goToManagePosts() {
        navigate("/manageposts")
    }

  return (
    <div>
        <h1>Streams</h1>
        <button onClick={goToManagePosts}>Manage my posts</button>
        <div>
            {
                postsLists.length !== 0 ? <PostsList postsLists={postsLists}/> : <div>There are no posts</div>
            }
        </div>
    </div>
  )
}
