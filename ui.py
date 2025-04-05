8 16 17 21
jdk_ver = 0
win = True
if win:
    if jdk_ver == 8:
        java_path = os.path.expanduser(f"~/Documents/Minecraft_server/jdk/jdk{str(jdk_ver)}/")
    elif jdk_ver == 16:
        java_path = os.path.expanduser(f"~/Documents/Minecraft_server/jdk/jdk{str(jdk_ver)}/")
    elif jdk_ver == 17:
        java_path = os.path.expanduser(f"~/Documents/Minecraft_server/jdk/jdk{str(jdk_ver)}/")
    elif jdk_ver == 21:
        java_path = os.path.expanduser(f"~/Documents/Minecraft_server/jdk/jdk{str(jdk_ver)}/")
else:
    if jdk_ver == 8:
        java_path = os.path.expanduser(f"~/Documents/Minecraft_server/jdk/jdk8/jdk1.8.0_442.jdk/Contents/Home/bin/java")
    elif jdk_ver == 16:
        java_path = os.path.expanduser(f"~/Documents/Minecraft_server/jdk/jdk16/Contents/Home/bin/java")
    elif jdk_ver == 17:
        java_path = os.path.expanduser(f"~/Documents/Minecraft_server/jdk/jdk17/jdk-17.0.14.jdk/Contents/Home/bin/java")
    elif jdk_ver == 21:
        java_path = os.path.expanduser(f"~/Documents/Minecraft_server/jdk/jdk{str(jdk_ver)}/")