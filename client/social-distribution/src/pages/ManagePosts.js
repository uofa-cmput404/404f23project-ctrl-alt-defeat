import React, { useEffect, useState } from 'react'
import ManagePostItem from '../components/ManagePostItem'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import SetVisibilityDialog from '../components/SetVisibilityDialog';

const managePostsUrl = 'http://127.0.0.1:5000/posts/manage'
const updateVisibilityUrl = 'http://127.0.0.1:5000/posts/visibility'
const restrictUrl = 'http://127.0.0.1:5000/posts/restrict'

function ManagePosts() {
    const styles = {
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
    const username = "philiponions" // temporary username
    const navigate = useNavigate();

    const [postSelected, setPostSelected] = useState(null);
    const [postsLists, setPostsLists] = useState([]);
    const [openVisibilityDialog, setOpenVisibilityDialog] = useState(false);
    const [openRestrictionsDialog, setRestrictionsDialog] = useState(false);
    const [defaultVisibility, setDefaultVisibility] = useState("");
    const [visibility, setVisibility] = useState("private");
    const [restrictedUsers, setRestrictedUsers] = useState([])
    const [restrictedUsername, setRestrictedUsername] = useState("")

    const restrictUserFetch = async () => {
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
                }
                setRestrictedUsername("") // Empty out field
            })
            .catch(error => {
            // Handle any errors that occur during the request
            console.error('Error:', error);
            })
        } catch (error) {
            console.error('Error:', error);
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
                axios.post(managePostsUrl, {
                    author_id: 1
                })
                .then(response => {
                // Handle the successful response here
                console.log('Response data:', response.data);
                    setPostsLists(response.data)
                })
                .catch(error => {
                // Handle any errors that occur during the request
                console.error('Error:', error);
                });
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

    function addRestrictedUser() {
        setRestrictedUsers([...restrictedUsers, restrictedUsername])
    }

  return (
    <div>
        <h1>My posts:</h1>
        <dialog open={openVisibilityDialog} style={styles.dialog}>
            <h1>Change visibility</h1>
            <form method="dialog">
                <select id="visibility" name="visibility" onChange={handleSelectChange}>
                    <option value="private">Private</option>
                    <option value="public">Public</option>                
                    <option value="unlisted">Unlisted</option>                
                </select>
                {/* <p>Set this private from:</p> */}
                {/* <input style={styles.text} type="text" id="fname" name="fname"></input> */}
                <button style={styles.submit} onClick={updateData}>OK</button>
                <button style={styles.cancel} onClick={() => setOpenVisibilityDialog(false)}>Cancel</button>
            </form>
            </dialog>
            <dialog open={openRestrictionsDialog} style={styles.dialog}>
            <h1>Restrictions</h1>
            <form method="dialog">
                <button>Check who this is restricted from</button>
                <p>Add user to restriction:</p>
                <input style={styles.text} type="text" id="fname" name="fname" onChange={handleUserRestrictedTextChange}></input>
                <button style={styles.submit} onClick={restrictUserFetch}>Add</button>                                
                <button style={styles.cancel} onClick={() => setRestrictionsDialog(false)}>Close</button>
            </form>
            </dialog>
        <ul>
            {
                postsLists.length ? 
                postsLists.map((item, index) => (
                    <ManagePostItem postLists={postsLists} 
                                    setPostsLists={setPostsLists} 
                                    item={item} index={index}
                                    openVisibilityDialog={openVisibilityDialog}
                                    setOpenVisibilityDialog={setOpenVisibilityDialog} 
                                    setRestrictionsDialog={setRestrictionsDialog}                                   
                                    setPostSelected={setPostSelected}/>
                )) : <div>You have no posts</div>
            }
        </ul>

    </div>
  )
}

export default ManagePosts