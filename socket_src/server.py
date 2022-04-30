import socket 
from _thread import *
import queue
import time
#서버 ip주소 확인
print("IP Address(Internal) : ",socket.gethostbyname(socket.gethostname()))


q = queue.Queue() #전송받은 문자열을 큐 자료구조형태로 입,출력.
#제슨(파이썬)으로 전송받을 문자들.
hangle = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ',
          'ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ','ㅐ','ㅒ','ㅔ','ㅖ',
          'ㅟ','ㅚ','ㅢ','*']

# 젯슨나노 음성자모음 클라이언트
def communication_with_python(client_socket, addr): 
    global q
    # 서버ip : 클라이언트 포트
    print('젯슨나노 접속성공!(', addr[0], ':', addr[1],')') 

    while True: 
        try:
            data = client_socket.recv(1024)
            q.put(data)
            
            if not data: 
                #print('test',data.decode())
                #print('Disconnected by 젯슨')
                break
            

        except ConnectionResetError as e:
            #print('Disconnected by 젯슨 예외처리')
            break

    #print("젯슨 클라이언트 접속 종료") # 예외발생시 젯슨과의 tcp연결 종료를 알리는 디벙깅용함수
    client_socket.close() #젯슨 과의 클라이언트 연결 종료

    
# 유니티 클라이언트
def communication_with_unity(client_socket, addr): 
    global q
    # 서버ip : 클라이언트 포트
    print('유니티접속 성공!(', addr[0], ':', addr[1],')') 

    while True: 
        try:
            data = client_socket.recv(1024)
            if not data: 
                print('유니티 연결 종료 ' + addr[0],':',addr[1])
                break
                
            data_from_queue = q.get() #큐의 맨앞에서 encode()형의 데이터를 가져온다.
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
    
    

#서버 ip,포트
HOST = socket.gethostbyname(socket.gethostname()) #서버 자신의 고정 ip 받아오기
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
