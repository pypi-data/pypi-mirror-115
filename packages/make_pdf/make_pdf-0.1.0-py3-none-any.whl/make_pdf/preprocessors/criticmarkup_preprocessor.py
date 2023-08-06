import re

from make_pdf import utils
from make_pdf.utils import _

ADD_EDIT = re.compile(r"(?s){\+\+(.*?)\+\+[ \t]*(\[(.*?)])?[ \t]*}")
DEL_EDIT = re.compile(r"(?s){--(.*?)--[ \t]*(\[(.*?)])?[ \t]*}")
COMM_EDIT = re.compile(r"(?s){>>(.*?)<<[ \t]*(\[(.*?)])?[ \t]*}")
MARK_EDIT = re.compile(r"(?s){==(.*?)==[ \t]*(\[(.*?)])?[ \t]*}")
SUB_EDIT = re.compile(r"""(?s){~~(?P<original>(?:[^~>]|~(?!>))+)~>(?P<new>(?:[^~]|~(?!~}))+)~~}""")


def preprocess_criticmarkup(file, verbose=False):
    """
    Replace all critic-markup-annotations in the given file with latex-changes-commands, so they get converted
    correctly.

    :param (str) file: the file to evaluate
    :param (bool) verbose: whether to output verbosely
    :rtype: str
    :return: the file with the replaced criticmarkup-commands
    """
    utils.echo_if_verbose(_("message_evaluating_criticmarkup"), verbose)
    return substitute_critic_markup_with_latex(file)


def substitute_critic_markup_with_latex(file):
    file = ADD_EDIT.sub(r"\\added{\1}", file)
    file = DEL_EDIT.sub(r"\\deleted{\1}", file)
    file = SUB_EDIT.sub(r"\\replaced{\2}{\1}", file)

    file = MARK_EDIT.sub(r"\\highlight{\1}", file)
    return COMM_EDIT.sub(r"\\comment{\1}", file)
