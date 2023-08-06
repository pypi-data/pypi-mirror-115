from pathlib import Path

import pypandoc

from make_pdf import utils
from make_pdf.utils import _


def stitch_files_together(files, verbose=False, message=_("message_stitching_files_together")):
    """
    Stitches the files on the provided path together - first converting them to markdown if necessary.

    :param (list[str]) files: the input-files to stitch together
    :param (bool) verbose: whether to output verbosely
    :rtype: str
    :return: A single file, resulting from all input-files.
    """
    utils.echo_if_verbose(message, verbose)
    stitched_file = ""
    for file in files:
        if utils.is_markdown_file(file):
            stitched_file = stitched_file + Path(file).read_text()
            stitched_file = stitched_file + "\n"
        else:
            stitched_file = stitched_file + pypandoc.convert_file(file, "md")
    return stitched_file
