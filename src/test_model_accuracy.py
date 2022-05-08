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
file = np.genfromtxt('data/hand_gesture_train.csv', delimiter=',')
np.random.shuffle(file)

train_data = file[:9000]
test_data = file[9000:]



angle = train_data[:,:-1].astype(np.float32) # x_train  >>> x=각도 20개
label = train_data[:, -1].astype(np.float32) # y_train  >>> y=모션 1개
knn = cv2.ml.KNearest_create()  #knn모델생성
knn.train(angle, cv2.ml.ROW_SAMPLE, label) #knn모델학습

test_angle = test_data[:,:-1].astype(np.float32) # x_test  >>> x=각도 20개
test_label = test_data[:, -1].astype(np.float32) # y_test  >>> y=모션 1개

'''
[[0.1556 0.0511 0.2075 0.2962 0.0316 0.0123 0.4483 0.6664 0.2123 0.366
  0.5924 0.2579 0.2895 0.5921 0.2511 0.5622 0.2792 0.2803 0.2615 0.    ]]
'''

for j in range(1,15,2):

    cnt = 0
    for i in range(len(test_angle)):
        ret, results, neighbours, dist = knn.findNearest(np.array([test_angle[i]]), j)
        if int(round(results[0][0]*30,1)) == int(round(test_label[i]*30,1)):
            cnt +=1

    print(f"k :{j}, accuracy : {cnt/len(test_angle)}")
