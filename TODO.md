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





-----
### 1.3.0




#### docs
- getting started
    - move out of readme
- api docs
    - improve
- usage docs
    - send email
    - different models
- templates
    - improve
    - add docs about adding your own






#### improve api swagger docs
- lots of api docs strings aren't showing up
- need to add params and stuff






#### revisit threads.py?
- is this working as expected?
- is there a better solution?






 

### [1.3.0] - 2026-01-DD
- Improved base / default email templates
    - Enhanced `base.html` template with modern, responsive design
    - Professional styling with better typography and spacing
    - Mobile-friendly layout with email client compatibility
    - Improved `contact.html` template with cleaner information display
    - All changes are backwards compatible - no configuration required
- Admin usability improvements
    - Better sorting and searching
    - More relevant columns
- Fixed issue with keys being put at top leveol instead of `error_fields`

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
