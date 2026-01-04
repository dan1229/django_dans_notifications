# TODO - Django Dan's Notifications
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹

-------------------------------------------------------
## [Unreleased]
-----





-----
### 1.4.0



#### add `metadata` field to base notification model
- add a field to the base notification model that can store extra data
- e.g.,:
    - `metadata = JSONField(blank=True, null=True)`
    - this will allow users to store extra data in the notification
    - e.g.,:
        - `{"meeting_id": "1234", "meeting_time": "2024-01-01 12:00:00"}`
-
- add to serializers and api docs



#### notification models - add more fields
- how to allow user to add extras fields?



---




#### notification basic api 'recipients' field
- only taking 1 recipient as a string - is this valid?
- if so add more docs - i.e., add docstrings to apis and stuff



#### email api - post api
- create and send emails via api
    - need some way for user to set the permissions for it
        - allowall, isauth or any class




### [1.4.0] - 2026-MM-DD
- TODO

-----
### 1.3.0




 

### [1.3.0] - 2026-01-03
- Improved base / default email templates
    - Enhanced `base.html` template with modern, responsive design
    - Professional styling with better typography and spacing
    - Mobile-friendly layout with email client compatibility
    - Improved `contact.html` template with cleaner information display
    - All changes are backwards compatible - no configuration required
- Admin usability improvements
    - Better sorting and searching
    - More relevant columns
- Improved email threading system with `EmailSender` class
  - Thread pool executor with configurable max workers (default: 3)
  - Automatic retry logic with exponential backoff for failed sends
  - Proper asynchronous execution (fixes previous .run() vs .start() bug)
  - Graceful shutdown on application exit
  - Optional synchronous mode for testing/debugging
- Fixed issue with keys being put at top level instead of `error_fields`
- Improved Swagger API docs
    - Specifically compatible with drf-yasg
- Complete documentation overhaul
    - Created comprehensive Getting Started guide
    - Added detailed Usage guide with examples
    - Improved API documentation with request/response examples
    - Enhanced Model documentation with full field descriptions
    - Expanded Email Templates documentation with custom template guide
    - Simplified README with links to new documentation

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
