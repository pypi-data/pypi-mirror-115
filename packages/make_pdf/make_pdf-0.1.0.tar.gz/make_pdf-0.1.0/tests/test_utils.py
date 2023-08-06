import pytest

from make_pdf import utils


def test_echo_if_verbose_with_verbose(mocker):
    """
    Test whether utils.echo_if_verbose outputs when called with verbose set to True.
    """
    expected_param = "Something should be output"

    echo = mocker.patch("click.echo")

    utils.echo_if_verbose(expected_param, True)

    echo.assert_called_once()
    echo.assert_called_with(expected_param)


def test_echo_if_verbose_without_verbose(mocker):
    """
    Test whether utils.echo_if_verbose does not when called with verbose set to False.
    """
    expected_param = "Nothing should be output"

    echo = mocker.patch("click.echo")

    utils.echo_if_verbose(expected_param, False)

    echo.assert_not_called()


def test_config_dir(mocker):
    """
    Test whether the config-dir-call calls app-dirs.
    """
    # noinspection SpellCheckingInspection
    user_config_dir = mocker.patch("appdirs.user_config_dir")

    utils.get_config_dir()

    user_config_dir.assert_called_once()


def test_resources_dir():
    """
    Test whether the provided resources-dir ends with the correct path (this should imply the dir being generated
    correctly)
    """
    resources_dir = utils.get_resources_dir()
    assert resources_dir.endswith("make_pdf/resources")


metadata_test_data = [
    ("./test.yml", True),
    ("file.YML", True),
    ("test.YML", True),
    ("test.yaml", True),
    ("/tmp/another-name.YAML", True),
    ("test.meta", False),
    ("test.json", False),
    ("file.tex", False),
    ("test.md", False),
    ("test.odt", False),
]
"""
Test-data for test_is_metadata_file
"""


@pytest.mark.parametrize("file,expected", metadata_test_data)
def test_is_metadata_file(file, expected):
    """
    Test whether is_metadata_file works correctly with different inputs.
    """
    assert utils.is_metadata_file(file) == expected


tex_test_data = [
    ("./test.tex", True),
    ("file.YML", False),
    ("test.YML", False),
    ("test.yaml", False),
    ("/tmp/another-name.YAML", False),
    ("test.meta", False),
    ("test.json", False),
    ("file.tex", True),
    ("file.TEX", True),
    ("test.md", False),
    ("test.odt", False),
]
"""
Test-data for test_is_tex_file
"""


@pytest.mark.parametrize("file,expected", tex_test_data)
def test_is_tex_file(file, expected):
    """
    Test whether is_tex_file works correctly with different inputs.
    """
    assert utils.is_tex_file(file) == expected


markdown_test_data = [
    ("./test.tex", False),
    ("file.YML", False),
    ("test.YML", False),
    ("test.yaml", False),
    ("/tmp/another-name.YAML", False),
    ("test.meta", False),
    ("test.json", False),
    ("file.tex", False),
    ("file.TEX", False),
    ("test.md", True),
    ("test.odt", False),
]
"""
Test-data for test_is_tex_file
"""


@pytest.mark.parametrize("file,expected", markdown_test_data)
def test_is_markdown_file(file, expected):
    """
    Test whether is_markdown_file works correctly with different inputs.
    """
    assert utils.is_markdown_file(file) == expected
