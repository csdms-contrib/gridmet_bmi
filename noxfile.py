"""Nox sessions for gridmet_bmi development."""

import os
import shutil
from itertools import chain
from pathlib import Path

import nox

PROJECT = "gridmet_bmi"
PACKAGE = PROJECT.replace("-", "_")
HERE = Path(__file__)
ROOT = HERE.parent
PATHS = [PACKAGE, "tests", "examples", HERE.name]

# Default sessions to run when nox is called without arguments
nox.options.sessions = ["lint", "test"]


@nox.session
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install(".[testing]")

    args = [
        "--cov",
        PACKAGE,
        "-vvv",
    ] + session.posargs

    if "CI" in os.environ:
        args.append(f"--cov-report=xml:{ROOT.absolute()!s}/coverage.xml")
        args.append(f"--cov-config={ROOT.absolute()!s}/pyproject.toml")

    session.run("pytest", *args)

    if "CI" not in os.environ:
        session.run("coverage", "report", "--ignore-errors", "--show-missing")


@nox.session(name="test-bmi")
def test_bmi(session: nox.Session) -> None:
    """Test the BMI with bmi-tester."""
    session.install("bmi-tester")
    session.install(".[testing]")

    session.run(
        "bmi-test",
        f"{PACKAGE}.bmi_gridmet:BmiGridmet",
        "--config-file",
        f"{ROOT}/examples/gridmet_bmi.yaml",
        "--root-dir",
        "examples",
        "-vvv",
    )


@nox.session
def lint(session: nox.Session) -> None:
    """Clean lint."""
    session.install("flake8")
    session.run("flake8", *PATHS)


@nox.session
def format(session: nox.Session) -> None:
    """Make pretty."""
    session.install("black", "isort")
    session.run("isort", *PATHS)
    session.run("black", *PATHS)


@nox.session
def build(session: nox.Session) -> None:
    """Make src and dist builds."""
    session.install(".[build]")
    session.run("python", "-m", "build")
    session.run("twine", "check", "dist/*")
    session.run("ls", "-l", "dist/")


@nox.session
def release(session):
    """Tag, build, and publish a new release to PyPI."""
    session.install(".[build]")
    session.run("fullrelease")


@nox.session(name="testpypi")
def publish_testpypi(session: nox.Session) -> None:
    """Build and upload to TestPyPI."""
    session.install(".[build]")
    session.run("python", "-m", "build")
    session.install("twine")
    session.run("twine", "check", "dist/*")
    session.run(
        "twine",
        "upload",
        "--skip-existing",
        "--repository-url",
        "https://test.pypi.org/legacy/",
        "dist/*",
    )


@nox.session(name="pypi")
def publish_pypi(session: nox.Session) -> None:
    """Build and upload to PyPI."""
    session.install(".[build]")
    session.run("python", "-m", "build")
    session.install("twine")
    session.run("twine", "check", "dist/*")
    session.run(
        "twine",
        "upload",
        "--skip-existing",
        "dist/*",
    )


@nox.session(python=False)
def clean(session: nox.Session) -> None:
    """Remove generated files."""
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree(f"{PACKAGE}.egg-info", ignore_errors=True)
    shutil.rmtree(".eggs", ignore_errors=True)
    shutil.rmtree(".pytest_cache", ignore_errors=True)
    shutil.rmtree(".tox", ignore_errors=True)
    shutil.rmtree("htmlcov", ignore_errors=True)

    if os.path.exists(".coverage"):
        os.remove(".coverage")
    if os.path.exists("coverage.xml"):
        os.remove("coverage.xml")

    for p in chain(ROOT.rglob("*.py[co]"), ROOT.rglob("__pycache__")):
        if p.is_dir():
            try:
                shutil.rmtree(p)
            except OSError:
                pass
        else:
            try:
                p.unlink()
            except OSError:
                pass


@nox.session(python=False)
def nuke(session: nox.Session) -> None:
    """Clean and remove session environments."""
    clean(session)
    shutil.rmtree(".nox", ignore_errors=True)
