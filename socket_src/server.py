import socket
import time
from thread_funs import set_server, waiting_client, run_thread

#서버 ip주소 확인(현재서버 주소 프린트)
print("IP Address(Internal) : ",socket.gethostbyname(socket.gethostname()))




print('서버 가동')
server_socket = set_server() #서버 세팅

while True:
    #클라이언트대기
    client_socket, addr, what_client = waiting_client(server_socket)
    #젯슨, 유니티 각각에 맞는 쓰레드 함수 생성및 실행
    run_thread(client_socket, addr, what_client)

print('server ended')
server_socket.close()
