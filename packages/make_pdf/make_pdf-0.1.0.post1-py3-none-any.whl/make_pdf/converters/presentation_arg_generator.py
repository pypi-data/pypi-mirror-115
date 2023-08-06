import os

from make_pdf import utils


def generate_presentation_args(options):
    """
    Generate a list with the args relating to the presentation-type to be passed to pandoc.

    :param (dict[str, Any]) options: the given options to convert the file
    :return: a list with all args to be passed to pandoc
    :rtype: list[str]
    """
    result = list()
    result.extend(["-t", "beamer"])
    result.extend(["-M", "theme:pureminimalistic"])
    result.extend(["-V", "aspectratio:" + options["aspect_ratio"]])
    result.extend(["-V", "themeoptions:customfont"])
    result.extend(["-V", "themeoptions:showmaxslides"])
    if "no_footer" in options and options["no_footer"]:
        result.extend(["-V", "themeoptions:nofooter"])
    result.extend(["-H", os.path.join(utils.get_resources_dir(), "tex/presentation/presentation.tex")])
    return result
