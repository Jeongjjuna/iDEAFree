import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3

from unicode import join_jamos
from functions import execute_tts

# 사용할 제스쳐 따로만들기!
GESTURE = {0:'zero', 1:'one', 2:'two', 3:'three', 4:'four', 5:'five',
    6:'six', 7:'seven', 8:'eight', 9:'nine', 10:'ten', 11:'eleven',12:'twelve',13:'thirteen',
    14:'14',15:'15',16:'16',17:'17',18:'18',19:'19',20:'20',21:'21',22:'22',23:'23',
    24:'24',25:'25',26:'26',27:'27',28:'28',29:'29',30:'30'}

HANGEUL = {0:'ㄱ', 1:'ㄴ', 2:'ㄷ', 3:'ㄹ', 4:'ㅁ', 5:'ㅂ',
    6:'ㅅ', 7:'ㅇ', 8:'ㅈ', 9:'ㅊ', 10:'ㅋ', 11:'ㅌ',12:'ㅍ',13:'ㅎ',
    14:'ㅏ',15:'ㅑ',16:'ㅓ',17:'ㅕ',18:'ㅗ',19:'ㅛ',20:'ㅜ',21:'ㅠ',22:'ㅡ',23:'ㅣ',
    24:'ㅐ',25:'ㅔ',26:'ㅚ',27:'ㅟ',28:'ㅒ',29:'예',30:'ㅢ'}

MAX_NUM_HANDS = 1 # 탐지할 손 개수 1개!
waiting_time = 120 # waiting_time프레임만큼 동작이 들어오는지 판단하는 변수
text_list = [] #입력받은 텍스트를 받아들일 변수
count = 0 #모션 체인지의 카운터 변수
count2 = [] # 음성변환으로의 카운터 변수
stack=[]

# MediaPipe hands model 파라미터 설정(손가져오기!)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=MAX_NUM_HANDS,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Gesture recognition model
file = np.genfromtxt('data/lastdata.csv', delimiter=',')
angle = file[:,:-1].astype(np.float32) # x_train  >>> x=각도 20개
label = file[:, -1].astype(np.float32) # y_train  >>> y=모션 1개
knn = cv2.ml.KNearest_create()  #knn모델생성
knn.train(angle, cv2.ml.ROW_SAMPLE, label) #knn모델학습


#웹캠에서 이미지 읽어오기
cap = cv2.VideoCapture(0)

