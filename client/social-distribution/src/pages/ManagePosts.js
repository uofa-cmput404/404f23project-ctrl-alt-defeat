import React, { useEffect, useState } from 'react'
import ManagePostItem from '../components/ManagePostItem'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const managePostsUrl = 'http://127.0.0.1:5000/posts/manage'
function ManagePosts() {
    const username = "philiponions" // temporary username
    const navigate = useNavigate();
    const [postsLists, setPostsLists] = useState([])

    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.post(managePostsUrl, {
                    author_id: username
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
        <ul>
            {
                postsLists.map((item, index) => (
                    <ManagePostItem postLists={postsLists} 
                                    setPostsLists={setPostsLists} 
                                    item={item} index={index}/>
                ))
            }
        </ul>
    </div>
  )
}

export default ManagePosts