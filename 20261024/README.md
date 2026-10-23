# 손 인식을 이용한 가상 공 제어

## 프로젝트 소개
카메라 영상에서 MediaPipe로 손을 인식하고, 엄지와 검지를 이용해 화면의 가상 공을 잡고 이동시키는 프로그램입니다.

## 사용 기술
- Python
- OpenCV
- MediaPipe Hand Landmarker
- NumPy
- GStreamer

## 주요 기능
- 카메라 영상을 좌우 반전하여 출력
- 엄지와 검지 끝의 위치 인식
- 공 근처에서 두 손가락을 모으면 공 잡기
- 공을 잡은 상태에서 손을 움직이면 공 이동
- 두 손가락을 벌리면 공 놓기
- 화면에 GRABBED / RELEASED 상태 표시

## 실행 준비
- Python과 NumPy, MediaPipe 설치
- GStreamer를 지원하는 OpenCV 및 카메라 사용 환경 준비
- MediaPipe Hand Landmarker 모델 파일 준비

모델 파일은 실행하는 위치를 기준으로 다음 경로에 있어야 합니다.

```text
src/models/MediaPipe/hand_landmarker.task
```

현재 코드는 Linux의 `/dev/video0` 카메라와 GStreamer 파이프라인을 사용하도록 작성되어 있습니다.

## 실행 방법
모델 경로가 준비된 작업 디렉터리에서 실행합니다.

```bash
python3 project01.py
```

## 조작 방법
1. 카메라에 손을 비춥니다.
2. 주황색 공 근처에서 엄지와 검지를 모아 공을 잡습니다.
3. 손을 움직여 공을 이동합니다.
4. 손가락을 벌려 공을 놓습니다.
5. 영상 창에서 `q` 키를 누르면 종료합니다.
