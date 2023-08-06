from make_pdf.constants import LETTER_METADATA_FILE
from make_pdf.converters.letter_arg_generator import (
    generate_letter_args,
    generate_letter_metadata_args,
    generate_letter_vars_file,
)


def test_generate_letter_args(mocker):
    """
    Test if generate_letter_argsargs returns the correct options.
    """
    mocker.patch("make_pdf.converters.letter_arg_generator.generate_letter_metadata_args", return_value=["metadata"])
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-V",
        "documentclass:scrlttr2",
        "-B",
        "tex/letter/before-letter.tex",
        "-A",
        "tex/letter/after-letter.tex",
        "metadata",
        "-H",
        LETTER_METADATA_FILE,
    ]

    actual = generate_letter_args({})

    assert actual == expected


def test_generate_letter_metadata_args_creates_from_tex_as_header():
    """
    Test if generate_letter_metadata_args adds from-file as header, if it is a tex-file.
    """
    expected = ["-H", "from.tex"]

    actual = generate_letter_metadata_args({"from": "from.tex"})

    assert actual == expected


def test_generate_letter_metadata_args_creates_from_yml_as_metadata():
    """
    Test if generate_letter_metadata_args adds from-file as metadata, if it is a yml-file.
    """
    expected = ["--metadata-file", "from.yml"]

    actual = generate_letter_metadata_args({"from": "from.yml"})

    assert actual == expected


def test_generate_letter_metadata_args_creates_to_tex_as_header():
    """
    Test if generate_letter_metadata_args adds to-file as header, if it is a tex-file.
    """
    expected = ["-H", "from.tex", "-H", "to.tex"]

    actual = generate_letter_metadata_args({"from": "from.tex", "to": "to.tex"})

    assert actual == expected


def test_generate_letter_metadata_args_creates_to_yml_as_metadata():
    """
    Test if generate_letter_metadata_args adds to-file as metadata, if it is a yml-file.
    """
    expected = ["-H", "from.tex", "--metadata-file", "to.yml"]

    actual = generate_letter_metadata_args({"from": "from.tex", "to": "to.yml"})

    assert actual == expected


def test_generate_letter_vars_file(mocker):
    """
    Test if generate_letter_args calls pypandoc correctly.
    """
    mocker.patch(
        "make_pdf.converters.letter_arg_generator.generate_letter_metadata_args", return_value=["letter-metadata"]
    )
    mocker.patch("make_pdf.converters.base_arg_generator.generate_metadata_args", return_value=["metadata"])
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")
    pypandoc_convert_text = mocker.patch("pypandoc.convert_text")
    file = "file"

    expected_extra_args = ["letter-metadata", "metadata", "--template", "tex/letter/lettervars-template.tex"]

    generate_letter_vars_file(file, {})

    pypandoc_convert_text.assert_called_once_with(
        file, "latex", "md", outputfile=LETTER_METADATA_FILE, extra_args=expected_extra_args
    )
