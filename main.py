import os
import webbrowser
import time
import requests
from urllib.parse import urlsplit
from os.path import basename
os.makedirs(os.path.expanduser("~/Documents/Minecraft_server"), exist_ok=True)

def clear():
    if win:
        os.system("cls")
    else:
        os.system("clear")

def eula():
    eula_path = "eula.txt"
    with open(eula_path, "w") as file:
        file.write("eula=true\n")
    print(f"{eula_path} 파일이 생성되었습니다.")

while True:
    print("현재 시스템 OS의 번호를 입력해주세요")
    print("1. 윈도우\n2. 맥OS\n3. 나가기")
    text_os=input("")
    if text_os == "1":
        win=True
        break
    elif text_os == "2":
        win=False
        break
    elif text_os == "3":
        quit()
    else:
        print("맞는 번호를 입력해주세요")

def server_download():
    clear()
    with open("version.txt", "r", encoding="utf-8") as f:
        versions = [line.strip() for line in f.readlines()]
    while True:
        text_ver = input("버전을 입력해주세요 ex) 1.12.2\n만약 무슨 버전이 있는지 모르는 경우 ? 를 입력하세요\n")
        if text_ver in versions:
            os.makedirs(os.path.expanduser(f"~/Documents/Minecraft_server/{server_type}/{text_ver}"), exist_ok=True)

            parts = text_ver.split(".")
            print(parts[1])
            time.sleep(10)
            break
        elif text_ver == "?":
            clear()
            print(f"버전은 다음과 같습니다\n{', '.join(open("version.txt").read().splitlines())}\n")
        else:
            print("잘못된 버전입니다 다시 입력해주세요\n")
    clear()

    if server_type == "paper":
        print("3초 후 열리는 웹사이트에서 원하는 버전의 다운로드 링크 주소를 복사한 뒤 여기에 붙여넣기 하세요")
        time.sleep(3)
        webbrowser.open("https://papermc.io/downloads/all")
    if server_type == "forge":
        print("3초 후 열리는 웹사이트에서 원하는 버전의 인스톨러 다운로드를 누른 후 오른쪽 위 스킵 버튼의 링크 주소를 복사한 뒤 여기에 붙여넣기 하세요")
        time.sleep(3)
        webbrowser.open("https://files.minecraftforge.net/net/minecraftforge/forge/")
    if server_type == "fabric":
        print("3초 후 열리는 웹사이트에서 원하는 버전을 선택한 후 서버 다운로드 버튼의 링크 주소를 복사한 뒤 여기에 붙여넣기 하세요")
        time.sleep(3)
        webbrowser.open("https://fabricmc.net/use/server/")
    url = input()
    file_name = basename(urlsplit(url).path)
    save_path = os.path.expanduser(f"~/Documents/Minecraft_server/{server_type}/{text_ver}/")  # 원하는 디렉토리 경로
    file_path = os.path.join(save_path, file_name)

    # 디렉토리가 없으면 생성
    os.makedirs(save_path, exist_ok=True)

    # 파일 다운로드 및 저장
    response = requests.get(url, stream=True)
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"파일이 {file_path}에 저장되었습니다!\n")
clear()
while True:
    print("1. 서버 설치\n2. 설치되어 있는 서버 실행\n3. 나가기")
    text1=input("원하는 메뉴의 번호를 입력하세요\n")

    if text1 == "1":
        clear()
        print("1. Paper(일반)\n2. Forge(모드)\n3. Fabric(모드)")
        text2=input("원하는 메뉴의 번호를 입력하세요\n")
        if text2 == "1":
            server_type="paper"
            server_download()
        elif text2 == "2":
            server_type = "forge"
            server_download()
        elif text2 == "3":
            server_type = "fabric"
            server_download()
        else:
            print("다시 입력해주세요")
    if text1 == "2":
        clear()
        print("놀랍게도 그는 아무것도 만들지 않았다")
    if text1 == "3":
        quit()