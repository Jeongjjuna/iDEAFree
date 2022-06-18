import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3
from unicode import join_jamos
from hanspell import spell_checker

def execute_tts(text_list):
    print("지화에 따라 추가된 모음자음 리스트: ",text_list)
    text_list = "".join(text_list)                               # 리스트를 문자열로
    print("문자열로 변경된 모음/자음",text_list)
    merge_jamo = join_jamos(text_list)   #단애인 지화 후 그 모/자음을 합체
    print("모음자음에서 합쳐진 단어로 => ",merge_jamo)
    
    spelled_sent = spell_checker.check(merge_jamo) #오타 맞춤범 검사
    merge_jamo = spelled_sent.checked
    print("오타수정 후", merge_jamo)
    #out=gTTS(text=merge_jamo,lang='ko')


    s = pyttsx3.init()    #여기서부터는 tts기술로 텍스트를 스피커에서 출력
    s.say(merge_jamo)
    s.runAndWait()
