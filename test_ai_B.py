"""load_scores의 CSV 처리 계약을 검증한다.

구현 모듈명이 다르면 아래 import를 바꾼 뒤 python -m pytest로 실행한다.
"""

import pytest

from scores import load_scores


@pytest.fixture
def csv_path(tmp_path):
    return tmp_path / "성적표.csv"


def test_loads_utf8_csv_in_input_order_without_modifying_file(csv_path):
    original = (
        'name,score\r\n'
        '  김하늘  , 100 \r\n'
        '" 박,지우 ", 0 \r\n'
        '김하늘, 87\r\n'
        '이서윤,42'
    ).encode("utf-8")
    csv_path.write_bytes(original)

    result = load_scores(str(csv_path))

    expected = [("김하늘", 100), ("박,지우", 0), ("김하늘", 87), ("이서윤", 42)]
    assert result == (expected, [])
    assert all(type(score) is int for _, score in result[0])
    assert csv_path.read_bytes() == original


def test_header_only_returns_empty_lists(csv_path):
    csv_path.write_bytes(b"name,score\n")

    assert load_scores(str(csv_path)) == ([], [])


def test_missing_file_propagates_file_not_found(csv_path):
    with pytest.raises(FileNotFoundError):
        load_scores(str(csv_path))


@pytest.mark.parametrize(
    "invalid_row",
    [
        pytest.param("  한 열만 있음  ", id="too-few-columns"),
        pytest.param('"김,하늘", 70 ,추가', id="too-many-columns"),
        pytest.param(",70", id="empty-name"),
        pytest.param(" \t ,70", id="whitespace-only-name"),
        pytest.param("김하늘,", id="empty-score"),
        pytest.param("김하늘, \t ", id="whitespace-only-score"),
        pytest.param("김하늘,일흔", id="non-numeric-score"),
        pytest.param("김하늘,70.5", id="fractional-score"),
        pytest.param("김하늘,-1", id="below-minimum"),
        pytest.param("김하늘,101", id="above-maximum"),
    ],
)
def test_records_invalid_row_and_continues_after_blank_line(csv_path, invalid_row):
    original = f"name,score\n앞 사람,20\n\n{invalid_row}\n뒷 사람,49\n".encode("utf-8")
    csv_path.write_bytes(original)

    valid, rejected = load_scores(str(csv_path))

    assert valid == [("앞 사람", 20), ("뒷 사람", 49)]
    assert isinstance(rejected, list)
    assert len(rejected) == 1
    assert_rejection(rejected[0], 4, invalid_row)
    assert csv_path.read_bytes() == original


def test_preserves_rejection_order_and_physical_line_numbers(csv_path):
    csv_path.write_bytes("name,score\n\n이름만\n유효,50\n\n다른 이름,101".encode("utf-8"))

    valid, rejected = load_scores(str(csv_path))

    assert valid == [("유효", 50)]
    assert len(rejected) == 2
    assert_rejection(rejected[0], 3, "이름만")
    assert_rejection(rejected[1], 6, "다른 이름,101", terminator="")


def assert_rejection(entry, line_number, raw_row, terminator="\n"):
    assert isinstance(entry, tuple)
    actual_line, actual_row, reason = entry
    assert type(actual_line) is int
    assert actual_line == line_number
    # 개행 포함 여부와 사유의 구체적인 문구는 명세에서 정하지 않는다.
    assert actual_row in (raw_row, raw_row + terminator)
    assert isinstance(reason, str)
    assert reason.strip()
