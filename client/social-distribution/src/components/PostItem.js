import React, { useState, useEffect }  from 'react'
import Markdown from "react-markdown";
import './PostItem.css';
import axios from 'axios';
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
  commentBox: {
    margin: '10px 0',
    display: 'flex',
    alignItems: 'center',
  },
  input: {
    flex: 1,
    marginRight: '10px',
  },

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

  const [comment, setComment] = useState('');
  const [comments, setComments] = useState([]);

  const selectToggleLike = async () => {
    console.log('toggle');

    props.setChangeLike(true);
    props.setPostSelected(props.item.post_id);
    props.setPostSelectedLiked(props.item.liked);
    props.setPostSelectedAuthor(props.item.author_id);
  }

  const fetchComments = async () => {
    try {
      const params = {
        comment_author_id: props.loginUser // Assuming this is the user ID
      };
      const apiUrl = process.env.HOSTNAME + `/authors/${props.item.author_id}/posts/${props.item.post_id}/comments`;
  
      const response = await axios.get(apiUrl, { params });
      if (response.data && response.data.comments) {
        setComments(response.data.comments); // Assuming the response has a 'comments' field
      } else {
        setComments([]); // In case the response does not have a 'comments' field
      }
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };
  
  useEffect(() => {
    fetchComments();
  }, [props.item, props.loginUser]); // Refetch comments when item or loginUser changes
  
  const handleCommentChange = (e) => {
    setComment(e.target.value);
  };


  //send comment to database
  const handleSendComment = async () => {
    if (!comment) return;
  
    const commentData = {
      comment_author_id: props.loginUser, //get user id
      comment_text: comment

    };
  
    try {
      const apiUrl = `http://127.0.0.1:5000/authors/${props.item.author_id}/posts/${props.item.post_id}/comments`;
      await axios.post(apiUrl, commentData);
      setComment('');
      fetchComments(); // Refresh comments after posting
    } catch (error) {
      console.error('Error posting comment:', error);
      // Optionally, handle the error more visibly to the user
    }
  };
  
  

  return (
    <li key={props.key}>
        <h3>{props.item.title}</h3>
        <div>Posted by: {props.item.username}</div>
        <div>{props.item.date_posted}</div>
        <div>{get_content_as_elements(props.item.content_type, props.item.content)}</div>
        
        <div style={styles.container} onClick={selectToggleLike}>
          {props.item.liked ?
            <img style={styles.img} src={likedImgUrl} /> :
            <img style={styles.img} src={notLikedImgUrl} onClick={selectToggleLike} /> 
          }
        </div>

        {/* Comment box and send button */}
        <div style={styles.commentBox}>
            <input
              type="text"
              value={comment}
              onChange={handleCommentChange}
              placeholder="Write a comment..."
              style={styles.input}
            />
            <button onClick={handleSendComment}>Send</button>
        </div>

        {/* Display comments with commenter's name and text */}
        <div>
          {comments.map((comment, index) => (
            <div key={`${comment.comment_name}-${index}`}>
              <strong>{comment.comment_name}:</strong> {comment.comment_text}
            </div>
          ))}
        </div>
    </li>
  );
}


export default PostItem
