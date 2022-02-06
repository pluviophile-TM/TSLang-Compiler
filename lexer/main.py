import re

file_path = 'TSLANG_Test.txt'
file_path2 = 'test2.txt'
counter = 1
line = 1
eof=False




signs = ["{", "}","(", ")", "[", "]", "?", "=", "+", "-", "*", "/", "%", "<", ">",  "!", ":",";","," ]
tokens = []
keys = ['function' , 'returns','return','end','if','else','while','do','foreach','of','val']


def next_character():
    global counter
    global eof
    if eof==True:
        return ''
    with open(file_path, 'r') as file:
        string = file.read(counter)
        char = string[counter-1:]
        file.close()
    counter = counter + 1
    if char=='':
        eof=True
    return char

def back_char():
    global counter
    counter-=1
    return

def tokenizer():

    while True:

        token = next_character()
        
        while token == ' ' or token=='\t':
            token=next_character()

        
    
        if token != '':
            if token == "-": #comment delete
                next_c = next_character() 
                if next_c=='-':
                    while True:
                        if token == "\n":
                            break
                        token = next_character()
                else:
                    back_char()

            if token in signs:
                if token=="<" or token==">" or token=="=" or token=="!":
                    if next_character()=='=':
                        token+='='
                    else:
                        back_char()
                tokens.append(token)        
                            
            elif token != " " and token != "\n":
                next_c = next_character()
                if token+next_c=='||' or token+next_c=='&&':
                    print('here', token+next_c)
                    token+=next_c
                    tokens.append(token)
                else:
                    while True:
                        if next_c=='|' or next_c=='&':
                            next_next_c=next_character()

                            if next_c+next_next_c=='||' or next_c+next_next_c=='&&':
                                tokens.append(token)
                                tokens.append(next_c+next_next_c)
                                break
                            else:
                                back_char()

                        if next_c in signs :
                            tokens.append(token)
                            tokens.append(next_c)
                            break
                        elif next_c == " " or next_c=="\n" or next_c=='':
                            tokens.append(token)
                            break
                        token += next_c
                        next_c = next_character()
                
        else:
            # End of file
            break
        
def isWhiteSpace(char):
    if char == '\n':
        global line
        line+=1
        return True
    if char==' ' or char=='\t':
        return True
    return False

def next_token():
    token = next_character()
        
    while isWhiteSpace(token):
        token=next_character()

    
    if token != '':
        if token == "-": #comment delete
            next_c = next_character() 
            if next_c=='-':
                while True:
                    if token == "\n":
                        global line
                        line+=1
                        break
                    token=next_character()
                while isWhiteSpace(token):
                    token = next_character()
            else:
                back_char()

        if token in signs:
            if token=="<" or token==">" or token=="=" or token=="!":
                if next_character()=='=':
                    token+='='
                else:
                    back_char()
            return token       
                        
        elif not isWhiteSpace(token):
            next_c = next_character()
            if token+next_c=='||' or token+next_c=='&&':
                token+=next_c
                return token
            else:
                while True:
                    if next_c=='|' or next_c=='&':
                        next_next_c=next_character()

                        if next_c+next_next_c=='||' or next_c+next_next_c=='&&':
                            back_char()
                            back_char()
                            return token

                        back_char()

                    if next_c in signs :
                        
                        back_char()
                        return(token)
                        
                    elif isWhiteSpace(next_c):
                        return token
                    token += next_c
                    next_c = next_character()
            
    else:
        return None

class Symbol:
    def __init__(self,name,isFunc,type) :
        self.name=name
        self.isFunc=isFunc
        self.type=type
        self.list=[]

def isKey(word):
    return word in keys

def isIden(word):
    if isKey(word):
        return False
    pattern = re.compile("[A-Za-z_][A-Za-z_0-9]*")
    if pattern.fullmatch(word) is not None:
        return True
    return False

def isNum(word):
    pattern = re.compile("[0-9]+")
    if pattern.fullmatch(word) is not None:
        return True
    return False











while not eof:
    print(next_token())



