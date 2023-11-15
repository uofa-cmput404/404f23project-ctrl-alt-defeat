
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS requestors;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS image_post;
DROP TABLE IF EXISTS friends;
DROP TABLE IF EXISTS follow_requests;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS shares;
DROP TABLE IF EXISTS post_restrictions;

CREATE TABLE posts (
    post_id TEXT PRIMARY KEY,
    author_id INTEGER NOT NULL,
    date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content_type TEXT NOT NULL DEFAULT "text/plain",
    content TEXT NOT NULL,
    image_id TEXT,
    visibility TEXT NOT NULL DEFAULT "public",
    FOREIGN KEY (image_id) REFERENCES image_post(img_id) ON DELETE SET NULL,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);


CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE requestors (
    requestor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE admins (
    admin_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE image_post (
    img_id TEXT PRIMARY KEY,
    author_id INTEGER NOT NULL,
    img_url TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT "public",
    date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);

CREATE TABLE friends (
    author_followee INTEGER NOT NULL,
    author_following INTEGER NOT NULL,
    FOREIGN KEY (author_followee) REFERENCES authors(author_id) ON DELETE CASCADE,
    FOREIGN KEY (author_following) REFERENCES authors(author_id) ON DELETE CASCADE
);

CREATE TABLE follow_requests (
     author_send INTEGER NOT NULL,
     author_receive INTEGER NOT NULL,
     FOREIGN KEY (author_send) REFERENCES authors(author_id),
     FOREIGN KEY (author_receive) REFERENCES authors(author_id)
 );

CREATE TABLE likes (
    like_id TEXT PRIMARY KEY,
    like_author_id INTEGER NOT NULL,
    post_id TEXT NOT NULL,
    time_liked TIMESTAMP NOT NULL,
    FOREIGN KEY (like_author_id) REFERENCES authors(author_id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE comments (
    post_id TEXT PRIMARY KEY,
    comment_author_id INTEGER NOT NULL,
    date_commented TIMESTAMP NOT NULL,
    FOREIGN KEY (comment_author_id) REFERENCES authors(author_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE shares(
    post_id TEXT PRIMARY KEY,
    share_author_id INTEGER NOT NULL,
    date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (share_author_id) REFERENCES authors(author_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE post_restrictions (
    post_id INTEGER,
    restricted_author_id INTEGER,
    FOREIGN KEY (post_id) REFERENCES posts (post_id),
    FOREIGN KEY (restricted_author_id) REFERENCES authors (author_id)
    UNIQUE (post_id, restricted_author_id) -- Unique constraint
);

CREATE TABLE nodes (
    node_id INTEGER,
    node_name TEXT,
    base_url TEXT NOT NULL    
);

