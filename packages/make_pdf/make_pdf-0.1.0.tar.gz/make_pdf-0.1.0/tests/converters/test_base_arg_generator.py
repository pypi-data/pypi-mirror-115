from make_pdf.converters.base_arg_generator import generate_metadata_args, generate_default_args
from make_pdf.enums import Language


def test_generate_metadata_args_adds_single_metadata_file():
    """
    Tests whether generate_metadata_args adds a single metadata-file as metadata-file.
    """
    expected = ["--metadata-file", "test.yml"]

    actual = generate_metadata_args({"metadata_files": ["test.yml"]})

    assert actual == expected


def test_generate_metadata_args_adds_multiple_metadata_files():
    """
    Tests whether generate_metadata_args adds multiple metadata-files as metadata-files.
    """
    expected = ["--metadata-file", "test.yml", "--metadata-file", "test2.yml"]

    actual = generate_metadata_args({"metadata_files": ["test.yml", "test2.yml"]})

    assert actual == expected


def test_generate_metadata_args_adds_title_metadata():
    """
    Tests whether generate_metadata_args adds the title-arg correctly.
    """
    expected = ["-M", "title:test"]

    actual = generate_metadata_args({"title": "test"})

    assert actual == expected


def test_generate_metadata_args_adds_author_metadata():
    """
    Tests whether generate_metadata_args adds the author-arg correctly.
    """
    expected = ["-M", "author:test"]

    actual = generate_metadata_args({"author": "test"})

    assert actual == expected


def test_generate_metadata_args_adds_date_metadata():
    """
    Tests whether generate_metadata_args adds the date-arg correctly.
    """
    expected = ["-M", "date:test"]

    actual = generate_metadata_args({"date": "test"})

    assert actual == expected


def test_generate_default_args_adds_default_options_for_english(mocker):
    """
    Tests whether generate_default_args adds the correct default args with the english language set.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-M",
        "lang:en-GB",
        "-M",
        "csquotes:true",
        "-M",
        "include-auto",
        "-V",
        "classoption:english",
        "-V",
        "urlcolor:red",
        "--pdf-engine=xelatex",
        "-H",
        "tex/packages.tex",
        "-H",
        "tex/utils.tex",
        "-H",
        "test.tex",
        "-H",
        "tex/localization.tex",
        "-H",
        "tex/main.tex",
        "-L",
        "filters/include-files.lua",
        "-L",
        "filters/fences.lua",
        "-L",
        "filters/criticmarkup.lua",
        "-L",
        "filters/currentdate.lua",
    ]

    actual = generate_default_args({"language": Language.ENGLISH, "theme_file": "test.tex"})

    assert actual == expected


def test_generate_default_args_adds_default_options_for_german(mocker):
    """
    Tests whether generate_default_args adds the correct default args with the german language set.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-M",
        "lang:de-DE",
        "-M",
        "csquotes:true",
        "-M",
        "include-auto",
        "-V",
        "classoption:german",
        "-V",
        "urlcolor:red",
        "--pdf-engine=xelatex",
        "-H",
        "tex/packages.tex",
        "-H",
        "tex/utils.tex",
        "-H",
        "test.tex",
        "-H",
        "tex/localization.tex",
        "-H",
        "tex/main.tex",
        "-L",
        "filters/include-files.lua",
        "-L",
        "filters/fences.lua",
        "-L",
        "filters/criticmarkup.lua",
        "-L",
        "filters/currentdate.lua",
    ]

    actual = generate_default_args({"language": Language.GERMAN, "theme_file": "test.tex"})

    assert actual == expected


def test_generate_default_args_adds_no_automatic_date_option(mocker):
    """
    Tests whether generate_default_args adds the correct no-automatic-date args.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-M",
        "lang:en-GB",
        "-M",
        "csquotes:true",
        "-M",
        "include-auto",
        "-V",
        "classoption:english",
        "-V",
        "urlcolor:red",
        "--pdf-engine=xelatex",
        "-H",
        "tex/packages.tex",
        "-H",
        "tex/utils.tex",
        "-H",
        "test.tex",
        "-H",
        "tex/localization.tex",
        "-H",
        "tex/main.tex",
        "-L",
        "filters/include-files.lua",
        "-L",
        "filters/fences.lua",
        "-L",
        "filters/criticmarkup.lua",
    ]

    actual = generate_default_args({"language": Language.ENGLISH, "theme_file": "test.tex", "no_automatic_date": True})

    assert actual == expected


def test_generate_default_args_adds_print_option(mocker):
    """
    Tests whether generate_default_args adds the correct print args.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-M",
        "lang:en-GB",
        "-M",
        "csquotes:true",
        "-M",
        "include-auto",
        "-V",
        "classoption:english",
        "-V",
        "urlcolor:red",
        "--pdf-engine=xelatex",
        "-H",
        "tex/packages.tex",
        "-H",
        "tex/utils.tex",
        "-H",
        "test.tex",
        "-H",
        "tex/localization.tex",
        "-H",
        "tex/main.tex",
        "-L",
        "filters/include-files.lua",
        "-L",
        "filters/fences.lua",
        "-L",
        "filters/criticmarkup.lua",
        "-L",
        "filters/currentdate.lua",
        "-V",
        "links-as-notes=true",
    ]

    actual = generate_default_args({"language": Language.ENGLISH, "theme_file": "test.tex", "print": True})

    assert actual == expected


def test_generate_default_args_adds_verbose_option(mocker):
    """
    Tests whether generate_default_args adds the correct verbose args.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-M",
        "lang:en-GB",
        "-M",
        "csquotes:true",
        "-M",
        "include-auto",
        "-V",
        "classoption:english",
        "-V",
        "urlcolor:red",
        "--pdf-engine=xelatex",
        "-H",
        "tex/packages.tex",
        "-H",
        "tex/utils.tex",
        "-H",
        "test.tex",
        "-H",
        "tex/localization.tex",
        "-H",
        "tex/main.tex",
        "-L",
        "filters/include-files.lua",
        "-L",
        "filters/fences.lua",
        "-L",
        "filters/criticmarkup.lua",
        "-L",
        "filters/currentdate.lua",
        "--verbose",
    ]

    actual = generate_default_args({"language": Language.ENGLISH, "theme_file": "test.tex", "verbose": True})

    assert actual == expected
