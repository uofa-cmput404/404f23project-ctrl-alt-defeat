import React from 'react'

function SetVisibilityDialog() {
  return (
    <dialog open>
    <p>Change visibility</p>
    <form method="text"></form>
    <form method="dialog">
        <button>OK</button>
    </form>
    </dialog>
  )
}

export default SetVisibilityDialog