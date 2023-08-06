import os

from make_pdf import utils


def generate_metadata_args(options):
    """
    Generate args relating to the metadata. Namely extract title, author and date as well as all provided
    metadata-files.

    :param (dict[str, Any]) options: the given options to convert the file
    :rtype: list[str]
    :return: a list with all args to be passed to pandoc
    """
    result = list()
    if "title" in options and options["title"]:
        result.extend(["-M", "title:" + options["title"]])
    if "author" in options and options["author"]:
        result.extend(["-M", "author:" + options["author"]])
    if "date" in options and options["date"]:
        result.extend(["-M", "date:" + options["date"]])
    if "metadata_files" in options and options["metadata_files"]:
        for file in options["metadata_files"]:
            result.extend(["--metadata-file", file])
    return result


def generate_default_args(options):
    """
    Generate a list with the args equal for all types to be passed to pandoc.

    :param (dict[str, Any]) options: the given options to convert the file
    :return: a list with all args to be passed to pandoc
    :rtype: list[str]
    """
    result = list()
    result.extend(["-M", "lang:" + options["language"].value["languageCode"]])
    result.extend(["-M", "csquotes:true"])
    result.extend(["-M", "include-auto"])
    result.extend(["-V", "classoption:" + options["language"].value["language"]])
    result.extend(["-V", "urlcolor:red"])
    result.append("--pdf-engine=xelatex")
    result.extend(["-H", os.path.join(utils.get_resources_dir(), "tex/packages.tex")])
    result.extend(["-H", os.path.join(utils.get_resources_dir(), "tex/utils.tex")])
    result.extend(["-H", options["theme_file"]])
    result.extend(["-H", os.path.join(utils.get_resources_dir(), "tex/localization.tex")])
    result.extend(["-H", os.path.join(utils.get_resources_dir(), "tex/main.tex")])
    result.extend(["-L", os.path.join(utils.get_resources_dir(), "filters/include-files.lua")])
    result.extend(["-L", os.path.join(utils.get_resources_dir(), "filters/fences.lua")])
    result.extend(["-L", os.path.join(utils.get_resources_dir(), "filters/criticmarkup.lua")])
    if "no_automatic_date" not in options or not options["no_automatic_date"]:
        result.extend(["-L", os.path.join(utils.get_resources_dir(), "filters/currentdate.lua")])
    if "print" in options and options["print"]:
        result.extend(["-V", "links-as-notes=true"])
    if "verbose" in options and options["verbose"]:
        result.append("--verbose")
    return result
