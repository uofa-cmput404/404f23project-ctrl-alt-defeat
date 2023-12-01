import React, { useState, useEffect } from 'react'
import PostItem from './PostItem'
import axios from 'axios';


function PostsList(props) {
  const rootUrl = window.location.origin;

  // Listen for each PostItem if logged in author presses like button
  const togglePostLike = (postSelected, postSelectedLiked, postSelectedAuthor) => {
    console.log("heard postsLists", postSelected, postSelectedLiked, postSelectedAuthor);

    // URL goes to AUTHOR of post, NOT the author who is logged in/sending like
    const sendLikeUrl = "http://127.0.0.1:5000/api/authors/" + postSelectedAuthor + '/inbox';

    if (postSelectedLiked === true) {
      console.log("unlike");
      // To unlike the post
      const sendUnlikeUrl = sendLikeUrl + '/unlike'
      try {
        axios.delete(sendUnlikeUrl, {
          data: {
            summary: props.username + " Unliked your post",
            type: "Unlike",
            author: {
              type: "author",
              id: rootUrl + "/authors/" + props.authorId, // like_author_id
              host: rootUrl + "/",
              displayName: props.username,
              url: rootUrl + "/authors/" + props.authorId,
              github: props.github === "" ? null : "https://github.com/" + props.github,
              profileImage: null
            },
            object: rootUrl + "/authors/" + props.authorId + "/posts/" + postSelected
          }
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
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
          summary: props.username + " Likes your post",
          type: "Like",
          author: {
            type: "author",
            id: rootUrl + "/authors/" + props.authorId, // like_author_id
            host: rootUrl + "/",
            displayName: props.username,
            url: rootUrl + "/authors/" + props.authorId,
            github: props.github === "" ? null : "https://github.com/" + props.github,
            profileImage: null
          },
          object: rootUrl + "/authors/" + props.authorId + "/posts/" + postSelected
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
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
  }

  return (
    <div>
        {
            props.postsLists.map((item, index) => (
                <PostItem item={item} index={index} 
                togglePostLike={togglePostLike}
                loginUser = {props.authorId}/>
            ))
        }
    </div>
    
  )
}

export default PostsList