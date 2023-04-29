from datetime import datetime

from sphinx_pyproject import SphinxConfig

config = SphinxConfig(globalns=globals())

author = config["author"]

start_year = config["start_year"]
year = datetime.now().year
if start_year != year:
    year = f"{start_year}-{year}"
copyright = f"{year} {author}"
