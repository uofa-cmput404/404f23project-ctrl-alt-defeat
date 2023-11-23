import React from 'react'
import Markdown from "react-markdown";
import './PostItem.css';

import notLikedImgUrl from "../notLiked_black_24dp.svg";
import likedImgUrl from "../liked_black_24dp.svg";

const styles = {
  img: {
    maxWidth: '50px',
    padding: '15px 5px 15px 0px',
    cursor: 'pointer'
  },
  
  container: {    
    padding: 20,
    marginTop: 10
  }
}


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

function PostItem(props) {
  const selectToggleLike = async () => {
    console.log('toggle');

    props.setChangeLike(true);
    props.setPostSelected(props.item.post_id);
    props.setPostSelectedLiked(props.item.liked);
    props.setPostSelectedAuthor(props.item.author_id);
  }

  return (
    <div style={styles.container} class="card">
        <h3>{props.item.title}</h3>
        <small class="text-muted">Posted by: {props.item.username}</small>        
        <small class="text-muted">{props.item.date_posted}</small>        
        <hr/>
        <div>{get_content_as_elements(props.item.content_type,props.item.content)}</div>
        
        <div onClick={selectToggleLike}>
        {// Show like icon as liked or not based on if logged in author has liked the post
        props.item.liked ?

            <img style={styles.img} src={likedImgUrl} />
          
            : <img style={styles.img} src={notLikedImgUrl} onClick={selectToggleLike} /> 
          
        }
        </div>
    </div>
  )
}

export default PostItem
