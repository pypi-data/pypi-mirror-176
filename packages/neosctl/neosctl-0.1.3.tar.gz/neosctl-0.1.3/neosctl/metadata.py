import httpx
import typer

from neosctl.auth import ensure_login
from neosctl.util import bearer
from neosctl.util import process_response


app = typer.Typer()


def metadata_url(ctx: typer.Context, postfix: str = "") -> str:
    return "{}/metadata{}".format(ctx.obj.get_gateway_api_url().rstrip("/"), postfix)


@app.command()
def product(ctx: typer.Context, product_name: str):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str) -> httpx.Response:
        return httpx.get(
            metadata_url(ctx, "/product/{}".format(product_name)),
            headers=bearer(ctx),
        )
    r = _request(ctx, product_name)

    process_response(r)


@app.command()
def add_tag(ctx: typer.Context, tag: str):
    @ensure_login
    def _request(ctx: typer.Context, tag: str) -> httpx.Response:
        return httpx.post(
            metadata_url(ctx, "/tag"),
            json={
                "tag": tag.lower(),
            },
            headers=bearer(ctx),
        )
    r = _request(ctx, tag)

    process_response(r)


@app.command()
def remove_tag(ctx: typer.Context, tag: str):
    @ensure_login
    def _request(ctx: typer.Context, tag: str) -> httpx.Response:
        return httpx.request(
            method="DELETE",
            url=metadata_url(ctx, "/tag"),
            json={
                "tag": tag.lower(),
            },
            headers=bearer(ctx),
        )
    r = _request(ctx, tag)

    process_response(r)


@app.command()
def list_tags(
    ctx: typer.Context,
    tag_filter: str = typer.Option(None, "--tag-filter", "-t"),
):
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        params = {}
        if tag_filter:
            params["tag_filter"] = tag_filter
        return httpx.get(
            url=metadata_url(ctx, "/tag"),
            params=params,
            headers=bearer(ctx),
        )
    r = _request(ctx)

    process_response(r)


@app.command()
def browse(ctx: typer.Context):
    """
    List source types.
    """
    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return httpx.get(
            url=metadata_url(ctx, "/browse"),
            headers=bearer(ctx),
        )
    r = _request(ctx)

    process_response(r)


@app.command()
def browse_databases(
    ctx: typer.Context,
    source_type: str = typer.Option(..., "--source-type", "-s"),
):
    """
    List databases by source type.
    """
    @ensure_login
    def _request(ctx: typer.Context, source_type: str) -> httpx.Response:
        return httpx.get(
            url=metadata_url(ctx, "/browse/{}".format(source_type)),
            headers=bearer(ctx),
        )
    r = _request(ctx, source_type)

    process_response(r)


@app.command()
def browse_datasets(
    ctx: typer.Context,
    source_type: str = typer.Option(..., "--source-type", "-s"),
    database: str = typer.Option(..., "--database", "-d"),
):
    """
    List datasets by source type and database.
    """
    @ensure_login
    def _request(ctx: typer.Context, source_type: str, database: str) -> httpx.Response:
        return httpx.get(
            url=metadata_url(ctx, "/browse/{}/{}".format(source_type, database)),
            headers=bearer(ctx),
        )
    r = _request(ctx, source_type, database)

    process_response(r)


@app.command()
def browse_dataset_metadata(
    ctx: typer.Context,
    source_type: str = typer.Option(..., "--source-type", "-s"),
    database: str = typer.Option(..., "--database", "-d"),
    dataset_urn: str = typer.Option(..., "--dataset-urn", "-du"),
):
    """
    Get dataset metadata by source type, database and dataset urn.
    """
    @ensure_login
    def _request(ctx: typer.Context, source_type: str, database: str, dataset_urn: str) -> httpx.Response:
        return httpx.get(
            url=metadata_url(ctx, "/browse/{}/{}/{}".format(source_type, database, dataset_urn)),
            headers=bearer(ctx),
        )
    r = _request(ctx, source_type, database, dataset_urn)

    process_response(r)


@app.command()
def add_pipeline(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", "-n"),
    schedule: str = typer.Option(
        ..., "--schedule", "-s", help='Pipeline schedule in crontab format (e.g. "* * * * *")',
    ),
    schedule_timezone: str = typer.Option(..., "--schedule-timezone", "-st"),
    source: str = typer.Option(
        ..., "--source", "-sr", help="Data source DSN (e.g. mysql://user:pass@host:3306/dbname)",
    ),
    include_tables: bool = typer.Option(True, "--include-tables", "-it", help="Applies only to relational DBs"),
    include_views: bool = typer.Option(True, "--include-views", "-iv", help="Applies only to relational DBs"),
):
    """
    Add an ingestion pipeline.
    """
    source_url = httpx.URL(source)
    request_data = {
        "pipeline_type": source_url.scheme,
        "pipeline_name": name,
        "schedule": schedule,
        "schedule_timezone": schedule_timezone,
        "source": {
            "host": source_url.netloc.decode(),
            "database": source_url.path.lstrip("/"),
            "username": source_url.username,
            "password": source_url.password,
            "include_tables": include_tables,
            "include_views": include_views,
        },
    }

    @ensure_login
    def _request(ctx: typer.Context, data: dict) -> httpx.Response:
        return httpx.post(
            metadata_url(ctx, "/pipeline"),
            json=data,
            headers=bearer(ctx),
        )
    r = _request(ctx, request_data)

    process_response(r)


@app.command()
def remove_pipeline(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", "-n"),
):
    """
    Remove an ingestion pipeline.
    """

    @ensure_login
    def _request(ctx: typer.Context, pipeline_name: dict) -> httpx.Response:
        return httpx.request(
            "DELETE",
            metadata_url(ctx, "/pipeline"),
            json={
                "pipeline_name": pipeline_name,
            },
            headers=bearer(ctx),
        )
    r = _request(ctx, name)

    process_response(r)


@app.command()
def product_description(
    ctx: typer.Context,
    product_name: str = typer.Option(..., "--product-name", "-p"),
    description: str = typer.Option(..., "--description", "-d"),
):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str, description: str) -> httpx.Response:
        return httpx.post(
            metadata_url(ctx, "/product/{}/description".format(product_name)),
            json={
                "description": description,
            },
            headers=bearer(ctx),
        )
    r = _request(ctx, product_name, description)

    process_response(r)


@app.command()
def product_field_tag(
    ctx: typer.Context,
    product_name: str = typer.Option(..., "--product-name", "-p"),
    field: str = typer.Option(..., "--field", "-f"),
    tag: str = typer.Option(..., "--tag", "-t"),
):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str, field: str, tag: str) -> httpx.Response:
        return httpx.post(
            metadata_url(ctx, "/product/{}/{}/tag".format(product_name, field)),
            json={
                "tag": tag.lower(),
            },
            headers=bearer(ctx),
        )
    r = _request(ctx, product_name, field, tag)

    process_response(r)


@app.command()
def product_field_description(
    ctx: typer.Context,
    product_name: str = typer.Option(..., "--product-name", "-p"),
    field: str = typer.Option(..., "--field", "-f"),
    description: str = typer.Option(..., "--description", "-d"),
):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str, field: str, description: str) -> httpx.Response:
        return httpx.post(
            metadata_url(ctx, "/product/{}/{}/description".format(product_name, field)),
            json={
                "description": description,
            },
            headers=bearer(ctx),
        )
    r = _request(ctx, product_name, field, description)

    process_response(r)
