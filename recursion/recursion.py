def print1toN(n):
    if n < 1:
        return
    print1toN(n - 1)
    print(n)

print1toN(100)