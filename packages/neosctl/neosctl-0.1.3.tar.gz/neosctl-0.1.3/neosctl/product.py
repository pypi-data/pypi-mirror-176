import json
import pathlib
import typing

import httpx
import typer

from neosctl.auth import ensure_login
from neosctl.schema import DataProductCreate
from neosctl.util import _get_index_params
from neosctl.util import bearer
from neosctl.util import process_response
from neosctl.util import send_output


app = typer.Typer()


def product_url(gateway_api_url: str) -> str:
    return "{}/product".format(gateway_api_url.rstrip("/"))


@app.command(name="create")
def create_from_json(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Data Product name"),
    engine: str = typer.Argument(..., help="Storage engine"),
    filepath: str = typer.Argument(..., help="Filepath of the table schema json payload"),
):
    @ensure_login
    def _request(ctx: typer.Context, name: str, dpc: DataProductCreate) -> httpx.Response:
        return httpx.post(
            "{dp_url}/{name}".format(dp_url=product_url(ctx.obj.get_gateway_api_url()), name=name),
            json=dpc.dict(exclude_none=True),
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
            fields = json.load(f)
        except json.decoder.JSONDecodeError:
            send_output(
                msg="Invalid schema file, must be json format.",
                exit_code=1,
            )

    dpc = DataProductCreate(engine=engine, fields=fields)

    r = _request(ctx, name, dpc)
    process_response(r)


@app.command()
def list(ctx: typer.Context):
    @ensure_login
    def _request(ctx: typer.Context):
        return httpx.get(product_url(ctx.obj.get_gateway_api_url()), headers=bearer(ctx))

    r = _request(ctx)
    process_response(r)


@app.command()
def delete_data(ctx: typer.Context, name: str):
    @ensure_login
    def _request(ctx: typer.Context, name: str) -> httpx.Response:
        return httpx.delete(
            "{dp_url}/{name}/data".format(dp_url=product_url(ctx.obj.gateway_api_url), name=name),
            headers=bearer(ctx),
        )

    r = _request(ctx, name)
    process_response(r)


@app.command()
def delete(ctx: typer.Context, name: str):
    @ensure_login
    def _request(ctx: typer.Context, name: str) -> httpx.Response:
        return httpx.delete(
            "{dp_url}/{name}".format(dp_url=product_url(ctx.obj.gateway_api_url), name=name),
            headers=bearer(ctx),
        )

    r = _request(ctx, name)
    process_response(r)


@app.command()
def publish(ctx: typer.Context, name: str):
    @ensure_login
    def _request(ctx: typer.Context, name: str) -> httpx.Response:
        return httpx.post(
            "{dp_url}/{name}/publish".format(dp_url=product_url(ctx.obj.gateway_api_url), name=name),
            headers=bearer(ctx),
        )

    r = _request(ctx, name)
    process_response(r)


@app.command()
def unpublish(ctx: typer.Context, name: str):
    @ensure_login
    def _request(ctx: typer.Context, name: str) -> httpx.Response:
        return httpx.delete(
            "{dp_url}/{name}/publish".format(dp_url=product_url(ctx.obj.gateway_api_url), name=name),
            headers=bearer(ctx),
        )

    r = _request(ctx, name)
    process_response(r)


@app.command(name="schema")
def get_schema(ctx: typer.Context, product_name: str):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str) -> httpx.Response:
        return httpx.get(
            "{dp_url}/{name}/schema".format(dp_url=product_url(ctx.obj.gateway_api_url), name=product_name),
            headers=bearer(ctx),
        )

    r = _request(ctx, product_name)
    process_response(r)


@app.command()
def preview(
    ctx: typer.Context,
    product_name: str,
    page: typing.Optional[int] = typer.Option(1),
    page_size: typing.Optional[int] = typer.Option(10),
    filters: typing.Optional[str] = typer.Option(None, help="Filter by format is column0:operation:value;col1:op:val"),
    sort: typing.Optional[str] = typer.Option(None, help="Sort by format column0:direction;col1:dir"),
    columns: typing.Optional[str] = typer.Option(None, help="Select columns for display by format column0,col1"),
):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str, params: typing.Dict) -> httpx.Response:
        return httpx.get(
            "{product_url}/{name}".format(
                product_url=product_url(ctx.obj.gateway_api_url),
                name=product_name,
            ),
            params=params,
            headers=bearer(ctx),
        )

    params = _get_index_params(page, page_size, filters, sort, columns)

    r = _request(ctx, product_name, params)
    process_response(r)
