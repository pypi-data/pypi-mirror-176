# Choubun 超文

> (this is not recommended as a real way of generating HTML!)

— [@contextlib.contextmanager](https://docs.python.org/3.5/library/contextlib.html#contextlib.contextmanager)

Choubun is an alternative approach to templating engines.
Where a traditional template system has you writing your templates as separate files,
Choubun allows you to mix Python control flow and HTML markup, all within Python's syntax.

To prevent injection vulnerabilities, Choubun uses [MarkupSafe](https://palletsprojects.com/p/markupsafe/) to escape unsafe text.
`markupsafe.Markup` is also reexported as `Markup` and `M`.

## How do I install it?
Choubun is [available on PyPI](https://pypi.org/project/choubun/).
Use `poetry add choubun` or your favorite dependency wrangler to start using Choubun in your project.

## What does code using Choubun look like?
```python
from choubun import Node
doc = Node()
doc.raw('<!DOCTYPE html>')
with doc.node('html', lang='en'):
	with doc.node('head'):
		doc.leaf('meta', charset='utf-8')
		for k, v in dict(
			viewport="width=device-width, initial-scale=1",
			referrer='no-referrer',
		).items():
			doc.leaf('meta', name=k, content=v)
	with doc.node('body'):
		doc.text("Page body")
```
