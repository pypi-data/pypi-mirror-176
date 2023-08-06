import pathlib
import typing

import httpx
import typer

from neosctl.auth import ensure_login
from neosctl.util import bearer
from neosctl.util import process_response
from neosctl.util import send_output


app = typer.Typer()
secret_app = typer.Typer()
app.add_typer(secret_app, name="secret")


def spark_url(name: str, gateway_api_url: str) -> str:
    return "{}/spark/{}".format(gateway_api_url.rstrip("/"), name)


def secret_url(name: str, gateway_api_url: str) -> str:
    return "{}/secret/{}".format(gateway_api_url.rstrip("/"), name)


@app.command()
def add_job(
    ctx: typer.Context,
    product_name: str,
    job_filepath: str = typer.Option(..., "--job-filepath", "-f"),
    docker_tag: str = typer.Option("v0.1.34", "--docker-tag", "-d"),
    executor_cores: int = typer.Option(1, "--executor-cores", "-ec"),
    executor_instances: int = typer.Option(1, "--executor-instances", "-ei"),
    executor_memory: str = typer.Option("512m", "--executor-memory", "-em"),
    driver_cores: int = typer.Option(1, "--driver-cores", "-dc"),
    driver_core_limit: str = typer.Option("1200m", "--driver-core-limit", "-dcl"),
    driver_memory: str = typer.Option("512m", "--driver-memory", "-dm"),
    spark_version: str = typer.Option("3.1.1", "--spark-version", "-sv"),
):
    @ensure_login
    def _request(
        ctx: typer.Context,
        product_name: str,
        f: typing.IO,
        docker_tag: str,
        executor_cores: int,
        executor_instances: int,
        executor_memory: str,
        driver_cores: int,
        driver_core_limit: str,
        driver_memory: str,
        spark_version: str,
    ) -> httpx.Response:
        return httpx.post(
            spark_url(product_name, ctx.obj.gateway_api_url),
            params={
                "docker_tag": docker_tag,
                "executor_cores": executor_cores,
                "executor_instances": executor_instances,
                "executor_memory": executor_memory,
                "driver_cores": driver_cores,
                "driver_core_limit": driver_core_limit,
                "driver_memory": driver_memory,
                "spark_version": spark_version,
            },
            files={"python_file": f},
            headers=bearer(ctx),
        )

    fp = pathlib.Path(job_filepath)
    if not fp.exists():
        send_output(
            msg="Can not find file: {}".format(fp),
            exit_code=1,
        )

    with fp.open("rb") as f:
        r = _request(
            ctx,
            product_name,
            f,
            docker_tag,
            executor_cores,
            executor_instances,
            executor_memory,
            driver_cores,
            driver_core_limit,
            driver_memory,
            spark_version,
        )

    process_response(r)


@app.command()
def job_status(ctx: typer.Context, product_name: str):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str) -> httpx.Response:
        return httpx.get(
            "{spark_url}".format(spark_url=spark_url(product_name, ctx.obj.gateway_api_url)),
            headers=bearer(ctx),
        )
    r = _request(ctx, product_name)

    process_response(r)


def render_logs(payload: typing.Dict):
    return "\n".join(payload["logs"])


@app.command()
def job_logs(ctx: typer.Context, product_name: str):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str) -> httpx.Response:
        return httpx.get(
            "{spark_url}/log".format(spark_url=spark_url(product_name, ctx.obj.gateway_api_url)),
            headers=bearer(ctx),
        )
    r = _request(ctx, product_name)

    process_response(r, render_logs)


@app.command()
def update_job(
    ctx: typer.Context,
    product_name: str,
    job_filepath: str = typer.Option(None, "--job-filepath", "-f"),
    docker_tag: str = typer.Option(None, "--docker-tag", "-d"),
    executor_cores: int = typer.Option(None, "--executor-cores", "-ec"),
    executor_instances: int = typer.Option(None, "--executor-instances", "-ei"),
    executor_memory: str = typer.Option(None, "--executor-memory", "-em"),
    driver_cores: int = typer.Option(None, "--driver-cores", "-dc"),
    driver_core_limit: str = typer.Option(None, "--driver-core-limit", "-dcl"),
    driver_memory: str = typer.Option(None, "--driver-memory", "-dm"),
    spark_version: str = typer.Option(None, "--spark-version", "-sv"),
):
    @ensure_login
    def _request(
        ctx: typer.Context,
        product_name: str,
        f: typing.Optional[typing.IO],
        docker_tag: typing.Optional[str],
        executor_cores: typing.Optional[int],
        executor_instances: typing.Optional[int],
        executor_memory: typing.Optional[str],
        driver_cores: typing.Optional[int],
        driver_core_limit: typing.Optional[str],
        driver_memory: typing.Optional[str],
        spark_version: typing.Optional[str],
    ) -> httpx.Response:
        params = {
            k: v
            for k, v in [
                ("docker_tag", docker_tag),
                ("executor_cores", executor_cores),
                ("executor_instances", executor_instances),
                ("executor_memory", executor_memory),
                ("driver_cores", driver_cores),
                ("driver_core_limit", driver_core_limit),
                ("driver_memory", driver_memory),
                ("spark_version", spark_version),
            ]
            if v is not None
        }
        files = {"python_file": f} if f else {}

        return httpx.put(
            spark_url(product_name, ctx.obj.gateway_api_url),
            params=params,
            files=files,
            headers=bearer(ctx),
        )

    if job_filepath:
        fp = pathlib.Path(job_filepath)
        if not fp.exists():
            send_output(
                msg="Can not find file: {}".format(fp),
                exit_code=1,
            )
    args = [
        docker_tag,
        executor_cores,
        executor_instances,
        executor_memory,
        driver_cores,
        driver_core_limit,
        driver_memory,
        spark_version,
    ]
    if job_filepath:
        with fp.open("rb") as f:
            r = _request(ctx, product_name, f, *args)
    else:
        r = _request(ctx, product_name, None, *args)

    process_response(r)


