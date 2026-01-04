# API Documentation

Django Dans Notifications provides REST API endpoints for managing different types of notifications. All endpoints require authentication as configured in your Django Rest Framework settings.

## Base URL

All endpoints are prefixed with the base URL you configured in your `urls.py`:

```
/api/notifications/
```

## Authentication

All API endpoints require authentication. Configure this in your `settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}
```

## Email Notifications

### List Email Notifications
**GET** `/api/notifications/email/`

Returns a paginated list of email notifications for the authenticated user.

**Response:**
```json
{
  "count": 50,
  "next": "http://api.example.com/notifications/email/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "subject": "Welcome Email",
      "recipients": "user@example.com",
      "sender": "noreply@example.com",
      "datetime_sent": "2024-01-15T10:30:00Z",
      "sent_successfully": true
    }
  ]
}
```

### Retrieve Email Notification
**GET** `/api/notifications/email/{id}/`

Get details of a specific email notification.

**Response:**
```json
{
  "id": 1,
  "subject": "Welcome Email",
  "recipients": "user@example.com",
  "sender": "noreply@example.com",
  "datetime_sent": "2024-01-15T10:30:00Z",
  "sent_successfully": true,
  "content": "Email content here..."
}
```

## Basic Notifications

### List Basic Notifications
**GET** `/api/notifications/basic/`

Returns a paginated list of basic notifications for the authenticated user.

**Query Parameters:**
- `read` (optional): Filter by read status (`true`/`false`)

**Response:**
```json
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "message": "Your profile was updated",
      "read": false,
      "datetime_sent": "2024-01-15T14:20:00Z",
      "sender": "system@example.com"
    }
  ]
}
```

### Retrieve Basic Notification
**GET** `/api/notifications/basic/{id}/`

Get details of a specific basic notification.

### Create Basic Notification
**POST** `/api/notifications/basic/`

Create a new basic notification.

**Request Body:**
```json
{
  "message": "New notification message",
  "recipients": "user@example.com"
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "message": "New notification message",
  "read": false,
  "datetime_sent": "2024-01-15T15:00:00Z",
  "recipients": "user@example.com"
}
```

### Update Basic Notification
**PATCH** `/api/notifications/basic/{id}/`

Mark a notification as read or update other allowed fields.

**Request Body:**
```json
{
  "read": true
}
```

**Response:** `200 OK`

## Push Notifications

### List Push Notifications
**GET** `/api/notifications/push/`

Returns a paginated list of push notifications for the authenticated user.

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "message": "New message received",
      "datetime_sent": "2024-01-15T16:45:00Z",
      "sent_successfully": true
    }
  ]
}
```

### Retrieve Push Notification
**GET** `/api/notifications/push/{id}/`

Get details of a specific push notification.

### Create Push Notification
**POST** `/api/notifications/push/`

Create and send a new push notification.

**Request Body:**
```json
{
  "message": "Push notification message",
  "recipients": "user@example.com"
}
```

**Response:** `201 Created`

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
Invalid request parameters or body.

```json
{
  "error": "Invalid request",
  "details": {
    "message": ["This field is required."]
  }
}
```

### 401 Unauthorized
Authentication credentials not provided or invalid.

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
User doesn't have permission to access this resource.

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
Requested notification not found.

```json
{
  "detail": "Not found."
}
```

## Pagination

All list endpoints support pagination with the following query parameters:

- `page`: Page number (default: 1)
- `page_size`: Number of items per page (configured in settings, default: 20)

Example:
```
GET /api/notifications/basic/?page=2&page_size=10
```

## Filtering and Ordering

### Basic Notifications
- Filter by read status: `?read=true` or `?read=false`

### All Notification Types
- Order by date: `?ordering=-datetime_sent` (newest first)
- Order by date: `?ordering=datetime_sent` (oldest first)