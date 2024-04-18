import nox

nox.options.default_venv_backend = "venv"
nox.options.reuse_existing_virtualenvs = True


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
        for django in ["4.2", "5.0"]
        if (python, django)
        not in [
            ("3.8", "5.0"),
            ("3.9", "5.0"),
        ]
    ],
)
def tests_with_coverage(session, django):
    session.install(f"Django>={django}")
    session.install("-e", ".")
    python_binary = f"{session.bin}/python{session.python}"
    session.run(python_binary, "manage.py", "test")
