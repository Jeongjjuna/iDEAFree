import socket
import time

import speech_recognition as sr
from jamo import h2j,j2hcj
from _thread import *
import queue
#from hanspell import spell_checker


# import serial
# serialport = serial.Serial("/dev/ttyUSB0",9600,timeout=3)


def string1(string):  # 조사를 단순화 하는 함수!

    string = string.replace('었다', '다')
    string = string.replace('했다', '하다')
    string = string.replace('했는가', '했나') #'는' 이랑 '가' 가 같이 붙어있을시 끝에 '가'가 생략되면서 이상해지니까 추가 밑에 있는 조사가 붙어있을 시 생각!
    string = string.replace('이와', '과')# 지훈이와 => 지훈과
    string = string.replace('이야', '')
    string = string.split()
    
    for i in range(len(string)):
        if string[i][-1] == "은" or string[i][-1] == "을" or string[i][-1] == "이" \
            or string[i][-1] == "는" or string[i][-1] == "과" or string[i][-1] == "와" or string[i][-1] == "가"\
        or string[i][-1] == "로" or string[i][-1]== "를":
            string[i] = list(string[i])
            del string[i][-1]
            string[i] ="".join(string[i])
    
    string = " ".join(string)

    return string

# 리스트에 ' '다음의 자음은 무조건 종성이다! (안녕 나는 지훈)
def dist_chosung_jongsung(str): #['ㅇ','ㅏ','ㄴ','ㄴ','ㅕ','ㅇ',' ','ㄴ','ㅏ','ㄴ','ㅡ','ㄴ',' ','ㅈ','ㅣ','ㅎ','ㅜ','ㄴ',' ']
    answer = []
    ja = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'] #자음리스트
    
    #단어 구분자를 '*'로 변환
    for i,x in enumerate(str):
        if x == ' ':
            str[i]='*'


    for i,x in enumerate(str):
        if x in ja: # 만약자음인데
            if str[i+1] in ja or str[i+1]=='*': #다음문자도 자음 혹은 단어구분자'*' 라면
                answer.append(' ')

        answer.append(x)
    return answer


def get_audio():           #마이크로 부터 음성 받아드리는 함수
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = " "
        try:
            said = r.recognize_google(audio, language="ko-KR")

        except Exception as e:
            print("Exception: " + str(e))
    return said

button = queue.Queue()
std = 0
# 유니티(서버) 로부터 버튼정보를 받는 쓰레드
def buttonData_from_unity(client_socket, k):
    global button, std
    # 서버ip : 클라이언트 포트
    print('젯슨유니티 통신단 접속성공!')

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('서버가 꺼진거겠죠?')
                break
            if std%2 == 0:
                print("음성차단모드")
            else:
                print("음성대기모드전환")
            std += 1
            
        except ConnectionResetError as e:
            break

    print('서버가 꺼진거겠죠?')
    client_socket.close() #서버와의 젯슨유니티 통신단 연결 종료




# 로컬은 127.0.0.1의 ip로 접속한다.
#HOST = '168.131.153.213'
HOST = '127.0.0.1'
# port는 위 서버에서 설정한 9999로 접속을 한다.
PORT = 9999 #사용할 주소 ip와 맞는 port 할당!!!
# 소켓을 만든다.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect함수로 접속을 한다.
client_socket.connect((HOST, PORT))
me = 'jetson' 
client_socket.send(me.encode())

time.sleep(0.5)
start_new_thread(buttonData_from_unity, (client_socket, 0))

td_list=['저기요','실례합니다','주완아','지훈아','야']



#std = "0"
# 10번의 루프로 send receive를 한다.
while True:    
    # data2 = serialport.readline()                                                                                                                                                                                                              
    # data2=data2.strip()
    # print(std,data2.decode())
    # if std == "1" and data2.decode() == "1":
    #     std = "0"
    
    # elif std == "0" and data2.decode() == "1":
    #     std = "1"
        

        
    #if std == "1":
    
    
    if std%2 == 0: #이때만 음성 입력받기
        print('음성을입력하세요')
        text= get_audio() #아마 여기가 무한대기(시간제한걸어서 해결해야될듯)
        print(text)
        # if text in td_list:
        #     serialport.write("v".encode())    

        jamo_str = j2hcj(h2j(text))
        jamo_str = list(jamo_str)
        jamo_str.append(' ')
        jamo_str = dist_chosung_jongsung(jamo_str)
        print(jamo_str)
        for msg in jamo_str:
            if std % 2 != 0 and msg ==' ':
                client_socket.send(msg.encode())
                time.sleep(0.5)
                client_socket.send("*".encode())
                break

            data = msg.encode()
            length = len(data)
            client_socket.sendall(length.to_bytes(4, byteorder="big"))
            client_socket.sendall(data)
            time.sleep(0.5)
        
    
    time.sleep(2)
    # else:
    #     print('wait')
    #     continue
            

client_socket.close()
