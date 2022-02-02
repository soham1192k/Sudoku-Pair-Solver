import sys,math
inp=open('input.csv','r')
b=inp.read().splitlines()
k=int(math.sqrt(len(b)/2))

a=[]
for i in range(2*(k**2)):
    a.append([])

ones=[]
ones_2=[]

#Reading the sudoku pair from the csv file
string=""
for i in range(2*(k**2)):
    for j in range(len(b[i])):
        if b[i][j]==',':
            a[i].append(string)
            string=""
        else:
            string=string+b[i][j]
    if string!="":
        a[i].append(string)
        string=""

#Storing the fixed values in 2 arrays
for i in range(k**2):
    for j in range(k**2):
        if a[i][j]==',' or a[i][j]=='0':
            pass
        else:
            ones.append((k**2)*i+j+1+(k**4)*(int(a[i][j])-1))

for i in range((k**2),2*(k**2)):
    for j in range(k**2):
        if a[i][j]==',' or a[i][j]=='0':
            pass
        else:
            ones_2.append((k**2)*(i-k**2)+j+1+(k**4)*(int(a[i][j])-1)+(k**6))

inp.close()

original_stdout=sys.stdout
file=open('encoding_CNF.txt','w')
sys.stdout=file

#Helper function for the clauses which states that not both should be true at the same time.
def pairwise(a):
    for z in range(len(a)):
        for i in range(z+1,len(a)):
            print(str(-a[z])+" "+str(-a[i])+" 0")

#DIMACS representation
print("p"+" "+"cnf"+" "+str(2*(k**6))+" "+str(0))

a=[]

#premises corresponding to the fixed values in the first sudoku pair
for i in ones:
	print(str(i)+" 0")

#premises corresponding to the fixed values in the second sudoku pair
for i in ones_2:
    print(str(i)+" 0")

#each cell should have exactly 1 value
for x in range(k**4):
    for i in range(k**2):
        #atleast one value
        val=x+i*(k**4)+1
        print(str(val)+" ",end="")
        a.append(val)
    print("0")
    #atmost one value
    pairwise(a)
    del a[:]

#handling the row condition
for x in range(k**2):
    for i in range(k**2):
        for p in range(k**2):
            val=x*(k**4)+i*(k**2)+1+p
            print(str(val)+" ",end="")
            a.append(val)
        print("0")
        pairwise(a)
        del a[:]

#handling the column condition
for x in range(k**2):
    for i in range(k**2):
        for p in range(k**2):
            val=x*(k**4)+i+1+p*(k**2)
            print(str(val)+" ",end="")
            a.append(val)
        print("0")
        pairwise(a)
        del a[:]

#Handling the box condition
for x in range(k**2):
    for p in range(k):
        for i in range(k):
            for l in range(k):
                for m in range(k):
                    val=x*(k**4)+p*(k**3)+k*i+(k**2)*l+m+1
                    print(str(val)+" ",end="")
                    a.append(val)
            print("0")
            pairwise(a)
            del a[:]

#Conditions for the second sudoku start here

#Each cell should have exactly 1 value
for x in range(k**4):
    for i in range(k**2):
        #Atleast one
        val=x+i*(k**4)+1+k**6
        print(str(val)+" ",end="")
        a.append(val)
    print("0")
    #Atmost one
    pairwise(a)
    del a[:]

#Row conditions
for x in range(k**2):
    for i in range(k**2):
        for p in range(k**2):
            val=x*(k**4)+i*(k**2)+1+p+k**6
            print(str(val)+" ",end="")
            a.append(val)
        print("0")
        pairwise(a)
        del a[:]

#Column conditions
for x in range(k**2):
    for i in range(k**2):
        for p in range(k**2):
            val=x*(k**4)+i+1+p*(k**2)+k**6
            print(str(val)+" ",end="")
            a.append(val)
        print("0")
        pairwise(a)
        del a[:]

#Box conditions
for x in range(k**2):
    for p in range(k):
        for i in range(k):
            for l in range(k):
                for m in range(k):
                    val=x*(k**4)+p*(k**3)+k*i+(k**2)*l+m+1+k**6
                    print(str(val)+" ",end="")
                    a.append(val)
            print("0")
            pairwise(a)
            del a[:]

#no two corresponding cells in the two sudokus should have the same value
for i in range(1,(k**6)+1):
    print(str(-i)+" "+str(-1*(i+(k**6)))+" 0")

file.close()
sys.stdout=original_stdout

with open('encoding_CNF.txt', 'r') as fin:
    data = fin.read().splitlines(True)
string="p cnf "+str(2*(k**6))+" "+str(len(data)-1)+"\n"
with open('encoding_CNF.txt', 'w') as fout:
    fout.writelines(string)
    fout.writelines(data[1:])
fin.close()
fout.close()
