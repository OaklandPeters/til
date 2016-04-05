# Mailchimp's Python API

## Open Your Profile

Assuming you are accessing this via Django:


```python
import mailchimp
from django.conf import settings
chimp = mailchimp.Mailchimp(settings.MAILCHIMP_KEY)
```

## List Campaigns

```python
all_campaigns = chimp.campaigns.list()
web_api_url = lambda web_id: "https://us2.admin.mailchimp.com/campaigns/wizard/html-url?id={0}".format(web_id)
summary = [(camp['title'], camp['id'], web_api_url(camp['web_id']))
                for camp in all_campaigns['data']]
```

## Update a Campaign with Mailchimp's Python API

To update a specific campaign, for any of the properties: html, sections, text, url, archive, archive_type:

```python
campaign_id = u'111111111'
new_url = 'www.foo.com/newsletters/bar/'
chimp.campaigns.update(campaign_id, "content", {"url": new_url})
```
