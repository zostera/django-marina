import nox
import os
import pathlib
import shutil

nox.options.default_venv_backend = "venv"
nox.options.reuse_existing_virtualenvs = True

PACKAGE_NAME = "django_registration"

NOXFILE_PATH = pathlib.Path(__file__).parents[0]
ARTIFACT_PATHS = (
    NOXFILE_PATH / "src" / f"{PACKAGE_NAME}.egg-info",
    NOXFILE_PATH / "build",
    NOXFILE_PATH / "dist",
    NOXFILE_PATH / "__pycache__",
    NOXFILE_PATH / "src" / "__pycache__",
    NOXFILE_PATH / "src" / PACKAGE_NAME / "__pycache__",
    NOXFILE_PATH / "tests" / "__pycache__",
)


def clean(paths=ARTIFACT_PATHS):
    """Clean up after a test run."""
    [
        shutil.rmtree(path) if path.is_dir() else path.unlink()
        for path in paths
        if path.exists()
    ]


@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", "check", ".")


@nox.session
def format(session):
    session.install("ruff")
    session.run("ruff", "format", ".")
    session.run("ruff", "check", ".", "--fix")


@nox.session(tags=["tests"])
@nox.parametrize(
    "python,django",
    [
        (python, django)
        for python in ["3.8", "3.9", "3.10", "3.11", "3.12"]
        for django in ["4.2", "5.0", "main"]
        if (python, django)
        not in [
            ("3.8", "5.0"),
            ("3.9", "5.0"),
            ("3.8", "main"),
            ("3.9", "main"),
        ]
    ],
)
def tests_with_coverage(session, django):
    session.install(
        (
            "https://github.com/django/django/archive/master.tar.gz"
            if django == "main"
            else f"Django~={django}.0"
        ),
        ".[tests]",
    )
    python_binary = f"{session.bin}/python{session.python}"
    python_version = session.run(python_binary, "--version", silent=True).strip()
    django_version = session.run(
        python_binary,
        "-Im",
        "django",
        "--version",
        silent=True,
    ).strip()
    session.log(f"Running tests with {python_version}/Django {django_version}")
    session.run(
        python_binary,
        "-Wonce::DeprecationWarning",
        "-Im",
        "coverage",
        "run",
        "manage.py",
        "test",
    )
    session.run(
        python_binary,
        "-Im",
        "coverage",
        "report",
        "--show-missing",
    )
    clean()


@nox.session(python=["3.11"], tags=["docs"])
def docs_build(session):
    """Build the package's documentation as HTML."""
    session.install(".[docs]")
    session.chdir("docs")
    session.run(
        f"{session.bin}/python{session.python}",
        "-Im",
        "sphinx",
        "-b",
        "html",
        "-d",
        f"{session.bin}/../tmp/doctrees",
        ".",
        f"{session.bin}/../tmp/html",
    )
    clean()
