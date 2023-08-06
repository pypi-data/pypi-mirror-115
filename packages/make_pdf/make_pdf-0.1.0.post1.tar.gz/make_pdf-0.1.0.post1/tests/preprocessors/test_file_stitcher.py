from unittest.mock import MagicMock

from make_pdf.preprocessors import file_stitcher


def test_stitch_files_together(mocker):
    """
    Test whether files will be stitched together in the correct order.
    """
    expected = "abc\nbbc"
    pypandoc_convert_text = mocker.patch("pypandoc.convert_file", side_effect=["abc\n", "bbc"])

    actual = file_stitcher.stitch_files_together(["file1", "file2"], False)

    assert actual == expected
    pypandoc_convert_text.assert_called()


def test_stitch_files_together_one_file(mocker):
    """
    Test whether one file will be returned correctly.
    """
    expected = "abc"
    pypandoc_convert_text = mocker.patch("pypandoc.convert_file", return_value="abc")

    actual = file_stitcher.stitch_files_together(["file1"], False)

    assert actual == expected
    pypandoc_convert_text.assert_called_once_with("file1", "md")


def test_stitch_files_together_uses_open_for_markdown(mocker):
    """
    Test whether files will be stitched together in the correct order.
    """
    expected = "abc\nbbc\n"
    mock_path = MagicMock()
    path_const_mock = mocker.patch("make_pdf.preprocessors.file_stitcher.Path", return_value=mock_path)
    mock_path.read_text.side_effect = ["abc", "bbc"]

    actual = file_stitcher.stitch_files_together(["file1.md", "file2.md"], False)

    assert actual == expected
    path_const_mock.assert_called()
    mock_path.read_text.assert_called()


def test_stitch_files_together_uses_open_for_markdown_one_file(mocker):
    """
    Test whether files will be stitched together in the correct order.
    """
    expected = "abc\n"
    mock_path = MagicMock()
    path_const_mock = mocker.patch("make_pdf.preprocessors.file_stitcher.Path", return_value=mock_path)
    mock_path.read_text.return_value = "abc"

    actual = file_stitcher.stitch_files_together(["file1.md"], False)

    assert actual == expected
    path_const_mock.assert_called_once_with("file1.md")
    mock_path.read_text.assert_called_once()
