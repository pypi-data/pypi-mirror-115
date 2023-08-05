import os
from typing import List

import typer
from plumbum import local

from gosu.cmds.python import _manage_env_vars, run

app = typer.Typer()


def _pm(cmds: List[str]):
    _manage_env_vars()
    run(["python", "-m", f"{get_project()}.manage", *cmds])


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
def test():
    _manage_env_vars()

    local.env["DEFAULT_CACHE"] = "locmemcache://"
    local.env["QUEUE_CACHE"] = "locmemcache://"
    rcfile = f"--rcfile={os.path.dirname(__file__)}/../.coveragerc_django"
    run(
        "coverage",
        "run",
        "--fail_under=15",
        rcfile,
        f"{get_project()}/manage.py",
        "test",
        ".",
        get_project(),
    )
    run(["coverage", "report", rcfile])


@app.command()
def notebook():
    local.env["DJANGO_ALLOW_ASYNC_UNSAFE"] = True
    _pm(["shell_plus", "--notebook"])
