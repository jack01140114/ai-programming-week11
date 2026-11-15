# 성적 CSV 검사기

## 무엇을 하나요 (What)

성적 CSV에서 유효한 이름과 점수를 읽고, 제외한 행의 번호와 이유를 출력합니다.

## 왜 만들었나요 (Why)

배포된 성적 파일에는 빈 점수, 범위를 벗어난 점수, 열 개수가 다른 행이 섞여 있습니다. 잘못된 행을 입력 순서대로 추적하고, 0점과 100점처럼 경계에 있는 성적이 올바르게 보존되는지 반복해서 검증할 수 있도록 테스트했습니다. 동명이인에 해당하는 유효한 행은 모두 남깁니다.

## 어떻게 쓰나요 (How)

Python 3.10 이상이 필요합니다. 저장소 폴더에서 실행합니다.

```bash
python -m pip install -r requirements-dev.txt
python load_scores.py scores.csv
```

배포된 `scores.csv`에서는 유효 행 5개와 제외 행 5개가 나옵니다.

## 어떻게 테스트하나요

```bash
python -m pytest -q test_load_scores.py
python -m pytest -q --cov=load_scores --cov-report=term-missing test_load_scores.py
```

실제 실행 결과

```text
............... [100%]
15 passed
load_scores.py   45 statements   9 missing   80%
Missing lines: 77-86
```

AI 비교는 각 파일을 따로 실행합니다.

```bash
python -m pytest -q test_ai_A.py
python -m pytest -q test_ai_B.py
```

A는 18개 통과했습니다. B는 `scores` 모듈을 가정해 원본 상태에서는 수집 중 오류가 났습니다. 임시 모듈을 통해 배포 구현에 연결하자 13개가 통과하고 1개가 실패했습니다. 함정 테스트도 원본 상태에서 같은 모듈 오류가 나며, 임시 모듈을 통해 `bug3_logic.find_max`에 연결하자 마지막 원소가 최댓값인 두 사례가 실패했습니다.

## 파일 구성

| 파일 | 하는 일 |
| --- | --- |
| `load_scores.py` | 배포판 성적 CSV 읽기 함수와 실행 진입점 |
| `scores.csv`, `empty.csv`, `weird.csv` | 실습에서 배포된 CSV 예제 |
| `test_load_scores.py` | 명세로 설계한 정상·예외·경계값 테스트 |
| `test_ai_A.py`, `test_ai_B.py` | 각각 구현과 명세를 입력으로 받은 테스트 원본 |
| `bug3_logic.py`, `test_ai_bug.py` | 마지막 원소를 놓치는 배포 코드와 AI 함정 테스트 |
| `requirements-dev.txt`, `pytest.ini` | 테스트 의존성과 기본 수집 설정 |
| `LICENSE` | 이 저장소에서 추가한 코드의 MIT 라이선스 |

## 만든 사람과 AI 사용 범위

- 작성자 GitHub 계정은 `jack01140114`입니다. 학번은 제출 문서에 기재합니다.
- Codex를 사용해 테스트 작성, 실행 결과 비교, README와 워크시트 정리를 보조했습니다. A·B·함정은 각각 새 대화에서 받았습니다.
- 기대 결과는 실습 명세의 0~100 범위, 동명이인 유지, 제외 기록 규칙에 따라 정했습니다. 자동 판정은 pytest 결과로 확인했습니다.

## 라이선스

새로 작성한 코드에는 [MIT License](LICENSE)를 적용합니다. 실습 배포 파일은 수업 제공 자료입니다.
