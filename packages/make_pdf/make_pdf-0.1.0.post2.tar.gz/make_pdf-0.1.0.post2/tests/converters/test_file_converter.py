import os

from make_pdf import constants
from make_pdf.converters.file_converter import convert_file, generate_pandoc_args
from make_pdf.enums import DocumentType, Language
from make_pdf.utils import _


def test_convert_file_sets_and_resets_locale(mocker, monkeypatch):
    """
    Test whether convert_file sets and resets the locale correctly.
    """
    expected_original_lang = Language.ENGLISH.value["locale"]
    expected_call_lang = Language.GERMAN.value["locale"]

    monkeypatch.setenv("LANG", expected_original_lang)
    mocker.patch("make_pdf.converters.file_converter.generate_pandoc_args")
    mocker.patch("pypandoc.convert_text")
    mocker.patch("os.path.exists", return_value=False)
    echo = mocker.patch("make_pdf.utils.echo_if_verbose")

    file = ""
    options = {
        "type": DocumentType.PLAIN,
        "out_file": "dummy",
        "language": Language.GERMAN,
        "verbose": False,
        "debug_latex": False,
    }

    convert_file(file, options)

    assert os.environ.get("LANG") == expected_original_lang

    echo.assert_called()
    echo.assert_called_with(_("message_set_locale_to").format(expected_call_lang), False)


def test_convert_file_sets_and_resets_locale_with_error(mocker, monkeypatch):
    """
    Test whether convert_file sets and resets the locale correctly.
    """
    expected_original_lang = Language.ENGLISH.value["locale"]

    monkeypatch.setenv("LANG", expected_original_lang)
    mocker.patch("make_pdf.converters.file_converter.generate_pandoc_args")
    mocker.patch("pypandoc.convert_text", side_effect=RuntimeError("test"))
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("click.echo")

    file = ""
    options = {
        "type": DocumentType.PLAIN,
        "out_file": "dummy",
        "language": Language.GERMAN,
        "verbose": False,
        "debug_latex": False,
    }

    convert_file(file, options)

    assert os.environ.get("LANG") == expected_original_lang


def test_convert_file_creates_and_deletes_temp_file_for_letter(mocker):
    """
    Test whether convert_file creates and deletes the letter-vars-temp-file if the type is "letter".
    """

    mocker.patch("make_pdf.converters.file_converter.generate_pandoc_args")
    mocker.patch("pypandoc.convert_text")
    generate_letter_vars_file = mocker.patch("make_pdf.converters.letter_arg_generator.generate_letter_vars_file")
    os_path_exists = mocker.patch("os.path.exists", return_value=True)
    os_remove = mocker.patch("os.remove")

    file = ""
    options = {
        "type": DocumentType.LETTER,
        "out_file": "dummy",
        "language": Language.GERMAN,
        "verbose": False,
        "debug_latex": False,
    }

    convert_file(file, options)

    generate_letter_vars_file.assert_called_once()
    os_path_exists.assert_called_once()
    os_path_exists.assert_called_with(constants.LETTER_METADATA_FILE)
    os_remove.assert_called_once()
    os_remove.assert_called_with(constants.LETTER_METADATA_FILE)


def test_convert_file_creates_and_deletes_temp_file_for_letter_with_error(mocker):
    """
    Test whether convert_file creates and deletes the letter-vars-temp-file if the type is "letter".
    """

    mocker.patch("make_pdf.converters.file_converter.generate_pandoc_args")
    mocker.patch("pypandoc.convert_text", side_effect=RuntimeError("test"))
    generate_letter_vars_file = mocker.patch("make_pdf.converters.letter_arg_generator.generate_letter_vars_file")
    os_path_exists = mocker.patch("os.path.exists", return_value=True)
    os_remove = mocker.patch("os.remove")
    mocker.patch("click.echo")

    file = ""
    options = {
        "type": DocumentType.LETTER,
        "out_file": "dummy",
        "language": Language.GERMAN,
        "verbose": False,
        "debug_latex": False,
    }

    convert_file(file, options)

    generate_letter_vars_file.assert_called_once()
    os_path_exists.assert_called_once()
    os_path_exists.assert_called_with(constants.LETTER_METADATA_FILE)
    os_remove.assert_called_once()
    os_remove.assert_called_with(constants.LETTER_METADATA_FILE)


