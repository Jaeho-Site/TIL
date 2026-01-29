text = "Python Programming"
# 부분 문자열 생성
n = 3
substrings = [text[i:i+n] for i in range(len(text)-n+1)]
print(substrings)  # ['Pyt', 'yth', 'tho', 'hon', 'on ', 'n P', ' Pr', 'Pro', 'rog', 'ogr', 'gra', 'ram', 'amm', 'mmi', 'min', 'ing']

# 문자열 대소문자 변환
print(text.upper())      # 'PYTHON PROGRAMMING' (대문자 변환)
print(text.lower())      # 'python programming' (소문자 변환)
print(text.title())      # 'Python Programming' (각 단어 첫 글자 대문자)
print(text.capitalize()) # 'Python programming' (첫 단어만 대문자)

# 공백 제거
text_with_space = "   Python  "
print(text_with_space.strip())  # 'Python' (양쪽 공백 제거)
print(text_with_space.lstrip()) # 'Python  ' (왼쪽 공백 제거)
print(text_with_space.rstrip()) # '   Python' (오른쪽 공백 제거)

# 문자열 반복 및 결합
print("Hello " * 3)  # 'Hello Hello Hello '
words = ["Python", "is", "awesome"]
print(" ".join(words))  # 'Python is awesome' (리스트 문자열 결합)