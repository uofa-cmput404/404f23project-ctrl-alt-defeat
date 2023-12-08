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

INSERT INTO public.authors (
author_id, username, github, password) VALUES (
'f2d79922-9571-11ee-b9d1-0242ac120002'::text, 'philiponions'::text, 'philiponions'::text, 'password'::text)
 returning author_id;

INSERT INTO public.authors (
author_id, username, password) VALUES (
'0ca265e4-9572-11ee-b9d1-0242ac120002'::text, 'maven'::text, 'password'::text)
 returning author_id;

INSERT INTO public.authors (
author_id, username, github, password) VALUES (
'2179aff4-9572-11ee-b9d1-0242ac120002'::text, 'mark'::text, 'mark8m'::text, 'password'::text)
 returning author_id;

 INSERT INTO public.authors (
author_id, username, password) VALUES (
'0d3aa4cb-b17d-4090-923f-8ac14185fae6'::text, 'coolguy456'::text, '$2b$12$Z/Tdtse3smqlTWPKv5KHfOt36SVZMPnGexmvOifTtVD5xXU06Ku7.'::text)
 returning author_id;

 INSERT INTO public.posts (
post_id, author_id, title, content_type, content, visibility) VALUES (
'77f8c164-957a-11ee-b9d1-0242ac120002'::text, '0ca265e4-9572-11ee-b9d1-0242ac120002'::text, 'Sentence'::text, 'text/plain'::text, 'The quick brown fox jumps over the lazy dog'::text, 'PUBLIC'::text)
 returning post_id;

 INSERT INTO public.posts (
post_id, author_id, title, content_type, content, visibility) VALUES (
'5f3be750-957a-11ee-b9d1-0242ac120002'::text, '0ca265e4-9572-11ee-b9d1-0242ac120002'::text, 'New post'::text, 'text/plain'::text, 'hello world'::text, 'PUBLIC'::text)
 returning post_id;

 INSERT INTO public.likes (
like_id, like_author_id, post_id, time_liked) VALUES (
'b77a8afc-957a-11ee-b9d1-0242ac120002'::text, '0ca265e4-9572-11ee-b9d1-0242ac120002'::text, '77f8c164-957a-11ee-b9d1-0242ac120002'::text, '2023-12-07 20:33:42.197728'::timestamp without time zone)
 returning like_id;

 INSERT INTO public.likes (
like_id, like_author_id, post_id, time_liked) VALUES (
'b96fdbf0-957a-11ee-b9d1-0242ac120002'::text, '0ca265e4-9572-11ee-b9d1-0242ac120002'::text, '5f3be750-957a-11ee-b9d1-0242ac120002'::text, '2023-12-07 20:33:42.197728'::timestamp without time zone)
 returning like_id;

INSERT INTO public.inbox_items (
inbox_item_id, sender_id, sender_display_name, sender_host, recipient_id, object_id, type) VALUES (
'ad4f22ac-9581-11ee-b9d1-0242ac120002'::text, '0d3aa4cb-b17d-4090-923f-8ac14185fae6'::text, 'coolguy456'::text, 'http://localhost:5000'::text, '0ca265e4-9572-11ee-b9d1-0242ac120002'::text, 'ecc5476a-957f-11ee-b9d1-0242ac120002'::text, 'comment'::text);

 INSERT INTO public.comments (
comment_id, comment_author_id, post_id, author_id, comment_text, status, date_commented) VALUES (
'ecc5476a-957f-11ee-b9d1-0242ac120002'::text, '0d3aa4cb-b17d-4090-923f-8ac14185fae6'::text, '5f3be750-957a-11ee-b9d1-0242ac120002'::text, '0ca265e4-9572-11ee-b9d1-0242ac120002'::text, 'Sensational'::text, 'private'::text, '2023-12-07 20:33:42.197728'::timestamp)
 returning comment_id;