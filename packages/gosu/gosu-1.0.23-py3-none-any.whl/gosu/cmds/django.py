import os
from typing import List

import typer
from plumbum import FG, ProcessExecutionError, local

from gosu.cmds.python import fix
from gosu.tools import _run_venv, manage_env_vars

app = typer.Typer()


def _pm(cmds: List[str]):
    manage_env_vars()
    _run_venv(["python", "-m", f"{get_project()}.manage", *cmds])


def get_project():
    if "DJANGO_SETTINGS_MODULE" not in local.env:
        return "example"
    else:
        return local.env["DJANGO_SETTINGS_MODULE"].split(".")[0]


@app.command()
def pm(ctx: typer.Context):
    _pm(ctx.args)


@app.command()
def migrate():
    _pm(["makemigrations"])
    _pm(["migrate"])


@app.command()
def test(env: str = typer.Argument("dev")):
    fix(env)
    manage_env_vars()

    local.env["DEFAULT_CACHE"] = "locmemcache://"
    local.env["QUEUE_CACHE"] = "locmemcache://"
    rcfile = f"--rcfile={os.path.dirname(__file__)}/../.coveragerc"
    _run_venv(
        [
            "coverage",
            "run",
            rcfile,
            "--parallel-mode",
            "--concurrency=multiprocessing",
            f"{get_project()}/manage.py",
            "test",
            ".",
            get_project(),
            # "--parallel=3",
        ]
    )
    _run_venv(["coverage", "combine", rcfile])
    _run_venv(["coverage", "report", rcfile])
    try:
        local.cmd.flake8["--config", f"{os.path.dirname(__file__)}/../.flake8"] & FG
    except ProcessExecutionError as e:
        exit(1)


@app.command()
def build():
    test()
    local.cmd.python3["setup.py", "sdist", "--formats=bztar"] & FG
    local.cmd.python3["setup.py", "clean"] & FG


@app.command()
def notebook():
    local.env["DJANGO_ALLOW_ASYNC_UNSAFE"] = True
    _pm(["shell_plus", "--notebook"])
