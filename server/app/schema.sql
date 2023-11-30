DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS requestors;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS image_post;
DROP TABLE IF EXISTS friends;
DROP TABLE IF EXISTS follow_requests;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS shares;
DROP TABLE IF EXISTS post_restrictions;
DROP TABLE IF EXISTS nodes;

CREATE TABLE posts (
    post_id TEXT PRIMARY KEY,
    author_id TEXT NOT NULL, --TEXT
    date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content_type TEXT NOT NULL DEFAULT "text/plain",
    content TEXT NOT NULL,
    image_id TEXT,
    visibility TEXT NOT NULL DEFAULT "public",
    FOREIGN KEY (image_id) REFERENCES image_post(img_id) ON DELETE SET NULL,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);


CREATE TABLE sc.authors (
    author_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    github TEXT ,
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
    FOREIGN KEY (like_author_id) REFERENCES authors(author_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE comment_likes (
    like_comment_author_id TEXT NOT NULL, --TEXT
    comment_id TEXT NOT NULL,
    time_liked TIMESTAMP NOT NULL,
    FOREIGN KEY (like_comment_author_id) REFERENCES authors(author_id),
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id)
);

CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    comment_author_id TEXT NOT NULL, --TEXT
    post_id TEXT NOT NULL, --TEXT
    author_id TEXT NOT NULL, --TEXT
    comment_text TEXT NOT NULL, --TEXT
    status TEXT NOT NULL,
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