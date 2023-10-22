import axios from 'axios';
import React from 'react'

const deleteUrl = 'http://127.0.0.1:5000/posts/delete'
function ManagePostItem(props) {
    const deleteData = async () => {
        try {
            // Make the GET request using Axios
                axios.post(deleteUrl, {
                    post_id: props.item.post_id
                })
                .catch(error => {
                // Handle any errors that occur during the request
                console.error('Error:', error);
                });
          } catch (error) {
            console.error('Error:', error);
          }
    }

    function processDelete() {
        if (window.confirm("Are you sure you want to delete this post?")) {
            console.log("Delete");
            console.log(props.item.post_id)

            try {
                // Make the GET request using Axios
                    axios.post(deleteUrl, {
                        post_id: props.item.post_id
                    })
                    .then(response => {
                        props.setPostsLists(oldValues => {                
                            return oldValues.filter(item => item.post_id !== props.item.post_id);
                        })        
                    })
                    .catch(error => {
                    // Handle any errors that occur during the request
                    console.error('Error:', error);
                    });
              } catch (error) {
                console.error('Error:', error);
            
            }
        }
    }

    return (
    <li key={props.key}>
        <div>
            <h3>{props.item.title}</h3>
        </div>
        <button onClick={processDelete}>Delete this post</button>
        <div>Posted by: {props.item.author_id}</div>
        <div>{props.item.date_posted}</div>
        <div>{props.item.content}</div>
    </li>
  )
}

export default ManagePostItem