while cap.isOpened():
    if len(text_list)!=0 and len(count2)==waiting_time: #waiting_time프레임동안 손가락이 추가로 읽히지 않았다면 그동안 모인 텍스트를 음성으로 출력
        execute_tts(text_list)
        text_list = [] #음성으로 출력 후 text_list 초기화

    ret, img = cap.read() #한프레임!!씩 이미지를 읽어온다.
    if not ret:
        continue
    
    #이미지 칼라(흑백) 및 반전 설정가능
    #img = cv2.flip(img, 1) 여기 주석처리하면 반전시킬 수 있음
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    #각도계산 하기!! 제일 중요!! 분석해서 실시간으로 모션 각도 추출해서 데이터셋 만들어야함!!!
    if result.multi_hand_landmarks is not None: #만약 손자체가 인식됐다면!
        count2= []
        for res in result.multi_hand_landmarks:
            
            #----------------------------------------------랜드마크로부터 데이터 값 추출 및 전처리-----------------------------------------
            joint = np.zeros((21, 3))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            # Compute angles between joints
            v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] # Parent joint
            v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] # Child joint
            v = v2 - v1 # [20,3]  #벡터값 생성 (x1-x2,y1-y2,z1-z3) >조인트점21개에서 벡터값으로 변환하여 20개의 벡터방향이나옴
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis] #벡터/벡터길이 >>Normalize  크기가 1인 벡터 만들기 (길이공식나중에확인하기~)

            # Get angle using arcos of dot product>>>>>> 각도구하기 공식! 수학공식임(논문참조)
            angle = np.arccos(np.einsum('nt,nt->n',
                v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18,3,3,3,3],:], 
                v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19,7,11,15,19],:])) # (19,)

            angle = np.degrees(angle) # Convert radian to degree        

            # 벡터 사이의 각도를 데이터로 가지는 numpy array 생성(분류할 데이터값들)
            data = np.array([angle], dtype=np.float32)# (19,)

            #19개의 데이터를 각도0~180도에 대하여 정규화 
            for d in range(len(data[0])):
                data[0][d] = round(data[0][d]/180, 4)

            #동서남북 구분코드
            # #(가령 ㄱ, ㄴ은 각 좌표의 각도는 같지만 서로 다른 분류값이기 때문에 손전체가 가르키는 방향변수를 추가로 학습하여 분류 할 수 있도록 한다.)
            if abs(joint[8][0]-joint[0][0])>abs(joint[8][1]-joint[0][1]):
                if joint[8][0]<joint[0][0]:
                    k = 0.0
                else:
                    k = 60.0
            else:
                if joint[8][1]>joint[0][1]:
                    k = 120.0
                else:
                    k = 180.0
            data=np.append(data[0],round(k/180, 4)) #추가된 방향정보의 변수 데이터값도 0~180사이로 정규화 해준다. 총4가지(0,60,120,180)
            data = np.array([data],dtype=np.float32)

            #knn으로 분류할 data numpy array 완성
            #-----------------------------------------------------------------------------------------------------------------------------


            #-----------------------------------------------------사용안하기로했음 -> 동서남북 구분 변수로 해결
            #앞 뒤 구분코드
            # if joint[2][0]-joint[17][0]>0: #손등이보인다
            #     kk = 0.0
            # else: #손바닥이보인다
            #     kk = 90.0
            # data=np.append(data[0],kk)
            # data = np.array([data],dtype=np.float32)
            #------------------------------------------------------

            #print(data)

            #------------------------------------------------------
            ret, results, neighbours, dist = knn.findNearest(data, 9) #knn머신러닝 모델을 이용하여 data값 분류 -->> 최적의 k값을 찾을 필요 있음
            idx = int(round(results[0][0]*30,1)) #정규화된 변수를 0~30인덱스로 변환한다(GESTURE, HANGEUL 리스트 변수의 인덱스를 사용하기 위함)

            # Draw gesture result(개발영역에서 디버깅 및 확인 할 용도)
            if idx in GESTURE.keys():
                cv2.putText(img, text=str(idx), org=(int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0] + 20)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
                #text=GESTURE[idx] 에서 HANGEUL 딕셔너리를 사용하면 더 보기좋을듯(OpenCv 한글 출력할 수 있는 솔루션 필요!)
            mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)
            

            #-----------실시간 손이 가지는 데이타값을 출력해보기위해 작성---------
            #데이터출력을 위한 20프레임간격출력
            # if count%20==0:
            #     for i in range(16):
            #         if  i == 15:
            #             print(data[0][i])
            #         else:
            #             print(data[0][i],end=",")
            #     count=0
            #--------------------------------------------------------------------

            stack.append(idx)
            if count%10==0:
                k=stack.pop()
                if stack.count(k)>=18:
                    len_text=len(text_list)
                    if len_text==0:
                        print(k,'입력완료') #이때 입력받았다고 사용자에게 알려줘야함 led?? 잠깐 텀이 필요함
                        text_list.append(HANGEUL[k])
                        time.sleep(0.3)
                        stack=[]
                    else:
                        #연속된 모음이 들어오는지 아닌지
                        for x in HANGEUL:
                            if HANGEUL[x]==text_list[len_text-1]:
                                index = x
                                break

                        if 14<=x<=30 and 14<=k<=30:
                            pass
                        else:
                            print(k,'입력완료') #이때 입력받았다고 사용자에게 알려줘야함 led?? 잠깐 텀이 필요함
                            text_list.append(HANGEUL[k])
                            time.sleep(0.3)
                            stack=[]
                else:
                    stack
                #print(list(angle))
            count+=1

    count2.append(0) #모션탐지가 안될때 카운팅하는 리스트

    cv2.imshow('Game', img)
    if cv2.waitKey(1) == ord('q'):
        break
