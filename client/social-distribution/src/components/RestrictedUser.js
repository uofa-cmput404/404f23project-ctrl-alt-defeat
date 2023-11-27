import axios from 'axios';
import React from 'react'

const unrestrictUrl = process.env.API_HOSTNAME + '/posts/unrestrict/'
function RestrictedUser(props) {  

  function removeRestriction(event) {
        event.preventDefault();
        alert("User removed from restriction")
        props.setRestrictedUsers(props.restrictedUsers.filter(e => e.username !== props.username
        ))

        console.log(props.username);
        console.log(props.postSelected);

        axios.delete(process.env.API_HOSTNAME + `/posts/unrestrict/${props.postSelected}/${props.username}`, (response) => {
            if (response.data === "success") {
              alert("User restricted successfully")
            }
            else {
              alert("Something went wrong")
            }
        })
    }

  return (
    <li>{props.username}
        <button onClick ={(event) => {removeRestriction(event)}}>Remove</button>
    </li>
  )
}

export default RestrictedUser