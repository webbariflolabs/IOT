def fib(n):
    k = [0.0,1.0]
    a,b = 0.0,1.0
    for i in range(n):
        a,b = b,a+b
        k.append(b)
    return k
print(fib(4))