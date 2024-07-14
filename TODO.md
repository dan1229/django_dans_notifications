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


-----

### 1.2.0



#### improve docs
- improve readme
- revisit other docs
- more badges
    - python/django versions
    - https://pypi.org/project/django-admin-interface/
        - more inspo

    


#### revisit threads.py?
- is this working as expected?
- is there a better solution?




#### add type support / stubs
- add mypy
- add ci stage to check for types?
- py.typed and thing in setup.cfg
- update docs



#### improve deps / reqs
- double check everything looks good
-
- django dans api toolkit
    - add dep for it
    - remove local code / serializers
    - update response handler functions
-
- improve status codes/api responses
    - i.e., 201 on creation
    - add 'message' to all responses
    -
    - standardize 'message' field and all that on returns
-
- tests for str_to_bool?



#### tests
- logging?
    - or ignore?
-
- apis
    - check coverage - can i fill in any gaps?
-
- higher coverage overall (> 90%)




### [1.2.0] - 2024-07-13
- Improved logging and logger support
    -  No more `print`s either!
- Improved tests and coverage!
    - Improved model tests
    - Improved and added API tests
    - All Python files now have tests
    - 90% coverage!!!
#### TODO

-------------------------------------------------------

##### Copyright 2024 © Daniel Nazarian.
