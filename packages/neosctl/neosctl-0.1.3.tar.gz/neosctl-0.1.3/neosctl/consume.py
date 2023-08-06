import typing

import httpx
import typer

from neosctl.auth import ensure_login
from neosctl.util import _get_index_params
from neosctl.util import bearer
from neosctl.util import process_response


app = typer.Typer()


def consume_url(gateway_api_url: str) -> str:
    return "{}/consume".format(gateway_api_url.rstrip("/"))


@app.command()
def query(
    ctx: typer.Context,
    statement: str,
):
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return httpx.post(
            url=consume_url(ctx.obj.gateway_api_url),
            json={
                "statement": statement,
            },
            headers=bearer(ctx),
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def product(
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
            "{consume_url}/{name}".format(
                consume_url=consume_url(ctx.obj.gateway_api_url),
                name=product_name,
            ),
            params=params,
            headers=bearer(ctx),
        )

    params = _get_index_params(page, page_size, filters, sort, columns)

    r = _request(ctx, product_name, params)
    process_response(r)
