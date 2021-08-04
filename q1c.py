r=[]
for i in range(0,5):
    r=input().split() #row strings splitted into list
    for j in range(0,5):
        if(r[j]=='1'):
            print(abs(i-2)+abs(j-2))
            break

