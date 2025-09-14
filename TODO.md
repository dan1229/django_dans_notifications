# TODO - Django Dan's Notifications
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹

-------------------------------------------------------
## [Unreleased]
-----




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



#### notification models - add more fields
- how to allow user to add extras fields?



-----
### 1.3.0



#### improve api swagger docs
- lots of api docs strings aren't showing up
- need to add params and stuff


#### notification basic api 'recipients' field
- only taking 1 recipient as a string - is this valid?
- if so add more docs - i.e., add docstrings to apis and stuff




#### email api - post api
- create and send emails via api
    - need some way for user to set the permissions for it
        - allowall, isauth or any class








#### revisit threads.py?
- is this working as expected?
- is there a better solution?







#### add `metadata` field to base notification model
- add a field to the base notification model that can store extra data
- e.g.,:
    - `metadata = JSONField(blank=True, null=True)`
    - this will allow users to store extra data in the notification
    - e.g.,:
        - `{"meeting_id": "1234", "meeting_time": "2024-01-01 12:00:00"}`
-
- add to serializers and api docs






#### error fields being weird?
- e.g.,:
```
POST
	http://127.0.0.1:8000/api/notifications/basic/
    {"message":"Daniel Nazarian (Entrepreneur2) is interested in your profile. Consider scheduling a meeting with them!","sender":"204c256f-e5bb-48d4-b512-510963b35e6e","recipients":["950997f1-4333-4aaa-baf4-48112440ba63"]}

{"recipients":["Not a valid string."],"message":"Error. Please try again later.","results":null,"error_fields":null}


why is 'recipients' a top level key?
```
- add it to the 'error_fields' key




#### improve base email templates
- improve it to make it look better
    - contact email is shit
- maybe add an .env var or something to set the base template?




#### fix admin usability
- most stuff should probably sort by date added
- some better controls / filters in general




### [1.3.0] - 2024-MM-DD
- TODO

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
