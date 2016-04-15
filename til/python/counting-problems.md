If you have a potentially erroring operation in a loop,
a simple logging approach is to catch errors into
an accumulator, and return all errors along with the
results.

This is approximately the mapping operation of the List
monad (Sequence or Iterable in Python terms) combined
with a List-version of the Error monad.

```python
def counting_problems(iterable, function):
    good = []
    bad = []
    for element in iterable:
        try:
            good += [function(element)]
        except Exception as exc:
            bad += [(element, exc)]
    return (good, bad)
```

Adding an abstraction layer on top of this adds:
* A logging step,
* Usable as a decorator
* Much more composable


```python
import pickle
import functools

LOG_FILE = 'error_log.pickle'

def problem_logger(function):
    """
    @todo: Make this incremental - so it doesn't override existing data.
    """
    @functools.wraps(function)
    def logging_wrapper(iterable):
        good, bad = counting_problems(iterable, function)

        with open(LOG_FILE, 'wb') as pickle_file:
            pickle.dump(bad, pickle_file)

        return good
    return logging_wrapper
    
```
