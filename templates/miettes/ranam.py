#bivalued lists


L=[1,2,3,4,5]

L2=[1,1,2,2,1,2]

def isBivalued(L):
    if len(L)<=2:
        return True

    else:
        a = L[0]
        b= L[1]

        if a==b:
            for i in range(2,len(L)):
                if L[i]!=b:
                    b=L[i]
                    break

        for i in range(2,len(L)):
            if L[i]!=a and L[i]!=b:
                return False
        return True
        


print(isBivalued(L))
print(isBivalued(L2))