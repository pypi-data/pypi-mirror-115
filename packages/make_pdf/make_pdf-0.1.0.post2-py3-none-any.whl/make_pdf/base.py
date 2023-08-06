import click

from .converters import file_converter
from .preprocessors import file_stitcher, diff_preprocessor, criticmarkup_preprocessor
from .utils import _

HELP_DECORATOR = click.help_option("-h", "--help", help=_("help_message_default"))
"""The decorator for the help-function"""

NO_TOC_DECORATOR = click.option("--no-toc", help=_("help_message_no_toc"), is_flag=True, default=False)
"""The decorator for commands offering a no-toc-option to disable the table-of-contents"""

TWO_COLUMNS_DECORATOR = click.option(
    "--two-columns", "-2", help=_("help_message_two_columns"), is_flag=True, default=False
)
"""The decorator for commands offering a two-column-mode, to display the text in two columns."""

TITLE_PAGE_DECORATOR = click.option("--title-page", help=_("help_message_title_page"), is_flag=True, default=False)
"""The decorator for commands offering the generation of a title-page."""


def default_decorators(func):
    """
    Creates the default decorators used by all commands.

    :param (function) func: the function called
    :rtype: function
    :returns: a decorator which applies all default decorators
    """
    files = click.argument("files", nargs=-1, type=click.Path(exists=True), required=True)
    theme = click.option("-t", "--theme", default="default", help=_("help_message_theme"))
    draft = click.option("-d", "--draft", default=False, is_flag=True, help=_("help_message_draft"))
    language = click.option("-l", "--language", default="german", help=_("help_message_language"))
    title = click.option("--title", help=_("help_message_title"))
    author = click.option("--author", help=_("help_message_author"))
    date = click.option("--date", help=_("help_message_date"))
    no_automatic_date = click.option(
        "--no-automatic-date", is_flag=True, default=False, help=_("help_message_no_automatic_date")
    )
    print_option = click.option("--print", "print_option", is_flag=True, default=False, help=_("help_message_print"))
    diff = click.option("--diff", help=_("help_message_diff"), type=click.Path(exists=True), multiple=True)
    debug_latex = click.option("--debug-latex", help=_("help_message_debug_latex"), is_flag=True, default=False)
    verbose = click.option("--verbose", help=_("help_message_verbose"), is_flag=True, default=False)
    no_footer = click.option("--no-footer", help=_("help_message_no_footer"), is_flag=True, default=False)
    no_header = click.option("--no-header", help=_("help_message_no_header"), is_flag=True, default=False)
    # Decorators are functions calling other functions. So to combine them, I need to compose all previously defined
    # decorators.
    return title(
        author(
            date(
                no_automatic_date(
                    print_option(
                        diff(
                            debug_latex(
                                verbose(no_footer(no_header(language(draft(files(theme(HELP_DECORATOR(func))))))))
                            )
                        )
                    )
                )
            )
        )
    )


@click.group(help=_("help_message_cli"))
@HELP_DECORATOR
def cli():
    """
    Base command for the make_pdf-tool. Needs to use a sub-command for further processing.
    """
    pass


@cli.result_callback()
def process_result(options):
    """
    Processes the result of the used subcommand. The returned file_options are used to generate the resulting PDF.

    :param (dict) options: the config-object returned by the used sub-command
    """
    verbose = options["verbose"]
    stitched_file = file_stitcher.stitch_files_together(options["files"], verbose)
    if options["should_diff"]:
        diff_file = file_stitcher.stitch_files_together(
            options["diff_files"], verbose, _("message_stitching_diff_files_together")
        )
        diffed_file = diff_preprocessor.diff_files(stitched_file, diff_file, verbose)
    else:
        diffed_file = stitched_file
    preprocessed_file = criticmarkup_preprocessor.preprocess_criticmarkup(diffed_file, verbose)
    exit_code = file_converter.convert_file(preprocessed_file, options)
    exit(exit_code)
