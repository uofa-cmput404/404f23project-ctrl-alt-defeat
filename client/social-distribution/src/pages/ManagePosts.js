import React, { useContext, useEffect, useState } from 'react'
import ManagePostItem from '../components/ManagePostItem'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import SetVisibilityDialog from '../components/SetVisibilityDialog';
import RestrictedUser from '../components/RestrictedUser';
import { UserContext } from '../App';

const managePostsUrl = 'http://127.0.0.1:5000/api/posts/manage'
const updateVisibilityUrl = 'http://127.0.0.1:5000/api/posts/visibility'
const restrictUrl = 'http://127.0.0.1:5000/api/posts/restrict'
const restrictionListUrl = 'http://127.0.0.1:5000/api/posts/restricted/'
const editUrl = 'http://127.0.0.1:5000/api/authors/'

function ManagePosts() {
    const styles = {
        container: {
            margin: 20
        },
        dialog: {
            position: 'fixed',
            zIndex: 2
        },
        text: {
            width: "100%",
            padding: "12px 20px",
            margin: "8px 0",
            display: "block",
            border: "1px solid #ccc",
            borderRadius: "4px",
            boxSizing: "border-box",
          },
          
          red: {
            backgroundColor: "#04AA6D",
          },

          green: {
            backgroundColor: "#eb4034",
          },

          submit: {
            width: "100%",
            backgroundColor: "#04AA6D",
            color: "white",
            padding: "14px 20px",
            margin: "8px 0",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer"
          },
          
          cancel: {
            width: "100%",
            backgroundColor: "#eb4034",
            color: "white",
            padding: "14px 20px",
            margin: "8px 0",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer"
          }

    }

    const {username, authorId} = useContext(UserContext);    
    const navigate = useNavigate();

    const [postSelected, setPostSelected] = useState(null);
    const [postsLists, setPostsLists] = useState([]);
    const [openVisibilityDialog, setOpenVisibilityDialog] = useState(false);
    const [openRestrictionsDialog, setRestrictionsDialog] = useState(false);
    const [defaultVisibility, setDefaultVisibility] = useState("");
    const [visibility, setVisibility] = useState("private");
    const [restrictedUsers, setRestrictedUsers] = useState([1,2,3,4,5]);
    const [restrictedUsername, setRestrictedUsername] = useState("");   
    const [openEditDialog, setOpenEditDialog] = useState(false);  
    const [editContent, setEditContent] = useState(""); 
    const [editTitle, setEditTitle] = useState(""); 
    const [edittedContentType, setEdittedContentType] = useState("");
    const [fetchDone, setFetchDone] = useState(false);

    const editRequest = async () => {
        // console.log(authorId);
        // console.log(postSelected);
        // console.log(editContent);
        // console.log(editTitle);
        // console.log(edittedContentType);        
        console.log({
            "content_type": edittedContentType,
            "content": editContent,
            "image_id": null,
            "visibility": visibility,
            "post_id": postSelected,
            "title": editTitle
        })
        axios.post(editUrl + authorId + "/" + postSelected + "/edit/", {
            "content_type": edittedContentType,
            "content": editContent,
            "image_id": null,
            "visibility": visibility,
            "post_id": postSelected,
            "title": editTitle
        }).then((response) => {
            if (response.data === "Post Updated Successfully") {
                
                setPostsLists(postsLists.map(item => {
                    if (item.post_id === postSelected) {
                      return { ...item, content: editContent, title: editTitle }; // Create a new object with the updated value
                    }
                    return item; // Return the original object for other items
                }))
                alert("The post was successfully edited.");
            } else {
                alert(response.data)
            }
        }).catch(error => {
            // Handle any errors that occur during the request
            console.error('Error:', error);
                alert('Error:', error);
        })

        setOpenEditDialog(false);


    }
    const restrictUser = async () => {
        if (restrictedUsername !== username) {            
            try {
                console.log(restrictedUsername);
                console.log(postSelected);
                // Update post request using Axios
                axios.post(restrictUrl, {
                    post_id: postSelected,
                    username: restrictedUsername
                })
                .then(response => {
                // Handle the successful response here            
                    if (response.data === "success") {
                        alert("User restricted successfully")
                    } else if (response.data === "duplicate") {
                        alert("You already added this user")
                    } else if (response.data === "not_exists") {
                        alert("This user does not exist");
                    }
                    setRestrictedUsername("") // Empty out field
                })
                .catch(error => {
                // Handle any errors that occur during the request
                console.error('Error:', error);
                    alert('Error:', error);
                })
            } catch (error) {
                console.error('Error:', error);
            }
        } else {
            alert("You can't restrict yourself")
        }
        setRestrictionsDialog(false);    
        
    }    

    const updateData = async () => {
        try {
            console.log(postSelected);
            console.log(visibility);
            // Update post request using Axios
            axios.post(updateVisibilityUrl, {
                post_id: postSelected,
                visibility: visibility
            })
            .then(response => {
            // Handle the successful response here            
                setPostsLists(postsLists.map(item => {
                    if (item.post_id === postSelected) {
                      return { ...item, visibility: visibility }; // Create a new object with the updated value
                    }
                    return item; // Return the original object for other items
                  }))
            })
            .catch(error => {
            // Handle any errors that occur during the request
            console.error('Error:', error);
            })
        } catch (error) {
            console.error('Error:', error);
        }
        
        setOpenVisibilityDialog(false);
    }

    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.get(managePostsUrl + `?author_id=${authorId}`)
                .then(response => {
                // Handle the successful response here
                console.log('Response data:', response.data);
                    setPostsLists(response.data)                    
                })
                .catch(error => {
                // Handle any errors that occur during the request
                console.error('Error:', error);
                })
                .finally(() => {
                    setFetchDone(true);
                })
          } catch (error) {
            console.error('Error:', error);
          }
    }
    useEffect(() => {
        fetchData();
    }, [])

    // Function to handle the selection change
    const handleSelectChange = (event) => {
        setVisibility(event.target.value);
        // console.log(event.target.value);
    };

    const handleUserRestrictedTextChange = (event) => {
        setRestrictedUsername(event.target.value);        
    };

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
                setEditContent(strippedBase64Image);
            // Now, 'strippedBase64Image' contains the base64-encoded image data without the prefix
            } else if (base64Image.startsWith(pngDataURL)) {
                const strippedBase64Image = base64Image.substring(pngDataURL.length);
                setEditContent(strippedBase64Image);
            // Now, 'strippedBase64Image' contains the base64-encoded image data without the prefix
            } else {
            // Handle the case where the string doesn't start with either data URL prefix
            console.error("The string does not start with a recognized data URL prefix.");
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

  return (
    <div style={styles.container}>
        <h1>My posts:</h1>
            <dialog  open={openVisibilityDialog} style={styles.dialog}>
            <h1>Change visibility</h1>
            <form method="dialog">
                <select id="visibility" name="visibility" onChange={handleSelectChange}>
                    <option value="private">Private</option>
                    <option value="PUBLIC">Public</option>   
                    <option value="unlisted">Unlisted</option>                
                    <option value="FRIENDS">Friends-Only</option>                    
                </select>
                {/* <p>Set this private from:</p> */}
                {/* <input style={styles.text} type="text" id="fname" name="fname"></input> */}
                <button style={styles.submit} onClick={updateData}>OK</button>
                <button style={styles.cancel} onClick={() => setOpenVisibilityDialog(false)}>Cancel</button>
            </form>
            </dialog>
            <dialog open={openEditDialog} style={styles.dialog}>
            <h1>Edit Post</h1>
            <form method="dialog">
                <label for="freeform">Change title</label>                
                <br/>
                <input  value={editTitle} onChange={(e) => setEditTitle(e.target.value)}></input>                
                <br/>
                <label for="freeform">Edit your post:</label>                
                <br/>
                                
                {edittedContentType === 'text/plain' || edittedContentType === 'text/markdown' ? <textarea id="freeform" name="freeform" rows="4" cols="50" value={editContent} onChange={(e) => setEditContent(e.target.value)}/> : <input type="file" id="img" name="img" accept="image/*" onChange={handleImageChange}></input>}                                
                {/* <p>Set this private from:</p> */}
                {/* <input style={styles.text} type="text" id="fname" name="fname"></input> */}
                <button style={styles.submit} onClick={editRequest}>OK</button>
                <button style={styles.cancel} onClick={() => setOpenEditDialog(false)}>Cancel</button>
            </form>
            </dialog>
            <dialog open={openRestrictionsDialog} style={styles.dialog}>
            <h1>Restrictions</h1>
            <p><i>You can restrict specific authors from seeing this post.</i></p>
            <form method="dialog">
                Restricted authors:
                {
                    restrictedUsers.length ? restrictedUsers.map((item) => {return <RestrictedUser username={item.username} 
                                                                                                   setRestrictedUsers={setRestrictedUsers}
                                                                                                   restrictedUsers={restrictedUsers}
                                                                                                   postSelected={postSelected}/>}) : null
                }

                <p>Add user to restriction:</p>
                <input style={styles.text} type="text" id="fname" name="fname" onChange={handleUserRestrictedTextChange}></input>
                <button style={styles.submit} onClick={restrictUser}>Add</button>                                
                <button style={styles.cancel} onClick={() => setRestrictionsDialog(false)}>Close</button>
            </form>
            </dialog>
        <div>
            {
                !fetchDone ?
                <div class="spinner-border" role="status">
                    {/* <span class="sr-only">Loading...</span> */}
                </div> :
                (postsLists.length ? 
                postsLists.map((item, index) => (
                    <ManagePostItem postLists={postsLists} 
                                    setPostsLists={setPostsLists} 
                                    item={item} index={index}
                                    openVisibilityDialog={openVisibilityDialog}
                                    setOpenVisibilityDialog={setOpenVisibilityDialog} 
                                    setRestrictionsDialog={setRestrictionsDialog}                                   
                                    setPostSelected={setPostSelected}
                                    setRestrictedUsers={setRestrictedUsers}  
                                    setOpenEditDialog={setOpenEditDialog}   
                                    setEditContent={setEditContent}  
                                    setEditTitle={setEditTitle}        
                                    setVisibility={setVisibility}             
                                    setEdittedContentType={setEdittedContentType}
                                    />
                )) : <div>You have no posts</div>)
            }
        </div>

    </div>
  )
}

export default ManagePosts