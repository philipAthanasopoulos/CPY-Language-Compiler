#int A
#int b,g,f
A = 1

def P1(X, Y):
#{
    #int e,f
    def P11(X):
    #{
        #int e
        e= A
        X = Y
        f = b
        return e
    #}
    b = X
    e = P11(X)
    e = P1(X,Y)
    X = b
    return e

#}

#def main
if b>1 and f<2 or g+1<f+b:
    f = P1(g)
else:
    f = 1
