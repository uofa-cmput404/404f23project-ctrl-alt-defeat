# CMPUT404-project-socialdistribution

CMPUT 404 Project: Social Distribution

Demonstration video:

[![IMAGE ALT TEXT](https://img.youtube.com/vi/sPBAbwMJKl8/0.jpg)](https://www.youtube.com/watch?v=sPBAbwMJKl8)

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

- [CMPUT404-project-socialdistribution](#cmput404-project-socialdistribution)
- [Contributors / Licensing](#contributors--licensing)
- [How to Access](#how-to-access)
- [Stories Completed](#stories-completed)
- [Notes / How to Install and Run Locally](#notes--how-to-install-and-run-locally)
  - [How to flask admin dashboard:](#how-to-flask-admin-dashboard)
  - [Testing HTTP Requests](#testing-http-requests)
  - [Unit Tests](#unit-tests)


# How to Access
If you are a TA marking this assignment, this project is available at the following:
- Credentials are provided in the eClass submission.
- Frontend application: https://cmput404-ctrl-alt-defeat-react-574ccb97869b.herokuapp.com/
- Backend: https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/
- Backend admin dashboard: https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/admin
- Detailed documentation of the endpoints used in the backend are available in the Swagger docs: https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/api/docs/

# Stories Completed
- [x] As an author I want to make public posts.
  - Posts can be made on the application by using the "New Post" button on the homepage once logged in.
- [x] As an author I want to edit public posts.
  - Posts can be edited by using the "Manage Posts" button on the top navbar and editing your respective post.
- [x] As an author, posts I create can link to images.
  - Posts can be linked to images by creating a Markdown post and using the embedded image syntax in Markdown, e.g. `![Meme](https://i.imgur.com/kxWumt8.png)`
- [x] As an author, posts I create can be images.
  - When creating new posts, you must select the "Image Only" option in the Type dropdown menu, and upload an image.
- [x] As a server admin, images can be hosted on my server.
  - When authors create image-only posts (see previous story), the image is stored in the server's database in base64 encoding.
- [x] As an author, posts I create can be private to another author
  - Private posts can be created by selecting the "Private" option in the Visbility dropdown menu when making a new post.
- [x] As an author, posts I create can be private to my friends
  - Friends-only posts can be craeted by selecting the "Friends Only" option in the Visibility dropdown menu when making a new post.
- [x] As an author, I can share other author's public posts
  - Authors can share other author's public posts by selecting the "Share to Public" button at the top-right corner of another author's public post.
- [x] As an author, I can re-share other author's friend posts to my friends
  - Authors can share other author's friend posts with their friends by selecting the "Share to Friends" button at the top-right corner of another author's friend post OR public post.
- [x] As an author, posts I make can be in simple plain text
  - You can select the "Plain Text" formatting option when making a new post.
- [x] As an author, posts I make can be in CommonMark
  - You can select the "Markdown" formatting option when making a new post.
- [x] As an author, I want a consistent identity per server
  - Signing in to our frontend application keeps you logged in to that browser until you logout.
- [x] As a server admin, I want to host multiple authors on my server
- [x] As a server admin, I want to share public images with users on other servers.
  - See the third and fourth stories (related to images).
- [x] As an author, I want to pull in my github activity to my "stream"
  - GitHub activity can be seen on the left side of the homepage/Stream once logged in.
  - Once logged in, you can add/change your GitHub username (not URL) by selecting the "Edit Profile" button at the top navbar, putting your username, and pressing "Link Github".
- [x] As an author, I want to post posts to my "stream"
  - Posts that an author makes are posted on their "Stream"
  - Stream and homepage are the same thing.
- [x] As an author, I want to delete my own public posts.
  - Posts can be deleted by using the "Manage Posts" button on the top navbar and deleting your respective post.
- [x] As an author, I want to befriend local authors
  - By using the "Search Users" textbox in the top navbar, you can type in a username/display name then press "Search".
  - The search results that appear are authors from the local node and remote nodes.
  - Follow/friend requests can be sent to authors by selecting "Follow" beside someone's username.
  - You can unfollow/unfriend authors by selecting "Unfollow" beside someone's username.
- [x] As an author, I want to befriend remote authors
  - See the previous story to befriend remote authors.
- [x] As an author, I want to feel safe about sharing images and posts with my friends -- images shared to friends should only be visible to friends. [public images are public]
  - Posts (plain text, Markdown, image-only) that are set to friends-only are only visible to friends.
- [x] As an author, when someone sends me a friends only-post I want to see the likes.
  - Friends-only posts present the like count.
- [x] As an author, comments on friend posts are private only to me the original author.
- [x] As an author, I want un-befriend local and remote authors
  - See the story related to befriending local and remote authors about how to un-befriend/unfollow.
- [x] As an author, I want to be able to use my web-browser to manage my profile
  - Selecting "Edit Profile" in the top navbar lets you change the username, password, and GitHub username.
- [x] As an author, I want to be able to use my web-browser to manage/author my posts
  - Select "New Post" on the homepage lets you create a new post.
- [x] As a server admin, I want to be able add, modify, and remove authors.
  - From the backend, the admin can access the admin dashboard to add, modify, remove authors.
  - Once logged in, select "Authors" from the navbar to see the authors.
  - Backend admin dashboard: https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/admin
- [x] As a server admin, I want to OPTIONALLY be able allow users to sign up but require my OK to finally be on my server
  - Registration can be done in the frontend application, but must wait for approval from the admin before logging in to the homepage.
  - The server admin can go to the backend admin dashboard, select "Requestors" from the navbar, and you can approve/delete requests to signup.
- [x] As a server admin, I don't want to do heavy setup to get the posts of my author's friends.
- [x] As a server admin, I want a restful interface for most operations
- [x] As an author, other authors cannot modify my public post
- [x] As an author, other authors cannot modify my shared to friends post.
- [x] As an author, I want to comment on posts that I can access
  - Comments can be made by typing in the comment textbox below posts in the homepage.
- [x] As an author, I want to like posts that I can access
  - Liking/unliking posts can be done by pressing the heart on the posts in the homepage.
- [x] As an author, my server will know about my friends
  - Your stream will show you all posts you have access to: public, friend posts, private posts
  - Exception to this is unlisted posts which can only be viewed by post URL or "Manage Posts" for your own unlisted posts.
- [x] As an author, When I befriend someone (they accept my friend request) I follow them, only when the other author befriends me do I count as a real friend -- a bi-directional follow is a true friend.
- [x] As an author, I want to know if I have friend requests.
  - On the left side of the homepage, you can see your friend requests and approve/delete accordingly.
- [x] As an author I should be able to browse the public posts of everyone
  - Your stream will show you all posts you have access to: public, friend posts, private posts
  - Exception to this is unlisted posts which can only be viewed by post URL or "Manage Posts" for your own unlisted posts.
- [x] As a server admin, I want to be able to add nodes to share with
  - Once logged in to the admin dashboard, you can go to "Nodes" in the top navbar, and add a username/password.
  - Nodes making requests to the API need to include the username and password by adding the "Authorization" header and base64 encoding of the `username:password` form.
- [x] As a server admin, I want to be able to remove nodes and stop sharing with them.
  - From the admin dashboard, you can go to "Nodes" in the top navbar to remove the nodes thus stop access to the API
- [x] As a server admin, I can limit nodes connecting to me via authentication.
  - Nodes must use authentication to connect to the API
  - The authentication is acheieved by adding a username and password in the "Nodes" section of the admin dashboard.
- [x] As a server admin, node to node connections can be authenticated with HTTP Basic Auth
  - See previous story.
- [x] As a server admin, I can disable the node to node interfaces for connections that are not authenticated!
  - See previous story.
- [x] As an author, I want to be able to make posts that are unlisted, that are publicly shareable by URI alone (or for embedding images)
  - When making a new post, you can select "Unlisted" in the Visibility dropdown menu.
  - You can access "Manage Posts" from the top navbar to see your unlisted posts and grab the post URL.

# Notes / How to Install and Run Locally
Install:
```
npm install --save react-toastify
npm install --save react-markdown
npm install bootstrap
```

## How to flask admin dashboard:
**Before running:**
```
pip3 install -r requirements.txt
```

**Run inside `server` folder:**
```python3 -m flask run```

**Admin page (local):**
```http://127.0.0.1:5000/api/admin/```

## Testing HTTP Requests
- Editing posts (POST)
  - Use path ```{server_url}/posts/authors/<author_id>/<post_id>/edit/ {json}```
  - The JSON, for now, must include the following:
    - title
    - content_type
    - content
    - img_id (can be 'null')
    - visibility

## Unit Tests
How to run unit tests

1. Install all packages in requirements.txt

2. Initialize a postgres database in your local machine

3. Create a .env file under the /server directory

4. Add these two variables inside them
- DATABASE_URL
    - The URL of the database you've initialized
        - Sample: "http://hueygonzales:password@localhost:5432/test_db"
- URL
    - URL of flask server
        - Sample: "http://localhost:5000"

5. Run unit tests by switching to the /server/unittests/ directory

sample run:
```python3 test_authors.py```
