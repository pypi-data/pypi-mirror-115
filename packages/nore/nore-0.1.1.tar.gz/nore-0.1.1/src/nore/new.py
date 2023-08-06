import pathlib
from typing import Optional
from urllib.request import urlopen

import click

from .util import get_environment_file_list, minimize_path


def get_download_url(environment: str) -> Optional[str]:
    language_file_list = get_environment_file_list()
    for language_file in language_file_list:
        if language_file.environment.lower() == environment.lower():
            return language_file.download_url
    click.secho(f"{environment} not found in available options")
    raise click.Abort()


def download_gitignore(
    environment: str,
    output_path: pathlib.Path,
    output_filename: str = ".gitignore"
):
    download_url = get_download_url(environment)
    with urlopen(download_url) as response, open(
        output_path / output_filename, "w"
    ) as file:
        if response.status == 200:
            content = response.read().decode("utf-8")
            try:
                file.write(content)
                click.secho(
                    f"Created .gitignore at {minimize_path(output_path / output_filename)}",
                    fg="green",
                )
            except OSError:
                click.secho("Error: Unable to write file", fg="red", err=True)
                click.Abort()
        else:
            click.secho("Error: Unable to download content", fg="red", err=True)
            click.Abort()
