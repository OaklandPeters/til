Putting a list of content into a grid or column layout has long been an annoyance in CSS. Modern layout tool - such `flex` and `column-count` make this considerably easier. However, modern browser support still lags, leaving parts of the CSS3 standard for `flex` unimplemented in most browsers (as of 03/31/2016) - and the need to support legacy browsers can mean these styles are out-of-bounds entirely.

So, here is a simple way to get responsive-friendly column/grid layout which is backwards compatible.


```html
<div class="outer">
    <ul class="container">
        <li class="element">Content 1</li>
        <li class="element">Content 2</li>
        <li class="element">Content 3</li>
        <li class="element">Content 4</li>
        <li class="element">Content 5</li>
        <li class="element">Content 6</li>
        <li class="element">Content 7</li>
        <li class="element">Content 8</li>
        <li class="element">Content 9</li>
        <li class="element">Content 10</li>
    </ul>
</div>
```

```css
// This is not layout-related, it simply defines content for the elements
.element {
  border: 1pt solid black;
  height: 100px;
  width: 100px;
  list-style-type: none;
}
```


# Grid Layout
```css
.container {
    overflow: hidden;
}

.element {
    float: left;
    display: block;
}
```

## Centered, two-column, margin between elements
```css
.container.two-column {
    margin: 0 auto;
    width: 220px;

    .element {
        margin-bottom: 10px;
    }
    .element:nth-of-type(2n+1) {
        margin-right: 10px;
    }
}
```


## Centered, one-column - useful for mobile
```css
.container.single-column {
    margin: 0 auto;
    width: 110px;

    .element {
        margin-bottom: 10px
    }
}
```
