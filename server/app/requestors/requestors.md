# OpenAPI Documentation for Flask Route

This documentation provides information on the API endpoint for the "Requestors" feature in the Flask server. This endpoint allows users to register as requestors.

## /register

### POST /register

This endpoint allows users to register as requestors by providing a unique username and a password.

#### Request Body

- `username` (string, required) - The username chosen by the requestor.
- `password` (string, required) - The password for the requestor's account.

#### Responses

- 200 OK
  - Registration is successful.
  - Response Body Example:
    ```json
    {
      "message": "Registration successful"
    }
    ```

- 200 OK
  - Username already exists in either the requestors or authors table.
  - Response Body Example:
    ```json
    {
      "error": "Username already exists"
    }
    ```

- 200 OK
  - An error occurred while registering.
  - Response Body Example:
    ```json
    {
      "error": "An error occurred while registering."
    }
    ```

Please ensure that these endpoints are used securely to manage user registrations and maintain data privacy.
