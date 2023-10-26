CMPUT404-project-socialdistribution
===================================

CMPUT 404 Project: Social Distribution

[Project requirements](https://github.com/uofa-cmput404/project-socialdistribution/blob/master/project.org) 

Contributors / Licensing
========================

Authors:
    
* Huey Gonzales
* Daniel Guo
* Mark Maligalig
* Andrew Rosario
* Jingtong Yang

Generally everything is LICENSE'D under the Apache License 2.0.

Install:
npm install --save react-toastify
npm install --save react-markdown

**How to flask admin dashboard:**
- **before running:**\
      pip3 install flask\
      pip3 install flask-admin\
      pip3 install flask_sqlalchemy
- **Run inside server:**\
      python3 -m flask run
- **Admin page:**\
      http://127.0.0.1:5000/admin/ 

**Testing HTTP requests**
Use curl or Postman.
- Editing posts (POST)
  - Use path ```{server_url}/posts/<post_id>/authors/<author_id> {json}```
  - The JSON, for now, must include the following:
    - title
    - content_type
    - content
    - img_id (can be 'null')
    - visibility
  - Images, at the moment, are not changed. So it doesn't work.
  - Exceptions thrown:
    - 400 if the data sent wasn't a JSON.
    - 404 if the post doesn't even exist.
    - KeyError if the JSON is missing keys.
    - DatabaseError if something goes wrong with the database commit.
