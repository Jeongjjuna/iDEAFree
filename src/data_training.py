import cv2
import mediapipe as mp
import numpy as np
import time

import pyttsx3
from unicode import join_jamos

# 탐지할 손 개수 1개!
max_num_hands = 1 

# 사용할 제스쳐 따로만들기!
gesture = {0:'zero', 1:'one', 2:'two', 3:'three', 4:'four', 5:'five',
    6:'six', 7:'seven', 8:'eight', 9:'nine', 10:'ten', 11:'eleven',12:'twelve',13:'thirteen',
    14:'14',15:'15',16:'16',17:'17',18:'18',19:'19',20:'20',21:'21',22:'22',23:'23',
    24:'24',25:'25',26:'26',27:'27',28:'28',29:'29',30:'30'}

han = {0:'ㄱ', 1:'ㄴ', 2:'ㄷ', 3:'ㄹ', 4:'ㅁ', 5:'ㅂ',
    6:'ㅅ', 7:'ㅇ', 8:'ㅈ', 9:'ㅊ', 10:'ㅋ', 11:'ㅌ',12:'ㅍ',13:'ㅎ',
    14:'ㅏ',15:'ㅑ',16:'ㅓ',17:'ㅕ',18:'ㅗ',19:'ㅛ',20:'ㅜ',21:'ㅠ',22:'ㅡ',23:'ㅣ',
    24:'ㅐ',25:'ㅔ',26:'ㅚ',27:'ㅟ',28:'ㅒ',29:'예',30:'ㅢ'}


# MediaPipe hands model 손가져오기!
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=max_num_hands,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9)


# Gesture recognition model
file = np.genfromtxt('data/jihun_data.csv', delimiter=',')
angle = file[:,:-1].astype(np.float32) # x_train  >>> x=각도 15개
label = file[:, -1].astype(np.float32) # y_train  >>> y=모션 1개
#knn = cv2.ml.KNearest_create() 
#knn.train(angle, cv2.ml.ROW_SAMPLE, label) #knn모델학습
stack=[]

#웹캠에서 이미지 읽어오기
cap = cv2.VideoCapture(0)

ccount = 0#400개데이터 뽑아내기
count = 0#모션 체인지의 카운터 변수
count2 = [] # 음성변환으로의 카운터 변수
text_list = [] #입력받은 텍스트를 받아들일 변수


while cap.isOpened():

#     if len(count2)==120: #50번돌 동안 손가락이 읽히지 않았다면
#         if len(text_list)!=0:    
#             print("지화에 따라 추가된 모음자음 리스트: ",text_list)
#             text_list = "".join(text_list)                               # 리스트를 문자열로
#             print("문자열로 변경된 모음/자음",text_list)
#             merge_jamo = join_jamos(text_list)   #단애인 지화 후 그 모/자음을 합체
#             print("모음자음에서 합쳐진 단어로 => ",merge_jamo)

#             s = pyttsx3.init()    #여기서부터는 tts기술로 텍스트를 스피커에서 출력
#             s.say(merge_jamo)
#             s.runAndWait()
#             text_list = []




    ret, img = cap.read() #한프레임!!씩 이미지를 읽어온다.
    if not ret:
        continue

    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


    #각도계산 하기!! 제일 중요 분석해서 실시간으로 모션 각도 추출해서 데이터셋 만들어야함!!!

    if result.multi_hand_landmarks is not None: #만약 손자체가 인식됐다면!
        count2= []
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21, 3))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            # print(joint)
            # time.sleep(5)

            # Compute angles between joints
            v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] # Parent joint
            v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] # Child joint
            v = v2 - v1 # [20,3]  #벡터값 생성 (x1-x2,y1-y2,z1-z3) >조인트점21개에서 벡터값으로 변환하여 20개의 벡터방향이나옴
            
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis] #벡터/벡터길이 >>Normalize  크기가 1인 벡터 만들기 (길이공식나중에확인하기~)

            # Get angle using arcos of dot product>>>>>> 각도구하기 공식! 수학공식임
            angle = np.arccos(np.einsum('nt,nt->n',
                v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18,3,3,3,3,],:], 
                v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19,7,11,15,19],:])) # [15,]

            angle = np.degrees(angle) # Convert radian to degree        

            # Inference gesture
            data = np.array([angle], dtype=np.float32)

            #동서남북 구분코드
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
            data=np.append(data[0],k)
            data = np.array([data],dtype=np.float32)


            #앞 뒤 구분코드
            # if joint[2][0]-joint[17][0]>0: #손등이보인다
            #     kk = 0.0
            # else: #손바닥이보인다
            #     kk = 90.0

            # data=np.append(data[0],kk)
            # data = np.array([data],dtype=np.float32)
            

#             ret, results, neighbours, dist = knn.findNearest(data, 12)
#             idx = int(results[0][0])

            # Draw gesture result
#             if idx in gesture.keys():
#                 std = idx
#                 cv2.putText(img, text='0', org=(int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0] + 20)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

            mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)
            
            
            
            
            if 20<ccount<421:
                #데이터출력을 위한 20프레임간격출력
                #if count%20==0:
                for i in range(20):
                    print(round(data[0][i]/180, 4),end=',')
                    #count=0
                print(round(30/30, 4))



#             stack.append(std)
#             if count%10==0:
#                 k=stack.pop()
#                 if stack.count(k)>=18:
#                     len_text=len(text_list)
#                     if len_text==0:
#                         #print(k,'입력완료') #이때 입력받았다고 사용자에게 알려줘야함 led?? 잠깐 텀이 필요함
#                         text_list.append(han[k])
#                         time.sleep(0.3)
#                         stack=[]
#                     else:
#                         #연속된 모음이 들어오는지 아닌지
#                         for x in han:
#                             if han[x]==text_list[len_text-1]:
#                                 index = x
#                                 break

#                         if 14<=x<=30 and 14<=k<=30:
#                             pass
#                         else:
#                             #print(k,'입력완료') #이때 입력받았다고 사용자에게 알려줘야함 led?? 잠깐 텀이 필요함
#                             text_list.append(han[k])
#                             time.sleep(0.3)
#                             stack=[]
#                 else:
#                     stack
#                 #print(list(angle))
            count+=1
            ccount+=1

    count2.append(0) #모션탐지가 안될때 카운팅하는 리스트

    cv2.imshow('Game', img)
    if cv2.waitKey(1) == ord('q'):
        break
