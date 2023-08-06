import os

from click import BadArgumentUsage, BadParameter

from make_pdf import utils
from make_pdf.enums import Language
from make_pdf.utils import _, METADATA_FILE_TYPES


def extract_default_parameters(
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
    Extract the default parameters and create a dict from their resulting options.

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
    :rtype: dict[str, Any]
    :returns: A config-object with the necessary options to generate a PDF with the given default parameters.
    """
    default_processing_config = {}
    default_processing_config.update(extract_files(files))
    default_processing_config.update(extract_theme_file(theme, verbose))
    default_processing_config.update(extract_language(language, verbose))
    default_processing_config.update(extract_simple_param("draft", draft, _("message_set_to_draft"), verbose))
    default_processing_config.update(
        extract_simple_param("title", title, _("message_using_title").format(title), verbose)
    )
    default_processing_config.update(
        extract_simple_param("author", author, _("message_using_author").format(author), verbose)
    )
    default_processing_config.update(extract_simple_param("date", date, _("message_using_date").format(date), verbose))
    default_processing_config.update(
        extract_simple_param(
            "no_automatic_date", no_automatic_date, _("message_no_automatic_date_will_be_set"), verbose
        )
    )
    default_processing_config.update(
        extract_simple_param("print", print_option, _("message_generate_for_printing"), verbose)
    )
    default_processing_config.update(extract_diff_files(diff, verbose))
    default_processing_config.update(
        extract_simple_param("debug_latex", debug_latex, _("message_only_debug_latex"), verbose)
    )
    default_processing_config.update(
        extract_simple_param("no_footer", no_footer, _("message_generate_no_footer"), verbose)
    )
    default_processing_config.update(
        extract_simple_param("no_header", no_header, _("message_generate_no_header"), verbose)
    )
    default_processing_config.update(extract_simple_param("verbose", verbose, verbose=verbose))
    return default_processing_config


def extract_files(files):
    """
    Extract the files from the input-files and create a dict with them.

    :param (list[str]) files: the input-files, which should be converted to PDF
    :returns: A config-object with the necessary options to generate a PDF with the given files.
    :rtype: dict(str, list[str])
    """
    content_files, metadata_files = divide_files_in_categories(files)
    if not content_files:
        raise BadArgumentUsage(_("error_no_content_files"))
    return {"files": content_files, "metadata_files": metadata_files}


def extract_diff_files(diff, verbose=False):
    """
    Extract the files from the input-files and create a dict with them.

    :param (list[str]) diff: the input-files, which should be diffed with the files
    :param (bool) verbose: whether to output verbosely
    :returns: A config-object with the necessary options to generate a PDF with the given diff-files.
    :rtype: dict(str, Any)
    """
    content_files, metadata_files = divide_files_in_categories(diff)
    if diff and not content_files:
        raise BadParameter(_("error_no_diff_content_files"))
    should_diff = False
    if diff:
        should_diff = True
        utils.echo_if_verbose(_("message_diffing_with_file"), verbose)
    return {"diff_files": content_files, "diff_metadata_files": metadata_files, "should_diff": should_diff}


def extract_simple_param(key, param, log_message=None, verbose=False):
    """
    Extract the given simple parameter and create a dict with the given key and the param as a value for it.

    :param (str) key: the key to set this param for in the dict
    :param (Any) param: the parameter to set into the dict
    :param (str) log_message: the log-message to output
    :param (bool) verbose: whether to output verbosely
    :rtype: dict[str, Any]
    :returns: A config-object with the necessary options to generate a PDF with the given parameter.
    """
    if param:
        utils.echo_if_verbose(log_message, verbose)
    return {key: param}


def divide_files_in_categories(files):
    """
    Divide the input-files into content and metadata-files.

    :param (list[str]) files: the input-files, which should be converted to PDF
    :rtype: tuple[list[str], list[str]]
    :return: the input-files divided into metadata-files and content-files
    """
    content_files = []
    metadata_files = []
    for file in files:
        _, ext = os.path.splitext(file)
        if ext in METADATA_FILE_TYPES:
            metadata_files.append(file)
        else:
            content_files.append(file)
    return content_files, metadata_files


def extract_theme_file(theme, verbose=False):
    """
    Extract the file-path of the provided theme.

    :param (str) theme: the name of the theme
    :param (bool) verbose: whether to output verbosely
    :rtype: dict[str, str]
    :return: a dict with the resulting options for this theme
    :raise BadParameter: if the given theme doesn't exist
    """
    if theme == "default":
        theme_file = os.path.join(utils.get_resources_dir(), "tex/default-header.tex")
    else:
        theme_file = os.path.join(utils.get_config_dir(), theme + "-header.tex")

    if not os.path.exists(theme_file):
        raise BadParameter(_("error_theme_not_existing"))
    utils.echo_if_verbose(_("message_using_theme").format(theme), verbose)

    return {"theme": theme, "theme_file": theme_file}


def extract_language(language, verbose=False):
    """
    Extract the enum for the given language.

    :param (str) language: the name of the language
    :param (bool) verbose: whether to output verbosely
    :rtype: dict[str, Language]
    :return: a dict with the resulting options for this language
    :raise BadParameter: if the given language isn't supported
    """
    language_enum = None
    for lang in Language:
        if language in lang.value["valid_inputs"]:
            language_enum = lang
            break

    if not language_enum:
        raise BadParameter(_("error_language_not_supported"))
    utils.echo_if_verbose(_("message_language_used").format(language_enum.value["language"]), verbose)

    return {"language": language_enum}


def extract_out_file(files, type_option, draft, debug_latex, verbose=False):
    base_name = os.path.splitext(files[0])[0]
    if debug_latex:
        return {}
    if draft:
        out_file = "{base_name}-draft.pdf".format(base_name=base_name)
    else:
        type_suffix = type_option.value
        out_file = "{base_name}-{suffix}.pdf".format(base_name=base_name, suffix=type_suffix)
    utils.echo_if_verbose(_("message_using_outfile").format(out_file), verbose)
    return {"out_file": out_file}
