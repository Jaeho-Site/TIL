text = "Python Programming"

# 문자열 슬라이싱 및 변환
print(text[0:4])   # 'Pyth' (인덱스 0부터 3까지 슬라이싱)
print(text[::2])   # 'Pto rgamn' (2칸씩 건너뛰기)
print(text[::-1])  # 'gnimmargorP nohtyP' (문자열 뒤집기)

# 문자열 분할 및 리스트 변환
words = text.split()  # 공백 기준 분할
print(words)          # ['Python', 'Programming']
print(list(text))     # ['P', 'y', 't', 'h', 'o', 'n', ' ', 'P', 'r', 'o', 'g', 'r', 'a', 'm', 'm', 'i', 'n', 'g']

# 문자열 검색 및 포함 여부
print(text.find("Python"))  # 0 (문자열 시작 위치 반환)
print(text.find("Java"))    # -1 (존재하지 않으면 -1 반환)
print("Python" in text)     # True (문자 포함 여부 확인)
print("Java" in text)       # False

# 문자열 치환 및 개수 세기
print(text.replace("P", "S"))  # 'Sython Srogramming' (문자 변경)
print(text.count("o"))         # 2 ('o'의 개수 세기)