import pytest

from load_scores import load_scores


@pytest.fixture
def write_scores(tmp_path):
    """헤더 다음에 테스트 데이터를 넣은 임시 CSV 파일을 만든다."""
    def write(rows):
        path = tmp_path / "scores.csv"
        path.write_text("이름,점수\n" + rows, encoding="utf-8")
        return path

    return write


def test_keeps_valid_rows_in_order_including_duplicate_names(write_scores):
    path = write_scores("  민수  , 85 \n지우,92\n민수,76\n")

    assert load_scores(path) == ([('민수', 85), ('지우', 92), ('민수', 76)], [])


def test_header_only_returns_two_empty_lists(write_scores):
    assert load_scores(write_scores("")) == ([], [])


def test_missing_file_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    "score, expected",
    [
        (-1, ([], [(2, "민수,-1", "점수가 0~100 밖")])),
        (0, ([("민수", 0)], [])),
        (1, ([("민수", 1)], [])),
        (99, ([("민수", 99)], [])),
        (100, ([("민수", 100)], [])),
        (101, ([], [(2, "민수,101", "점수가 0~100 밖")])),
    ],
)
def test_score_boundaries(write_scores, score, expected):
    assert load_scores(write_scores(f"민수,{score}\n")) == expected


@pytest.mark.parametrize(
    "row, reason",
    [
        pytest.param("민수", "열 개수가 2가 아님", id="one-column"),
        pytest.param("민수,80,추가", "열 개수가 2가 아님", id="three-columns"),
        pytest.param("민수,", "점수가 비어 있음", id="empty-score"),
        pytest.param("민수,  ", "점수가 비어 있음", id="spaces-only-score"),
        pytest.param("민수,80.5", "점수가 정수가 아님", id="decimal-score"),
        pytest.param("민수,결석", "점수가 정수가 아님", id="text-score"),
        pytest.param(",80", "이름이 비어 있음", id="empty-name"),
        pytest.param("  ,80", "이름이 비어 있음", id="spaces-only-name"),
    ],
)
def test_invalid_row_is_recorded_with_line_text_and_reason(write_scores, row, reason):
    assert load_scores(write_scores(row + "\n")) == ([], [(2, row, reason)])


def test_blank_lines_are_ignored_and_processing_continues(write_scores):
    path = write_scores("\n민수,88\n지우,결석\n\n수빈,101\n하늘,70\n")

    assert load_scores(path) == (
        [("민수", 88), ("하늘", 70)],
        [(4, "지우,결석", "점수가 정수가 아님"), (6, "수빈,101", "점수가 0~100 밖")],
    )
