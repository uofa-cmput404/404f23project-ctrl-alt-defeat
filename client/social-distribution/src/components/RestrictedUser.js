import React from 'react'

function RestrictedUser(props) {
    function removeRestriction(event) {
        event.preventDefault();
    }

  return (
    <li>{props.username}
        <button onClick ={(event) => {removeRestriction(event)}}>Remove</button>
    </li>
  )
}

export default RestrictedUser