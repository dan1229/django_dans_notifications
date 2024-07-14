# APIs

There are numerous API endpoints available for different front ends to interact with notifications.

## Emails

- `/api/notifications/email/`
  - **GET** - List all email notifications associated with the user.
  - **GET** - Retrieve a specific email notification by ID.

## Basic

- `/api/notifications/basic/`
  - **GET** - List all basic notifications associated with the user.
  - **GET** - Retrieve a specific basic notification by ID.
  - **POST** - Create a new basic notification.
    - **Parameters**: 
      - `message` (required)
  - **PATCH** - Partially update a specific basic notification.
    - **Parameters**:
      - `read` (optional)

## Push

- `/api/notifications/push/`
  - **GET** - List all push notifications associated with the user.
  - **GET** - Retrieve a specific push notification by ID.
  - **POST** - Create a new push notification.
    - **Parameters**: 
      - `message` (required)