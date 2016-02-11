# Removing Elements with LXML and the Problem Tail Text

[LXML](https://github.com/lxml/lxml) appends trailing text, which is not wrapped inside it's own tag, as the `.tail` attribute of the tag just prior. For example:

```html
<div>
    <p>
        p-inner
    </p>
    p-trailing
    <aside>
        aside-inner
    </aside>
    aside-trailing
</div>
```

when parsed, does unintuitive things with the trailing bits of text:

```python
tree = lxml.html.fragment_fromstring("<div><p>p-inner</p>p-trailing<aside>aside-inner</aside>aside-trailing</div>")
p_tag = tree.xpath("//p")[0]
aside_tag = tree.xpath("//aside")[0]

assert(p_tag.text == 'p-inner')

assert(p_tag.tail == 'p-trailing')
```

This becomes an issue in parsing when you want to remove a tag. What should you do with `.tail` of the removed element? One option is to append it to the `.tail` of the prior sibling element, and if there is no prior sibling element, then to the `.tail` of the parent.

```python
def remove_element(el):
    """
    Remove an lxml.html.Element, accounting for potential .tail text.
    """
    parent = el.getparent()
    if el.tail:
        prev = el.getprevious()
        if prev is not None:
            if prev.tail:
                prev.tail += el.tail
            else:
                prev.tail = el.tail
        else:
            if parent.text:
                parent.text += el.tail
            else:
                parent.text = el.tail
    parent.remove(el)
```

In which case this becomes:

```python
remove_element(aside_tag)  # mutates tree in place
cut = lxml.html.tostring(tree)
assert(cut == b'<div><p>p-inner</p>p-trailingaside-trailing</div>')
```
