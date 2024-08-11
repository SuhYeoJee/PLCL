# PLC MONITOR TEMPLATE

## PLC 주소의 값을 화면에 표시하는 프로그램


### LOG

> v2.00
- `QT Designer` 사용해서 `.ui` 파일로 화면 생성
- `QThread`로 주기적 갱신
- `state` 별 `dataset` 적용
- `PLC_ADDR`의 `DATASET LINEEDIT`에 자동적용


***

> v1.00
- MVC 클래스 분리
- `WindowBuilder`: 위젯, 레이아웃 생성기
- `controller` 클래스에서 `ConfigParser`사용