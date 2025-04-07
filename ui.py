import os
bash_script = 'echo 계속하려면 Enter 키를 누르세요...; read; exit'
os.system(f'osascript -e \'tell application "Terminal" to do script "{bash_script}"\'')
