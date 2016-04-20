# Reverse Foreign Key Lookups and F-Objects

*Goal:* get all objects of model type A, which are referenced in model type B,
*but* this reference is one-way from B --> A.

This can be easily handled via a single query, via a reverse lookup on a foreign-key.

## A Concrete Example

Consider a media-related Django app, with models for article Series, and Newsletters
used to send out emails about alerts and updates to series. For simplicity,
we are going to assume each Series may have at most one Newsletter associated.

*Goal:* Get all newsletters which are referred to by at least one series.

```python
from django.db import models

# In series/models.py
class Series(models.Model):
    # article-related information not shown, since it's not relevant at this time
    title = models.CharField(max_length=150, default="") 
    slug = models.CharField(max_length=150)
    newsletter = models.ForeignKey("newsletters.Newsletter", blank=True, null=True)

# In newsletters/models.py
class Newsletter(models.Model):
    title = models.CharField(max_length=150, default="") 
    slug = models.CharField(max_length=150)
```


A Series has a reference (foreign-key) to a Newsletter, but Newsletter
models do not have a reference back. Thus, if we want to select Newsletters
based on criteria in Series, inside a query - then we will need to use a
reverse foreign key.


Note - because there is a foreign-key relationship from Series to Newsletter,
Django will automatically generate a `newsletter.series_set` field for any
Newsletter instance.

Since we would like to create a self-reference in a `filter()`-query,
we will make use of Django's `F` objects.


```python
from django.db import F

from newsletters.models import Newsletter
from series.models import Series

# Get all newsletters which are referred to by at least one series
newsletters = Newsletter.objects.filter(series__newsletter=F('pk'))
```
