using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.Net.Sockets;
using System.Text;
using System;
using System.IO;
using System.Runtime.InteropServices;


public class MainController : MonoBehaviour
{
    //캐릭터 애니메이터 정의
    private Animator animator;

    //서버와의 tcp통신을 위한 준비
    TcpClient client;
    //string serverIP = "168.131.153.213"; //서버 아이피 입력 : //정식배포용(연구실서버용)
    string serverIP = "192.168.56.1"; //지훈집서버 테스트용
    int port = 9999;
    byte[] receivedBuffer;
    StreamReader reader;
    bool socketReady = false;
    NetworkStream stream;

    char std ; //이 전 글자를 저장하고있는 변수

    private void Awake()
    {
        animator = GetComponent<Animator>();
        CheckReceive(); // 서버와 연걸안됐으면 연결시켜주는 함수
    }

    private void Update()
    {
        if (socketReady) //서버와 정상적으로 연결 되었을 시
        {
            if (stream.DataAvailable) //데이터를 받는다면
            {
                receivedBuffer = new byte[100];
                stream.Read(receivedBuffer, 0, receivedBuffer.Length);
                string msg = Encoding.UTF8.GetString(receivedBuffer, 0, receivedBuffer.Length);

                
                //들어오는 문자열에 따른 유니티 애니메이터 파라미터값 조정

                if (msg[0] == 'ㄱ')
                {   
                    if (std == 'ㄱ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 0);
                    Debug.Log("ㄱ출력"); //디버깅용 console출력함수
                }
                else if (msg[0] == 'ㄴ')
                {   
                    if (std == 'ㄴ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 1);
                    Debug.Log("ㄴ출력");
                }
                else if (msg[0] == 'ㄷ')
                {   
                    if (std == 'ㄷ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 2);
                    Debug.Log("ㄷ출력");
                }
                else if (msg[0] == 'ㄹ')
                {   
                    if (std == 'ㄹ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 3);
                    Debug.Log("ㄹ출력");
                }
                else if (msg[0] == 'ㅁ')
                {   
                    if (std == 'ㅁ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 4);
                    Debug.Log("ㅁ출력");
                }
                else if (msg[0] == 'ㅂ')
                {   
                    if (std == 'ㅂ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 5);
                    Debug.Log("ㅂ출력");
                }
                else if (msg[0] == 'ㅅ')
                {   
                    if (std == 'ㅅ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 6);
                    Debug.Log("ㅅ출력");
                }
                else if (msg[0] == 'ㅇ')
                {   
                    if (std == 'ㅇ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 7);
                    Debug.Log("ㅇ출력");
                }
                else if (msg[0] == 'ㅈ')
                {   
                    if (std == 'ㅈ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 8);
                    Debug.Log("ㅈ출력");
                }
                else if (msg[0] == 'ㅊ')
                {   
                    if (std == 'ㅊ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 9);
                    Debug.Log("ㅊ출력");
                }
                else if (msg[0] == 'ㅋ')
                {   
                    if (std == 'ㅋ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 10);
                    Debug.Log("ㅋ출력");
                }
                else if (msg[0] == 'ㅌ')
                {   
                    if (std == 'ㅌ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 11);
                    Debug.Log("ㅌ출력");
                }
                else if (msg[0] == 'ㅍ')
                {   
                    if (std == 'ㅍ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 12);
                    Debug.Log("ㅍ출력");
                }
                else if (msg[0] == 'ㅎ')
                {   
                    if (std == 'ㅎ')
                    {   
                        animator.SetInteger("jamo", 1);  
                    }
                    animator.SetInteger("Speed", 13);
                    Debug.Log("ㅎ출력");
                }
                else if (msg[0] == 'ㅏ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 14);
                    Debug.Log("ㅏ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅑ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 15);
                    Debug.Log("ㅑ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅓ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 16);
                    Debug.Log("ㅓ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅕ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 17);
                    Debug.Log("ㅕ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅗ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 18);
                    Debug.Log("ㅗ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅛ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 19);
                    Debug.Log("ㅛ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅜ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 20);
                    Debug.Log("ㅜ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅠ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 21);
                    Debug.Log("ㅠ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅡ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 22);
                    Debug.Log("ㅡ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅣ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 23);
                    Debug.Log("ㅣ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅐ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 24);
                    Debug.Log("ㅐ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅒ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 25);
                    Debug.Log("ㅒ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅔ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 26);
                    Debug.Log("ㅔ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅖ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 27);
                    Debug.Log("ㅖ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅟ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 28);
                    Debug.Log("ㅟ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅚ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 29);
                    Debug.Log("ㅚ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == 'ㅢ')
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 30);
                    Debug.Log("ㅢ출력");
                    animator.SetInteger("jamo2", 0);
                }
                else if (msg[0] == '*') //단어 출력후 준비모션으로 돌아가는 문자'*'
                {   
                    animator.SetInteger("jamo", 0);
                    animator.SetInteger("Speed", 100);
                    Debug.Log("준비모션");
                }

                else if (msg[0] == ' ') //중성 다음글자가 초성이 아닌 종성으로 빠진다는것을 알려주기 위한 공백문자
                {   
                    animator.SetInteger("jamo2", 1);
                    animator.SetInteger("jamo", 0);
                    Debug.Log("종성들어갈준비 온!");
                }
                

                
                if (msg[0] != '*')
                {   
                    std = msg[0];
                }        
            }
        }
    }

    // 서버와 연결됐는지 체크 후 안 됐으면 서버연결해주는 함수
    void CheckReceive()
    {
        if (socketReady) return;
        try
        {
            client = new TcpClient(serverIP, port);

            if (client.Connected)
            {
                stream = client.GetStream();
                Debug.Log("Connect Success");
                socketReady = true;
            }
        }
        catch (Exception e)
        {
            Debug.Log("On client connect exception " + e);
        }
    }


    void OnApplicationQuit()
    {
        CloseSocket();
    }

    void CloseSocket()
    {
        if (!socketReady) return;

        reader.Close();
        client.Close();
        socketReady = false;
    }
}
