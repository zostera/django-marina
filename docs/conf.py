import importlib
from datetime import datetime

import tomllib

with open("../pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

project = pyproject["project"]["name"]
project_with_underscores = project.replace("-", "_")
module = importlib.import_module(f"{project_with_underscores}")

authors = ", ".join(author["name"] for author in pyproject["project"]["authors"])
release = module.__version__
version = ".".join(release.split(".")[:2])
year = datetime.now().year
copyright = f"{year} {authors}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_mdinclude",
]
pygments_style = "sphinx"
htmlhelp_basename = f"{project}-doc"
html_theme = "sphinx_rtd_theme"
