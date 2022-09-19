# APIs

There are numerous API endpoints available for different front ends to interact with notifications.

## Emails
- `/notifications/emails/`
  - GET     - list
  - GET     - retrieve (@param id)

## Basic
- `/notifications/basic/`
  - GET     - list
  - GET     - retrieve (@param id)
  - POST    - create (@param message)
  - PATCH   - partial_update (@param read)

## Push
- `/notifications/push/`
  - GET     - list
  - GET     - retrieve (@param id)
  - POST    - create (@param message)
