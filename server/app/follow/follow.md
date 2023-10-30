# OpenAPI Documentation for Follow Routes

This documentation provides information on the API endpoints for the "Follow" feature in the Flask server. These endpoints allow users to search for other users, send and manage follow requests, and handle follow requests from other users.

## /usersearch

### GET /usersearch

This endpoint allows users to search for other users based on a search query.

#### Query Parameters

- `query` (string, optional) - The search query to filter user names.

#### Responses

- 200 OK
  - Returns a list of users that match the search query.
  - Response Body Example:
    ```json
    {
      "users": [
        {
          "id": 1,
          "username": "user123"
        },
        {
          "id": 2,
          "username": "john_doe"
        }
      ]
    }
    ```

- 200 OK
  - No matching users found.
  - Response Body Example:
    ```json
    {
      "users": []
    }
    ```

## /follow_request

### POST /follow_request

This endpoint allows users to send follow requests to other users.

#### Request Body

- `author_send` (integer, required) - The ID of the author sending the follow request.
- `author_receive` (integer, required) - The ID of the author receiving the follow request.

#### Responses

- 200 OK
  - Follow request sent successfully.
  - Response Body Example:
    ```json
    {
      "message": "Follow request sent"
    }
    ```

- 200 OK
  - Already following the user.
  - Response Body Example:
    ```json
    {
      "message": "Already following"
    }
    ```

- 200 OK
  - Follow request has already been sent.
  - Response Body Example:
    ```json
    {
      "message": "Follow request already sent"
    }
    ```

## /show_requests

### GET /show_requests

This endpoint allows users to retrieve a list of pending follow requests sent to them.

#### Query Parameters

- `authorId` (integer, optional) - The ID of the user for whom follow requests are to be retrieved.

#### Responses

- 200 OK
  - Returns a list of pending follow requests.
  - Response Body Example:
    ```json
    {
      "followRequests": [
        {
          "id": 1,
          "username": "user123"
        },
        {
          "id": 2,
          "username": "john_doe"
        }
      ]
    }
    ```

- 200 OK
  - No pending follow requests found.
  - Response Body Example:
    ```json
    {
      "followRequests": []
    }
    ```

## /accept_request

### POST /accept_request

This endpoint allows users to accept a pending follow request.

#### Request Body

- `author_followee` (integer, required) - The ID of the user who is accepting the follow request.
- `author_following` (integer, required) - The ID of the user who sent the follow request.

#### Responses

- 200 OK
  - Follow request accepted successfully.
  - Response Body Example:
    ```json
    {
      "message": "Follow request accepted"
    }
    ```

- 200 OK
  - Follow request not found.
  - Response Body Example:
    ```json
    {
      "message": "Follow request not found"
    }
    ```

## /reject_request

### POST /reject_request

This endpoint allows users to reject a pending follow request.

#### Request Body

- `author_followee` (integer, required) - The ID of the user who is rejecting the follow request.
- `author_following` (integer, required) - The ID of the user who sent the follow request.

#### Responses

- 200 OK
  - Follow request rejected successfully.
  - Response Body Example:
    ```json
    {
      "message": "Follow request rejected"
    }
    ```

- 200 OK
  - Follow request not found.
  - Response Body Example:
    ```json
    {
      "message": "Follow request not found"
    }
    ```
