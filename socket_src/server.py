import socket 
from _thread import *
import queue
import time
from thread_funs import *

print("IP Address(Internal) : ",socket.gethostbyname(socket.gethostname()))#서버 ip주소 확인
python_to_unity_queue = queue.Queue() #전송받은 문자열을 큐 자료구조형태로 입,출력.
#제슨(파이썬)으로 전송받을 문자들.
hangle = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ',
          'ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ','ㅐ','ㅒ','ㅔ','ㅖ',
          'ㅟ','ㅚ','ㅢ','*']

#서버 ip,포트
#HOST = socket.gethostbyname(socket.gethostname()) #서버 자신의 고정 ip 받아오기
HOST = '127.0.0.1'
PORT = 9999

#서버연결
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 
print('서버 가동!!')

k = 0 # 젯슨 > 유니티 순으로 클라이언트를 받을 카운팅 변수
while True:
    
    print('클라이언트 접속 대기중...')
    #accept들어올때 까지 대기
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024) #들어오면 곧바로 클라이언트로부터 내가 어떤 클라이언트인지 메세지 받기
          
    #받은 메세지가 'unity' 라면 유니티 쓰레드함수로 이동
    if data.decode() == 'unity':
        start_new_thread(communication_with_unity, (client_socket, addr)) #유니티
    #받은 메세지가 'unity'가 아니라면 음성인식 쓰레드함수로 이동
    else:
        start_new_thread(communication_with_python, (client_socket, addr)) #젯슨

    
print('server ended')
server_socket.close()
