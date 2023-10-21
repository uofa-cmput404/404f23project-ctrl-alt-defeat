import React, { useEffect } from 'react'
import PostItem from './PostItem'


function PostsList(props) {  
  return (
    <ul>
        {
            props.postsLists.map((item, index) => (
                <PostItem item={item} index={index}/>
            ))
        }
    </ul>
    
  )
}

export default PostsList