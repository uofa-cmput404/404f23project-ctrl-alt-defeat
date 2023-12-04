-- Drop tables if they exist
DROP TABLE IF EXISTS post_restrictions;
DROP TABLE IF EXISTS shares;
DROP TABLE IF EXISTS comment_likes;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS follow_requests;
DROP TABLE IF EXISTS friends;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS requestors;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS nodes;
DROP TABLE IF EXISTS authors CASCADE;
DROP TABLE IF EXISTS inbox_items;

CREATE TABLE authors (
    author_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    github TEXT,
    password TEXT NOT NULL
);

CREATE TABLE requestors (
    requestor_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE admins (
    admin_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

-- Create tables
CREATE TABLE posts (
    post_id TEXT PRIMARY KEY,
    author_id TEXT NOT NULL,
    date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content_type TEXT NOT NULL DEFAULT 'text/plain',
    content TEXT NOT NULL,
    image_id TEXT,
    visibility TEXT NOT NULL DEFAULT 'PUBLIC',
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE friends (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    author_followee TEXT NOT NULL,
    author_following TEXT NOT NULL,
    host TEXT NOT NULL
    --FOREIGN KEY (author_followee) REFERENCES authors(author_id) ON DELETE CASCADE,
    --FOREIGN KEY (author_following) REFERENCES authors(author_id) ON DELETE CASCADE
);

CREATE TABLE follow_requests (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    author_send TEXT NOT NULL,
    author_receive TEXT NOT NULL,    
    host TEXT DEFAULT 'local' NOT NULL,
    FOREIGN KEY (author_receive) REFERENCES authors(author_id)
);

CREATE TABLE likes (
    like_id TEXT PRIMARY KEY,
    like_author_id TEXT NOT NULL,
    post_id TEXT NOT NULL,
    time_liked TIMESTAMP NOT NULL,    
    FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
);

CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    comment_author_id TEXT NOT NULL, --TEXT
    post_id TEXT NOT NULL, --TEXT
    author_id TEXT NOT NULL, --TEXT
    comment_text TEXT NOT NULL, --TEXT
    status TEXT NOT NULL,
    date_commented TIMESTAMP NOT NULL,    
    FOREIGN KEY (post_id) REFERENCES posts(post_id)  ON DELETE CASCADE
);

CREATE TABLE comment_likes (
    comment_like_id TEXT PRIMARY KEY, --TEXT
    like_comment_author_id TEXT NOT NULL, --TEXT
    comment_id TEXT NOT NULL,
    time_liked TIMESTAMP NOT NULL,
    FOREIGN KEY (like_comment_author_id) REFERENCES authors(author_id),
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id) ON DELETE CASCADE
);


CREATE TABLE shares(
    post_id TEXT PRIMARY KEY,
    share_author_id TEXT NOT NULL,
    date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (share_author_id) REFERENCES authors(author_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE post_restrictions (
    post_id TEXT,
    restricted_author_id TEXT,
    FOREIGN KEY (post_id) REFERENCES posts (post_id),
    FOREIGN KEY (restricted_author_id) REFERENCES authors (author_id),
    UNIQUE (post_id, restricted_author_id)
);

CREATE TABLE nodes (
    node_id INTEGER PRIMARY KEY,
    node_name TEXT,
    username TEXT NOT NULL,
    password TEXT NOT NULL   
);

-- inbox_item_id = unique identifier within inbox_items
-- object_id = posts: post_id, follow request: follow_request_id*
--             post/comment likes: like_id*, comments: comment_id
--             *these ids only exist in our database
CREATE TABLE inbox_items (
    inbox_item_id TEXT NOT NULL PRIMARY KEY,
    sender_id TEXT NOT NULL,
    sender_display_name TEXT NOT NULL,
    sender_host TEXT NOT NULL,
    recipient_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    type TEXT NOT NULL,
    date_received TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);