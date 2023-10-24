import axios from 'axios';
import React from 'react'

const unrestrictUrl = 'http://127.0.0.1:5000/posts/unrestrict/'
function RestrictedUser(props) {  

  function removeRestriction(event) {
        event.preventDefault();
        alert("User removed from restriction")
        props.setRestrictedUsers(props.restrictedUsers.filter(e => e.username !== props.username
        ))

        console.log(props.username);
        console.log(props.postSelected);

        axios.delete(`http://127.0.0.1:5000/posts/unrestrict/${props.postSelected}/${props.username}`, (response) => {
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