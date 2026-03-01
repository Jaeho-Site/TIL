### 내 풀이 ###
score=['D0','D+','C0','C+','B0','B+','A0','A+']
fscore=0
total=0
F=0.0
for _ in range(20):
    a,b,c=input().split()
    if c=='P':
        continue   
    fscore+=float(b)
    if c=='F':
        continue   
    for i, s in enumerate(score):
        if s==c:
            total+=(float(b)*(0.5*float(i)+1.0))

print(f'{total/fscore:0.6f}') 

### 딕셔너리를 활용한 정답 풀이 ###
grade_dict = {
    'A+': 4.5, 'A0': 4.0, 'B+': 3.5, 'B0': 3.0,
    'C+': 2.5, 'C0': 2.0, 'D+': 1.5, 'D0': 1.0, 'F': 0.0
}

total_points = 0.0  # (학점 × 과목평점)의 합
total_credits = 0.0 # 학점의 총합

for _ in range(20):
    line = input().split()
    if not line: break # 입력이 20줄 미만일 경우 대비
    
    subject, credit, grade = line
    credit = float(credit)

    if grade == 'P':
        continue
    
    total_credits += credit
    total_points += credit * grade_dict[grade]

print(f"{total_points / total_credits:.6f}")