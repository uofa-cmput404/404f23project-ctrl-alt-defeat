import axios from 'axios';
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom';
import LikeSymbol from '../components/LikeSymbol';
import CommentIcon from '../components/CommentIcon';

const inboxUrl = 'http://127.0.0.1:5000/api/';

function Inbox() {
    let { post_id, author_id } = useParams();
    const [fetchDone, setFetchDone] = useState(false);
    const [inboxItems, setInboxItems] = useState([])

    const styles = {
        card: {
            width: "50%",
            
        },
        container: {
            justifyContent: "center",
            width: "100%",
            marginTop: "20px"
        },
        subContainer: {
            display: "flex",
            justifyContent: "center"
        }
    }
    
    const fetchData = async () => {
        try {
            // Make the GET request using Axios
                axios.get(inboxUrl + "authors/" + author_id + "/inbox")
                .then(response => {
                // Handle the successful response here
                let responseData = response.data.items
                for (let i = 0; i < responseData.length; i++) {

                    responseData[i]["url"] = "http://localhost:3000" + "/authors/" + author_id + "/posts/" + responseData[i]["post_id"] 
                }
                console.log(response.data.items);
                setInboxItems(response.data.items);
                // setPostSelected(response.data);                                   
                // setUsername(response.data.author.displayName);
                })
                .catch(error => {
                // Handle any errors that occur during the request
                // console.error('Error:', error);
                // setPostSelected("invalid"); 
                }).finally(() => {
                    setFetchDone(true);
                });;
          } catch (error) {
            console.error('Error:', error);
          }
    }
    useEffect(() => {
        fetchData();        
    }, []);

  return (
    <div style={styles.container}>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"/>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        <center><h1>Inbox</h1></center>
        <div style={styles.subContainer}>
            {
                inboxItems.length > 0 ?
                <div class="card" style={styles.card}>
                    <ul class="list-group">
                        {
                            inboxItems.map((e) => {                        
                                return <li style={{padding: "10px"}} class="list-group-item">
                                    <div style={{display: "flex"}}>
                                        {(e.type === "Like" && <><LikeSymbol/><a style={{marginLeft: "20px"}} href={e.url}>{e.summary}</a></>)}                                        
                                        {(e.type === "comment" && <div><CommentIcon/><a style={{marginLeft: "20px"}} href={e.url}>{e.summary}</a> 
                                                    <div class="card" style={{marginTop: "10px", padding: "20px"}}>"{e.comment}"</div></div>)}   
                                    </div></li>
                            })
                        }                
                    </ul>
                    </div>
                    
                    : <div>Your inbox is empty!</div>
            }

        </div>
    </div>
  )
}

export default Inbox