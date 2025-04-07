import os
import webbrowser
import time
import requests
from urllib.parse import urlsplit
import shutil
import tarfile
import sys
server_list_folder = os.getcwd()
os.makedirs(os.path.expanduser("~/Documents/Minecraft_server"), exist_ok=True)
jdk_folder_path = os.path.expanduser(f"~/Documents/Minecraft_server/jdk")
os.makedirs(jdk_folder_path, exist_ok=True)
jdk_install_list = [f for f in os.listdir(jdk_folder_path) if os.path.isdir(os.path.join(jdk_folder_path, f))]

server_folder_path = os.path.expanduser(f"~/Documents/Minecraft_server")

# 1. 상위 폴더 이름 (jdk 제외)
server_list = [f for f in os.listdir(server_folder_path)
               if os.path.isdir(os.path.join(server_folder_path, f)) and f != "jdk"]

# 2. 각 상위 폴더 아래의 하위 폴더 경로 생성
server_version_list = []
for parent_folder in server_list:
    parent_path = os.path.join(server_folder_path, parent_folder)
    sub_folders = [os.path.join(parent_folder, sub) for sub in
    [f for f in os.listdir(parent_path)
    if os.path.isdir(os.path.join(parent_path, f))]]
    server_version_list.extend(sub_folders)

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
        sys.exit()
    else:
        print("맞는 번호를 입력해주세요")
def get_valid_folder_name():
    invalid_chars = r'[<>:"/\\|?*] '
    reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]

    while True:
        text_name = input("서버의 이름을 입력하세요(실제 서버명이 아닌 폴더명입니다): ")
        if not text_name:
            print("서버 이름을 입력해야 합니다")
            continue

        if any(char in invalid_chars for char in text_name):
            print("사용할 수 없는 기호(공백)가 포함되어 있습니다. 다시 입력해주세요.")
            continue
        elif text_name.upper() in reserved_names:
            print("예약된 이름은 사용할 수 없습니다. 다시 입력해주세요.")
            continue
        else:
            return text_name

