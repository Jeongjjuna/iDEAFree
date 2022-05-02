import socket 
from _thread import *
import time
import queue
#서버, 클라이언트, 쓰레드관련 함수 모음--------------------------------------------------------------------

#전역변수 선언----------------------------------------------------------------

python_to_unity_queue = queue.Queue() #파이썬으로부터 받은문자들
unity_to_python_queue = queue.Queue() #유니티로부터 받은문자들

#제슨(파이썬)으로 전송받을 문자리스트
hangle = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ',
        'ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ','ㅐ','ㅒ','ㅔ','ㅖ',
        'ㅟ','ㅚ','ㅢ','*']

#-----------------------------------------------------------------------------

# 젯슨나노 음성자모음 클라이언트
def communication_with_python(client_socket, addr):
    global python_to_unity_queue, unity_to_python_queue
    # 서버ip : 클라이언트 포트
    print('젯슨나노 접속성공!(', addr[0], ':', addr[1],')') 

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                #print('젯슨나노 연결 종료' + addr[0],':',addr[1])
                break
            print(data.decode().strip())
            python_to_unity_queue.put(data)
            
        except ConnectionResetError as e:
            #print('Disconnected by 젯슨 예외처리')
            break

    print('젯슨나노 연결 종료' + addr[0],':',addr[1]) # 예외발생시 젯슨과의 tcp연결 종료를 알리는 디벙깅용함수
    client_socket.close() #젯슨 과의 클라이언트 연결 종료


# 유니티 클라이언트
def communication_with_unity(client_socket, addr): 
    global python_to_unity_queue, unity_to_python_queue
    # 서버ip : 클라이언트 포트
    print('유니티접속 성공!(', addr[0], ':', addr[1],')') 

    while True:
        try:
            #data_from_unity = client_socket.recv(1024) #여기서 대기하고 있기때문에 이부분은 또다른 쓰레드로 만들어야 할듯!
            # if not data_from_unity: 
            #     print('유니티 연결 종료 ' + addr[0],':',addr[1])
            #     break
            
            #유니티에서 파이썬으로 전달하는 데이터받아서 집어넣기
            # if data_from_unity.decode() == 'ChangeHanddetectionMode':
            #     unity_to_python_queue.put(data_from_unity)
            # elif data_from_unity.decode() == 'ChangListenMode':
            #     unity_to_python_queue.put(data_from_unity)

            data_from_queue = python_to_unity_queue.get() #큐의 맨앞에서 encode()형의 데이터를 가져온다.
            if data_from_queue: #데이터 값이 존재한다면
                if data_from_queue == b'\x00\x00\x00\x03': #서버에서의 전송받을 시 공백구분데이터 > 이때는 패스
                    continue
                else:
                    #받은 데이터가 hangle 안에 있는 문자열 일 때
                    if data_from_queue.decode() in hangle:# !!!! data.decode() 는data유형을 실제로 변환시키지 않는다.
                        print('발신',data_from_queue.decode(),end='') #전송된 데이터와 유니티로의 전송이 성공했을때를 알려주는 디버깅용 함수
                        print(' >>> 유니티로 전송 발신 성공')
                        client_socket.send(data_from_queue) #실제 유니티로 데이터 전송
                        time.sleep(0.25)
                        
                    elif data_from_queue.decode() == ' ':
                        print('발신',data_from_queue.decode(),end='') #전송된 데이터와 유니티로의 전송이 성공했을때를 알려주는 디버깅용 함수
                        print(' >>> 유니티로 전송 발신 성공')
                        client_socket.send(data_from_queue) #실제 유니티로 데이터 전송
                        time.sleep(0.1)
            
        except ConnectionResetError as e:
            print('Disconnected by 유니티 예외처리')# 예외발생시 유니티와의 tcp연결 종료를 알리는 디벙깅용함수
            break
    
    print("유니티 클라이언트 접속 종료")
    client_socket.close() #클라이언트 연결 종료


def set_server():
    #서버 ip,포트
    #HOST = socket.gethostbyname(socket.gethostname()) #서버 자신의 고정 ip 받아오기
    HOST = '127.0.0.1'
    PORT = 9999
    #서버연결
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT)) 
    server_socket.listen()
    return server_socket


def waiting_client(server_socket):
    print('클라이언트 접속 대기중...')
    client_socket, addr = server_socket.accept() #accept들어올때 까지 대기
    what_client = client_socket.recv(1024) # ex) data = 'unity' or 'jetson'

    return client_socket, addr, what_client


def run_thread(client_socket, addr, what_client):
    #받은 메세지가 'unity' 라면 유니티 쓰레드함수로 이동
    if what_client.decode() == 'unity':
        start_new_thread(communication_with_unity, (client_socket, addr)) #유니티
    #받은 메세지가 'unity'가 아니라면 음성인식 쓰레드함수로 이동
    else:
        start_new_thread(communication_with_python, (client_socket, addr)) #젯슨
