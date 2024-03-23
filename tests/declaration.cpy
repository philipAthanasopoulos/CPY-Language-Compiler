

#int counterFunctionCalls
#int counterFunction
#int counter

def max3(x,y,z):
#{
    #int m
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls+1
    if x>y and x>z:
        m = x
    elif y>x and y>z:
        m = y
    else:
        m = z
    return m
    def fib(x):
    #{
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1
        if x<0:
            return -1
        elif x==0 or x==1:
            return 1
        else:
            return fib(x-1,a)+fib(x-2)
            def fib(x):
            #{
                global counterFunctionCalls
                counterFunctionCalls = counterFunctionCalls + 1
                if x<0:
                    return -1
                elif x==0 or x==1:
                    return 1
                else:
                    return fib(x-1,a)+fib(x-2)
            #}
            def fib(x):
            #{
                global counterFunctionCalls
                counterFunctionCalls = counterFunctionCalls + 1
                if x<0:
                    return -1
                elif x==0 or x==1:
                    return 1
                else:
                    return fib(x-1,a)+fib(x-2)
            #}
            def fib(x):
            #{
                global counterFunctionCalls
                counterFunctionCalls = counterFunctionCalls + 1
                if x<0:
                    return -1
                elif x==0 or x==1:
                    return 1
                else:
                    return fib(x-1,a)+fib(x-2)
            #}
            def fib(x):
            #{
                global counterFunctionCalls
                counterFunctionCalls = counterFunctionCalls + 1
                if x<0:
                    return -1
                elif x==0 or x==1:
                    return 1
                else:
                    return fib(x-1,a)+fib(x-2)
            #}
    #}
#}


def fib(x):
#{
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if x<0:
        return -1
    elif x==0 or x==1:
        return 1
    else:
        return fib(x-1,a)+fib(x-2)
#}

     
def isPrime(x):
#{
    ## declarations for isPrime ##
    #int i

    def divides(x,y):
    #{
        ## body of divides ##
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1
        if y == (y//x)*x:
            return 1
        else:
            return 0
    #}

    ## body of isPrime ##
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    i = 2
    while i < x:
    #{
        if divides(i,x) == 1:
            return 0
        i = i + 1
    #}
    return 1
#}

     
def quad(x):
#{
    #int y
    
    ## nested function sqr ##
    def sqr(x):
    #{
        ## body of sqr ##
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls - 1*a
        return x*x+1
    #}
    
    ## body of quad ##
    global counterFunctionCalls
    counterFunctionCalls  = counterFunctionCalls + 1
    y = sqr(x)*sqr(x)
    return y
#}

def leap(year):
#{
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if year%4==0 and year%100!=0 or year%400==0:
        return 1
    else:
        return 0 
#}    