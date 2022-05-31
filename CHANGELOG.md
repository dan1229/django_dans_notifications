# CHANGELOG for Django Dans Notifications
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹
##### Contact me at <dnaz@danielnazarian.com>

-------------------------------------------------------

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


-------------------------------------------------------

## [Released]

### [1.0.0] - 2022-05-28
- Initial release!

-------------------------------------------------------

## [Unreleased]

-------------------------------------------------------
### TODO

#### docs
- api docs
  - improve
- usage docs
  - send email
  - different models
- templates
  - improve
  - add docs about adding your own

-----

#### tests
- post api tests

-----

#### notification models
- how to allow user to add extras fields?

-----

#### mypy typing

mypy + django stubs

-----
#### templates

do we need the actual 'templates' folder?
- can we just store it as a string in the db?
  - data migration as 'fixture'
  - need users to be able to add their own
    - probably weird for them to copy paste into admin

user editable
- users add to their own 'templates' folder

-----
#### apis

email api
- finish POST endpoint?
  - can replace other email endpoint?
  
-----


coverage
- codecov
- badge

ci
- add lint/flake8 check
- badge

-----
### 1.0.1



how to include settings with package
- https://stackoverflow.com/questions/37264326/django-reusable-application-configuration
- i.e., for rest framework settings
  - could just say you need to add it?


remove api response handler
- create more generic django apis


cd - add python build and stuff


### [1.0.1] - 2022-05-31
- LOTS of cleanup and refactoring
- CI/CD improvements
- Refactored notifications app to work better with standard Django app

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)
##### Copyright 2022 © Daniel Nazarian.
