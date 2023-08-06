import os

import pypandoc

from make_pdf import utils
from make_pdf.constants import LETTER_METADATA_FILE
from make_pdf.converters import base_arg_generator


def generate_letter_args(options):
    """
    Generate a list with the args relating to the letter type to be passed to pandoc.

    :param (dict[str, Any]) options: the given options to convert the file
    :return: a list with all args to be passed to pandoc
    :rtype: list[str]
    """
    result = list()
    result.extend(["-V", "documentclass:scrlttr2"])
    result.extend(["-B", os.path.join(utils.get_resources_dir(), "tex/letter/before-letter.tex")])
    result.extend(["-A", os.path.join(utils.get_resources_dir(), "tex/letter/after-letter.tex")])
    result.extend(generate_letter_metadata_args(options))
    result.extend(["-H", LETTER_METADATA_FILE])

    return result


def generate_letter_metadata_args(options):
    """
    Generate a list with the needed extra-metadata-options for the letter-type.

    :param (dict[str, Any]) options: the given options to convert the file
    :return: a list with all args to be passed to pandoc
    :rtype: list[str]
    """
    result = list()
    if utils.is_tex_file(options["from"]):
        result.extend(["-H", options["from"]])
    else:
        result.extend(["--metadata-file", options["from"]])
    if "to" in options and options["to"]:
        if utils.is_tex_file(options["to"]):
            result.extend(["-H", options["to"]])
        else:
            result.extend(["--metadata-file", options["to"]])
    return result


def generate_letter_vars_file(file, options):
    """
    Generate temporary letter-vars-file, to correctly set all koma-vars for the template.

    :param (str) file: the file to convert
    :param (dict[str, Any]) options: the given options to convert the file
    """
    extra_args = list()
    extra_args.extend(generate_letter_metadata_args(options))
    extra_args.extend(base_arg_generator.generate_metadata_args(options))
    extra_args.extend(["--template", os.path.join(utils.get_resources_dir(), "tex/letter/lettervars-template.tex")])
    pypandoc.convert_text(file, "latex", "md", outputfile=LETTER_METADATA_FILE, extra_args=extra_args)
