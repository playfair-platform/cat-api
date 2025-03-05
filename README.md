# Consumer Action Taskforce (cat-api)

## About
This is a library which aims to make Consumer Protection data easily accessible through an API.

## Supported Consumer Indexable Resources:
- (in progress) Consumer Action Taskforce (CAT) (https://wiki.rossmanngroup.com)



## Installation
(soon on pypi)

or:
`pip install git+git@github.com:playfair-platform/cat-api.git`

## Usage
```py
import catd

results = catd.Wiki.search("google")

if len(results) > 0:
    content = results[0].get_page()
```

or:
```py
import catd

results = catd.Wiki.search("google")
content = catd.Wiki.get_page(page_id=results[0].page_id)
```

