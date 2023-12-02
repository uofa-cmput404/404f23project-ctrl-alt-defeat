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
  
  container: {
    padding: 20,
    marginTop: 10,

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

  const handleToggleLike = async () => {
    console.log('toggle');

    props.togglePostLike(props.item.post_id, props.item.liked, props.item.author_id);
  }

  const fetchComments = async () => {
    try {
      const params = {
          'Authorization' : process.env.REACT_APP_AUTHORIZATION,
          comment_author_id: props.loginUser // Assuming this is the user ID
      };
      const apiUrl = process.env.REACT_APP_API_HOSTNAME + `/api/authors/${props.item.author_id}/posts/${props.item.post_id}/comments`;
  
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
      const apiUrl = process.env.REACT_APP_API_HOSTNAME + `/api/authors/${props.item.author_id}/posts/${props.item.post_id}/comments/${commentId}/toggle-like`;
  
      // Send the POST request
      await axios.post(apiUrl, {
          like_comment_author_id: props.loginUser
      }, {
          headers: {
              'Authorization' : process.env.REACT_APP_AUTHORIZATION
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
  const deleteComment = async (commentId) => {
    try {
      // API URL to delete the comment
      const apiUrl = `http://127.0.0.1:5000/api/authors/${props.item.author_id}/posts/${props.item.post_id}/comments/${commentId}`;

      // Send the DELETE request
      await axios.delete(apiUrl);

      // Update the comments in the local state to reflect the deletion
      const updatedComments = comments.filter(comment => comment.comment_id !== commentId);
      setComments(updatedComments);
    } catch (error) {
      console.error('Error deleting comment:', error);
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
      const apiUrl = process.env.REACT_APP_API_HOSTNAME + `/api/authors/${props.item.author_id}/posts/${props.item.post_id}/comments`;
      await axios.post(apiUrl, commentData, {
          headers: {
              'Authorization' : process.env.REACT_APP_AUTHORIZATION
          }
      });
      setComment('');
      fetchComments(); // Refresh comments after posting
    } catch (error) {
      console.error('Error posting comment:', error);
      // Optionally, handle the error more visibly to the user
    }
  };
  
  

  return (
    <div style={styles.container} class="card">
        <h3><a href={"http://localhost:3000/authors/" + props.item.author_id + "/posts/" + props.item.post_id}   >{props.item.title}</a></h3>
        <small class="text-muted">Posted by: {props.item.username}</small>
        <small class="text-muted">{props.item.date_posted}</small>
        <hr/>
        <div>{getContentAsElements(props.item.content_type,props.item.content)}</div>
        
        <div onClick={handleToggleLike}>
        {// Show like icon as liked or not based on if logged in author has liked the post
        props.item.liked ?

            <img style={styles.img} src={likedImgUrl} />

            : <img style={styles.img} src={notLikedImgUrl} />

        }
        </div>
        <div style={styles.commentBox}>
            <input
              type="text"
              value={comment}
              onChange={handleCommentChange}
              placeholder="Write a comment..."
              style={styles.input}
            />
            <button class="btn btn-primary" onClick={handleSendComment}>Send</button>
        </div>
 {/* Display comments with commenter's name, text, like button, and delete button */}
 <div>
        {comments.map((comment, index) => (
          <div key={`${comment.comment_id}-${index}`} 
               style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
            <div>
              <span style={{ fontWeight: 'bold' }}>{comment.comment_name}:</span>
              <span style={{ marginLeft: '8px' }}>{comment.comment_text}</span>
            </div>
            <div>
              <button
                onClick={() => toggleLikeComment(comment.comment_id)}
                style={{ border: 'none', background: 'none', cursor: 'pointer', marginRight: '10px' }}
              >
                <img
                  src={comment.liked ? likedImgUrl : notLikedImgUrl}
                  alt="Like"
                  style={{ width: '24px', height: '24px' }}
                />
              </button>
              {comment.comment_author_id === props.loginUser && (
                <button
                  onClick={() => deleteComment(comment.comment_id)}
                  style={{ border: 'none', background: 'none', cursor: 'pointer' }}
                >
                  Delete
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}


export default PostItem
