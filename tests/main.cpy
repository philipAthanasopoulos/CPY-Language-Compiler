#def man
#int i
counterFunctionCalls = 0

i = int(input())
print(i)


i = 1600
while i<=2000:
#{
    print(leap(i))
    i = i + 400
#}
print(leap(2023))
print(leap(2024))
print(quad(3))
print(fib(5))

i=1
while i<=12:
#{
    print(isPrime(i))
    i = i + 1
#}

print(counterFunctionCalls)
