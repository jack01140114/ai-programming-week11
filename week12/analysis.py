from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent


def 정제(df: pd.DataFrame, *, show_counts: bool = False) -> pd.DataFrame:
    """배포 명세 순서대로 점수와 분류값을 정제한다."""
    counts = {"시작": len(df)}
    clean = df.dropna(subset=["점수"])
    counts["빈 칸 제거"] = len(clean)
    clean = clean.drop_duplicates().copy()
    counts["중복 제거"] = len(clean)
    clean["반"] = clean["반"].str.strip()
    clean["과목"] = clean["과목"].str.strip()
    counts["공백 정리"] = len(clean)
    clean = clean.loc[clean["점수"].between(0, 100)].copy()
    counts["범위 밖 제거"] = len(clean)

    if show_counts:
        for stage, count in counts.items():
            print(f"{stage}: {count}")
    return clean


def 반별평균(df: pd.DataFrame) -> pd.Series:
    return df.groupby("반")["점수"].mean()


def main() -> None:
    raw = pd.read_csv(DATA_DIR / "scores_2026.csv", dtype={"학번": str})
    score = raw["점수"]
    print(f"원본: {raw.shape[0]}행 × {raw.shape[1]}열")
    print(f"빈 점수: {score.isna().sum()}, 완전 중복: {raw.duplicated().sum()}")
    print(f"반: {raw['반'].unique().tolist()}, 과목: {raw['과목'].unique().tolist()}")
    print(f"원본 점수 범위: {score.min():g}~{score.max():g}\n")

    clean = 정제(raw, show_counts=True)
    math = clean.loc[clean["과목"].eq("수학")]
    print(f"\n수학 행 수: {len(math)}")
    print(f"\n반별 평균\n{반별평균(clean).round(2).to_string()}")
    print("\n과목·반별 평균")
    print(clean.groupby(["과목", "반"])["점수"].mean().unstack().round(2))

    grouped = clean.groupby("반")["점수"]
    stats = grouped.agg(개수="count", 평균="mean", 중앙값="median", 최댓값="max")
    print(f"\n반별 통계\n{stats.round(2).to_string()}")
    print(f"\n그룹 합계 / 전체 합계: {grouped.sum().sum():g} / {clean['점수'].sum():g}")
    print(f"그룹 개수 / 전체 행: {grouped.count().sum()} / {len(clean)}")

    spot = math.loc[math["반"].eq("1반"), "점수"]
    values = [int(value) for value in spot]
    print(f"스팟 체크 (1반 수학): {values}, 합계 {spot.sum():g}, 평균 {spot.mean():g}")


if __name__ == "__main__":
    main()
