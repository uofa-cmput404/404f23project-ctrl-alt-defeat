import React from 'react'
import Markdown from "react-markdown";


import notLikedImgUrl from "../notLiked_black_24dp.svg";
import likedImgUrl from "../liked_black_24dp.svg";

const styles = {
  img: {
    maxWidth: '50px',
    padding: '15px 5px 15px 0px',
    cursor: 'pointer'
  },
  
  /*container: {
    display: 'flex',
    alignItems: 'center',
    padding: '5px 0px 5px 5px',
    fontSize: '16px',
    cursor: 'pointer',
    backgroundColor: '#808080',
    color: 'white',
    border: 'none',
    width: '85px',
    borderRadius: '4px',
    justifyCenter: 'center'
  }*/

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
    <li key={props.key}>
        <h3>{props.item.title}</h3>
        <div>Posted by: {props.item.username}</div>
        <div>{props.item.date_posted}</div>
        <div>{get_content_as_elements(props.item.content_type,props.item.content)}</div>
        
        <div style={styles.container} onClick={selectToggleLike}>
        {// Show like icon as liked or not based on if logged in author has liked the post
        props.item.liked ?

            <img style={styles.img} src={likedImgUrl} />
          
            : <img style={styles.img} src={notLikedImgUrl} onClick={selectToggleLike} /> 
          
        }
        </div>
    </li>
  )
}

export default PostItem