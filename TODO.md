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



#### email api - post api
- create and send emails via api



#### revisit threads.py?
- is this working as expected?
- is there a better solution?


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



### [1.3.0] - 2024-MM-DD
- TODO

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
