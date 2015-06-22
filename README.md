#### Icons

```
{% load icons %}
{% icon "heart" "4x" "foo" %}
```

This will produce:

```
<img class="icon foo" src="/static/open-iconic/svg/heart.svg" onerror="this.src='/static/open-iconic/png/heart-4x.png'; this.onerror=null;">
```

I don't want to include the entire open-iconic set in the Git repo, so you'll need to copy them into the static directory as needed. The default png fallback uses a `-4x.png` suffix, so you can just do `{% icon "heart" %}` if you don't need a different fallback suffix or additional CSS classes.
