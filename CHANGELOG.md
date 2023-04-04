# CHANGELOG for Django Dans Notifications

#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹

##### Contact me at <dnaz@danielnazarian.com>

-------------------------------------------------------

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


-------------------------------------------------------

## [Released]


### [1.1.15] - 2022-04-04
- ACTUAL FIX for recipients_contains lol!!


### [1.1.14] - 2022-04-04
- recipients_contains fix for ID support


### [1.1.13] - 2022-04-04
- Updated GET/List APIs to include recipients listed as IDs


### [1.1.12] - 2022-01-04
- Email threads fix


### [1.1.11] - 2022-01-04
- Send emails on threads to avoid blocking


### [1.1.10] - 2022-10-27
- Email templates fixes


### [1.1.9] - 2022-09-19
- Logging fixes
- Better error handling
- Fix file attachment in emails
- Documentation improvements


### [1.1.8] - 2022-09-16
- Email subject fix
- Doc improvements
- Email attachment/ICS support


### [1.1.7] - 2022-08-04
- Added line breaks to email templates
- Doc updates


### [1.1.6] - 2022-08-03
- IN_TEST fix for POST email API


### [1.1.5] - 2022-07-20
- Fixed datetime_sent on BaseNotification


### [1.1.4] - 2022-07-20
- Support for `TEAM_NAME` setting
- Fixed emails in test mode


### [1.1.3] - 2022-07-20
- Support for `TEAM_NAME` setting
- Fixed emails in test mode


### [1.1.2] - 2022-07-06
- Some hotfixes


### [1.1.1] - 2022-07-05
- Added contact email template
- Improved email template docs
- Fixed datetime sent for emails bug
- Improved Django admin


### [1.1.0] - 2022-06-04
- User editable Email Templates!
  - Including docs
- Flake8 + Linting improvements 


### [1.0.7] - 2022-05-30
- Email Template paths fix


### [1.0.6] - 2022-05-30
- Package name update


### [1.0.5] - 2022-05-30
- URL fixes


### [1.0.4] - 2022-05-30
- Migration fixes


### [1.0.3] - 2022-05-30
- HOTFIX 2
- LOTS of cleanup and refactoring
- CI/CD improvements
    - lint
    - test_python
    - release
- Coverage!
- Refactored notifications app to work better with standard Django app


### [1.0.2] - 2022-05-30
- HOTFIX
- LOTS of cleanup and refactoring
- CI/CD improvements
    - lint
    - test_python
    - release
- Coverage!
- Refactored notifications app to work better with standard Django app


### [1.0.1] - 2022-05-30
- LOTS of cleanup and refactoring
- CI/CD improvements
    - lint
    - test_python
    - release
- Coverage!
- Refactored notifications app to work better with standard Django app


### [1.0.0] - 2022-05-28
- Initial release!


-------------------------------------------------------

## [Unreleased]

### TODO

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

-----

#### notification models

- how to allow user to add extras fields?

-----

#### mypy typing

mypy + django stubs


-----

### 1.2.0

#### logging
- switch from print statements :/
- how to integrate with django logging?
    - can we grab the default logger or something?


#### tests
- post api tests
- higher coverage overall (> 90%)


### [1.2.0] - 2022-MM-DD
#### TODO

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)

##### Copyright 2022 © Daniel Nazarian.
