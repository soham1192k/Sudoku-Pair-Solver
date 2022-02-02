import random,os

k=int(input("ENTER THE VALUE OF K: "))

#Returns the value in some cell, corresponding to some premise number
def val(n):
    ret=int((n-1)/(k**4))+1
    if ret>(k**2):
        ret=ret-(k**2)
    return ret

#Returns information about the row,col,box,cell number, and also which sudoku is it
def help(n):
    if n>(k**6):
        #corresponds to the second sudoku
        which=2
        n=n-(k**6)
    else:
        #corresponds to the first sudoku
        which=1
    cell=n-(val(n)-1)*(k**4)
    row=int((cell-1)/(k**2))+1
    col=cell%(k**2)
    if col==0:
        col=(k**2)
    box=(int((row-1)/k))*k+(int((col-1)/k)+1)
    return row,col,cell,box,which

#remove a number from the sudoku: if multiple solutions, put it back. if unique solution, then good to go.
#Try for all possible numbers in the array
def maximise_holes(arr):
    length=len(arr)
    for i in range(length):
        num=arr.pop(0)
        val=soln_count(arr)
        if val==2:
            arr.append(num)
        elif val==1:
            pass
        elif val==0:
            arr.append(num)

#When some value is fixed in the cell, the allowed variables list shortens. This function will do this operation
def fix(a,n):
    value=val(n)
    row,col,cell,box,which=help(n)
    
    # removes the premises for other values of the same cell
    for i in range(k**2):
        if which==2:
            offset=(k**6)
        else:
            offset=0
        if((cell+i*(k**4)+(offset)) in a):
            a.remove(cell+i*(k**4)+offset)

    #handling row conditions
    for i in range(k**2):
        if which==2:
            offset=(k**6)
        else:
            offset=0
        if((row-1)*(k**2)+i+1+(k**4)*(value-1)+offset) in a:
            a.remove((row-1)*(k**2)+i+1+(k**4)*(value-1)+offset)

    #handling column conditions
    for i in range(k**2):
        if which==2:
            offset=(k**6)
        else:
            offset=0
        if (col+i*(k**2)+(k**4)*(value-1)+offset) in a:
            a.remove(col+i*(k**2)+(k**4)*(value-1)+offset)

    #handling box conditions
    for r in range(int((box-1)/k)*k+1,int((box-1)/k)*k+(k+1)):
        temp=box%k
        if(temp==0):
            temp=k
        for c in range((temp-1)*k+1,(temp-1)*k+(k+1)):
            if which==2:
                offset=(k**6)
            else:
                offset=0
            if (r-1)*(k**2)+c+(k**4)*(value-1)+offset in a:
                a.remove((r-1)*(k**2)+c+(k**4)*(value-1)+offset)

    #the corresponding cell in the other sudoku should not have the same value
    if which==2:
        if n-(k**6) in a:
            a.remove(n-(k**6))
    else:
        if n+(k**6) in a:
            a.remove(n+(k**6))

#Same function as the function in ../generate_encoding.py
def pairwise(a,encoding_file):
	for l in range(len(a)):
		for i in range(l+1,len(a)):
			encoding_file.write(str(-a[l])+" "+str(-a[i])+" "+"0\n")

