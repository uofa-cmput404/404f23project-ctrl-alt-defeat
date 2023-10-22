import React, { useEffect, useState } from 'react'
import PostsList from '../components/PostsList'
import axios from 'axios';

const postsUrl = 'http://127.0.0.1:5000/posts/'

export default function Stream() {

    // const username = "philiponions" // temporary username


    const [postsLists, setPostsLists] = useState([])
    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.post(postsUrl, {
                    author_id: 1
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

  return (
    <div>
        <h1>Streams</h1>
        <div>
            <PostsList postsLists={postsLists}/>
        </div>
    </div>
  )
}
