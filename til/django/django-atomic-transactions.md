# Atomic Transactions in Django


Django's `transaction.atomic` property can be used to ensure that a function is handled atomically. Thus if anything goes wrong, then all of the changes made by that function are rolled-back. By default, views are wrapped in this function. However, you can explicitly use it for utility functions, or even in-line in scripts.


```python
from django.db import transaction


# Can be used as a decorator
@transaction.atomic
def my_function(data):
    r1 = data.db_action_1()
    r2 = data.db_action_2()
    try:
        r2.method()
    except r2.DoesNotExist as exc:
        # Now, the effects of db_action_1 and db_action_2 will be rolled-back
        raise exc
    
# Or as a context-manager
def my_script(data):
    with transaction.atomic():
        r1 = data.db_action_1()
        r2 = data.db_action_2()
        try:
            r2.method()
        except r2.DoesNotExist as exc:
            # Now, the effects of db_action_1 and db_action_2 will be rolled-back
            raise exc
```
