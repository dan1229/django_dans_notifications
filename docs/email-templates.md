# Email Templates
This file is intended to document and explain all the email templates in this project so you can use them properly. By default, this project will include a handful that are necessary for the app to work however as you add templates, please include them in this document.


### default.html
Default email template. You probably will never send this, it's primarily for errors.


### empty.html
Empty email template. Used for contact forms and messages where the 'message' or 'content' can be supplied

| Name      | Type | Required | Description                    |
|-----------|------|----------|--------------------------------|
| `message` | str  | yes      | Body message/content for email |


### password_reset.html
Email to send on a password reset request. Should include link for user to go to, to actually reset their password.

#### Context Variables
| Name                 | Type | Required | Description           |
|----------------------|------|----------|-----------------------|
| `password_reset_url` | str  | yes      | URL to direct user to |



### template.html
Template email. This just contains template HTML to fill in as you create new EmailTemplates. This will also probably never be explicitly sent.


