import csv

mode = ""
fileobject = ""
headers = []

def fileobj(file1,mode_u,header):
    if type(mode_u) == list:
        raise Exception("Mode cannot be a list || Format - fileobj(filename,mode,headers) || headers must be lists || mode and filename must be strings")
    mode_check = mode_u.lower()
    fileobject = file1
    if mode_check == "read":
        mode = "r"
    elif mode_check == "write":
        mode = "w"
    elif mode_check == "append":
        mode = "a"
    elif mode_check == "intsec":
        mode = "i"
    else:
        raise Exception("Invalid Mode  \nCurrent Modes :- read , write , append , intsec")
        quit()

    if type(header) == list:
        headers = header
    else:
        raise Exception("Header Must Be a List!")
        quit()
    return file1

def writebetween(oldpar,newpar):
    try:
        fileobj = fileobject
        hint = []
        fileobj = open(fileobject,'r')
        reader = csv.reader(fileobj)
        for row in reader:
            hint.append(row)
        x=0
        y=0
        a=0
        b=0
        for item in hint:
            for items in item:
                if items == oldpar:
                   print("is")
                   x=a
                   y=b+1
                   break
            a+=1
        b+=1
        hint[x][y] = newpar
        with open(fileobject, 'w+', newline ='') as myfile:
            write = csv.writer(myfile)
            write.writerows(hint)
            print(f"Successfully changed parameter to {newpar}")
            quit()
    except Exception as e:
        raise Exception("Error :- ",e)
        quit()

fileobject = fileobj(r"C:\Users\Bhai Log\Downloads\New folder\names.csv",'intsec',['Name','Hours'])
writebetween("Kanishk","something")
