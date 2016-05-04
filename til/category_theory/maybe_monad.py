class Maybe:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str.format("{0}({1})", self.__class__.__name__, self.value)

    _errors = (LookupError, AttributeError)

    def bind(self, function):
        try:
            value = function(self.value)
        except self._errors:
            value = None
        return type(self)(value)

    def __getitem__(self, key):
        return self.bind(lambda value: value[key])

    def __call__(self, *args, **kwargs):
        return self.bind(lambda value: value(*args, **kwargs))

    def __rshift__(self, function):
        return self.bind(function)

    def __lshift__(self, function):
        return function(self.value)

    def __getattr__(self, name):
        return self.bind(lambda value: getattr(value, name))

    def __bool__(self):
        return self.value.__bool__()

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        return False

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return self.value != other.value
        return True


try:
    from django.core.exceptions import ObjectDoesNotExist
except ImportError:
    class ObjectDoesNotExist(Exception):
        """Dummy exception"""

class DjangoMaybe(Maybe):
    """Also allows for catching Django query .get(...) which would raise
    DoesNotExist errors.
    """
    _errors = (LookupError, AttributeError, ObjectDoesNotExist)

#
#   Testing
#
class Section:
    def __init__(self, articles, users):
        self._articles = articles
        self._users = users
    @property
    def articles(self):
        return self._articles
    @property
    def users(self):
        return self._users
    def __repr__(self):
        return "Section({0}, {1})".format(self._articles, self._users)

class Article:
    def __init__(self, title, **keywords):
        self.title = title
        for name, value in keywords.items():
            setattr(self, name, value)
    def __repr__(self):
        return "Article({0})".format(self.title)

class Record(dict):
    def __repr__(self):
        return "Record{0}".format(dict.__repr__(self))

    def read_it(self):
        return [str("{0}: {1}\n".format(name, value)) for name, value in self.items()]


basic_article = Article("Basic")
html_article = Article("HTML", html="<html></html>")

section = Section([basic_article, html_article],
                  {'John': Record(one=1, two=2), 'Ringo': Record(red='rr', blue='bb')})

maybe = Maybe(section)

print()
print("section:", type(section), section)
print()
import ipdb
ipdb.set_trace()
print()


class TestMaybe:
    def test_basic(self):
        has_data = maybe.users['Ringo'].read_it()[0].value
        no_data = maybe.users['Paul'].read_it()[0].value
        self.assertEqual(has_data, 'red: rr\n')
        self.assertEqual(no_data, None)



def django_test():
    # Original way
    try:
        in_this_issue = self.toc.tocsection_set.get(name="In This Issue")
    except TocSection.DoesNotExist:
        in_this_issue = None

    if in_this_issue:
        article = in_this_issue.tocarticle_set.first()
        html = getattr(article, 'html', None)
        if html:
            return html
    # Otherwise, construct a hook
    hook = "..."
    return hook

    # with Maybe
    result = (Maybe(self.toc.tocsection_set).get(name="In This Issue")
             .tocarticle_set.first().html).value
    if result:
        return result
    else:
        hook = "..."
        return hook
