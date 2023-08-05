import asyncio
import os
import sys
from functools import wraps
from typing import Any, Callable, Optional

import click
from aiohttp import ClientResponse, ClientSession
from bs4 import BeautifulSoup, ResultSet, Tag
from yaml import Loader, dump, load


def run_async(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs) -> Any:
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def _colorize(text: str, color: str) -> str:
    return click.style(str(text), fg=color)


async def _get_response(url: str, session: ClientSession) -> ClientResponse:
    resp: ClientResponse = await session.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
        },
        ssl=False,
    )
    resp.raise_for_status()
    return resp


async def _get_html(url: str, session: ClientSession) -> BeautifulSoup:
    response: ClientResponse = await _get_response(url, session)
    return BeautifulSoup(await response.text(), "html.parser")


def _read_yaml_file(file_path: str) -> str:
    with open(file_path) as f:
        content: str = f.read()
    return content


def _save_yaml_file(file_path: str, data: dict) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        content: Any = dump(data, indent=4, default_flow_style=False)
        f.write(content)


def _get_target_tag(tags: list, all_versions: bool) -> str:
    if all_versions:
        return tags[0]
    for t in tags:
        if not any(v in t for v in ("a", "b", "rc")):
            return t
    return tags[0]


async def run(dry_run: bool, all_versions: bool, verbose: bool) -> None:
    session: ClientSession = ClientSession()
    try:
        file_path: str = os.path.join(os.getcwd(), ".pre-commit-config.yaml")
        yaml_str: str = _read_yaml_file(file_path)
        data: Any = load(yaml_str, Loader)
        skip_repo: list = []
        tasks: list = []
        no_diff: list = []
        diff: list = []

        for i, repository in enumerate(data["repos"]):
            if not repository["repo"].startswith("http"):
                skip_repo.append(i)
                continue
            tasks.append(_get_html(f"{repository['repo']}/tags", session))

        results: Any = await asyncio.gather(*tasks)

        for i in range(len(data["repos"])):
            if i in skip_repo:
                continue
            rep: dict = data["repos"][i]
            hook: str = rep["repo"].split("/")[-1]
            tag_versions: list = []
            tags: Optional[ResultSet] = results[i].find_all(
                "div", class_="Box-row position-relative d-flex"
            )
            if not tags:
                raise Exception(f"No tags found for repo: {data['repos'][i]['repo']}")
            for tag in tags:
                v: Optional[Tag] = tag.find("a")
                if not v:
                    raise Exception(
                        f"No tags found for repo: {data['repos'][i]['repo']}"
                    )
                tag_versions.append(v.text)

            target_ver: str = _get_target_tag(tag_versions, all_versions)
            if rep["rev"] != target_ver:
                diff.append(
                    f"{hook} - {_colorize(rep['rev'], 'yellow')} -> {_colorize(target_ver + ' ✘', 'red')}"
                )
                data["repos"][i]["rev"] = target_ver
            else:
                no_diff.append(f"{hook} - {_colorize(rep['rev'] + ' ✔', 'green')}")

        if verbose:
            click.echo("\n".join(no_diff))

        if diff:
            click.echo("\n".join(diff))
            if not dry_run:
                _save_yaml_file(".pre-commit-config.yaml", data)
                click.echo(_colorize("Changes detected and applied", "green"))
            else:
                raise click.ClickException(_colorize("Changes detected", "red"))
        else:
            click.echo(_colorize("No changes detected", "green"))

    except Exception as ex:
        sys.exit(str(ex))

    finally:
        await session.close()


@click.command()
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    show_default=True,
    default=False,
    help="Dry run only checks for new versions",
)
@click.option(
    "-a",
    "--all-versions",
    is_flag=True,
    show_default=True,
    default=False,
    help="Include alpha/beta versions",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Display complete output",
)
@run_async
async def cli(dry_run: bool, all_versions: bool, verbose: bool):
    await run(dry_run, all_versions, verbose)


if __name__ == "__main__":
    cli()
