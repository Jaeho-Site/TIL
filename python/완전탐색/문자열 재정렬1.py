"""
요구 시간 nlogn 정도
배열을 한번 훑는다(N) -> 숫자를 제거하고 새로운 배열로 만든다
알파벳, 숫자 배열을 각각 정렬한다. (nlogn)
숫자 배열을 뒤에 붙인다.
"""
data=list(input())

int_arr=[]
chr_arr=[]
num = ['0','1','2','3','4','5','6','7','8','9']

for i in data:
    if i in num: # isdigit() or isalpha()사용
        int_arr.append(i)
    else:
        chr_arr.append(i)

int_arr.sort()
chr_arr.sort()


# print("".join(chr_arr + int_arr)) 아래를 한줄로 처리
answer="".join(chr_arr)
answer+="".join(int_arr)
print(answer)