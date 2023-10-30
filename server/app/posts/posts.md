# OpenAPI Documentation for Posts Routes

This documentation provides information on the API endpoints for the "Posts" feature in the Flask server. These endpoints allow users to interact with posts, manage their visibility, and make changes to their posts.

## /restricted

### GET /restricted

This endpoint allows you to get a list of users who have been restricted from viewing a specific post.

#### Query Parameters

- `post_id` (string, required) - The ID of the post for which you want to retrieve restricted users.

#### Responses

- 200 OK
  - Returns a list of usernames who are restricted from viewing the post.
  - Response Body Example:
    ```json
    ["username1", "username2"]
    ```

- 200 OK
  - No restricted users found.
  - Response Body Example:
    ```json
    []
    ```

## /restrict

### POST /restrict

This endpoint allows you to restrict a specific user from viewing a post.

#### Request Body

- `post_id` (string, required) - The ID of the post to restrict access to.
- `username` (string, required) - The username of the user to be restricted.

#### Responses

- 200 OK
  - User successfully restricted from the post.
  - Response Body Example:
    ```
    "success"
    ```

- 200 OK
  - User not found.
  - Response Body Example:
    ```
    "not_exists"
    ```

- 200 OK
  - Attempt to add a duplicate restriction.
  - Response Body Example:
    ```
    "duplicate"
    ```

## /unrestrict

### DELETE /unrestrict

This endpoint allows you to remove a user's restriction from viewing a post.

#### Path Parameters

- `post_id` (string, required) - The ID of the post from which the user should be unrestricted.
- `username` (string, required) - The username of the user to be unrestricted.

#### Responses

- 200 OK
  - User successfully unrestricted from the post.
  - Response Body Example:
    ```
    "success"
    ```

- 200 OK
  - User not found.
  - Response Body Example:
    ```
    "not_exists"
    ```

## /visibility

### POST /visibility

This endpoint allows you to change the visibility of a specific post.

#### Request Body

- `post_id` (string, required) - The ID of the post to change visibility for.
- `visibility` (string, required) - The new visibility setting for the post.

#### Responses

- 200 OK
  - Post visibility changed successfully.
  - Response Body Example:
    ```
    "success"
    ```

- 200 OK
  - Error occurred while changing post visibility.
  - Response Body Example:
    ```
    "error"
    ```

## /delete

### POST /delete

This endpoint allows you to delete a specific post.

#### Request Body

- `post_id` (string, required) - The ID of the post to be deleted.

#### Responses

- 200 OK
  - Post deleted successfully.
  - Response Body Example:
    ```
    "success"
    ```

- 200 OK
  - Error occurred while deleting the post.
  - Response Body Example:
    ```
    "error"
    ```

## /manage

### POST /manage

This endpoint allows you to manage posts, specifically retrieving posts created by a specific user.

#### Request Body

- `author_id` (string, required) - The ID of the user for whom you want to retrieve their posts.

#### Responses

- 200 OK
  - Returns a list of posts created by the specified user.
  - Response Body Example:
    ```
    [
      {
        "post_id": "123",
        "author_id": "456",
        "title": "Sample Post",
        "content_type": "text/plain",
        "content": "This is the content of the post.",
        "image_id": "789",
        "visibility": "public",
        "date_posted": "2023-10-29 12:34:56"
      },
      {
        "post_id": "124",
        "author_id": "456",
        "title": "Another Post",
        "content_type": "text/plain",
        "content": "This is another post content.",
        "image_id": "790",
        "visibility": "friends-only",
        "date_posted": "2023-10-30 14:45:00"
      }
    ]
    ```

- 200 OK
  - No posts found for the specified user.
  - Response Body Example:
    ```
    []
    ```

## /

### POST /

This endpoint allows you to retrieve posts based on visibility settings and restrictions.

#### Request Body

- `author_id` (string, required) - The ID of the user making the request.

#### Responses

- 200 OK
  - Returns a list of posts based on visibility settings and restrictions.
  - Response Body Example:
    ```
    [
      {
        "post_id": "123",
        "author_id": "456",
        "title": "Sample Post",
        "content_type": "text/plain",
        "content": "This is the content of the post.",
        "image_id": "789",
        "visibility": "public",
        "date_posted": "2023-10-29 12:34:56"
      },
      {
        "post_id": "124",
        "author_id": "456",
        "title": "Another Post",
        "content_type": "text/plain",
        "content": "This is another post content.",
        "image_id": "790",
        "visibility": "friends-only",
        "date_posted": "2023-10-30 14:45:00"
      }
    ]
    ```

- 200 OK
  - No posts found based on visibility settings and restrictions.
  - Response Body Example:
    ```
    []
    ```

## /new

### POST /new

This endpoint allows you to create a new post.

#### Request Body

- `author_id` (string, required) - The ID of the user creating the post.
- `title` (string, required) - The title of the post.
- `content` (string, required) - The content of the post.
- `visibility` (string, required) - The visibility setting for the post (public, friends-only, etc.).
- `content_type` (string, required) - The type of content (text/plain, text/markdown, etc.).
- `image_id` (string, optional) - The ID of the attached image (if any).

#### Responses

- 200 OK
  - Post created successfully.
  - Response Body Example:
    ```
    "success"
    ```

- 412 Precondition Failed
  - Invalid content type provided.
  - Response Body Example:
    ```
    "Invalid content type"
    ```

## /authors/{author_id}/{post_id}/image

### GET /authors/{author_id}/{post_id}/image

This endpoint allows you to retrieve the image associated with a specific post. 

#### Path Parameters

- `author_id` (string, required) - The ID of the author of the post.
- `post_id` (string, required
