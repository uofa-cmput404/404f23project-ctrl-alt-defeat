import React, { useState, useEffect } from 'react'
import PostItem from './PostItem'


function PostsList(props) {  
  const [changeLike, setChangeLike] = useState(false);
  const [postSelected, setPostSelected] = useState(null);
  const [postSelectedLiked, setPostSelectedLiked] = useState(null);

  if (changeLike === true) {
    console.log("heard postsLists", changeLike, postSelected, postSelectedLiked);

    if (postSelectedLiked === true) {
      console.log("unlike");
      props.setPostsLists(props.postsLists.map(item => {
        if (item.post_id === postSelected) {
          return { ...item, liked: false}; // Create a new object with the unliked value
        }
        return item; // Return the original object for other items
      }))
    } else {
      console.log("like");
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