import pandas as pd
import pytest

from analysis import DATA_DIR, 반별평균, 정제


@pytest.fixture(scope="module")
def scores():
    return 정제(pd.read_csv(DATA_DIR / "scores_2026.csv", dtype={"학번": str}))


@pytest.fixture(scope="module")
def mini():
    return 정제(pd.read_csv(DATA_DIR / "mini.csv", dtype={"학번": str}))


def test_정제_후_100행(scores):
    row_count = len(scores)
    assert row_count == 100


def test_정제_후_두_반(scores):
    assert sorted(scores["반"].unique()) == ["1반", "2반"]


def test_그룹_합계와_개수_보존(scores):
    grouped = scores.groupby("반")["점수"]
    assert grouped.sum().sum() == scores["점수"].sum() == 7484
    assert grouped.count().sum() == len(scores)


def test_미니_데이터_계산과_일치(mini):
    assert len(mini) == 7
    assert 반별평균(mini).to_dict() == {"1반": 80.0, "2반": 70.0}
