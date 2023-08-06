import click

from make_pdf import base, utils
from make_pdf.utils import _
from .param_extractor import (
    extract_default_parameters,
    extract_simple_param,
    extract_out_file,
)
from ..enums import DocumentType


@base.cli.command(help=_("help_message_plain"))
@base.default_decorators
@base.TITLE_PAGE_DECORATOR
@base.NO_TOC_DECORATOR
@base.TWO_COLUMNS_DECORATOR
@click.option("--short", "-s", is_flag=True, default=False, help=_("help_message_plain_short"))
@click.option("--legal", is_flag=True, default=False, help=_("help_message_plain_legal"))
def plain(
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
    title_page,
    no_toc,
    two_columns,
    short,
    legal,
):
    """
    Generate a plain document, for example for a report or an article.

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
    :param (bool) title_page: if the document should generated a title-page
    :param (bool) no_toc: if the document should generate a table of contents
    :param (bool) two_columns: whether the document should be formatted with two columns
    :param (bool) short: whether the document should use a short-layout
    :param (bool) legal: whether '§' should be added to all section-titles
    :rtype: dict[str, Any]
    :returns: A config-object with the necessary options to generate a PDF with the given settings.
    """
    utils.echo_if_verbose("Printing verbose output!", verbose)
    processing_config = extract_simple_param("type", DocumentType.PLAIN, _("message_type_is_plain"), verbose)
    # The following code will be the same as in plain, which is okay in this case.
    # noinspection DuplicatedCode
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
        extract_simple_param("title_page", title_page, _("message_title_page_will_be_generated"), verbose)
    )
    processing_config.update(extract_simple_param("no_toc", no_toc, _("message_no_toc_will_be_generated"), verbose))
    processing_config.update(
        extract_simple_param("two_columns", two_columns, _("message_two_columns_layout_will_be_used"), verbose)
    )
    processing_config.update(extract_simple_param("short", short, _("message_short_is_set"), verbose))
    processing_config.update(extract_simple_param("legal", legal, _("message_legal_is_set"), verbose))
    processing_config.update(
        extract_out_file(processing_config["files"], processing_config["type"], draft, debug_latex, verbose)
    )

    return processing_config
