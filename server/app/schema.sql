-- Drop tables if they exist
DROP TABLE IF EXISTS sc.post_restrictions;
DROP TABLE IF EXISTS sc.shares;
DROP TABLE IF EXISTS sc.comments;
DROP TABLE IF EXISTS sc.likes;
DROP TABLE IF EXISTS sc.follow_requests;
DROP TABLE IF EXISTS sc.friends;
DROP TABLE IF EXISTS sc.image_post;
DROP TABLE IF EXISTS sc.admins;
DROP TABLE IF EXISTS sc.requestors;
DROP TABLE IF EXISTS sc.authors;
DROP TABLE IF EXISTS sc.posts;


CREATE TABLE sc.authors (
    author_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    github TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE sc.requestors (
    requestor_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE sc.admins (
    admin_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);


CREATE TABLE sc.image_post (
    img_id TEXT PRIMARY KEY,
    author_id TEXT NOT NULL,
    img_url TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT 'public',
    date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (author_id) REFERENCES sc.authors(author_id) ON DELETE CASCADE
);

-- Create tables
CREATE TABLE sc.posts (
    post_id TEXT PRIMARY KEY,
    author_id TEXT NOT NULL,
    date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content_type TEXT NOT NULL DEFAULT 'text/plain',
    content TEXT NOT NULL,
    image_id TEXT,
    visibility TEXT NOT NULL DEFAULT 'public',
    FOREIGN KEY (image_id) REFERENCES sc.image_post(img_id) ON DELETE SET NULL,
    FOREIGN KEY (author_id) REFERENCES sc.authors(author_id) ON DELETE CASCADE
);

CREATE TABLE sc.friends (
    author_followee TEXT NOT NULL,
    author_following TEXT NOT NULL,
    FOREIGN KEY (author_followee) REFERENCES sc.authors(author_id) ON DELETE CASCADE,
    FOREIGN KEY (author_following) REFERENCES sc.authors(author_id) ON DELETE CASCADE
);

CREATE TABLE sc.follow_requests (
    author_send TEXT NOT NULL,
    author_receive TEXT NOT NULL,
    FOREIGN KEY (author_send) REFERENCES sc.authors(author_id),
    FOREIGN KEY (author_receive) REFERENCES sc.authors(author_id)
);

CREATE TABLE sc.likes (
    like_id TEXT PRIMARY KEY,
    like_author_id TEXT NOT NULL,
    post_id TEXT NOT NULL,
    time_liked TIMESTAMP NOT NULL,
    FOREIGN KEY (like_author_id) REFERENCES sc.authors(author_id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES sc.posts(post_id)
);

CREATE TABLE sc.comments (
    post_id TEXT PRIMARY KEY,
    comment_author_id TEXT NOT NULL,
    date_commented TIMESTAMP NOT NULL,
    FOREIGN KEY (comment_author_id) REFERENCES sc.authors(author_id),
    FOREIGN KEY (post_id) REFERENCES sc.posts(post_id)
);

CREATE TABLE sc.shares(
    post_id TEXT PRIMARY KEY,
    share_author_id TEXT NOT NULL,
    date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (share_author_id) REFERENCES sc.authors(author_id),
    FOREIGN KEY (post_id) REFERENCES sc.posts(post_id)
);

CREATE TABLE sc.post_restrictions (
    post_id TEXT,
    restricted_author_id TEXT,
    FOREIGN KEY (post_id) REFERENCES sc.posts (post_id),
    FOREIGN KEY (restricted_author_id) REFERENCES sc.authors (author_id),
    UNIQUE (post_id, restricted_author_id)
);

CREATE TABLE sc.nodes (
    node_id INTEGER,
    node_name TEXT,
    base_url TEXT NOT NULL    
);