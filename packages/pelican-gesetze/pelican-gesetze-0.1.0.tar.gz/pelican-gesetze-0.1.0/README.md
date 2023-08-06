# Pelican plugin for [`py-gesetze`](https://codeberg.org/S1SYPHOS/py-gesetze)

`pelican-gesetze` links german legal norms, dependency-free & GDPR-friendly.


## Installation

It's available from [PyPi](https://pypi.org/project/pelican-gesetze) using a package manager of your choice:

```text
# Using 'pip'
pip install pelican-gesetze

# Using 'poetry'
poetry add pelican-gesetze
```


## Getting started

Using `pelican-gesetze` is straightforward: After installing it, the jinja filter `gesetzify` is available:

```html
<p class="content">
    {{ page.content | gesetzify }}
</p>
```


## Configuration

The following settings need to be prepended by `GESETZE_` to work, eg for enabling full `title` attributes, define `GESETZE_TITLE_ATTRIBUTE = 'full'` [in your settings](https://docs.getpelican.com/en/latest/settings.html#settings) (most likely `pelicanconf.py`).


| Setting             | Type        | Default                                        | Description                                    |
| ------------------- | ----------- | ---------------------------------------------- | ---------------------------------------------- |
| `DRIVER_ORDER`      | `list|str`  | `['gesetze', 'dejure', 'buzer', 'lexparency']` | Controls providers (and their respective order |
| `TITLE_ATTRIBUTE`   | `str|False` | `False`                                        | Controls `title` attribute                     |
| `CUSTOM_ATTRIBUTES` | `dict`      | `{"target": "_blank"}`                         | Defines HTML attribute defaults                |

For more information, see [here](https://codeberg.org/S1SYPHOS/py-gesetze/#configuration).


## Roadmap

- [x] Update `README.md`
- [ ] Add tests