#Generates the encoding corresponding to some array
#If string is empty, it just generates the normal encoding
#If string is non empty, we append string to the encoding file [So that we dont get the same solution again]
def gen_encoding(arr,string):
    if(string==""):
        encoding_file=open("encoding.txt","w")
        encoding_file.write("p cnf "+str(2*(k**6))+" "+str(0)+"\n")
        a=[]

        #Handling the fixed values
        for i in arr:
            encoding_file.write(str(i)+" 0\n")

        #Every cell should have exactly 1 value
        for x in range(k**4):
            string=""
            for l in range(k**2):
                string=string+(str(x+l*(k**4)+1)+" ")
                a.append(x+l*(k**4)+1)
            string=string+"0\n"
            encoding_file.write(string)
            pairwise(a,encoding_file)
            del a[:]

        #Handling row conditions
        for x in range(k**2):
            for l in range(k**2):
                string=""
                for p in range(k**2):
                    string=string+(str(x*(k**4)+l*(k**2)+1+p)+" ")
                    a.append(x*(k**4)+l*(k**2)+1+p)
                string=string+"0\n"
                encoding_file.write(string)
                pairwise(a,encoding_file)
                del a[:]

        #Handling column conditions
        for x in range(k**2):
            for l in range(k**2):
                string=""
                for p in range(k**2):
                    string=string+(str(x*(k**4)+l+1+p*(k**2))+" ")
                    a.append(x*(k**4)+l+1+p*(k**2))
                string=string+"0\n"
                encoding_file.write(string)
                pairwise(a,encoding_file)
                del a[:]

        #Handling box conditions
        for x in range(k**2):
            for p in range(k):
                for z in range(k):
                    string=""
                    for l in range(k):
                        for m in range(k):
                            string=string+(str(x*(k**4)+p*(k**3)+k*z+(k**2)*l+m+1)+" ")
                            a.append(x*(k**4)+p*(k**3)+k*z+(k**2)*l+m+1)
                    string=string+"0\n"
                    encoding_file.write(string)
                    pairwise(a,encoding_file)
                    del a[:]

        #Second sudoku conditions start here
        #Every cell should have exactly 1 value
        for x in range(k**4):
            string=""
            for l in range(k**2):
                string=string+(str(x+l*(k**4)+(k**6)+1)+" ")
                a.append(x+l*(k**4)+1+(k**6))
            string=string+"0\n"
            encoding_file.write(string)
            pairwise(a,encoding_file)
            del a[:]

        #Handling row conditions
        for x in range(k**2):
            for l in range(k**2):
                string=""
                for p in range(k**2):
                    string=string+(str(x*(k**4)+l*(k**2)+1+p+(k**6))+" ")
                    a.append(x*(k**4)+l*(k**2)+1+p+(k**6))
                string=string+"0\n"
                encoding_file.write(string)
                pairwise(a,encoding_file)
                del a[:]

        #Handling column conditions
        for x in range(k**2):
            for l in range(k**2):
                string=""
                for p in range(k**2):
                    string=string+(str(x*(k**4)+l+1+p*(k**2)+(k**6))+" ")
                    a.append(x*(k**4)+l+1+p*(k**2)+(k**6))
                string=string+"0\n"
                encoding_file.write(string)
                pairwise(a,encoding_file)
                del a[:]

        #Handling box conditions
        for x in range(k**2):
            for p in range(k):
                for z in range(k):
                    string=""
                    for l in range(k):
                        for m in range(k):
                            string=string+(str(x*(k**4)+p*(k**3)+k*z+(k**2)*l+m+1+(k**6))+" ")
                            a.append(x*(k**4)+p*(k**3)+k*z+(k**2)*l+m+1+(k**6))
                    string=string+"0\n"
                    encoding_file.write(string)
                    pairwise(a,encoding_file)
                    del a[:]
        
        #No two corresponding cells in the two sudokus should be the same
        string=""
        for i in range(1,(k**6)+1):
            string=string+(str(-i)+" "+str(-1*(i+(k**6)))+" 0\n")
        encoding_file.write(string)

        encoding_file.close()


        with open('encoding.txt', 'r') as fin:
            data = fin.read().splitlines(True)
        string="p cnf "+str(2*(k**6))+" "+str(len(data)-1)+"\n"
        with open('encoding.txt', 'w') as fout:
            fout.writelines(string)
            fout.writelines(data[1:])
        fin.close()
        fout.close()

    else:
        encoding_file=open("encoding.txt","w")
        encoding_file.write("p cnf "+str(2*(k**6))+" "+str(0)+"\n")
        encoding_file.write(string+"0\n")
        a=[]

        #Handling the fixed values
        for i in arr:
            encoding_file.write(str(i)+" 0\n")

        #Every cell should have exactly 1 value
        for x in range(k**4):
            string=""
            for l in range(k**2):
                string=string+(str(x+l*(k**4)+1)+" ")
                a.append(x+l*(k**4)+1)
            string=string+"0\n"
            encoding_file.write(string)
            pairwise(a,encoding_file)
            del a[:]

        #Handling row conditions
        for x in range(k**2):
            for l in range(k**2):
                string=""
                for p in range(k**2):
                    string=string+(str(x*(k**4)+l*(k**2)+1+p)+" ")
                    a.append(x*(k**4)+l*(k**2)+1+p)
                string=string+"0\n"
                encoding_file.write(string)
                pairwise(a,encoding_file)
                del a[:]

        #Handling column conditions
        for x in range(k**2):
            for l in range(k**2):
                string=""
                for p in range(k**2):
                    string=string+(str(x*(k**4)+l+1+p*(k**2))+" ")
                    a.append(x*(k**4)+l+1+p*(k**2))
                string=string+"0\n"
                encoding_file.write(string)
                pairwise(a,encoding_file)
                del a[:]

        #Handling box conditions
        for x in range(k**2):
            for p in range(k):
                for z in range(k):
                    string=""
                    for l in range(k):
                        for m in range(k):
                            string=string+(str(x*(k**4)+p*(k**3)+k*z+(k**2)*l+m+1)+" ")
                            a.append(x*(k**4)+p*(k**3)+k*z+(k**2)*l+m+1)
                    string=string+"0\n"
                    encoding_file.write(string)
                    pairwise(a,encoding_file)
                    del a[:]

        #Second sudoku conditions start here  
        #Every cell should have exactly 1 value
        for x in range(k**4):
            string=""
            for l in range(k**2):
                string=string+(str(x+l*(k**4)+(k**6)+1)+" ")
                a.append(x+l*(k**4)+1+(k**6))
            string=string+"0\n"
            encoding_file.write(string)
            pairwise(a,encoding_file)
            del a[:]

        #Handling row conditions
        for x in range(k**2):
            for l in range(k**2):
                string=""
                for p in range(k**2):
                    string=string+(str(x*(k**4)+l*(k**2)+1+p+(k**6))+" ")
                    a.append(x*(k**4)+l*(k**2)+1+p+(k**6))
                string=string+"0\n"
                encoding_file.write(string)
                pairwise(a,encoding_file)
                del a[:]

        #Handling column conditions
        for x in range(k**2):
            for l in range(k**2):
                string=""
                for p in range(k**2):
                    string=string+(str(x*(k**4)+l+1+p*(k**2)+(k**6))+" ")
                    a.append(x*(k**4)+l+1+p*(k**2)+(k**6))
                string=string+"0\n"
                encoding_file.write(string)
                pairwise(a,encoding_file)
                del a[:]

        #Handling box conditions
        for x in range(k**2):
            for p in range(k):
                for z in range(k):
                    string=""
                    for l in range(k):
                        for m in range(k):
                            string=string+(str(x*(k**4)+p*(k**3)+k*z+(k**2)*l+m+1+(k**6))+" ")
                            a.append(x*(k**4)+p*(k**3)+k*z+(k**2)*l+m+1+(k**6))
                    string=string+"0\n"
                    encoding_file.write(string)
                    pairwise(a,encoding_file)
                    del a[:]
        
        #No two corresponding cells in the two sudokus should have the same value
        string=""
        for i in range(1,(k**6)+1):
            string=string+(str(-i)+" "+str(-1*(i+(k**6)))+" 0\n")
        encoding_file.write(string)

        encoding_file.close()

        with open('encoding.txt', 'r') as fin:
            data = fin.read().splitlines(True)
        string="p cnf "+str(2*(k**6))+" "+str(len(data)-1)+"\n"
        with open('encoding.txt', 'w') as fout:
            fout.writelines(string)
            fout.writelines(data[1:])
        fin.close()
        fout.close()

