n=int(input())
x=input().split() #str list
for i in range (0,n):
    x[i]=int(x[i]) #int eq
x.sort(reverse=True)
l=[]
for i in range (0,n):
    l.append(x[i])  
    if(sum(l)>(sum(x)/2)):
        break
print(i+1)