def test_convert_file_does_not_create_and_delete_temp_file_if_no_letter(mocker):
    """
    Test whether convert_file doesn't create and delete letter-vars-temp-file if the type isn't "letter".
    """
    mocker.patch("make_pdf.converters.file_converter.generate_pandoc_args")
    mocker.patch("pypandoc.convert_text")
    generate_letter_vars_file = mocker.patch("make_pdf.converters.letter_arg_generator.generate_letter_vars_file")
    os_path_exists = mocker.patch("os.path.exists", return_value=False)
    os_remove = mocker.patch("os.remove")

    file = ""
    options = {
        "type": DocumentType.PLAIN,
        "out_file": "dummy",
        "language": Language.GERMAN,
        "verbose": False,
        "debug_latex": False,
    }

    convert_file(file, options)

    generate_letter_vars_file.assert_not_called()
    os_path_exists.assert_called_once()
    os_path_exists.assert_called_with(constants.LETTER_METADATA_FILE)
    os_remove.assert_not_called()


def test_convert_file_respects_debug_latex_true(mocker):
    """
    Test whether convert_file respects the debug_latex-option.
    """
    mocker.patch("make_pdf.converters.file_converter.generate_pandoc_args", return_value=[""])
    pypandoc_convert_text = mocker.patch("pypandoc.convert_text")
    mocker.patch("os.path.exists", return_value=False)

    file = ""
    options = {
        "type": DocumentType.PLAIN,
        "out_file": "dummy",
        "language": Language.GERMAN,
        "verbose": False,
        "debug_latex": True,
    }

    convert_file(file, options)

    pypandoc_convert_text.assert_called_once()
    pypandoc_convert_text.assert_called_with(file, "latex", "md", extra_args=[""])


def test_convert_file_respects_debug_latex_false(mocker):
    """
    Test whether convert_file respects the debug_latex-option set to false.
    """
    mocker.patch("make_pdf.converters.file_converter.generate_pandoc_args", return_value=[""])
    pypandoc_convert_text = mocker.patch("pypandoc.convert_text")
    mocker.patch("os.path.exists", return_value=False)

    file = ""
    options = {
        "type": DocumentType.PLAIN,
        "out_file": "dummy",
        "language": Language.GERMAN,
        "verbose": False,
        "debug_latex": False,
    }

    convert_file(file, options)

    pypandoc_convert_text.assert_called_once()


def test_convert_file_handles_runtime_exception(mocker):
    """
    Test whether convert_file handles a RuntimeException correctly.
    """
    mocker.patch("make_pdf.converters.file_converter.generate_pandoc_args", return_value=[""])
    pypandoc_convert_text = mocker.patch("pypandoc.convert_text", side_effect=RuntimeError("test"))
    mocker.patch("os.path.exists", return_value=False)
    echo = mocker.patch("click.echo")

    file = ""
    options = {
        "type": DocumentType.PLAIN,
        "out_file": "dummy",
        "language": Language.GERMAN,
        "verbose": False,
        "debug_latex": False,
    }

    convert_file(file, options)

    pypandoc_convert_text.assert_called_once()
    echo.assert_called_with("test", err=True)


