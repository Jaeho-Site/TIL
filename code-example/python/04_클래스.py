# ============================================================
#  정보처리기사 실기 - Python 04. 클래스
# ============================================================
#  [Java와 비교해서 콕 집기]
#  1. 생성자는 __init__(self, ...) - 언더바 2개씩!
#  2. 모든 메서드의 첫 매개변수는 self (호출할 땐 안 넘김)
#  3. 상속: class Child(Parent):  ← extends 대신 괄호
#  4. 오버라이딩 시 부모 호출: super().메서드()
#  5. 클래스 변수(모든 객체 공유) vs 인스턴스 변수(self.x) 구분
# ============================================================

# ---------------------------------------------------
# [문제 1] 클래스 속성 순회 기출 (답: SKIDDP)
# myVar.a 의 각 문자열에서 첫 글자 i[0]만 이어붙인다.
# Seoul Kyeongi Inchon Daejeon Daegu Pusan
#  S      K      I       D      D     P
# ---------------------------------------------------
class CharClass:
    a = ['Seoul', 'Kyeongi', 'Inchon', 'Daejeon', 'Daegu', 'Pusan']

myVar = CharClass()
str01 = ''
for i in myVar.a:
    str01 = str01 + i[0]
print(str01)                    # SKIDDP

# ---------------------------------------------------
# [문제 2] 클래스 변수 교환 기출 (시나공: 답 10 20 / 20 10)
# x, y는 클래스 변수. chg에서 self.x = ... 로 대입하면
# 그 객체만의 인스턴스 변수가 새로 만들어져 값이 바뀐 것처럼 동작.
# 출력 추적: 처음 10 20 → chg() 후 20 10
# ---------------------------------------------------
class Cls:
    x, y = 10, 20

    def chg(self):
        temp = self.x
        self.x = self.y
        self.y = temp

obj = Cls()
print(obj.x, obj.y)             # 10 20
obj.chg()
print(obj.x, obj.y)             # 20 10

# ---------------------------------------------------
# [문제 3] __init__ 생성자와 인스턴스 변수 (빈칸 단골)
# __init__은 객체를 만들 때 자동 호출.
# self.name처럼 self.에 붙여야 객체의 변수가 된다.
# ---------------------------------------------------
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def show(self):
        print(self.name, self.score)

s1 = Student('Kim', 90)
s2 = Student('Lee', 85)
s1.show()                       # Kim 90
s2.show()                       # Lee 85

# ---------------------------------------------------
# [문제 4] 클래스 변수 vs 인스턴스 변수 (Java static과 같은 논리)
# count는 클래스 변수 → 모든 객체가 공유하며 누적
# Java 02장의 static 카운터와 완전히 같은 출제 포인트
# ---------------------------------------------------
class Counter:
    count = 0                   # 클래스 변수 (공유)

    def __init__(self):
        Counter.count += 1      # 클래스 이름으로 접근해 누적

c1 = Counter()
c2 = Counter()
c3 = Counter()
print(Counter.count)            # 3

# ---------------------------------------------------
# [문제 5] 상속과 오버라이딩 (2023년~ 출제 증가)
# 자식이 재정의하면 자식 것이 실행 (Java와 동일한 동적 바인딩)
# super().__init__(...)으로 부모 생성자 호출
# ---------------------------------------------------
class Animal:
    def __init__(self, name):
        self.name = name

    def cry(self):
        return '...'

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)  # 부모 생성자 호출 (빈칸 단골)

    def cry(self):              # 오버라이딩
        return '멍멍'

pets = [Animal('나비'), Dog('바둑이')]
for p in pets:
    print(p.name, p.cry())      # 나비 ... / 바둑이 멍멍

# ---------------------------------------------------
# [문제 6] 상속 + 메서드 호출 순서 추적 (기출 변형)
# d.info() → 자식에 없음 → 부모의 info() 실행
#   info() 안의 self.cry()는 "실제 객체" 기준 → 자식의 cry()!
#   (Java 다형성과 같은 원리 - 언어가 달라도 출제 포인트는 같다)
# ---------------------------------------------------
class Parent:
    def cry(self):
        return 'parent'

    def info(self):
        return self.cry() + ' info'

class Child(Parent):
    def cry(self):
        return 'child'

d = Child()
print(d.info())                 # child info (parent info 아님!)

# ============================================================
# [전체 정답 모음]
# SKIDDP / 10 20 / 20 10 / Kim 90 / Lee 85 / 3
# 나비 ... / 바둑이 멍멍 / child info
#
# [시험장 체크리스트]
# 1. self는 정의에만 있고 호출 시엔 안 넘긴다
# 2. 클래스 변수는 공유(=Java static), self.변수는 객체별
# 3. 부모 메서드 안의 self.xxx()도 실제 객체(자식) 기준으로 실행
# 4. __init__, super().__init__() 철자가 빈칸으로 출제됨
# ============================================================
