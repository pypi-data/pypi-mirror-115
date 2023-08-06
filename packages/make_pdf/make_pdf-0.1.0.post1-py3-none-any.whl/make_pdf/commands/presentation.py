import click

from make_pdf import base, utils
from make_pdf.utils import _
from .param_extractor import extract_default_parameters, extract_simple_param, extract_out_file
from ..enums import DocumentType


@base.cli.command(help=_("help_message_presentation"))
@base.default_decorators
@click.option("--aspect-ratio", help=_("help_message_presentation_aspect_ration"), default="169")
def presentation(
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
    aspect_ratio,
):
    """
    Generates a presentation from the document.

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
    :param (str) aspect_ratio: the name of the aspect-ratio to be used for the presentation
    :rtype: dict[str, Any]
    :returns: A config-object with the necessary options to generate a PDF with the given settings.
    """
    utils.echo_if_verbose("Printing verbose output!", verbose)
    processing_config = extract_simple_param(
        "type", DocumentType.PRESENTATION, _("message_type_is_presentation"), verbose
    )
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
    processing_config.update(
        extract_simple_param("aspect_ratio", aspect_ratio, _("aspect_ratio_is_set").format(aspect_ratio), verbose)
    )
    processing_config.update(
        extract_out_file(processing_config["files"], processing_config["type"], draft, debug_latex, verbose)
    )

    return processing_config