@app.command()
def remove_job(ctx: typer.Context, product_name: str):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str) -> httpx.Response:
        return httpx.delete(
            spark_url(product_name, ctx.obj.gateway_api_url),
            headers=bearer(ctx),
        )

    r = _request(ctx, product_name)
    process_response(r)


@app.command()
def trigger_job(ctx: typer.Context, product_name: str):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str) -> httpx.Response:
        return httpx.post(
            "{spark_url}/trigger".format(spark_url=spark_url(product_name, ctx.obj.gateway_api_url)),
            headers=bearer(ctx),
        )

    r = _request(ctx, product_name)
    process_response(r)


@app.command()
def schedule_job(
    ctx: typer.Context,
    product_name: str = typer.Option(..., "--product-name", "-pn"),
    schedule: str = typer.Option(..., "--schedule", "-s", help='Schedule in crontab format (e.g. "* * * * *")'),
):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str, cron_expression: str) -> httpx.Response:
        return httpx.post(
            "{spark_url}/scheduled".format(spark_url=spark_url(product_name, ctx.obj.gateway_api_url)),
            json={
                "cron_expression": cron_expression,
            },
            headers=bearer(ctx),
        )

    r = _request(ctx, product_name, schedule)
    process_response(r)


@secret_app.command()
def add(
    ctx: typer.Context,
    product_name: str,
    secrets: typing.List[str] = typer.Option(..., "--secret", "-s", help="Secret in the form key:value"),
):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str, payload: typing.Dict) -> httpx.Response:
        return httpx.post(
            secret_url(product_name, ctx.obj.gateway_api_url),
            json=payload,
            headers=bearer(ctx),
        )
    payload = {"data": {}}
    for s in secrets:
        name, value = s.split(":")
        payload["data"][name] = value

    r = _request(ctx, product_name, payload)

    process_response(r)


@secret_app.command()
def update(
    ctx: typer.Context,
    product_name: str,
    secrets: typing.List[str] = typer.Option(..., "--secret", "-s", help="Secret in the form key:value"),
):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str, payload: typing.Dict) -> httpx.Response:
        return httpx.patch(
            secret_url(product_name, ctx.obj.gateway_api_url),
            json=payload,
            headers=bearer(ctx),
        )
    payload = {"data": {}}
    for s in secrets:
        name, value = s.split(":")
        payload["data"][name] = value

    r = _request(ctx, product_name, payload)

    process_response(r)


@secret_app.command()
def remove(
    ctx: typer.Context,
    product_name: str,
):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str) -> httpx.Response:
        return httpx.delete(
            secret_url(product_name, ctx.obj.gateway_api_url),
            headers=bearer(ctx),
        )

    r = _request(ctx, product_name)

    process_response(r)


@secret_app.command()
def remove_key(
    ctx: typer.Context,
    product_name: str,
    keys: typing.List[str] = typer.Option(..., "--key", "-k", help="Key name you wish to remove from secret"),
):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str, keys: typing.List[str]) -> httpx.Response:
        return httpx.request(
            "DELETE",
            "{secret_url}/key".format(secret_url=secret_url(product_name, ctx.obj.gateway_api_url)),
            json={"keys": keys},
            headers=bearer(ctx),
        )

    r = _request(ctx, product_name, keys)

    process_response(r)


@secret_app.command()
def get(
    ctx: typer.Context,
    product_name: str,
):
    @ensure_login
    def _request(ctx: typer.Context, product_name: str) -> httpx.Response:
        return httpx.get(
            secret_url(product_name, ctx.obj.gateway_api_url),
            headers=bearer(ctx),
        )

    r = _request(ctx, product_name)

    process_response(r)
