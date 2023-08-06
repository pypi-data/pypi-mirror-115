from make_pdf.preprocessors.diff_preprocessor import diff_files


def test_diff_files_add():
    """
    Test whether diff_files creates the correct criticmarkup for adding.
    """
    expected = "Test{++ adding++}!"

    file = "Test adding!"
    diff_file = "Test!"
    actual = diff_files(file, diff_file)
    assert actual == expected


def test_diff_files_delete():
    """
    Test whether diff_files creates the correct CritcMarkup for deleting.
    """
    expected = "Test{-- deleting--}!"

    file = "Test!"
    diff_file = "Test deleting!"
    actual = diff_files(file, diff_file)
    assert actual == expected


def test_diff_files_replacing():
    """
    Test whether diff_files creates the correct CritcMarkup for deleting.
    """
    expected = "Test {~~old~>new~~}!"

    file = "Test new!"
    diff_file = "Test old!"
    actual = diff_files(file, diff_file)
    assert actual == expected
