import axios from 'axios';
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom';

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
                    let url_list = responseData[i]["object"].split("/");
                    let author_index = url_list.findIndex(e => e === "authors");
                    let post_index = url_list.findIndex(e => e === "posts");
                    
                    author_index++;
                    post_index++;

                    responseData[i]["url"] = "http://localhost:3000" + "/authors/" + url_list[author_index] + "/posts/" + url_list[post_index] 
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
                                return <li style={{padding: "10px"}} class="list-group-item"><div style={{display: "flex"}}><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg><a style={{marginLeft: "20px"}} href={e.url}>{e.summary}</a></div></li>
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