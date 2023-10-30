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
    
  // Listen for each PostItem if logged in author presses like button
  if (changeLike === true) {
    console.log("heard postsLists", changeLike, postSelected, postSelectedLiked);

    if (postSelectedLiked === true) {
      console.log("unlike");
      // To unlike the post


      props.setPostsLists(props.postsLists.map(item => {
        if (item.post_id === postSelected) {
          return { ...item, liked: false}; // Create a new object with the unliked value
        }
        return item; // Return the original object for other items
      }))


    } else {
      console.log("like");
      // To like the post

      props.setPostsLists(props.postsLists.map(item => {
        if (item.post_id === postSelected) {
          return { ...item, liked: true}; // Create a new object with the liked value
        }
        return item; // Return the original object for other items
      }))
    }


    setChangeLike(false);
  }

  return (
    <ul>
        {
            props.postsLists.map((item, index) => (
                <PostItem item={item} index={index} setChangeLike = {setChangeLike} 
                setPostSelected = {setPostSelected}
                setPostSelectedLiked={setPostSelectedLiked} />
            ))
        }
    </ul>
    
  )
}

export default PostsList