import React, {useState, useRef} from 'react'
import Markdown from 'react-markdown'
import rehypeRaw from "rehype-raw";


 const MarkdownEditor = ({content,onChange}) => {
      const [markdown, setMarkdown] = useState("Write whatever.");
      const [isFetching,setIsFetching] = useState(false);
      const textAreaRef = useRef(null)
      const handleChange = (e) => {
          onChange(e.target.value);
      }


      const handleImageServerButtonClick = async() => {
          try {
              setIsFetching(true);

              let author_id = prompt("Enter the author_id (This field is optional):");
              const post_id = prompt("Enter the post_id:");

              const textArea = textAreaRef.current;
              const start = textArea.selectionStart;
              const end = textArea.selectionEnd;

              if (author_id === "") {
                  author_id = "NONE"
              }

              const response = await fetch(`http://localhost:5000/authors/${author_id}/posts/${post_id}/image`);
              if (response.ok != true) {
                  const errorMessage = await response.text();
                  throw new Error(errorMessage)
              }

              const imageURL = await response.text()
              console.log(imageURL)
                // <a href="http://localhost:5000/authors/${author_id}/posts/${post_id}/image">
              //const imageToEmbed = `<img src="${imageURL}">`
              //const imageToEmbed = ''
              const imageToEmbed = `![${post_id}](${imageURL})`
              const newContent = content.substring(0, start) + imageToEmbed + content.substring(end);
              onChange(newContent)

              textArea.setSelectionRange(start, end + imageToEmbed.length);
              textArea.focus();

          } catch (e){
              console.error('Error: ', e.message);
          } finally {
              setIsFetching(false);
          }
      }

      const handleInsertLinkButtonClick = () => {
          const textArea = textAreaRef.current;
          const start = textArea.selectionStart;
          const end = textArea.selectionEnd;

          let selected = content.substring(start,end);

          const linkURL = prompt("Enter URL to embed:")
          if (linkURL){
              if (!selected){
                  selected = linkURL
              }
              //const linkToEmbed = `[${selected}](http://${linkURL})`;

              const linkToEmbed = `<a href="http://${linkURL}" target="_blank">${selected}</a>`
              const newContent = content.substring(0, start) + linkToEmbed + content.substring(end);
              onChange(newContent)

              textArea.setSelectionRange(start, end + linkToEmbed.length);
              textArea.focus();
          }
      }



  return (
      <div>
          <div>
              <button onClick={handleImageServerButtonClick} disabled={isFetching}>
                  {isFetching === true ? 'Getting Image...' : 'Embed User Image'}
              </button>
              <button onClick={handleInsertLinkButtonClick}>
                  {'Add Hyperlink'}
              </button>
          </div>
          <textarea value={content} onChange={handleChange} ref = {textAreaRef} style ={{width :'300px',height:'300px'}}/>
          <div>
              <p>Content Preview</p>
              <Markdown rehypePlugins={[rehypeRaw]} urlTransform={(value:string) => value}>{content}</Markdown>
          </div>
      </div>
  );
};

export default MarkdownEditor;