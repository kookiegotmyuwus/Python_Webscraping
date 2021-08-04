a=input()
a=a.lower()
s=""
l=['a' , 'e' , 'i' , 'o' , 'u' , 'y']
for i in a:
    if i not in l:
        s=s+'.'+i
print(s)