def get_valid_url():
    while True:
        url = input("다운로드 링크를 복사해주세요: ")
        if not url:
            print("다운로드 링크를 입력해주세요.")
            continue
        try:
            # URL 형식 검사
            result = urlsplit(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError("유효하지 않은 URL입니다.")

            # URL 접속 가능 여부 확인
            response = requests.head(url, timeout=5)  # HEAD 요청으로 응답 코드만 확인 (빠름)
            response.raise_for_status()  # 200 OK 외의 응답 코드에 대해 예외 발생
            return url  # 정상적인 URL이면 반환

        except requests.exceptions.RequestException as e:
            print(f"URL 접속 실패: {e}. 다시 입력해주세요.")
        except ValueError as e:
            print(f"오류: {e} 다시 입력해주세요.")
        except Exception as e:
            print(f"알 수 없는 오류 발생: {e}. 다시 입력해주세요.")

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def server_download():
    global jdk_url, jdk_ver, jdk_file_type_tar
    jdk_file_type_tar = False
    clear()
    os.chdir(server_list_folder)
    with open(resource_path("version.txt"), "r", encoding="utf-8") as f:
        versions = [line.strip() for line in f]
    while True:
        text_ver = input("버전을 입력해주세요 ex) 1.12.2\n만약 무슨 버전이 있는지 모르는 경우 ? 를 입력하세요\n")
        if text_ver in versions:
            parts = text_ver.split(".")
            parts = int(parts[1])
            if parts <= 16:
                if win:
                    jdk_url = "https://builds.openlogic.com/downloadJDK/openlogic-openjdk/8u442-b06/openlogic-openjdk-8u442-b06-windows-x64.zip"
                else:
                    jdk_url = "https://builds.openlogic.com/downloadJDK/openlogic-openjdk/8u442-b06/openlogic-openjdk-8u442-b06-mac-x64.zip"
                jdk_ver = 8
                print("jdk 8")
            elif parts == 17:
                if win:
                    jdk_url = "https://download.java.net/java/GA/jdk16.0.2/d4a915d82b4c4fbb9bde534da945d746/7/GPL/openjdk-16.0.2_windows-x64_bin.zip"
                else:
                    jdk_url = "https://download.java.net/java/GA/jdk16.0.2/d4a915d82b4c4fbb9bde534da945d746/7/GPL/openjdk-16.0.2_osx-x64_bin.tar.gz"
                    jdk_file_type_tar=True
                jdk_ver = 16
                print("jdk 16")
            elif 18 <= parts <= 20:
                if win:
                    jdk_url = "https://builds.openlogic.com/downloadJDK/openlogic-openjdk/17.0.14+7/openlogic-openjdk-17.0.14+7-windows-x64.zip"
                else:
                    jdk_url = "https://builds.openlogic.com/downloadJDK/openlogic-openjdk/17.0.14+7/openlogic-openjdk-17.0.14+7-mac-x64.zip"
                jdk_ver = 17
                print("jdk 17")
            elif 21 <= parts:
                if win:
                    jdk_url = "https://builds.openlogic.com/downloadJDK/openlogic-openjdk/21.0.6+7/openlogic-openjdk-21.0.6+7-windows-x64.zip"
                else:
                    jdk_url = "https://builds.openlogic.com/downloadJDK/openlogic-openjdk/21.0.6+7/openlogic-openjdk-21.0.6+7-mac-x64.zip"
                jdk_ver = 21
                print("jdk 21")
            if f"jdk{str(jdk_ver)}" in jdk_install_list:
                print("Jdk 설치 확인")
                time.sleep(1)
            else:
                save_path = os.path.expanduser(f"~/Documents/Minecraft_server/jdk/jdk{str(jdk_ver)}")
                os.makedirs(save_path, exist_ok=True)
                if jdk_file_type_tar:
                    file_path = os.path.join(save_path, f"jdk{str(jdk_ver)}.tar.gz")
                else:
                    file_path = os.path.join(save_path, f"jdk{str(jdk_ver)}.zip")
                # 자바 다운로드 및 저장
                response = requests.get(jdk_url, stream=True)
                print("JDK 설치중")
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                # 자바 압축해제
                print("압축 해제중")
                parent_dir = os.path.expanduser(f"~/Documents/Minecraft_server/jdk/jdk{str(jdk_ver)}")

                if jdk_file_type_tar:
                    with tarfile.open(file_path, "r:gz") as tar:
                        tar.extractall(parent_dir, filter="fully_trusted")
                else:
                    shutil.unpack_archive(file_path, parent_dir,"zip")
                # 내부 폴더 확인
                subdirs = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]
                if subdirs:
                    target_dir = os.path.join(parent_dir, subdirs[0])  # 내부 폴더 경로
                    for item in os.listdir(target_dir):
                        src = os.path.join(target_dir, item)
                        dst = os.path.join(parent_dir, item)
                        # 파일 및 폴더 이동
                        shutil.move(src, dst)
                    # 빈 폴더 삭제
                    os.rmdir(target_dir)
            break
        elif text_ver == "?":
            clear()
            print(f"버전은 다음과 같습니다\n{', '.join(open(resource_path('version.txt'), encoding='utf-8').read().splitlines())}\n")
        else:
            print("잘못된 버전입니다 다시 입력해주세요\n")
    clear()
    text_name = get_valid_folder_name()
    os.makedirs(os.path.expanduser(f"~/Documents/Minecraft_server/{server_type}/{text_ver}/{text_name}"), exist_ok=True)
    if server_type == "paper":
        print("3초 후 열리는 웹사이트에서 원하는 버전의 다운로드 링크 주소를 복사한 뒤 여기에 붙여넣기 하세요")
        print(f"다운 받아야 하는 버전은 {text_ver}입니다")
        time.sleep(3)
        webbrowser.open("https://papermc.io/downloads/all")
    if server_type == "forge":
        print("3초 후 열리는 웹사이트에서 원하는 버전의 인스톨러 다운로드를 누른 후 오른쪽 위 스킵 버튼의 링크 주소를 복사한 뒤 여기에 붙여넣기 하세요")
        print(f"다운 받아야 하는 버전은 {text_ver}입니다")
        time.sleep(3)
        webbrowser.open("https://files.minecraftforge.net/net/minecraftforge/forge/")
    if server_type == "fabric":
        print("3초 후 열리는 웹사이트에서 원하는 버전을 선택한 후 서버 다운로드 버튼의 링크 주소를 복사한 뒤 여기에 붙여넣기 하세요")
        print(f"다운 받아야 하는 버전은 {text_ver}입니다")
        time.sleep(3)
        webbrowser.open("https://fabricmc.net/use/server/")
    url = get_valid_url()

    file_name = "server.jar"
    save_path = os.path.expanduser(f"~/Documents/Minecraft_server/{server_type}/{text_ver}/{text_name}/")
    file_path = os.path.join(save_path, file_name)

    # 파일 다운로드 및 저장
    response = requests.get(url, stream=True)

    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"파일이 {file_path}에 저장되었습니다!")
    print("서버 실행")
    if win:
        if jdk_ver == 8:
            java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk8/bin/java.exe")
        elif jdk_ver == 16:
            java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk26/bin/java.exe")
        elif jdk_ver == 17:
            java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk17/bin/java.exe")
        elif jdk_ver == 21:
            java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk21/bin/java.exe")
    else:
        if jdk_ver == 8:
            java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk8/jdk1.8.0_442.jdk/Contents/Home/bin/java")
        elif jdk_ver == 16:
            java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk16/Contents/Home/bin/java")
        elif jdk_ver == 17:
            java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk17/jdk-17.0.14.jdk/Contents/Home/bin/java")
        elif jdk_ver == 21:
            java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk21/jdk-21.0.6.jdk/Contents/Home/bin/java")
    f = open(f"{os.path.expanduser(f"~/Documents/Minecraft_server")}/{server_type}/{text_ver}/{text_name}/eula.txt", 'w')
    f.write("eula=true")
    f.close()
    os.chdir(f"{os.path.expanduser(f"~/Documents/Minecraft_server")}/{server_type}/{text_ver}/{text_name}")
    if server_type == "forge":
        os.system(f"{java_path} -jar {os.path.expanduser(f"~/Documents/Minecraft_server")}/{server_type}/{text_ver}/{text_name}/server.jar --installServer {os.path.expanduser(f"~/Documents/Minecraft_server")}/{server_type}/{text_ver}/{text_name}")
        if win:
            path = os.path.expanduser(f"~/Documents/Minecraft_server/{server_type}/{text_ver}/{text_name}/run.bat")
        else:
            path = os.path.expanduser(f"~/Documents/Minecraft_server/{server_type}/{text_ver}/{text_name}/run.sh")
        with open(path, 'r') as f:
            lines = f.readlines()
        line_split = lines[5].split(' ')
        line_split[0] = java_path  # java를 java_path로 교체
        lines[5] = ' '.join(line_split)
        with open(path, 'w') as f:
            f.writelines(lines)
        if win:
            os.system("run.bat")
        else:
            os.system("./run.sh")
        print("\n\n")
    else:
        print("3초후 서버가 열립니다. 만약 server.properties를 수정하고 싶은 경우 서버가 완전히 열린후 stop으로 서버를 정지한 뒤 수정해주세요")
        time.sleep(3)
        if win:
            os.system(f"{java_path} -jar {os.path.expanduser(f"~/Documents/Minecraft_server")}\\{server_type}\\{text_ver}\\{text_name}\\server.jar")
        else:
            os.system(f"{java_path} -jar {os.path.expanduser(f"~/Documents/Minecraft_server")}/{server_type}/{text_ver}/{text_name}/server.jar")
        print("\n")
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
            print("다시 입력해주세요1")
    elif text1 == "2":
        clear()
        server_folder_path = os.path.expanduser(f"~/Documents/Minecraft_server")

        # 1. 상위 폴더 이름 (jdk 제외)
        server_list = [f for f in os.listdir(server_folder_path)
                       if os.path.isdir(os.path.join(server_folder_path, f)) and f != "jdk"]

        # 2. 각 상위 폴더 아래의 하위 폴더 경로 생성
        server_version_list = []
        for parent_folder in server_list:
            parent_path = os.path.join(server_folder_path, parent_folder)
            for sub1 in os.listdir(parent_path):
                sub1_path = os.path.join(parent_path, sub1)
                if os.path.isdir(sub1_path):
                    for sub2 in os.listdir(sub1_path):
                        sub2_path = os.path.join(sub1_path, sub2)
                        if os.path.isdir(sub2_path):
                            server_version_list.append(os.path.join(parent_folder, sub1, sub2))

        while True:
            print("현재 설치되어있는 서버는 다음과 같습니다")
            for i, version in enumerate(server_version_list, 1):
                print(f"{i}. {version}")
            print("이중 어떤 서버를 실행할까요")
            server_num = input()
            try:
                index = int(server_num) - 1
                if not (0 <= index < len(server_version_list)):
                    raise IndexError
                # print(server_version_list[index])
                break
            except ValueError:
                clear()
                print("숫자를 입력해주세요.")
            except IndexError:
                clear()
                print("유효한 번호를 입력해주세요.")

        if win:
            server_type,version,server_folder_name = server_version_list[index].split('\\')
        else:
            server_type,version,server_folder_name = server_version_list[index].split('/')
        parts = version.split(".")
        parts = int(parts[1])
        if parts <= 16:
            jdk_ver = 8
        elif parts == 17:
            jdk_ver = 16
        elif 18 <= parts <= 20:
            jdk_ver = 17
        elif 21 <= parts:
            jdk_ver = 21
        if win:
            if jdk_ver == 8:
                java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk8/bin/java.exe")
            elif jdk_ver == 16:
                java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk16/bin/java.exe")
            elif jdk_ver == 17:
                java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk17/bin/java.exe")
            elif jdk_ver == 21:
                java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk21/bin/java.exe")
        else:
            if jdk_ver == 8:
                java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk8/jdk1.8.0_442.jdk/Contents/Home/bin/java")
            elif jdk_ver == 16:
                java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk16/Contents/Home/bin/java")
            elif jdk_ver == 17:
                java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk17/jdk-17.0.14.jdk/Contents/Home/bin/java")
            elif jdk_ver == 21:
                java_path = os.path.expanduser("~/Documents/Minecraft_server/jdk/jdk21/jdk-21.0.6.jdk/Contents/Home/bin/java")
        # print(f"{java_path} {os.path.expanduser(f"~/Documents/Minecraft_server")}/{server_version_list[int(server_num)-1]}/server.jar")
        clear()
        print("3초후 서버가 켜집니다. 서버를 종료하고 싶다면 save-all로 저장한 뒤 stop을 쳐주세요")
        time.sleep(3)
        os.chdir(f"{os.path.expanduser(f"~/Documents/Minecraft_server")}/{server_version_list[index]}")
        if server_type == "forge":
            if win:
                os.system("run.bat")
            else:
                os.system("./run.sh")
        else:
            if win:
                os.system(f"{java_path} -jar {os.path.expanduser(f"~/Documents/Minecraft_server")}\\{server_version_list[index]}\\server.jar")
            else:
                os.system(f"{java_path} -jar {os.path.expanduser(f"~/Documents/Minecraft_server")}/{server_version_list[index]}/server.jar")
        print("\n서버가 종료되었습니다")
        input("계속하려면 Enter 키를 누르세요...")
        clear()
    elif text1 == "3":
        sys.exit()
    else:
        clear()
        print("다시 입력해주세요\n")
