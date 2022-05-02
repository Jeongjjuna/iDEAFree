import socket
import queue
import time
from thread_funs import set_server, waiting_client, run_thread

#서버 ip주소 확인(현재서버 주소 프린트)
print("IP Address(Internal) : ",socket.gethostbyname(socket.gethostname()))

#전역변수 선언----------------------------------------------------------------

python_to_unity_queue = queue.Queue() #파이썬으로부터 받은문자들
unity_to_python_queue = queue.Queue() #유니티로부터 받은문자들

#제슨(파이썬)으로 전송받을 문자리스트
hangle = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ',
          'ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ','ㅐ','ㅒ','ㅔ','ㅖ',
          'ㅟ','ㅚ','ㅢ','*']

#-----------------------------------------------------------------------------

if __name__ == "__main__":
    print('서버 가동')
    server_socket = set_server() #서버 세팅
    
    while True:
        #클라이언트대기
        client_socket, addr, what_client = waiting_client(server_socket)
        #젯슨, 유니티 각각에 맞는 쓰레드 함수 생성및 실행
        run_thread(client_socket, addr, what_client)
    
    print('server ended')
    server_socket.close()
