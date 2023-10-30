# OpenAPI Documentation for Author Routes

This documentation provides information on the API endpoints for the "Authors" resource in the Flask server. These endpoints allow users to log in, update their username, and update their password.

## /login

### POST /login

This endpoint is used for user authentication and allows users to log in to the system by providing their username and password.

#### Request Body

- `username` (string, required) - The username of the author.
- `password` (string, required) - The password associated with the username.

#### Responses

- 200 OK
  - Successful login.
  - Response Body Example:
    ```json
    {
      "message": "Login successful",
      "author_id": 1
    }
    ```

- 400 Bad Request
  - Invalid or missing request parameters.
  - Response Body Example:
    ```json
    {
      "message": "Wrong Password"
    }
    ```
- 404 Not Found
  - The provided username does not exist.
  - Response Body Example:
    ```json
    {
      "message": "User not found"
    }
    ```

## /update_username

### POST /update_username

This endpoint allows users to update their username. The new username must not already exist in the system.

#### Request Body

- `new_username` (string, required) - The new username to be set.
- `authorId` (integer, required) - The author's ID for whom the username should be updated.

#### Responses

- 200 OK
  - Username updated successfully.
  - Response Body Example:
    ```json
    {
      "message": "Username updated successfully"
    }
    ```

- 400 Bad Request
  - The new username already exists in the system.
  - Response Body Example:
    ```json
    {
      "error": "Username already exists"
    }
    ```

- 500 Internal Server Error
  - An error occurred while updating the username.
  - Response Body Example:
    ```json
    {
      "error": "An error occurred while updating the username."
    }
    ```

## /update_password

### POST /update_password

This endpoint allows users to update their password.

#### Request Body

- `new_password` (string, required) - The new password to be set.
- `authorId` (integer, required) - The author's ID for whom the password should be updated.

#### Responses

- 200 OK
  - Password updated successfully.
  - Response Body Example:
    ```json
    {
      "message": "Password updated successfully"
    }
    ```

- 500 Internal Server Error
  - An error occurred while updating the password.
  - Response Body Example:
    ```json
    {
      "error": "An error occurred while updating the password."
    }
    ```
