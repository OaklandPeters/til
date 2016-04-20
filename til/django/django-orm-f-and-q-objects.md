# Django ORM's F & Q objects

Django's ORM offers advanced control via it's `F` (field) and `Q` (query) objects. These objects underly the normal Django ORM interface, but offer more functionality, power and control.

They are also more elegant - and correspond more closely to functional programming patterns.

However, if you are comfortable with SQL queries, they are not that difficult to use either.

Here is an example of a relatively complex query which is difficult (or impossible) to express in the ORM without Q & F objects.



Example model structure:



```python
# My App models.py
from django.db import models

class STATUS:
    """Enum/Flag constants"""
    DRAFT = 0
    REVIEW = 1
    SCHEDULED = 2
    LIVE = 3

class Article(models.Model):
    status = models.IntegerField()  # flag - STATUS
    date_published = models.DateTimeField()

class Newsletter(models.Model):
    last_sent = models.DateTimeField()

class Report(models.Model):
    articles = models.ManyToManyField(Article)
    newsletter = models.ForeignKey(Newsletter)
    status = models.IntegerField()
```

Notes:
(1) an `F` object is used on the RHS of `Q(article__date_published__gte=F('newsletter__last_sent'))`, in order to refer to the `newsletter` attribute of the outer Report object.

(2) The use of `Q` objects allows a clean articulation of SQL's `and`/`or` clauses.


```python
from django.db.models import F, Q, Count
# Some models from a media-related app
from my_app.models import Report, Article, Newsletter


reports = Report.objects.filter(
    Q(article__status=STATUS.LIVE) & (
        Q(article__date_published__gte=F('newsletter__last_sent'))
        | Q(newsletter__last_sent__isnull=True)
    )
)
```

An equivalent way of writing this, which is a little easier to read:

```python
reports = (Report.objects
    .filter(article__status=STATUS.LIVE)
    .filter(Q(newsletter__last_sent__isnull=True) |
            Q(article__date_published__gte=F('newsletter__last_sent')))
)
```

