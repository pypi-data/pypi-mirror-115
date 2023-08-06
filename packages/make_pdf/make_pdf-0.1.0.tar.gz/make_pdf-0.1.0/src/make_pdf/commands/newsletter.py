from make_pdf import base, utils
from make_pdf.utils import _


from .param_extractor import (
    extract_default_parameters,
    extract_simple_param,
    extract_out_file,
)
from ..enums import DocumentType


@base.cli.command(help=_("help_message_newsletter"))
@base.default_decorators
def newsletter(
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
):
    """
    Generates as a themed newsletter. This will put all sections in boxes and sets the header to a fixed name with boxes.

    :param (list[str]) files: the input-files, which should be converted to PDF
    :param (str) theme: the name of the theme to be used
    :param (bool) draft: if the document should be generated as a draft
    :param (str) language: the name of the language to be used
    :param (str) title: the title to be used
    :param (str) author: the author to be used
    :param (str) date: the date to be used
    :param (bool) no_automatic_date: if the document should not set an automatic date as a fallback
    :param (bool) print_option: if the document should be generated for printing
    :param (list[str]) diff: the file to diff with the input-file
    :param (bool) debug_latex: whether to output debug-latex-code instead of generating a PDF
    :param (bool) verbose: whether to output verbosely
    :param (bool) no_footer: if the document shouldn't set a footer
    :param (bool) no_header: if the document shouldn't set a header
    :rtype: dict[str, Any]
    :returns: A config-object with the necessary options to generate a PDF with the given settings.
    """
    utils.echo_if_verbose("Printing verbose output!", verbose)
    processing_config = extract_simple_param("type", DocumentType.NEWSLETTER, _("message_type_is_newsletter"), verbose)
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
        extract_out_file(processing_config["files"], processing_config["type"], draft, debug_latex, verbose)
    )

    return processing_config
