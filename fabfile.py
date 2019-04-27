from fabric.operations import local

SOURCE_DIRS = ["src"]


def reformat(fix=False):
    if fix == "fix":
        isort_before_autoflake()
    autoflake()
    isort()
    black()
    flake8()


def isort_before_autoflake():
    for source_dir in SOURCE_DIRS:
        local(f"isort -rc -sl {source_dir}")


def isort():
    for source_dir in SOURCE_DIRS:
        local(f"isort -rc {source_dir}")


def autoflake():
    local("autoflake -ir {} --remove-all-unused-imports".format(" ".join(SOURCE_DIRS)))


def black():
    local("black .")


def flake8():
    local("flake8 {}".format(" ".join(SOURCE_DIRS)))
