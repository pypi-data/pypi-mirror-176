import json
import os
import pathlib

import httpx
import typer

from neosctl import util
from neosctl.auth import ensure_login
from neosctl.schema import DataProductCreate
from neosctl.util import process_response
from neosctl.util import send_output


app = typer.Typer()


def product_url(ctx: typer.Context) -> str:
    return "{}/product".format(ctx.obj.get_gateway_api_url().rstrip("/"))


@app.command(name="create")
def create_from_json(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
    engine: str = typer.Argument(..., help="Storage engine"),
    filepath: str = typer.Argument(..., help="Filepath of the table schema json payload"),
):
    """Create a data product.
    """
    @ensure_login
    def _request(ctx: typer.Context, dpc: DataProductCreate) -> httpx.Response:
        return util.post(
            ctx,
            "{dp_url}/{name}".format(dp_url=product_url(ctx), name=name),
            json=dpc.dict(exclude_none=True),
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

    r = _request(ctx, dpc)
    process_response(r)


@app.command()
def list(ctx: typer.Context):
    """List data products.
    """
    @ensure_login
    def _request(ctx: typer.Context):
        return util.get(ctx, product_url(ctx))

    r = _request(ctx)
    process_response(r)


@app.command()
def delete_data(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Delete data from a data product.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            "{dp_url}/{name}/data".format(dp_url=product_url(ctx), name=name),
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def delete(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Delete a data product.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            "{dp_url}/{name}".format(dp_url=product_url(ctx), name=name),
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def publish(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Publish a data product.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.post(
            ctx,
            "{dp_url}/{name}/publish".format(dp_url=product_url(ctx), name=name),
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def unpublish(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Unpublish a product.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            "{dp_url}/{name}/publish".format(dp_url=product_url(ctx), name=name),
        )

    r = _request(ctx)
    process_response(r)


@app.command(name="schema")
def get_schema(
    ctx: typer.Context,
    product_name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Get data product schema.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            "{dp_url}/{name}/schema".format(dp_url=product_url(ctx), name=product_name),
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def preview(
    ctx: typer.Context,
    product_name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Preview data product data.

    Get the first 25 rows of a data product's data.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            "{product_url}/{name}".format(
                product_url=product_url(ctx),
                name=product_name,
            ),
        )

    r = _request(ctx)
    process_response(r)
