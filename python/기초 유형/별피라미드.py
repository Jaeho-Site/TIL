n = int(input())

# 위쪽 (중앙 포함)
for i in range(n):
    spaces = n - 1 - i
    stars = 2 * i + 1
    print(" " * spaces + "*" * stars)

# 아래쪽
for i in range(n - 2, -1, -1):
    spaces = n - 1 - i
    stars = 2 * i + 1
    print(" " * spaces + "*" * stars)