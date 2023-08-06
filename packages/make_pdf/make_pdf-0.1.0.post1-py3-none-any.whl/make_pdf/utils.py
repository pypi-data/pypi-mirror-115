import gettext
import os

import appdirs
import click

METADATA_FILE_TYPES = [".yml", ".yaml", ".YML", ".YAML"]
"""File types used for metadata-files."""

TEX_FILE_TYPES = [".tex", ".TEX"]
"""File types used for tex-files."""

MARKDOWN_FILE_TYPES = [".md", ".MD"]
"""File types used for md-files."""


def echo_if_verbose(output, verbose):
    """
    Echo the given output, if verbose is set.

    :param (str) output: the text to echo
    :param (bool) verbose: whether to echo the given output
    """
    if verbose:
        click.echo(output)


def get_config_dir():
    """
    Get the dir where config-files for the app are stored.
    :rtype: str
    :return: the dir where config-files for the app are stored.
    """
    return appdirs.user_config_dir("make_pdf", "EorlBruder")


def get_resources_dir():
    """
    Get the dir with the resources of this app.
    :rtype: str
    :return: the dir with the resources of this app.
    """
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "resources")


def is_metadata_file(file):
    """
    Checks whether the provided file is a metadata-file. Meaning that it is a file with a YAML-extension.

    :param (str) file: the file to check
    :rtype: bool
    :return: whether the provided file is a metadata-file.
    """
    _, ext = os.path.splitext(file)
    return ext in METADATA_FILE_TYPES


def is_tex_file(file):
    """
    Checks whether the provided file is a tex-file. Meaning that it is a file with a LaTeX-extension.

    :param (str) file: the file to check
    :rtype: bool
    :return: whether the provided file is a tex-file.
    """
    _, ext = os.path.splitext(file)
    return ext in TEX_FILE_TYPES


def is_markdown_file(file):
    """
    Checks whether the provided file is a markdown-file. Meaning that it is a file with a Markdown-extension.

    :param (str) file: the file to check
    :rtype: bool
    :return: whether the provided file is a markdown-file.
    """
    _, ext = os.path.splitext(file)
    return ext in MARKDOWN_FILE_TYPES


# Configure the gettext-setup, as to enable all files to use _ for translations.
localedir = os.path.join(get_resources_dir(), "locales")
translate = gettext.translation("base", localedir, fallback=True)
_ = translate.gettext
"""The configured translator to use for translating in this app."""
