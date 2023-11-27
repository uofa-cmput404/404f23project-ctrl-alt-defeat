import axios from 'axios';
import React from 'react'

const unrestrictUrl = process.env.API_HOSTNAME + '/api/posts/unrestrict/'
function RestrictedUser(props) {  

  function removeRestriction(event) {
        event.preventDefault();
        alert("User removed from restriction")
        props.setRestrictedUsers(props.restrictedUsers.filter(e => e.username !== props.username
        ))

        console.log(props.username);
        console.log(props.postSelected);

        axios.delete(process.env.API_HOSTNAME + `/api/posts/unrestrict/${props.postSelected}/${props.username}`, {headers:{'Authorization' : 'Basic ' + process.env.USERPASSBASE64}})
            .then((response) => {
            if (response.data === "success") {
              alert("User restricted successfully")
            }
            else {
              alert("Something went wrong")
            }
        }).catch(error => {
          console.error('Error:', error);
          });
    }

  return (
    <li>{props.username}
        <button onClick ={(event) => {removeRestriction(event)}}>Remove</button>
    </li>
  )
}

export default RestrictedUser