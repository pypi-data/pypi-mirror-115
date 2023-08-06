import os

import click

from make_pdf import base, utils
from make_pdf.utils import _
from .param_extractor import extract_default_parameters, extract_simple_param, extract_out_file
from ..enums import DocumentType


@base.cli.command(help=_("help_message_letter"))
@base.default_decorators
@click.option("--to", help=_("help_message_letter_to"))
@click.option("--from", "from_option", help=_("help_message_letter_from"))
def letter(
    files,
    theme,
    draft,
    language,
    title,
    author,
    date,
    no_automatic_date,
    print_option,
    diff,
    debug_latex,
    verbose,
    no_footer,
    no_header,
    to,
    from_option,
):
    """
    Generates a letter from the document.

    :param (list[str]) files: the input-files, which should be converted to PDF
    :param (str) theme: the name of the theme to be used
    :param (bool) draft: if the document should be generated as a draft
    :param (str) language: the name of the language to be used
    :param (str) title: the title to be used
    :param (str) author: the author to be used
    :param (str) date: the date to be used
    :param (bool) no_automatic_date: if the document should not set an automatic date as a fallback
    :param (bool) print_option: if the document should be generated for printing
    :param (list[str]) diff: the files to diff with the input-file
    :param (bool) debug_latex: whether to output debug-latex-code instead of generating a PDF
    :param (bool) verbose: whether to output verbosely
    :param (bool) no_footer: if the document shouldn't set a footer
    :param (bool) no_header: if the document shouldn't set a header
    :param (str) to: the name of the file with the data for the person receiving the letter
    :param (str) from_option: the name of the file with the data for the person sending the letter
    :rtype: dict[str, Any]
    :returns: A config-object with the necessary options to generate a PDF with the given settings.
    """
    utils.echo_if_verbose("Printing verbose output!", verbose)
    processing_config = extract_simple_param("type", DocumentType.LETTER, _("message_type_is_letter"), verbose)
    processing_config.update(
        extract_default_parameters(
            files,
            theme,
            draft,
            language,
            title,
            author,
            date,
            no_automatic_date,
            print_option,
            diff,
            debug_latex,
            verbose,
            no_footer,
            no_header,
        )
    )
    processing_config.update(extract_letter_metadata(to, from_option, theme, verbose))
    processing_config.update(
        extract_out_file(processing_config["files"], processing_config["type"], draft, debug_latex, verbose)
    )

    return processing_config


def extract_letter_metadata(to, from_option, theme, verbose):
    """
    Extract the options for the letter-metadata.

    :param Optional(str) to: the name of the file with the data for the person receiving the letter
    :param Optional(str) from_option: the name of the file with the data for the person sending the letter
    :param (str) theme: the name of the theme to be used
    :param (bool) verbose: whether to output verbosely
    :rtype: dict[str, Any]
    :returns: A config-object with the necessary options to generate a PDF with the given settings.
    """
    letter_metadata = {}
    if to:
        to_file = extract_to_file(to)
        if not to_file:
            raise click.BadParameter(_("error_to_file_not_found"))
        letter_metadata.update({"to": to_file})
        utils.echo_if_verbose(_("message_to_metadata_set").format(to_file), verbose)

    from_file = extract_from_file(from_option, theme)
    if not from_file:
        raise click.BadParameter(_("error_from_file_not_found"))
    letter_metadata.update({"from": from_file})
    utils.echo_if_verbose(_("message_from_metadata_set").format(from_file), verbose)
    return letter_metadata


def extract_to_file(to):
    """
    Extract the corresponding to-file  Might be referencing a yaml or tex-file directly or in the config-dir.

    :param (str) to: the to-files name or identifier.
    :rtype: str
    :return: the path to the from-file
    """
    if (utils.is_metadata_file(to) or utils.is_tex_file(to)) and os.path.exists(to):
        return to
    result = os.path.join(utils.get_config_dir(), to + "-to.yml")
    if os.path.exists(result):
        return result
    result = os.path.join(utils.get_config_dir(), to + "-to.tex")
    if os.path.exists(result):
        return result


def extract_from_file(from_option, theme):
    """
    Extract the corresponding to-file  Might be referencing a yaml or tex-file directly or in the config-dir. Falls
    back to checking whether a from-file with this theme-name exists.

    :param (str) from_option: the from-files name or identifier.
    :param (str) theme: the theme name to fall back to.
    :rtype: str
    :return: the path to the from-file
    """
    if from_option:
        if (utils.is_metadata_file(from_option) or utils.is_tex_file(from_option)) and os.path.exists(from_option):
            return from_option
        result = os.path.join(utils.get_config_dir(), from_option + "-from.yml")
        if os.path.exists(result):
            return result
        result = os.path.join(utils.get_config_dir(), from_option + "-from.tex")
        if os.path.exists(result):
            return result
    result = os.path.join(utils.get_config_dir(), theme + "-from.yml")
    if os.path.exists(result):
        return result
    result = os.path.join(utils.get_config_dir(), theme + "-from.tex")
    if os.path.exists(result):
        return result
