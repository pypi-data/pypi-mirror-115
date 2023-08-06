import pathlib
from typing import List, Optional
from urllib.request import urlopen

import click
import pydantic
from click.exceptions import Exit


class FileInfo(pydantic.BaseModel):
    filename: str = pydantic.Field(..., alias="name")
    url: pydantic.HttpUrl
    download_url: Optional[pydantic.HttpUrl] = None
    size: int = pydantic.Field(..., ge=0)
    type: str

    class Config:
        allow_mutation = False

    @property
    def environment(self) -> Optional[str]:
        if self.filename.endswith(".gitignore"):
            return self.filename.removesuffix(".gitignore").lower()
        return None


def minimize_path(path: pathlib.Path) -> pathlib.Path:
    if path.is_relative_to(pathlib.Path.cwd()):
        return "." / path.relative_to(pathlib.Path.cwd())
    elif path.is_relative_to(pathlib.Path.home()):
        return "~" / path.relative_to(pathlib.Path.home())
    else:
        return path


def get_environment_file_list() -> List[FileInfo]:
    gitignore_url = "https://api.github.com/repos/github/gitignore/contents/"
    with urlopen(gitignore_url) as response:
        if response.status != 200:
            click.secho(
                f"Unable to open {response.url} ({response.status})",
                fg="red",
                err=True,
            )
            raise Exit(code=1)
        try:
            file_list = pydantic.parse_raw_as(List[FileInfo], response.read())
        except pydantic.ValidationError as e:
            click.secho(
                f"Unable to parse response from {response.url}\n\n{e}",
                fg="red",
                err=True,
            )
            raise Exit(code=1)
    return list(
        filter(
            lambda x: x.type == "file" and x.filename.endswith(".gitignore"), file_list
        )
    )
