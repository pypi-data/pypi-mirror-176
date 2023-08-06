import json
import pathlib
import typing

import httpx
import typer

from neosctl import schema
from neosctl.auth import ensure_login
from neosctl.util import bearer
from neosctl.util import process_response
from neosctl.util import send_output


app = typer.Typer()


def iam_url(iam_api_url: str, postfix: str = "") -> str:
    return "{}/{}".format(iam_api_url.rstrip("/"), postfix)


@app.command()
def list(
    ctx: typer.Context,
    page: int = typer.Option(1, help="Page number."),
    page_size: int = typer.Option(10, help="Page size number."),
    resource: typing.Optional[str] = typer.Option(None, help="Resource nrn."),
):
    @ensure_login
    def _request(ctx: typer.Context):
        params = {"page": page, "page_size": page_size}
        if resource:
            params["resource"] = resource

        return httpx.get(
            iam_url(ctx.obj.get_iam_api_url(), "policy/users"),
            headers=bearer(ctx),
            params=params,
        )

    r = _request(ctx)
    process_response(r)


@app.command(name="create")
def create_from_json(
    ctx: typer.Context,
    filepath: str = typer.Argument(..., help="Filepath of the user policy json payload"),
):
    @ensure_login
    def _request(ctx: typer.Context, user_policy: schema.UserPolicy) -> httpx.Response:
        return httpx.post(
            "{iam_url}".format(iam_url=iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            json=user_policy.dict(),
            headers=bearer(ctx),
        )

    fp = pathlib.Path(filepath)
    if not fp.exists():
        send_output(
            msg="Can not find file: {}".format(fp),
            exit_code=1,
        )

    with fp.open() as f:
        try:
            user_policy_payload = json.load(f)
        except json.decoder.JSONDecodeError:
            send_output(
                msg="Invalid schema file, must be json format.",
                exit_code=1,
            )

    user_policy = schema.UserPolicy(**user_policy_payload)

    r = _request(ctx, user_policy)
    process_response(r)


@app.command(name="update")
def update_from_json(
    ctx: typer.Context,
    principal: str = typer.Argument(..., help="Principal uuid"),
    filepath: str = typer.Argument(..., help="Filepath of the user policy json payload"),
):
    @ensure_login
    def _request(ctx: typer.Context, principal: str, user_policy: schema.UserPolicy) -> httpx.Response:
        return httpx.put(
            "{iam_url}".format(iam_url=iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params={"user_nrn": principal},
            json=user_policy.dict(),
            headers=bearer(ctx),
        )

    fp = pathlib.Path(filepath)
    if not fp.exists():
        send_output(
            msg="Can not find file: {}".format(fp),
            exit_code=1,
        )

    with fp.open() as f:
        try:
            user_policy_payload = json.load(f)
        except json.decoder.JSONDecodeError:
            send_output(
                msg="Invalid schema file, must be json format.",
                exit_code=1,
            )

    user_policy = schema.UserPolicy(**user_policy_payload)

    r = _request(ctx, principal, user_policy)
    process_response(r)


@app.command()
def delete(ctx: typer.Context, user_nrn: str):
    @ensure_login
    def _request(ctx: typer.Context, name: str) -> httpx.Response:
        return httpx.delete(
            "{iam_url}".format(iam_url=iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params={"user_nrn": user_nrn},
            headers=bearer(ctx),
        )

    r = _request(ctx, user_nrn)
    process_response(r)


@app.command()
def get(ctx: typer.Context, user_nrn: str):
    @ensure_login
    def _request(ctx: typer.Context, name: str) -> httpx.Response:
        return httpx.get(
            "{iam_url}".format(iam_url=iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params={"user_nrn": user_nrn},
            headers=bearer(ctx),
        )

    r = _request(ctx, user_nrn)
    process_response(r)
