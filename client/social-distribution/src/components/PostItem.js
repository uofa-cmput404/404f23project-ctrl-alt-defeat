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


function getContentAsElements(content_type, content){
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
          'Authorization' : 'Basic ' + 'Q3RybENDdHJsVjpwYXNzd29yZA==',
          comment_author_id: props.loginUser // Assuming this is the user ID
      };
      const apiUrl = 'https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com' + `/api/authors/${props.item.author_id}/posts/${props.item.post_id}/comments`;
  
      const response = await axios.get(apiUrl, { params });
      if (response.data && response.data.comments) {
        // Map through each comment and add a 'liked' property based on the user's like status
        const updatedComments = response.data.comments.map(comment => ({
          ...comment,
          liked: comment.isLikedByCurrentUser 
        }));
        setComments(updatedComments);
      } else {
        setComments([]);
      }
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };
  

  const toggleLikeComment = async (commentId) => {
    try {
      // Construct the URL for the POST request
      const apiUrl = 'https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com' + `/api/authors/${props.item.author_id}/posts/${props.item.post_id}/comments/${commentId}/toggle-like`;
  
      // Send the POST request
      await axios.post(apiUrl, { like_comment_author_id: props.loginUser }, {headers: {
          'Authorization' : 'Basic ' + 'Q3RybENDdHJsVjpwYXNzd29yZA=='
          }});
  
      // Update the like status in the local state
      const updatedComments = comments.map(comment => {
        if (comment.comment_id === commentId) {
          return { ...comment, liked: !comment.liked };
        }
        return comment;
      });
  
      setComments(updatedComments);
    } catch (error) {
      console.error('Error toggling like status:', error);
      // Optionally, handle the error more visibly to the user
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
      const apiUrl = 'https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com' + `/api/authors/${props.item.author_id}/posts/${props.item.post_id}/comments`;
      await axios.post(apiUrl, commentData, {headers: {'Authorization' : 'Basic ' + 'Q3RybENDdHJsVjpwYXNzd29yZA=='}});
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
        <div>{getContentAsElements(props.item.content_type, props.item.content)}</div>
        
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

         {/* Display comments with commenter's name, text, and like button */}
         <div>
        {comments.map((comment, index) => (
          <div key={`${comment.comment_id}-${index}`} 
               style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <div>
              <span style={{ fontWeight: 'bold' }}>{comment.comment_name}:</span>
              <span style={{ marginLeft: '8px' }}>{comment.comment_text}</span>
            </div>
            <button 
              onClick={() => toggleLikeComment(comment.comment_id)}
              style={{ border: 'none', background: 'none', cursor: 'pointer' }}
            >
              <img 
                src={comment.liked ? likedImgUrl : notLikedImgUrl} 
                alt="Like" 
                style={{ width: '24px', height: '24px' }}
              />
            </button>
          </div>
        ))}
      </div>
    </li>
  );
}


export default PostItem
