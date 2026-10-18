# Python Assignment 02

몸이 아파 수업에 참석하지 못해 과제 제출이 늦었습니다.
강의 자료를 참고하여 과제를 작성했고, 늦었지만 지금이라도 제출합니다.
제출이 늦어 죄송합니다.

## 1. 과제 설명
OpenCV를 활용하여 농구공 영역과 외곽선을 검출하는 프로그램입니다.
강의 자료 `02_Computer-Vision.ipynb`의 예제를 참고했습니다.

주요 기능:
- LAB 색공간 변환 및 CLAHE 적용
- 농구공 색상 범위로 이진 마스크 생성
- Opening과 Closing 결과 비교
- Opening 후 Closing을 적용하여 최종 마스크 생성
- 가장 큰 외곽선을 선택하여 농구공 영역과 외곽선 표시

## 2. 실행 환경
- Python 3
- OpenCV
- NumPy
- Matplotlib
- 실행 명령어: python3 20261017/assignment02.py

## 3. 참고 사항
- 저장소의 `src/images/basketball_crop.jpg`를 사용합니다.
- 실행하려면 Python 파일과 함께 이미지 파일도 필요합니다.
- 마스크 비교 결과와 최종 농구공 검출 결과를 각각 표시합니다.
- 강의 예제처럼 면적이 가장 큰 외곽선을 농구공 영역으로 선택합니다.
