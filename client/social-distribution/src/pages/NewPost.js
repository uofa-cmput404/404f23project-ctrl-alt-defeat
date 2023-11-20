import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { UserContext } from '../App';

const newPostUrl = 'http://127.0.0.1:5000/posts/new'

export default function NewPost(props) {

  // Modified from login.js
  const styles = {
      container: {
        display: 'flex',
        flexDirection: 'column',
        //alignItems: 'center',
        padding: '10px',
        height: '100vh'
      },
      title: {
        padding: '10px',
        fontSize: '16px',
        width: '400px'
      },
      content: {
        //margin: '10px',
        padding: '10px',
        fontSize: '16px',
        height: '200px',
        width: '400px'
      },
      button_post: {
        padding: '10px 20px',
        margin: '10px 0px',
        fontSize: '16px',
        cursor: 'pointer',
        backgroundColor: '#808080',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        width: '25vw'
      },
      button_goback: {
        padding: '10px 20px',
        margin: '10px 0px',
        fontSize: '16px',
        cursor: 'pointer',
        backgroundColor: '#d1d1d1',
        color: '#808080',
        border: 'none',
        borderRadius: '4px',
        width: '25vw'
      },
      buttonHover_post: {
        backgroundColor: '#666666'
      },
      buttonHover_goback: {
        backgroundColor: '#aaaaaa'
      }
    };

  const {username, authorId} = useContext(UserContext);
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [contentType, setContentType] = useState("text/plain");
  const [imageId, setImageId] = useState(null);
  // TODO: Add private, unlisted settings (public for now)
  // TODO: Add restrictions option (for unlisted)
  const [visibility, setVisibility] = useState("public");

  const jpegDataURL = 'data:image/jpeg;base64,';
  const pngDataURL = 'data:image/png;base64,';

  const handleNewPost = async () => {
    // Send POST request with new post info
    if (title === "" || content === "") {
      alert("Please enter a title and content.");
    
    } else {
    
      try {
        console.log(JSON.stringify({author_id: authorId, content_type: contentType, title: title, content: content, visibility: visibility, image_id: imageId}));
        axios.post(newPostUrl, {
          author_id: authorId,
          content_type: contentType,
          title: title,
          content: content,
          visibility: visibility,
          image_id: imageId
        })
        .then(response => {
          if (response.data === "success") {
            alert("Post successfully posted");
            navigate("/homepage");
          }
        })
        .catch(error => {
          console.error('Error:', error);
        })
      
      } catch (error) {
          console.error('Error:', error);
      }

    }

  };


  // Function to handle the selection of visibility change
  const handleSelectVisibility = (event) => {
    setVisibility(event.target.value);
    //console.log(event.target.value);
  };

  // TODO: Erase content text box when the post type is switching from image to text or markdown
  const handleSelectContentType = (event) => {
    setContentType(event.target.value);
    //console.log(event.target.value);
  }

  const restrictUser = () => { // TODO: Check restrictUser.js 
    alert("This is a WIP. You can restrict authors from this post after you post it. Click on 'Manage my posts' on the stream.");
  }

  // Functions encodeImageToBase64, handleImageChange 
  // are from ManagePosts.js
  const encodeImageToBase64 = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const base64Image = e.target.result; // The base64 encoded image string
      // You can now send this 'base64Image' to your backend or use it in your React component
      // Assuming 'base64Image' is your base64-encoded image string
      const jpegDataURL = 'data:image/jpeg;base64,';
      const pngDataURL = 'data:image/png;base64,';
      
      if (base64Image.startsWith(jpegDataURL)) {
          const strippedBase64Image = base64Image.substring(jpegDataURL.length);              
            setContent(strippedBase64Image);
            setContentType("image/jpeg;base64");
        // Now, 'strippedBase64Image' contains the base64-encoded image data without the prefix
        } else if (base64Image.startsWith(pngDataURL)) {
            const strippedBase64Image = base64Image.substring(pngDataURL.length);
            setContent(strippedBase64Image);
            setContentType("image/png;base64");
        // Now, 'strippedBase64Image' contains the base64-encoded image data without the prefix
        } else {
        // Handle the case where the string doesn't start with either data URL prefix
        console.error("The string does not start with a recognized data URL prefix.");
        alert("Please only upload JPG or PNG files.");
        }

    };
    reader.readAsDataURL(file);
  };

  const handleImageChange = (e) => {        
    const file = e.target.files[0];
    console.log(file);
    if (file) {
      encodeImageToBase64(file);
    } else {
        alert("No file selected.");
    }                  
  };

  const handleGoBack = () => {
    navigate("/homepage");
  }

  return (
    <div style={styles.container}>
      <h2>New Post</h2>

      <p>Visibility</p>
      <form method="dialog">
        <select id="visibility" name="visibility" onChange={handleSelectVisibility}>
          <option value="public">Public</option>
          <option value="private">Private</option>
          <option value="friends-only">Friends-Only</option>
          <option value="unlisted">Unlisted</option>
        </select>
      </form>

      <hr></hr>
      <button style={{width: '20vw'}} onClick={restrictUser}>Set restrictions</button>

      <p>How would you like to format your post?</p>
      <form method="dialog">
        <select id="content-type" name="content-type" onChange={handleSelectContentType}>
          <option value="text/plain">Plain Text</option>
          <option value="text/markdown">Markdown</option>
          <option value="UNKNOWN-IMAGE-TYPE">Image Only</option>
        </select>
      </form>

      <p>Title</p>
      <input   
        style={styles.title}
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <p>Content</p>
      {contentType === 'text/plain' || contentType === 'text/markdown' ? <textarea id="freeform" type="text" placeholder="What's on your mind?" name="freeform" rows="4" cols="50" style={styles.content} value={content} onChange={(e) => setContent(e.target.value)}/> 
      
      : <input type="file" id="img" name="img" accept="image/jpeg, image/png" onChange={handleImageChange}></input>} 

      <button style={styles.button_post} 
      onClick={handleNewPost}
      onMouseOver={(e) => e.currentTarget.style.backgroundColor = styles.buttonHover_post.backgroundColor}
      onMouseOut={(e) => e.currentTarget.style.backgroundColor = styles.button_post.backgroundColor}>
        Post
      </button>
      <button style={styles.button_goback} 
      onClick={handleGoBack}
      onMouseOver={(e) => e.currentTarget.style.backgroundColor = styles.buttonHover_goback.backgroundColor}
      onMouseOut={(e) => e.currentTarget.style.backgroundColor = styles.button_goback.backgroundColor}>
        Cancel
      </button>
    </div>
  );
}
