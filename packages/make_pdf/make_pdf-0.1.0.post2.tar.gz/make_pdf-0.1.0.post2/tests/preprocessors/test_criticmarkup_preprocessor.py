from make_pdf.preprocessors.criticmarkup_preprocessor import preprocess_criticmarkup


def test_preprocess_criticmarkup_added():
    """
    Test whether critic-markup additions get changed correctly.
    """
    expected = "Added \\added{Test}"

    actual = preprocess_criticmarkup("Added {++Test++}", False)

    assert actual == expected


def test_preprocess_criticmarkup_deleted():
    """
    Test whether critic-markup deletions get changed correctly.
    """
    expected = "Deleted \\deleted{Test}"

    actual = preprocess_criticmarkup("Deleted {--Test--}", False)

    assert actual == expected


def test_preprocess_criticmarkup_replaced():
    """
    Test whether critic-markup replacing gets changed correctly.
    """
    expected = "Replaced \\replaced{Test}{Test2}"

    actual = preprocess_criticmarkup("Replaced {~~Test2~>Test~~}", False)

    assert actual == expected


def test_preprocess_criticmarkup_highlight():
    """
    Test whether critic-markup highlightings get changed correctly.
    """
    expected = "Highlighted \\highlight{Test}"

    actual = preprocess_criticmarkup("Highlighted {==Test==}", False)

    assert actual == expected


def test_preprocess_criticmarkup_comment():
    """
    Test whether critic-markup comments get changed correctly.
    """
    expected = "Commented \\comment{Test}"

    actual = preprocess_criticmarkup("Commented {>>Test<<}", False)

    assert actual == expected
