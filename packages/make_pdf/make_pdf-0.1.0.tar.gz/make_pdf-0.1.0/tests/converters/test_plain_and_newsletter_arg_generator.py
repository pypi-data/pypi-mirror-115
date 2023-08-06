from make_pdf.converters.plain_and_newsletter_arg_generator import generate_plain_and_newsletter_args
from make_pdf.enums import DocumentType


def test_generate_plain_and_newsletter_args_for_plain(mocker):
    """
    Test whether generate_plain_and_newsletter_args generates correct args for plain file.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-N",
        "-V",
        "secnumdepth:4",
        "-V",
        "classoption:final",
        "--toc",
        "-V",
        "classoption:onecolumn",
        "-V",
        "classoption:notitlepage",
        "-H",
        "tex/plain_and_newsletter/plain.tex",
    ]

    actual = generate_plain_and_newsletter_args({"type": DocumentType.PLAIN})

    assert actual == expected


def test_generate_plain_and_newsletter_args_respects_draft(mocker):
    """
    Test whether generate_plain_and_newsletter_args generates correct args for draft.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-N",
        "-V",
        "secnumdepth:4",
        "-V",
        "classoption:draft",
        "--toc",
        "-V",
        "classoption:onecolumn",
        "-V",
        "classoption:notitlepage",
        "-H",
        "tex/plain_and_newsletter/plain.tex",
    ]

    actual = generate_plain_and_newsletter_args({"type": DocumentType.PLAIN, "draft": True})

    assert actual == expected


def test_generate_plain_and_newsletter_args_respects_legal(mocker):
    """
    Test whether generate_plain_and_newsletter_args generates correct args for legal.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-N",
        "-V",
        "secnumdepth:4",
        "-V",
        "classoption:final",
        "-V",
        "classoption:legal",
        "--toc",
        "-V",
        "classoption:onecolumn",
        "-V",
        "classoption:notitlepage",
        "-H",
        "tex/plain_and_newsletter/plain.tex",
    ]

    actual = generate_plain_and_newsletter_args({"type": DocumentType.PLAIN, "legal": True})

    assert actual == expected


def test_generate_plain_and_newsletter_args_for_no_toc(mocker):
    """
    Test whether generate_plain_and_newsletter_args generates correct args for no_toc.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-N",
        "-V",
        "secnumdepth:4",
        "-V",
        "classoption:final",
        "-V",
        "classoption:onecolumn",
        "-V",
        "classoption:notitlepage",
        "-H",
        "tex/plain_and_newsletter/plain.tex",
    ]

    actual = generate_plain_and_newsletter_args({"type": DocumentType.PLAIN, "no_toc": True})

    assert actual == expected


def test_generate_plain_and_newsletter_args_respectes_two_column(mocker):
    """
    Test whether generate_plain_and_newsletter_args generates correct args for two-column.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-N",
        "-V",
        "secnumdepth:4",
        "-V",
        "classoption:final",
        "--toc",
        "-V",
        "classoption:twocolumn",
        "-V",
        "classoption:notitlepage",
        "-H",
        "tex/plain_and_newsletter/plain.tex",
    ]

    actual = generate_plain_and_newsletter_args({"type": DocumentType.PLAIN, "two_column": True})

    assert actual == expected


def test_generate_plain_and_newsletter_args_respects_title_page(mocker):
    """
    Test whether generate_plain_and_newsletter_args generates correct args for title-page.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-N",
        "-V",
        "secnumdepth:4",
        "-V",
        "classoption:final",
        "--toc",
        "-V",
        "classoption:onecolumn",
        "-V",
        "classoption:titlepage",
        "-H",
        "tex/plain_and_newsletter/plain.tex",
    ]

    actual = generate_plain_and_newsletter_args({"type": DocumentType.PLAIN, "title_page": True})

    assert actual == expected


def test_generate_plain_and_newsletter_args_respects_short(mocker):
    """
    Test whether generate_plain_and_newsletter_args generates correct args for short.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-N",
        "-V",
        "secnumdepth:4",
        "-V",
        "classoption:final",
        "--toc",
        "-V",
        "classoption:onecolumn",
        "-V",
        "classoption:notitlepage",
        "-V",
        "classoption:short",
        "-H",
        "tex/plain_and_newsletter/plain.tex",
    ]

    actual = generate_plain_and_newsletter_args({"type": DocumentType.PLAIN, "short": True})

    assert actual == expected


def test_generate_plain_and_newsletter_args_respects_no_footer(mocker):
    """
    Test whether generate_plain_and_newsletter_args generates correct args for no-footer.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-N",
        "-V",
        "secnumdepth:4",
        "-V",
        "classoption:final",
        "--toc",
        "-V",
        "classoption:onecolumn",
        "-V",
        "classoption:notitlepage",
        "-V",
        "classoption:nofooter",
        "-H",
        "tex/plain_and_newsletter/plain.tex",
    ]

    actual = generate_plain_and_newsletter_args({"type": DocumentType.PLAIN, "no_footer": True})

    assert actual == expected


def test_generate_plain_and_newsletter_args_respects_no_header(mocker):
    """
    Test whether generate_plain_and_newsletter_args generates correct args for no-header.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-N",
        "-V",
        "secnumdepth:4",
        "-V",
        "classoption:final",
        "--toc",
        "-V",
        "classoption:onecolumn",
        "-V",
        "classoption:notitlepage",
        "-V",
        "classoption:noheader",
        "-H",
        "tex/plain_and_newsletter/plain.tex",
    ]

    actual = generate_plain_and_newsletter_args({"type": DocumentType.PLAIN, "no_header": True})

    assert actual == expected


def test_generate_plain_and_newsletter_args_for_newsletter(mocker):
    """
    Test whether generate_plain_and_newsletter_args generates correct args for newsletter file.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-H",
        "tex/plain_and_newsletter/newsletter.tex",
        "-V",
        "secnumdepth:4",
        "-V",
        "classoption:final",
        "-V",
        "classoption:twocolumn",
        "-V",
        "classoption:notitlepage",
        "-H",
        "tex/plain_and_newsletter/plain.tex",
    ]

    actual = generate_plain_and_newsletter_args({"type": DocumentType.NEWSLETTER})

    assert actual == expected
