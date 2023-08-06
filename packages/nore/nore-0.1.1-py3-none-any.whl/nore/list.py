import itertools
import math
import os
from typing import List

import click

from .util import get_environment_file_list


def get_printable_environment_list_lines(
    language_list: List[str], min_space=2, max_space=5
):
    max_word_length = max([len(language) for language in language_list])
    word_spacing = (os.get_terminal_size().columns - min_space) % max_word_length
    word_spacing = max(min(word_spacing, max_space), min_space)
    cols = int(
        (os.get_terminal_size().columns - min_space) / (max_word_length + word_spacing)
    )
    rows = int(math.ceil(len(language_list) / cols))
    transformed_list = itertools.zip_longest(
        *[language_list[i : i + rows] for i in range(0, len(language_list), rows)],
        fillvalue="",
    )
    return [
        (" " * word_spacing).join(
            map(
                lambda x: f"{x:{max_word_length}}",
                row,
            )
        )
        for row in transformed_list
    ]


def print_environment_list():
    language_list = sorted(map(lambda x: x.environment, get_environment_file_list()))
    for line in get_printable_environment_list_lines(language_list):
        click.secho(line, fg="green")
