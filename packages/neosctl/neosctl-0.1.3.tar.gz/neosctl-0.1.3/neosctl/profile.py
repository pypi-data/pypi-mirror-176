import typing

import typer

from neosctl import constant
from neosctl import schema
from neosctl.util import get_user_profile_section
from neosctl.util import prettify_json
from neosctl.util import remove_config
from neosctl.util import send_output
from neosctl.util import upsert_config


app = typer.Typer()


@app.command()
def init(
    ctx: typer.Context,
    gateway_api_url: typing.Optional[str] = typer.Option(None, "--gateway-api-url", "-g"),
    registry_api_url: typing.Optional[str] = typer.Option(None, "--registry-api-url", "-r"),
    iam_api_url: typing.Optional[str] = typer.Option(None, "--iam-api-url", "-i"),
    username: typing.Optional[str] = typer.Option(None, "--username", "-u"),
    auth_flow: typing.Optional[constant.AuthFlow] = typer.Option(None, "--auth-flow", "-a"),
):
    typer.echo("Initialising [{}] profile.".format(ctx.obj.profile_name))
    if gateway_api_url is None:
        gateway_api_url = typer.prompt(
            "Gateway API url",
            default=ctx.obj.get_gateway_api_url(),
        )
    if registry_api_url is None:
        registry_api_url = typer.prompt(
            "Registry API url",
            default=ctx.obj.get_registry_api_url(),
        )
    if iam_api_url is None:
        iam_api_url = typer.prompt(
            "IAM API url",
            default=ctx.obj.get_iam_api_url(),
        )
    if username is None:
        kwargs = {}
        if ctx.obj.profile:
            kwargs["default"] = ctx.obj.profile.user
        username = typer.prompt(
            "Username",
            **kwargs,
        )
    if auth_flow is None:
        kwargs["default"] = constant.AuthFlow.keycloak.value
        if ctx.obj.profile:
            kwargs["default"] = ctx.obj.profile.auth_flow
        auth_flow = typer.prompt("Auth flow", **kwargs)
        auth_flow = constant.AuthFlow(auth_flow)

    profile = schema.Profile(
        gateway_api_url=gateway_api_url,
        registry_api_url=registry_api_url,
        iam_api_url=iam_api_url,
        user=username,
        access_token="",
        refresh_token="",
        auth_flow=auth_flow,
    )

    upsert_config(ctx, profile)


@app.command()
def delete(
    ctx: typer.Context,
):
    typer.confirm("Remove [{}] profile".format(ctx.obj.profile_name), abort=True)
    remove_config(ctx)


@app.command()
def view(
    ctx: typer.Context,
):
    send_output(
        msg=prettify_json({**get_user_profile_section(ctx.obj.config, ctx.obj.profile_name)}),
    )
