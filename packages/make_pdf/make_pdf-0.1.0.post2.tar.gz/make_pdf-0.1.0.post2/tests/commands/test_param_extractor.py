import pytest
from click import BadParameter, BadArgumentUsage

from make_pdf import utils
from make_pdf.commands import param_extractor
from make_pdf.enums import Language

simple_param_extract_test_data = [
    ("title_page", True, {"title_page": True}),
    ("title_page", False, {"title_page": False}),
    ("test_key", "test_value", {"test_key": "test_value"}),
]
"""
Test data for the simple-param extraction
"""


@pytest.mark.parametrize("key,value,expected", simple_param_extract_test_data)
def test_extract_simple_param(key, value, expected):
    """
    Test whether the simple-param-extractor returns the expected dict
    """
    actual = param_extractor.extract_simple_param(key, value)
    assert actual == expected


simple_param_extract_test_data = [
    ("Message should be shown", True, True),
    ("Message shouldn't be shown", False, False),
]
"""
Test data for the simple-param message testing
"""


@pytest.mark.parametrize("message,verbose,expected", simple_param_extract_test_data)
def test_extract_simple_param_message(mocker, message, verbose, expected):
    """
    Test whether the simple-param-extractor outputs the message when expected to.
    """
    echo = mocker.patch("click.echo")

    param_extractor.extract_simple_param("key", "value", message, verbose)

    if expected:
        echo.assert_called_once()
        echo.assert_called_with(message)
    else:
        echo.assert_not_called()


file_test_data = [
    ([], [], []),
    (["test.md"], ["test.md"], []),
    (["test.yml"], [], ["test.yml"]),
    (["test.md", "test.yml"], ["test.md"], ["test.yml"]),
    (["test.md", "test2.md", "test.yml"], ["test.md", "test2.md"], ["test.yml"]),
    (["test.md", "test2.yml", "test.yml"], ["test.md"], ["test2.yml", "test.yml"]),
    (["test.odt", "test2.yml", "test.yml"], ["test.odt"], ["test2.yml", "test.yml"]),
]
"""
Test data for the file-tests
"""


@pytest.mark.parametrize("files,expected_content,expected_metadata", file_test_data)
def test_extract_files(files, expected_content, expected_metadata):
    """
    Test whether the file-extraction returns the correct config-object or raises appropriate errors.
    """

    if not expected_content:
        with pytest.raises(BadArgumentUsage):
            param_extractor.extract_files(files)
    else:
        expected = {"files": expected_content, "metadata_files": expected_metadata}

        actual = param_extractor.extract_files(files)

        assert expected == actual


@pytest.mark.parametrize("files,expected_content,expected_metadata", file_test_data)
def test_extract_diff_files(files, expected_content, expected_metadata):
    """
    Test whether the file-extraction returns the correct config-object or raises appropriate errors.
    """
    if files:
        expected_should_diff = True
    else:
        expected_should_diff = False

    if not expected_content and expected_should_diff:
        with pytest.raises(BadParameter):
            param_extractor.extract_diff_files(files)
    else:
        expected = {
            "diff_files": expected_content,
            "diff_metadata_files": expected_metadata,
            "should_diff": expected_should_diff,
        }

        actual = param_extractor.extract_diff_files(files)

        assert expected == actual


@pytest.mark.parametrize("files,expected_content,expected_metadata", file_test_data)
def test_divide_files_in_categories(files, expected_content, expected_metadata):
    """
    Test whether files get correctly divided into categories.
    """
    actual_content, actual_metadata = param_extractor.divide_files_in_categories(files)

    assert actual_content == expected_content
    assert actual_metadata == expected_metadata


def test_extract_theme_file_default(mocker):
    """
    Tests whether the theme-file-extraction works for the default theme.
    """
    expected = {"theme": "default", "theme_file": "./make_pdf/resources/tex/default-header.tex"}
    expected_path = "./make_pdf/resources/tex/default-header.tex"
    theme_name = "default"

    utils.echo_if_verbose("nothing", False)

    get_resources_dir = mocker.patch("make_pdf.utils.get_resources_dir", return_value="./make_pdf/resources")
    get_config_dir = mocker.patch("make_pdf.utils.get_config_dir")
    os_path_exists = mocker.patch("os.path.exists", return_value=True)

    actual = param_extractor.extract_theme_file(theme_name)

    assert actual == expected
    get_resources_dir.assert_called_once()
    os_path_exists.assert_called_once()
    os_path_exists.assert_called_with(expected_path)
    get_config_dir.assert_not_called()


def test_extract_theme_file_custom(mocker):
    """
    Tests whether the theme-file-extraction works for a custom theme.
    """
    expected = {"theme": "awesome_theme", "theme_file": "~/.config/make_pdf/awesome_theme-header.tex"}
    expected_path = "~/.config/make_pdf/awesome_theme-header.tex"
    theme_name = "awesome_theme"

    utils.echo_if_verbose("nothing", False)

    get_resources_dir = mocker.patch("make_pdf.utils.get_resources_dir")
    get_config_dir = mocker.patch("make_pdf.utils.get_config_dir", return_value="~/.config/make_pdf")
    os_path_exists = mocker.patch("os.path.exists", return_value=True)

    actual = param_extractor.extract_theme_file(theme_name)

    assert actual == expected
    get_resources_dir.assert_not_called()
    os_path_exists.assert_called_once()
    os_path_exists.assert_called_with(expected_path)
    get_config_dir.assert_called_once()


def test_extract_theme_file_custom_not_present(mocker):
    """
    Tests whether the theme-file-extraction throws an exception for a non-existing custom theme.
    """
    expected_path = "~/.config/make_pdf/awesome_theme-header.tex"
    theme_name = "awesome_theme"

    utils.echo_if_verbose("nothing", False)

    get_resources_dir = mocker.patch("make_pdf.utils.get_resources_dir")
    get_config_dir = mocker.patch("make_pdf.utils.get_config_dir", return_value="~/.config/make_pdf")
    os_path_exists = mocker.patch("os.path.exists", return_value=False)

    with pytest.raises(BadParameter):
        param_extractor.extract_theme_file(theme_name)

    get_resources_dir.assert_not_called()
    os_path_exists.assert_called_once()
    os_path_exists.assert_called_with(expected_path)
    get_config_dir.assert_called_once()


# noinspection SpellCheckingInspection
language_test_data = [
    ("en", Language.ENGLISH),
    ("EN", Language.ENGLISH),
    ("english", Language.ENGLISH),
    ("englisch", None),
    ("de", Language.GERMAN),
    ("DE", Language.GERMAN),
    ("german", Language.GERMAN),
    ("deutsch", Language.GERMAN),
    ("deutsh", None),
    ("es", None),
]
"""
Test data for the language-extraction-test
"""


@pytest.mark.parametrize("lang_code,expected", language_test_data)
def test_extract_language(lang_code, expected):
    """
    Tests whether the language-extraction works.
    """
    if expected:
        assert param_extractor.extract_language(lang_code) == {"language": expected}
    else:
        with pytest.raises(BadParameter):
            param_extractor.extract_language(lang_code)