#Checks if some sudoku pair has multiple solutions,unique solution or no solutions
def soln_count(arr):
    #Generate the encoding
    gen_encoding(arr,"")
    #Run minisat
    os.system("minisat encoding.txt temp.txt>/dev/null 2>/dev/null")
    file=open('temp.txt','r')
    a=file.read().splitlines()
    file.close()

    #If UNSAT straightaway, no solns
    if(a[0]=="UNSAT"):
        return 0
    else:
        a.pop(0)
        b=a[0].split(" ")
        b.pop(-1)
        arr2=[i for i in arr]
        
        #We will append the negation of the rules in the first solution, so that we don't get the same solution again
        string=""
        for j in b:
            if(int(j)>0):
                if int(j) not in arr2:
                    string=string+str(-int(j))+" "
       
        #Generate the new encoding
        gen_encoding(arr2,string)

        #Run minisat again
        os.system("minisat encoding.txt temp.txt>/dev/null 2>/dev/null")
        f=open("temp.txt","r")
        data=f.read().splitlines()
        f.close()

        #If this time no more solns, then unique solutions
        if(data[0]=="UNSAT"):
            return 1
        else:
            #Otherwise multiple solns
            return 2

#print the output in a user friendly manner
def build_output(arr):
    file=open('output.csv','w')
    first=[["0" for x in range(k**2)] for y in range(k**2)]
    second=[["0" for x in range(k**2)] for y in range(k**2)]
    for i in arr:
        value=val(i)
        row,col,cell,box,which=help(i)
        if which==1:
            first[row-1][col-1]=str(value)
        else:
            second[row-1][col-1]=str(value)

    for i in range(k**2):
        for j in range(k**2):
            file.write(first[i][j])
            if j<(k**2)-1:
                file.write(",")
        file.write("\n")
    
    for i in range(k**2):
        for j in range(k**2):
            file.write(second[i][j])
            if j<(k**2)-1:
                file.write(",")
        file.write("\n")
    file.close()

def main():
    #Initially,all variables are possible.
    allowed=[i+1 for i in range(2*(k**6))]
    #Initially, nothing is fixed
    fixed=[]

    #Infinite while loop
    while(True):
        #Pick a random index
        index=random.randint(0,len(allowed)-1)
        #Check what number is stored at that index
        num=allowed[index]
        
        #Try to fix this value
        fixed.append(num)
        #Count the number of solutions
        nos=soln_count(fixed)

        #If multiple solutions exist,we have to fix what values are allowed in the sudoku
        if(nos==2):
            fix(allowed,num)
        #If one solution exists, congrats :)
        elif(nos==1):
            break 
        elif(nos==0):
            fixed.pop(-1)
            allowed.remove(num)

    maximise_holes(fixed)
    build_output(fixed)
    os.system("rm -rf *.txt")

main()