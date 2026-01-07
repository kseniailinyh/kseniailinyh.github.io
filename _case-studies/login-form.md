---
layout: base
title: "Improving the Login Page"
body_class: case-study
---
<div class="content" markdown="1">

![Cover image for login form case study](login-form-cover.png)

## Initiative

While there wasn't an&nbsp;established process for reviewing support cases in&nbsp;our company, I&nbsp;took the initiative to&nbsp;dive into them myself. I&nbsp;discovered a&nbsp;significant number of&nbsp;cases related to&nbsp;blocked accounts. Intrigued, I&nbsp;decided to&nbsp;investigate the login form's functionality.

## The Issues

It&nbsp;turned out the login form was poorly designed:

![Issue 1 with initial login form](login-form-01.png)

- The form didn&rsquo;t show users passwords, so&nbsp;they can&rsquo;t be&nbsp;sure if&nbsp;it&nbsp;is&nbsp;correct or&nbsp;not.
- It&nbsp;didn&rsquo;t warn users about account locking after several failed attempts.
- The form didn&rsquo;t notify users when they were locked; it&nbsp;only notifies users about locking if&nbsp;they typed the correct password.
- The locking lasts for 15&nbsp;minutes, but the form didn&rsquo;t warn users about&nbsp;it.
- The form didn&rsquo;t allow password resets if&nbsp;the account was locked.

These issues explained the high number of&nbsp;support requests. Moreover, there were error messages in&nbsp;different styles and with unclear wording.

## Solution

While tempted to&nbsp;redesign the entire form (and&nbsp;I redesigned&nbsp;it, but only for the portfolio case, the original form looks less appealing), I&nbsp;realized that small, targeted changes would be&nbsp;more efficient and quicker for the development team to&nbsp;implement.

![Redesigned login form step 1](login-form-04.png)
![Redesigned login form step 2](login-form-05.png)

I&nbsp;prioritized these changes based on&nbsp;their potential impact, drawing from my&nbsp;experience, and presented them to&nbsp;stakeholders.

![Prioritized changes presentation](login-form-06.png)

## Project Status

The project was approved and is&nbsp;currently in&nbsp;development.

Although I&nbsp;can&rsquo;t present metrics yet, I&nbsp;plan to&nbsp;use the support case numbers as&nbsp;a&nbsp;baseline post-release. My&nbsp;hypothesis is&nbsp;that these small changes will enhance user experience providing clarity and transparency and, as&nbsp;a&nbsp;result, reduce support requests.

[Next project →]({{ "/case-studies/bureau/" | relative_url }})

</div>
