import sys,os
import generate_encoding
out=sys.stdout
file=open('output.txt','w')
sys.stdout=file

k=generate_encoding.k

inp=open('solution.txt','r')

#Reading from the output produced by minisat
a=inp.read().splitlines()

#If first line says UNSAT, then no solution
if a[0]=="UNSAT" or k==1:
    print("No Solution Exists!")
    os.system("rm -rf solution.txt __pycache__ encoding_CNF.txt")
else:
    a.pop(0)#Remove the first line which says SAT/UNSAT
    b=a[0].split(" ")
    b.pop(-1)

    #Declaring the 2 sudokus to store the outputs
    c1=[['0' for j in range(k**2)] for i in range(k**2)]
    c2=[['0' for j in range(k**2)] for i in range(k**2)]
    
    for j in b:
        z=int(j)
        if z>0 and z>(k**6):
            z=z-(k**6)
            l=int(int((z-1)/(k**4))+1)
            m=z-(l-1)*(k**4)
            row=int((m-1)/(k**2))
            col=(m-1)%(k**2)
            c2[row][col]=l
        elif z>0:
            l=int(int((z-1)/(k**4))+1)
            m=z-(l-1)*(k**4)
            row=int((m-1)/(k**2))
            col=(m-1)%(k**2)
            c1[row][col]=l

    print("First Sudoku:")
    for i in range(k**2):
        for j in range(2*(k**2)+1):
            print("-",end="")
        print("")
        for j in range(k**2):
            print(c1[i][j],end="")
            print("|",end="")
        print("")
    for i in range(2*(k**2)+1):
        print("-",end="")
    print("")

    print("")
    print("Second Sudoku:")
    for i in range(k**2):
        for j in range(2*(k**2)+1):
            print("-",end="")
        print("")
        for j in range(k**2):
            print(c2[i][j],end="")
            print("|",end="")
        print("")
    for i in range(2*(k**2)+1):
        print("-",end="")
    
    os.system("rm -rf solution.txt __pycache__ encoding_CNF.txt")

file.close()
sys.stdout=out