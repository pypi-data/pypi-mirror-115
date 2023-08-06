import os

import click
import pypandoc

from make_pdf import utils
from make_pdf.constants import LETTER_METADATA_FILE
from make_pdf.converters import base_arg_generator
from make_pdf.converters import letter_arg_generator
from make_pdf.converters import plain_and_newsletter_arg_generator
from make_pdf.converters import presentation_arg_generator
from make_pdf.enums import DocumentType
from make_pdf.utils import _


def convert_file(file, options):
    """
    Convert the input-file to a PDF with the given options.

    :param (str) file: the file to convert
    :param (dict[str, Any]) options: the given options to convert the file
    """
    pandoc_args = generate_pandoc_args(options)
    utils.echo_if_verbose(str(pandoc_args), options["verbose"])

    if options["type"] == DocumentType.LETTER:
        letter_arg_generator.generate_letter_vars_file(file, options)

    old_locale = os.environ.get("LANG")
    os.environ["LANG"] = options["language"].value["locale"]
    utils.echo_if_verbose(_("message_set_locale_to").format(os.environ["LANG"]), options["verbose"])

    exit_code = 0

    try:
        if options["debug_latex"]:
            output = pypandoc.convert_text(file, "latex", "md", extra_args=pandoc_args)
            click.echo(output)
        else:
            click.echo(_("message_writing_file").format(options["out_file"]))
            pypandoc.convert_text(file, "pdf", "md", outputfile=options["out_file"], extra_args=pandoc_args)
    except RuntimeError as e:
        click.echo(e.args[0], err=True)
        exit_code = 1
    finally:
        if os.path.exists(LETTER_METADATA_FILE):
            os.remove(LETTER_METADATA_FILE)
        os.environ["LANG"] = old_locale
    return exit_code


def generate_pandoc_args(options):
    """
    Generate a list with the args to be passed to pandoc.

    :param (dict[str, Any]) options: the given options to convert the file
    :return: a list with all args to be passed to pandoc
    :rtype: list[str]
    """
    result = base_arg_generator.generate_default_args(options)
    if options["type"] == DocumentType.PLAIN or options["type"] == DocumentType.NEWSLETTER:
        result.extend(plain_and_newsletter_arg_generator.generate_plain_and_newsletter_args(options))
    elif options["type"] == DocumentType.LETTER:
        result.extend(letter_arg_generator.generate_letter_args(options))
    elif options["type"] == DocumentType.PRESENTATION:
        result.extend(presentation_arg_generator.generate_presentation_args(options))
    result.extend(["-H", os.path.join(utils.get_resources_dir(), "tex/final-hook.tex")])
    return result
