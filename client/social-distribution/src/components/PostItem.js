import React from 'react'

function PostItem(props) {
  return (
    <li key={props.key}>
        <h3>{props.item.title}</h3>
        <div>Posted by: {props.item.author_id}</div>
        <div>{props.item.date_posted}</div>
        <div>{props.item.content}</div>
    </li>
  )
}

export default PostItem