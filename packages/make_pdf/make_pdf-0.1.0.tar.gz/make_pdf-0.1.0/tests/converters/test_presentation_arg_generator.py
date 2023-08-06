from make_pdf.converters.presentation_arg_generator import generate_presentation_args


def test_generate_presentation_args(mocker):
    """
    Test whether correct presentation args are generated.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-t",
        "beamer",
        "-M",
        "theme:pureminimalistic",
        "-V",
        "aspectratio:169",
        "-V",
        "themeoptions:customfont",
        "-V",
        "themeoptions:showmaxslides",
        "-H",
        "tex/presentation/presentation.tex",
    ]

    actual = generate_presentation_args({"aspect_ratio": "169"})

    assert actual == expected


def test_generate_presentation_args_4_3_aspect_ratio(mocker):
    """
    Test whether correct presentation args are generated with 4:3 aspect-ratio.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-t",
        "beamer",
        "-M",
        "theme:pureminimalistic",
        "-V",
        "aspectratio:43",
        "-V",
        "themeoptions:customfont",
        "-V",
        "themeoptions:showmaxslides",
        "-H",
        "tex/presentation/presentation.tex",
    ]

    actual = generate_presentation_args({"aspect_ratio": "43"})

    assert actual == expected


def test_generate_presentation_args_no_footer(mocker):
    """
    Test whether correct presentation args are generated with 4:3 aspect-ratio.
    """
    mocker.patch("make_pdf.utils.get_resources_dir", return_value="")

    expected = [
        "-t",
        "beamer",
        "-M",
        "theme:pureminimalistic",
        "-V",
        "aspectratio:169",
        "-V",
        "themeoptions:customfont",
        "-V",
        "themeoptions:showmaxslides",
        "-V",
        "themeoptions:nofooter",
        "-H",
        "tex/presentation/presentation.tex",
    ]

    actual = generate_presentation_args({"aspect_ratio": "169", "no_footer": True})

    assert actual == expected
