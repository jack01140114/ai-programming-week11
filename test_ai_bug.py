import pytest

from scores import find_max


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        pytest.param([9, 3, 5], 9, id="max-first"),
        pytest.param([2, 9, 5], 9, id="max-middle"),
        pytest.param([2, 5, 9], 9, id="max-last"),
        pytest.param([-8, -2, -5], -2, id="all-negative"),
        pytest.param([4, 4, 1], 4, id="duplicate-max"),
        pytest.param([7], 7, id="single-item"),
        pytest.param([8, 3], 8, id="two-items-max-first"),
        pytest.param([2, 9], 9, id="two-items-max-last"),
    ],
)
def test_find_max(scores, expected):
    assert find_max(scores) == expected


def test_find_max_empty_list_raises_index_error():
    with pytest.raises(IndexError):
        find_max([])
