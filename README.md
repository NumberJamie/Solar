# Solar

A very, very simple python http server, that is supposed to respond with html content.

## Installation

Recommended is to use `python3.10` or higher, this project is made using `python3.12` and the preferred version to use.

clone this repo in the desired location.\
Go into the cloned repo: `cd Solar`.\
Create a virtual environment using your preferred method i.e. using your IDE or via the commandline.\
Install the requirements: `pip install -r requirements.txt`\
Run the `main.py` file and your http server should start on: `localhost:8000`.\
If you see a `404` page it should have worked.

## Dependencies

While there are some dependencies present in the `requirements.txt`, these are not 100% required.

- Jinja2: The templating language used, required if no changes to the project are made.
- MarkupSafe: Required for Jinja2.
- pony: Not required just my preferred ORM. 

## Basic example

In this example whe are adding a simple endpoint to `localhost:8000/`.

Add the router to the `urls` variable in the `core/server/http.py` or make your own location for this just make
sure to import it and make it equal to the same `urls` variable.

```python
import re

urls = [
    (re.compile('/'), HomeView)
]
```

Now that we have a url, we need to implement the HomeView class, make a new file in `core/templates`.

```python
from .templates import BaseTemplate

class HomeView(BaseTemplate):
    template = 'index.html' # should be in /templates
    
    def get(self) -> str:
        return self.render(title=self.last)
```

Only the `GET` requests return a `str` the other implemented methods (`DELETE`, `POST`) return a `HTTPStatus`. Naming
your functions is also important since that in uppercase is the method of the request and therefor is responsible for 
that request.

When adding pagination, the query parameters are globally available to all templates as `{{ query }}` so filters stay 
the same between pages and the page number increases.

## Additional info

In the `core/values.py` are some or the general values used:

- `MEDIA_URL`: url paths starting with this endpoint will serve files.
- `MEDIA_PATH`: absolute path to your media folder, ment for user uploaded files, photos and other general files.
- `STATIC_URL`: url paths starting with this endpoint will serve these static files.
- `STATIC_PATH`: absolute path to your static folder, ment for css, js and other general site-related files.
- `TEMPLATES`: absolute path to your template folder.

The `BaseTemplate` class located in the `/core/templates/template.py` has some handy things.

- `self.path`: the url path split by `/` as a list.
- `self.page`: the current page (for pagination)
- `self.last`: last item in the path.
- `self.query`: the url query parameters as a `dict[str:list]`.
- `self.get_bool()`: get and convert a query item by the key and return a `bool` or `None`.
- `self.get_str()`: get a query item by the key and return first item in the list as a `str`.
- `self.get_bool()`: get a query item by the key and return the entire `list`.
- When you want the get request to return an error you can `return self.send(HTTPStatus)`

Handy to know is that post requests require the `application/x-www-form-urlencoded` content type.
