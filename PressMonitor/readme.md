# PressMonitor

## PLC 주소의 값을 화면에 표시하는 프로그램


그래서 이제 뭐함
3. plc 통신 모듈 작성


port
2004(TCP), 2005(UDP), 502(MODBUS)

https://jeong-f.tistory.com/88
https://fortex66.tistory.com/6
https://fortex66.tistory.com/13
https://dibrary.tistory.com/158
https://sol.ls-electric.com/uploads/document/16855850048210/PLC_XGT_Ethernet%20%EC%A0%84%EC%9A%A9%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%20PC%EC%99%80%20%ED%86%B5%EC%8B%A0%20%EB%B0%A9%EB%B2%95%20_KO_V1_%EA%B3%B5%EA%B0%9C.pdf


~ 기존 mixer의 경우 Cnet 시리얼통신(XGT) ~ 

netsh interface ip set address "이더넷 4" static 192.168.0.10 255.255.255.0 192.168.0.1
~ 또 이녀석이 문제임 ~
위 명령으로 이더넷 ip 바꾸고 2004로 연결하면 connect는 된 것 같은데 값이 안와..
명령을 잘못 보낸걸까 연결이 안된걸까


```
>>> client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>>> client_socket.connect((SERVER_IP, 123))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ConnectionRefusedError: [WinError 10061] 대상 컴퓨터에서 연결을 거부했으므로 연결하지 못했습니다
>>> client_socket.connect((SERVER_IP, 2004)) 
>>>
```
이걸로 보면 연결은 된걸지도.. 프레임을 짜서 다시 와야겠다


명령을 일단 다시 써서 보내봐야겠지
프로토콜 문서:
https://ssqcdn.azureedge.net/ssqblob/largefile/document/17181661459030/XGL-EFMTB_T8_Manual_V3.6_202406_KR.pdf
이거 보고 소켓으로 쏴보고 결과 보면 될거같은데 문서가 도저히 안읽어짐



연결: 시리얼 / 이더넷
프로토콜: 전용통신(XGT) / 모드버스

** CMD를 잘 빚어서 던지고 받는 구조 **

시리얼: port(com), baudrate
이더넷: ip, port(server)

pip
- serial, pyserial
- sockect
- pymodbus
