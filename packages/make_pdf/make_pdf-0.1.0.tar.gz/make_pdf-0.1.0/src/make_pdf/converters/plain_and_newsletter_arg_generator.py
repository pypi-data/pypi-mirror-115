import os

from make_pdf import utils
from make_pdf.enums import DocumentType


def generate_plain_and_newsletter_args(options):
    """
    Generate a list with the args relating to the plain-type to be passed to pandoc.

    :param (dict[str, Any]) options: the given options to convert the file
    :return: a list with all args to be passed to pandoc
    :rtype: list[str]
    """
    result = list()
    if options["type"] == DocumentType.NEWSLETTER:
        result.extend(["-H", os.path.join(utils.get_resources_dir(), "tex/plain_and_newsletter/newsletter.tex")])
    else:
        result.append("-N")
    result.extend(["-V", "secnumdepth:4"])
    if "draft" in options and options["draft"]:
        result.extend(["-V", "classoption:draft"])
    else:
        result.extend(["-V", "classoption:final"])
    if "legal" in options and options["legal"]:
        result.extend(["-V", "classoption:legal"])
    if ("no_toc" not in options or not options["no_toc"]) and not options["type"] == DocumentType.NEWSLETTER:
        result.append("--toc")
    if "two_column" in options and options["two_column"] or options["type"] == DocumentType.NEWSLETTER:
        result.extend(["-V", "classoption:twocolumn"])
    else:
        result.extend(["-V", "classoption:onecolumn"])
    if "title_page" in options and options["title_page"]:
        result.extend(["-V", "classoption:titlepage"])
    else:
        result.extend(["-V", "classoption:notitlepage"])
    if "short" in options and options["short"]:
        result.extend(["-V", "classoption:short"])
    if "no_footer" in options and options["no_footer"]:
        result.extend(["-V", "classoption:nofooter"])
    if "no_header" in options and options["no_header"]:
        result.extend(["-V", "classoption:noheader"])
    result.extend(["-H", os.path.join(utils.get_resources_dir(), "tex/plain_and_newsletter/plain.tex")])
    return result
