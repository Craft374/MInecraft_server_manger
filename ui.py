# version.txt 파일의 내용을 줄 단위 리스트로 저장
with open("version.txt", "r", encoding="utf-8") as f:
    versions = [line.strip() for line in f.readlines()]

# 사용자 입력과 비교
user_input = input("버전을 입력하세요: ").strip()
if user_input in versions:
    print("통과")
else:
    print("빠꾸")
