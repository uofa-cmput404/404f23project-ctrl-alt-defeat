import React from 'react'
import Markdown from "react-markdown";


function get_content_as_elements(content_type, content){
    if (content_type === "text/plain"){
        return(<p>{content}</p>);
    }
    else if (content_type === "text/markdown"){
        return(<Markdown>{content}</Markdown>);
    }
    else if (content_type === "image/png;base64" || content_type === "image/jpeg;base64")
    {
        //var image = new Image();
        //let decodedString = atob(content);
        let tag = 'data:' + content_type + "," + content;
        return (<img src={tag}/>)
    }
}
function PostItem(props) {
  return (
    <li key={props.key}>
        <h3>{props.item.title}</h3>
        <div>Posted by: {props.item.author_id}</div>
        <div>{props.item.date_posted}</div>
        <div>{get_content_as_elements(props.item.content_type,props.item.content)}</div>
    </li>
  )
}

export default PostItem