import React, { useEffect, useRef, useState } from 'react'
import PostsList from '../components/PostsList'
import UserSearch from '../components/UserSearch';
import Profile from '../components/Profile';
import FollowRequests from '../components/followRequests';
import axios from 'axios';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import PostItem from '../components/PostItem';
import Markdown from "react-markdown";
import notLikedImgUrl from "../notLiked_black_24dp.svg";
import likedImgUrl from "../liked_black_24dp.svg";

const postsUrl = 'http://127.0.0.1:5000/api/';


export default function IndividualPost() {;    
    const [postSelected, setPostSelected] = useState([]);
    const [username, setUsername] = useState("");
    const navigate = useNavigate();
    let { post_id, author_id } = useParams();
    const [fetchDone, setFetchDone] = useState(false);

    const styles = {
        container: {
            margin: "20px"
        }
    }

    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.get(postsUrl + "authors/" + author_id + "/posts/" + post_id + "/display")
                .then(response => {
                // Handle the successful response here
                
                setPostSelected(response.data);                                   
                setUsername(response.data.author.displayName);
                })
                .catch(error => {
                // Handle any errors that occur during the request
                console.error('Error:', error);
                setPostSelected("invalid"); 
                }).finally(() => {
                    setFetchDone(true);
                });;
          } catch (error) {
            console.error('Error:', error);
          }
    }
    useEffect(() => {
        fetchData();        
    }, []);

    function get_content_as_elements(content_type, content){        
        if (content_type === "text/plain"){
            return(<p>{content}</p>);
        }
        else if (content_type === "text/markdown"){
            return(<Markdown>{content}</Markdown>);
        }
        else if (content_type === "image/png;base64" || content_type === "image/jpeg;base64")
        {
            //var image = new Image();
            //let decodedString = atob(content);
            let tag = 'data:' + content_type + "," + content;
            return (<img width={500} src={tag}/>) // Set to have width of 500 for now
        }
        else if (content_type === "image/png;url" || content_type === "image/jpeg;url"){
            //change width property or remove it, resizing will be done at the style level.
            return(<img src={content} width="100px"/>);
        }
    }

    
    return (
        <div style={styles.container}>
            <button class="btn btn-secondary" style={{width: '20vw'}} onClick={() => navigate("/homepage")}>Back to Homepage</button>
            { !fetchDone ?
                        <div class="spinner-border" role="status">
                            <span class="sr-only"></span>
                        </div> :
             
             (postSelected !== "invalid" ?
                <div>
                    <h3>{postSelected.title}</h3>
                    <div>Posted by: {username}</div>
                    <div>{postSelected.published}</div>
                    <div>{get_content_as_elements(postSelected.contentType,postSelected.content)}</div>                
                </div>
                : <h1>Post not found</h1> )
             }
        </div>
    );
}