def test_generate_pandoc_args_calls_plain_for_plain(mocker):
    """
    Test whether generate_pandoc_args calls the plain-generation for the plain-type.
    """
    expected = ["default", "plain", "-H", "/resources/tex/final-hook.tex"]

    general_options = mocker.patch(
        "make_pdf.converters.base_arg_generator.generate_default_args", return_value=["default"]
    )
    plain_options = mocker.patch(
        "make_pdf.converters.plain_and_newsletter_arg_generator.generate_plain_and_newsletter_args",
        return_value=["plain"],
    )
    letter_options = mocker.patch(
        "make_pdf.converters.letter_arg_generator.generate_letter_args", return_value=["letter"]
    )
    presentation_options = mocker.patch(
        "make_pdf.converters.presentation_arg_generator.generate_presentation_args", return_value=["presentation"]
    )
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="/resources")

    options = {"type": DocumentType.PLAIN}

    actual = generate_pandoc_args(options)

    assert actual == expected

    general_options.assert_called_once()
    plain_options.assert_called_once()
    letter_options.assert_not_called()
    presentation_options.assert_not_called()


def test_generate_pandoc_args_calls_plain_for_newsletter(mocker):
    """
    Test whether generate_pandoc_args calls the plain-generation for the newsletter-type.
    """
    expected = ["default", "plain", "-H", "/resources/tex/final-hook.tex"]

    general_options = mocker.patch(
        "make_pdf.converters.base_arg_generator.generate_default_args", return_value=["default"]
    )
    plain_options = mocker.patch(
        "make_pdf.converters.plain_and_newsletter_arg_generator.generate_plain_and_newsletter_args",
        return_value=["plain"],
    )
    letter_options = mocker.patch(
        "make_pdf.converters.letter_arg_generator.generate_letter_args", return_value=["letter"]
    )
    presentation_options = mocker.patch(
        "make_pdf.converters.presentation_arg_generator.generate_presentation_args", return_value=["presentation"]
    )
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="/resources")

    options = {"type": DocumentType.NEWSLETTER}

    actual = generate_pandoc_args(options)

    assert actual == expected

    general_options.assert_called_once()
    plain_options.assert_called_once()
    letter_options.assert_not_called()
    presentation_options.assert_not_called()


def test_generate_pandoc_args_calls_letter_for_letter(mocker):
    """
    Test whether generate_pandoc_args calls the letter-generation for the letter-type.
    """
    expected = ["default", "letter", "-H", "/resources/tex/final-hook.tex"]

    general_options = mocker.patch(
        "make_pdf.converters.base_arg_generator.generate_default_args", return_value=["default"]
    )
    plain_options = mocker.patch(
        "make_pdf.converters.plain_and_newsletter_arg_generator.generate_plain_and_newsletter_args",
        return_value=["plain"],
    )
    letter_options = mocker.patch(
        "make_pdf.converters.letter_arg_generator.generate_letter_args", return_value=["letter"]
    )
    presentation_options = mocker.patch(
        "make_pdf.converters.presentation_arg_generator.generate_presentation_args", return_value=["presentation"]
    )
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="/resources")

    options = {"type": DocumentType.LETTER}

    actual = generate_pandoc_args(options)

    assert actual == expected

    general_options.assert_called_once()
    plain_options.assert_not_called()
    letter_options.assert_called_once()
    presentation_options.assert_not_called()


def test_generate_pandoc_args_calls_presentation_for_presentation(mocker):
    """
    Test whether generate_pandoc_args calls the presentation-generation for the presentation-type.
    """
    expected = ["default", "presentation", "-H", "/resources/tex/final-hook.tex"]

    general_options = mocker.patch(
        "make_pdf.converters.base_arg_generator.generate_default_args", return_value=["default"]
    )
    plain_options = mocker.patch(
        "make_pdf.converters.plain_and_newsletter_arg_generator.generate_plain_and_newsletter_args",
        return_value=["plain"],
    )
    letter_options = mocker.patch(
        "make_pdf.converters.letter_arg_generator.generate_letter_args", return_value=["letter"]
    )
    presentation_options = mocker.patch(
        "make_pdf.converters.presentation_arg_generator.generate_presentation_args", return_value=["presentation"]
    )
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="/resources")

    options = {"type": DocumentType.PRESENTATION}

    actual = generate_pandoc_args(options)

    assert actual == expected

    general_options.assert_called_once()
    plain_options.assert_not_called()
    letter_options.assert_not_called()
    presentation_options.assert_called_once()
