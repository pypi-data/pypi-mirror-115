from difflib import SequenceMatcher

from make_pdf import utils
from make_pdf.utils import _


def diff_files(file, diff_file, verbose=False):
    """
    Diff the two given files and set all differences in critcmarkup

    :param (str) file: the new file, which should be generated
    :param (str) diff_file: the old file to be diffed with the new one
    :param (bool) verbose: whether to output verbosely
    :rtype: str
    :return: a diff-file with all changes as criticmarkup
    """
    utils.echo_if_verbose(_("message_diffing_files"), verbose)
    matcher = SequenceMatcher(lambda x: False, file, diff_file, False)
    opcodes = matcher.get_opcodes()
    result = ""
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            for item in file[i1:i2]:
                result = result + item
        if tag == "delete":
            result = result + "{++"
            for item in file[i1:i2]:
                result = result + item
            result = result + "++}"
        if tag == "insert":
            result = result + "{--"
            for item in diff_file[j1:j2]:
                result = result + item
            result = result + "--}"
        if tag == "replace":
            result = result + "{~~"
            for item in diff_file[j1:j2]:
                result = result + item
            result = result + "~>"
            for item in file[i1:i2]:
                result = result + item
            result = result + "~~}"
    return result
