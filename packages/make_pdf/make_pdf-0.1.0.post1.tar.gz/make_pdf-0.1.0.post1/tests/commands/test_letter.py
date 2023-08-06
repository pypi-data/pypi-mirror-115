import pytest
from click import BadParameter

from make_pdf.commands import letter

# The side-effect (third param) indicates when the os.exists-call returns. Thus [True] returns on the first try,
# [False, True] on the second and so on...
to_test_data = [
    ("test.yml", "test.yml", [True]),
    ("test.tex", "test.tex", [True]),
    ("test", "~/.config/make_pdf/test-to.yml", [True]),
    ("test", "~/.config/make_pdf/test-to.tex", [False, True]),
    ("test", None, [False, False]),
]
"""
Test-data for the to-extraction-test.
"""


@pytest.mark.parametrize("to,expected,side_effect", to_test_data)
def test_extract_to_file(mocker, to, expected, side_effect):
    """
    Test whether the to-filename gets extracted correctly.
    """
    mocker.patch("make_pdf.utils.get_config_dir", return_value="~/.config/make_pdf")
    mocker.patch("os.path.exists", side_effect=side_effect)

    actual = letter.extract_to_file(to)

    assert actual == expected


# The side-effect (third param) indicates when the os.exists-call returns. Thus [True] returns on the first try,
# [False, True] on the second and so on...
from_test_data = [
    (None, "theme", "~/.config/make_pdf/theme-from.yml", [True]),
    ("test.yml", "theme", "test.yml", [True]),
    ("test.tex", "theme", "test.tex", [True]),
    ("test", "theme", "~/.config/make_pdf/test-from.yml", [True]),
    ("test", "theme", "~/.config/make_pdf/test-from.tex", [False, True]),
    ("test", "theme", "~/.config/make_pdf/theme-from.yml", [False, False, True]),
    ("test", "theme", "~/.config/make_pdf/theme-from.tex", [False, False, False, True]),
    ("test", "theme", None, [False, False, False, False]),
]
"""
Test-data for the from-extraction-test.
"""


@pytest.mark.parametrize("from_option,theme,expected,side_effect", from_test_data)
def test_extract_from_file(mocker, from_option, theme, expected, side_effect):
    """
    Test whether the from-filename gets extracted correctly.
    """
    mocker.patch("make_pdf.utils.get_config_dir", return_value="~/.config/make_pdf")
    mocker.patch("os.path.exists", side_effect=side_effect)

    actual = letter.extract_from_file(from_option, theme)

    assert actual == expected


letter_test_data = [
    (None, None, "theme", None, "~/.config/make_pdf/theme-from.tex", {"from": "~/.config/make_pdf/theme-from.tex"}),
    (None, None, "theme", None, None, None),
    ("test", None, "theme", None, "~/.config/make_pdf/theme-from.tex", None),
    (
        "text.yml",
        None,
        "theme",
        "text.yml",
        "~/.config/make_pdf/theme-from.tex",
        {"to": "text.yml", "from": "~/.config/make_pdf/theme-from.tex"},
    ),
    (
        "text.yml",
        "from.yml",
        "theme",
        "text.yml",
        "from.yml",
        {"to": "text.yml", "from": "from.yml"},
    ),
]
"""
Test-data for the letter-extraction-test.
"""


@pytest.mark.parametrize("to, from_option,theme,to_return,from_return,expected", letter_test_data)
def test_extract_letter_metadata(mocker, to, from_option, theme, to_return, from_return, expected):
    """
    Test whether the letter-params get extracted correctly.
    """
    mocker.patch("make_pdf.commands.letter.extract_to_file", return_value=to_return)
    mocker.patch("make_pdf.commands.letter.extract_from_file", return_value=from_return)

    if to and not to_return:
        with pytest.raises(BadParameter):
            letter.extract_letter_metadata(to, from_option, theme, False)
    elif not from_return:
        with pytest.raises(BadParameter):
            letter.extract_letter_metadata(to, from_option, theme, False)
    else:
        actual = letter.extract_letter_metadata(to, from_option, theme, False)

        assert actual == expected
