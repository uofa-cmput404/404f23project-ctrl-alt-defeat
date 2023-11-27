import React, { useState, useEffect } from 'react'
import PostItem from './PostItem'
import axios from 'axios';


function PostsList(props) {  
  // Whether user has clicked like
  const [changeLike, setChangeLike] = useState(false);

  // Post ID of post selected
  const [postSelected, setPostSelected] = useState(null);

  // Like status of post selected
  const [postSelectedLiked, setPostSelectedLiked] = useState(null);

  // Author of post selected
  const [postSelectedAuthor, setPostSelectedAuthor] = useState('');
    
  // Listen for each PostItem if logged in author presses like button
  if (changeLike === true) {
    console.log("heard postsLists", changeLike, postSelected, postSelectedLiked, postSelectedAuthor);

    // URL goes to AUTHOR of post, NOT the author who is logged in/sending like
    const sendLikeUrl = process.env.API_HOSTNAME + "/authors/" + postSelectedAuthor + '/inbox';

    if (postSelectedLiked === true) {
      console.log("unlike");
      // To unlike the post
      const sendUnlikeUrl = sendLikeUrl + '/unlike'
      try {
        axios.post(sendUnlikeUrl, {
          like_author_id: props.authorId,
          post_id: postSelected
        })
        .then(response => {
          // Handle successful response
          // Update front-end to reflect change
          props.setPostsLists(props.postsLists.map(item => {
            if (item.post_id === postSelected) {
              return { ...item, liked: false}; // Create a new object with the unliked value
            }
            return item; // Return the original object for other items
          }))


        })
        .catch(error => {
          console.error('Error:', error);
          });
      } catch (error) {
        console.error('Error:', error);
      }


    } else {
      console.log("like");
      // To like the post
      try {
        axios.post(sendLikeUrl, {
          like_author_id: props.authorId,
          post_id: postSelected
        })
        .then(response => {
          // Handle successful response
          // Update front-end to reflect change
          props.setPostsLists(props.postsLists.map(item => {
            if (item.post_id === postSelected) {
              return { ...item, liked: true}; // Create a new object with the liked value
            }
            return item; // Return the original object for other items
          }))


        })
        .catch(error => {
          console.error('Error:', error);
          });
      } catch (error) {
        console.error('Error:', error);
      }

    }


    setChangeLike(false);
  }

  return (
    <ul>
        {
            props.postsLists.map((item, index) => (
                <PostItem item={item} index={index} 
                setChangeLike = {setChangeLike} 
                setPostSelected = {setPostSelected}
                setPostSelectedLiked={setPostSelectedLiked}
                setPostSelectedAuthor={setPostSelectedAuthor} 
                loginUser = {props.authorId}/>
            ))
        }
    </ul>
    
  )
}

export default PostsList