def isPrime(n: int):
    if n < 2:
        return False
    elif n == 2:
        return True
    
    for i in range(2, int(n**(1/2))+1, 1):
        if n % i == 0:
            return False
    return True
        
        
a,b = 3, 5

i = 1
lastI = i


while True:
    if isPrime(a) and isPrime(b):
        print(i-lastI)
        lastI = i
    a += 2
    b += 2
    i += 1