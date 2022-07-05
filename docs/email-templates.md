# Email Templates

This file is intended to document and explain all the email templates in this project so you can use them properly. By default, this project will include a handful that are necessary for the app to
work however as you add templates, please include them in this document.

## Adding Your Own

To add your own email template, simply add a `.html` file to your local templates folder. You can also place it in `templates/emails` like so:

```
notification_email = NotificationEmail.objects.send_email(
    subject,
    "emails/file.html",
    from_email,
    [to_email],
    {context_dict},
)
```

An `EmailTemplate` object will be automatically created for every HTML file and thus viewable in the admin.

## Built in Templates

For your convenience, a number of HTML templates have been included by default.

### contact.html

Used for contact style emails.

| Name        | Type | Required | Description                         |
|-------------|------|----------|-------------------------------------|
| `name`      | str  | yes      | Name of person filling out form     |
| `email`     | str  | yes      | Email of person filling out form    |
| `message`   | str  | yes      | Body message/content for email      |
| `team_name` | str  | no       | Name of 'team' running this project |

### default.html

Default email template. You probably will never send this, it's primarily for errors.

| Name        | Type | Required | Description                         |
|-------------|------|----------|-------------------------------------|
| `team_name` | str  | no       | Name of 'team' running this project |

### empty.html

Empty email template. Used for contact forms and messages where the 'message' or 'content' can be supplied

| Name        | Type | Required | Description                         |
|-------------|------|----------|-------------------------------------|
| `message`   | str  | yes      | Body message/content for email      |
| `team_name` | str  | no       | Name of 'team' running this project |

### password_reset.html

Email to send on a password reset request. Should include link for user to go to, to actually reset their password.

| Name                 | Type | Required | Description                         |
|----------------------|------|----------|-------------------------------------|
| `password_reset_url` | str  | yes      | URL to direct user to               |
| `team_name`          | str  | no       | Name of 'team' running this project |

### template.html

Template email. This just contains template HTML to fill in as you create new EmailTemplates. This will also probably never be explicitly sent.


