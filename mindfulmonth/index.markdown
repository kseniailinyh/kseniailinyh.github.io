---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title: "Mindful Month"

---

# Mindful Month
<p class="subtitle">Month of awareness, good habits, and self-love</p>

Hi! I'm Ksenia, and this is my mindfulness project that I created with my friends in 2017. It started as a mailing list designed to teach people how to live a calm and happy life.

Think of it as an advent calendar, but instead of sweets, you get a short, easy task for each day of the month. These tasks include meditating for 5 minutes, avoiding phone use for a day, practicing gratitude, and more. Many of these tasks have the potential to become lasting habits.

Originally, this was distributed as a newsletter, but the platform I used suspended my account. So, I've decided to share these messages here instead. Using AI, I've translated all the content and created new accompanying images.


## Letters

<ol>
  {% for post in site.posts reversed %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </li>
  {% endfor %}
</ol>

## What readers say

More than 3000 people subscribed and shared feedback like the following:

*— This advent calendar is just a bomb. I think it should be exhibited in the museum of new media. It’s like augmented reality, just not another stupid game on an iPhone, but something meaningful.*

<footer>Alexey</footer>

*— Thank you! I really liked your idea, and I did most of the exercises. There is more order in life*

<footer>Elizaveta</footer>

*— Thank you! Thanks to your course, I was inspired and deleted the application in contact from my phone! And I can say that life without an app is great! Thanks! And I feel that this is not the last change — I found an android application, QualityTime, which tracks the running applications and the time of their use. Still waiting for me optimization!*

<footer>Nadezhda</footer>
