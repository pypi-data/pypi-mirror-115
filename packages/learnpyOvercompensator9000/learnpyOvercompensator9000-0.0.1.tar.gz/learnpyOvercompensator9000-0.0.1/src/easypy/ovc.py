def Display(value):
    print(value)

def UserInput(prompt,itype):
    if itype.lower()=='integer':
        print(prompt)
        a=int(input())
        return a
    elif itype.lower()=='string':
        print(prompt)
        b=input()
        return b
    elif itype.lower()=='decimal':
        print(prompt)
        c=float(input())
        return c

def Calculator(num1,num2,operator):
    if operator=='+':
        return num1+num2
    elif operator=='-':
        if num1>num2:
            return num1-num2
        else:
            return num2-num1
    elif operator=='*' or operator=='x'.lower():
        return num2*num1
    elif operator=='/':
        if num1>num2:
            return num1/num2
        else:
            return num2/num1

def DataType(value,dtype):
    if dtype=='integer'.lower():
        return int(value)
    elif dtype=='decimal'.lower():
        return float(value)
    elif dtype=='string'.lower():
        return str(value)

def Bool(val):
    b=True
    if val=='is true'.lower():
        b=True
        return b
    elif val=='is false'.lower() or val=='is not true'.lower():
        b=False
        return b

def Openfile(filename,mode):
    if mode.lower()=='collect data':
        return open(filename)
    elif mode.lower()=='write data':
        return open(filename,'w')
    elif mode.lower()=='add data':
        return open(filename,'a')

def Readfromfile(filehandle):
    return filehandle.read()

def WriteToFile(filehandle,text):
    return filehandle.write(text)

def Closefile(filehandle):
    return filehandle.close()


    

    
