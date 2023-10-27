import axios from 'axios';
import React from 'react'
import Markdown from 'react-markdown';

const deleteUrl = 'http://127.0.0.1:5000/posts/delete'
function ManagePostItem(props) {
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

    function selectVisibility() {
        props.setOpenVisibilityDialog(true);
        props.setPostSelected(props.item.post_id);
        // console.log(props.item.post_id);
    }

    function selectRestriction() {
        props.setRestrictionsDialog(true);
        props.setPostSelected(props.item.post_id);
        getRestrictedUsers();
    }

    function selectEdit() {
        props.setOpenEditDialog(true);    
        props.setEditContent(props.item.content);
        props.setPostSelected(props.item.post_id);
        props.setEditTitle(props.item.title);
        props.setEdittedContentType(props.item.content_type);
    }

    function getRestrictedUsers() {
        const restrictionListUrl = `http://127.0.0.1:5000/posts/restricted?post_id=${props.item.post_id}`
        console.log(restrictionListUrl)
        axios.get(restrictionListUrl).then((response) => {
            console.log(response.data)
            props.setRestrictedUsers(response.data)
        })
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
    

    return (
    <li key={props.key}>
        <div>
            <h3>{props.item.title}</h3>
        </div>
        <button onClick={selectEdit}>Edit</button>
        <button onClick={processDelete}>Delete this post</button>
        <button onClick={selectVisibility}>Change visibility</button>
        <button onClick={selectRestriction}>Restrictions</button>
        <div>{props.item.date_posted}</div>
        <div>{get_content_as_elements(props.item.content_type,props.item.content)}</div>
        <div>Visibility: {props.item.visibility}</div>
    </li>
  )
}

export default ManagePostItem