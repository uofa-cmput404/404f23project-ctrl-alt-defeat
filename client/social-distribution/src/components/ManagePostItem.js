import axios from 'axios';
import React from 'react'
import Markdown from 'react-markdown';
import './ManagePostItem.css';

const deleteUrl = 'http://127.0.0.1:5000/api/posts'
function ManagePostItem(props) {
    const styles = {
        button: {marginRight: 5},     
        container: {
            padding: 20,
            maxWidth: "50%",
            marginTop: 10
        }   
    }
    function processDelete() {
        if (window.confirm("Are you sure you want to delete this post?")) {
            console.log("Delete");
            console.log(props.item.post_id)

            try {
                // Make the GET request using Axios
                    axios.delete(deleteUrl + "/" + props.item.post_id)
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
        props.setVisibility(props.item.visibility);             
        props.setEditTitle(props.item.title);
        props.setEdittedContentType(props.item.content_type);
    }

    function getRestrictedUsers() {
        const restrictionListUrl = `http://127.0.0.1:5000/api/posts/restricted?post_id=${props.item.post_id}`
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
    <div style={styles.container} class="card">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"/>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        <div>
            <h3>{props.item.title}</h3>
            
            <div><small class="text-muted">{props.item.date_posted}</small></div>
            <div><small class="text-muted">Visibility: {props.item.visibility}</small></div>                                
            {props.item.visibility !== "private" && <a href={'http://127.0.0.1:3000/authors/'+ props.item.author_id + "/posts/" + props.item.post_id}>{'http://127.0.0.1:3000/authors/'+ props.item.author_id + "/posts/" + props.item.post_id}</a>}
        </div>        
        <hr/>        
        
        <div>{get_content_as_elements(props.item.content_type,props.item.content)}</div>
        
        <div style={{marginTop: 10}}>
            <button style={styles.button} onClick={selectEdit} type="button" class="btn btn-primary"><i class="fa fa-edit"></i> Edit</button>
            <button style={styles.button} onClick={processDelete} type="button" class="btn btn-primary"><i class="fa fa-trash"></i> Delete</button>
            <button style={styles.button} onClick={selectVisibility} type="button" class="btn btn-warning"><i class="fa fa-eye"></i> Visibility</button>
            <button style={styles.button} onClick={selectRestriction}type="button" class="btn btn-danger"><i class="fa fa-ban"></i> Restrictions</button>
        </div>
    </div>
  )
}

export default ManagePostItem
