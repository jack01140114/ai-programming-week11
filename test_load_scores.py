import pytest

from load_scores import load_scores


def write_csv(tmp_path, text):
    path = tmp_path / "sample.csv"
    path.write_text(text, encoding="utf-8")
    return path


def test_ordinary_file_preserves_order_and_equal_names(tmp_path):
    path = write_csv(tmp_path, "name,score\n하나,88\n두리,75\n하나,91\n")
    assert load_scores(path) == ([("하나", 88), ("두리", 75), ("하나", 91)], [])


def test_blank_line_is_skipped_without_report(tmp_path):
    path = write_csv(tmp_path, "name,score\n하나,88\n\n두리,75\n")
    assert load_scores(path) == ([("하나", 88), ("두리", 75)], [])


def test_quoted_comma_is_part_of_name(tmp_path):
    path = write_csv(tmp_path, 'name,score\n"최,네번",77\n')
    assert load_scores(path) == ([("최,네번", 77)], [])


def test_missing_file_propagates_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_header_only_returns_two_empty_lists(tmp_path):
    path = write_csv(tmp_path, "name,score\n")
    assert load_scores(path) == ([], [])


@pytest.mark.parametrize(
    "score,valid",
    [(-1, False), (0, True), (1, True), (99, True), (100, True), (101, False)],
)
def test_score_boundaries(tmp_path, score, valid):
    path = write_csv(tmp_path, f"name,score\n하나,{score}\n")
    if valid:
        assert load_scores(path) == ([("하나", score)], [])
    else:
        assert load_scores(path) == ([], [(2, f"하나,{score}", "점수가 0~100 밖")])

@pytest.mark.parametrize(
    "row,reason",
    [
        ("하나,80,추가", "열 개수가 2가 아님"),
        (",80", "이름이 비어 있음"),
        ("하나,", "점수가 비어 있음"),
        ("하나,결석", "점수가 정수가 아님"),
    ],
)
def test_invalid_row_is_reported_and_next_row_is_preserved(tmp_path, row, reason):
    path = write_csv(tmp_path, f"name,score\n{row}\n두리,75\n")
    assert load_scores(path) == ([("두리", 75)], [(2, row, reason)])
