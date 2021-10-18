f=open("f.txt","r")
g=open("out.txt","w")
l=f.readlines()
ch=l[0]
print(len(ch))
li=[]
s=""

for j in range(1,len(ch)):
    if ch[j-1]==" ":
        if ch[j]==" ":
            continue
        else:
            s+="\n"
            li.append(s)
    else:
        s+=ch[j-1]

g.writelines(li)
g.close()
f.close()
print(s)